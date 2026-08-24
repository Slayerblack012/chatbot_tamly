import base64
import datetime
import json
import logging
import os
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.bot_engine import CounselorEngine, sanitize_messages_for_gemini
from core.knowledge_base import ASSESSMENT_QUIZZES, COGNITIVE_DISTORTIONS, PSYCHOEDU_ARTICLES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("an_nhien.server")

load_dotenv()

app = FastAPI(
    title="An Nhien Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(GZipMiddleware, minimum_size=500)

allowed_origins_env = os.getenv("CORS_ORIGINS", "")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
if not allowed_origins:
    allowed_origins = ["http://localhost:8000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_and_privacy_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    csp_directives = [
        "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'",
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https: cdn.jsdelivr.net",
        "style-src 'self' 'unsafe-inline' https: fonts.googleapis.com cdn.jsdelivr.net",
        "font-src 'self' https: fonts.gstatic.com data:",
        "media-src 'self' https: cdn.pixabay.com data: blob:",
        "img-src 'self' data: https: blob: cdn.jsdelivr.net",
        "connect-src 'self' https: wss: ws:",
        "frame-ancestors 'self'",
        "base-uri 'self'",
        "form-action 'self'"
    ]
    response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=86400"
    return response


RATE_LIMIT_WINDOW = 60
MAX_REQUESTS_PER_WINDOW = 45
request_history: Dict[str, List[float]] = defaultdict(list)
TRUST_PROXY_HEADERS = os.getenv("TRUST_PROXY_HEADERS", "false").lower() in ("true", "1", "yes")


def get_client_ip(request: Request) -> str:
    """Lấy địa chỉ IP của client. Chỉ đọc header proxy nếu TRUST_PROXY_HEADERS=true để chống giả mạo."""
    if TRUST_PROXY_HEADERS:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
            if client_ip:
                return client_ip
        real_ip = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(client_ip: str) -> None:
    now = time.time()
    valid_timestamps = [t for t in request_history[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(valid_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        request_history[client_ip] = valid_timestamps
        logger.warning(f"Rate limit triggered for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Yêu cầu quá nhanh. Vui lòng thử lại sau giây lát."
        )
    valid_timestamps.append(now)
    request_history[client_ip] = valid_timestamps

    if len(request_history) > 500:
        stale_keys = [
            ip for ip, times in request_history.items()
            if not times or (now - times[-1] >= RATE_LIMIT_WINDOW)
        ]
        for ip in stale_keys:
            request_history.pop(ip, None)


try:
    engine = CounselorEngine()
except Exception as exc:
    logger.error(f"Lỗi khởi tạo CounselorEngine: {exc}", exc_info=True)
    engine = CounselorEngine(api_key="")


def b64_decode_json(encoded_str: str) -> Dict[str, Any]:
    try:
        raw_bytes = base64.b64decode(encoded_str.encode("utf-8"))
        return json.loads(raw_bytes.decode("utf-8"))
    except Exception as e:
        logger.warning(f"Lỗi giải mã Base64 payload: {e}")
        raise HTTPException(status_code=400, detail="Dữ liệu truyền tải không hợp lệ.")


def b64_encode_text(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


class EncryptedPayload(BaseModel):
    p: str = Field(..., min_length=1, max_length=150000)


@app.get("/api/health")
async def health_check():
    """Endpoint kiểm tra trạng thái hoạt động thực tế (R7)."""
    if not engine.is_ready():
        engine.reload()
    is_ready = engine.is_ready()
    return {
        "status": "ready" if is_ready else "maintenance",
        "ready": is_ready
    }


@app.get("/api/knowledge")
async def get_knowledge():
    """Trả về dữ liệu giáo dục tâm lý và trắc nghiệm (đã đóng gói)."""
    payload_data = {
        "distortions": COGNITIVE_DISTORTIONS,
        "articles": PSYCHOEDU_ARTICLES,
        "quizzes": ASSESSMENT_QUIZZES
    }
    encoded = b64_encode_text(json.dumps(payload_data, ensure_ascii=False))
    return {"d": encoded}


@app.post("/api/chat")
async def chat_stream(payload: EncryptedPayload, request: Request):
    """Xử lý chat thời gian thực qua Base64 Encoded Async SSE Stream (Non-blocking)."""
    client_ip = get_client_ip(request)
    check_rate_limit(client_ip)

    if not engine.is_ready():
        async def not_ready_gen():
            msg = b64_encode_text("Hệ thống đang bảo trì kết nối. Bạn vui lòng thử lại sau.")
            yield f"data: {json.dumps({'d': msg, 'f': 1})}\n\n"
        return StreamingResponse(not_ready_gen(), media_type="text/event-stream")

    data = b64_decode_json(payload.p)
    raw_messages = data.get("messages", [])
    mode = str(data.get("mode", "empathy"))[:20]
    raw_mood_context = data.get("mood_context")
    raw_temp = data.get("temperature", 0.8)

    try:
        temperature = max(0.0, min(2.0, float(raw_temp)))
    except (ValueError, TypeError):
        temperature = 0.8

    mood_context = None
    if isinstance(raw_mood_context, dict):
        try:
            s_level = max(1, min(10, int(raw_mood_context.get("stress_level", 4))))
        except (ValueError, TypeError):
            s_level = 4

        mood_context = {
            "mood_name": str(raw_mood_context.get("mood_name", "Bình yên"))[:50],
            "stress_level": s_level,
            "note": str(raw_mood_context.get("note", ""))[:500]
        }

    if not isinstance(raw_messages, list) or len(raw_messages) == 0:
        raise HTTPException(status_code=400, detail="Danh sách tin nhắn trống.")

    recent_raw = raw_messages[-30:]
    clean_messages = sanitize_messages_for_gemini(recent_raw)

    if not clean_messages:
        raise HTTPException(status_code=400, detail="Nội dung tin nhắn không hợp lệ.")

    async def event_generator():
        try:
            async for chunk in engine.async_stream_chat(
                messages=clean_messages,
                mode=mode,
                mood_context=mood_context,
                temperature=temperature
            ):
                if chunk:
                    encoded_chunk = b64_encode_text(chunk)
                    yield f"data: {json.dumps({'d': encoded_chunk, 'f': 0})}\n\n"

            yield f"data: {json.dumps({'d': '', 'f': 1})}\n\n"
        except Exception as exc:
            logger.error(f"Lỗi trong async event_generator: {exc}", exc_info=True)
            err_str = str(exc).lower()
            if any(kw in err_str for kw in ["429", "resource_exhausted", "quota", "rate limit", "too many requests"]):
                err_msg = b64_encode_text("**An Nhiên xin lỗi bạn nhé.**\n\nHiện tại mình đang cần vài phút tĩnh dưỡng và nạp lại năng lượng do số lượng cuộc trò chuyện trong phiên vượt quá giới hạn của hệ thống.\n\nTrong lúc chờ đợi, bạn hãy thử hít thở thật sâu, uống một ngụm nước ấm hoặc ghé qua mục Thư Giãn & Tĩnh Tâm để thả lỏng một chút nhé. Mình sẽ sớm quay lại cùng bạn.")
            else:
                err_msg = b64_encode_text("\n\n*(An Nhiên đang gặp gián đoạn kết nối tạm thời. Bạn hãy thử gửi lại sau giây lát nhé.)*")
            yield f"data: {json.dumps({'d': err_msg, 'f': 1})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Content-Type": "text/event-stream; charset=utf-8"
        }
    )


@app.post("/api/summary")
async def generate_summary(payload: EncryptedPayload, request: Request):
    """Tạo bản đúc kết lời nhắn nhủ (được mã hóa Base64)."""
    client_ip = get_client_ip(request)
    check_rate_limit(client_ip)

    if not engine.is_ready():
        raise HTTPException(status_code=503, detail="Dịch vụ chưa sẵn sàng.")

    data = b64_decode_json(payload.p)
    raw_messages = data.get("messages", [])
    if not isinstance(raw_messages, list) or len(raw_messages) < 2:
        raise HTTPException(status_code=400, detail="Cuộc trò chuyện quá ngắn.")

    clean_messages = sanitize_messages_for_gemini(raw_messages[-30:])
    summary_text = await engine.async_generate_session_summary(clean_messages)
    return {"d": b64_encode_text(summary_text)}



db_sessions: Dict[str, Dict[str, Any]] = {}
db_moods: List[Dict[str, Any]] = []
db_quiz_results: List[Dict[str, Any]] = []

class SessionCreateRequest(BaseModel):
    title: str = Field(default="Cuộc trò chuyện mới", max_length=100)
    messages: List[Dict[str, Any]] = Field(default_factory=list)

class SessionUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    messages: Optional[List[Dict[str, Any]]] = None

class MoodCreateRequest(BaseModel):
    mood: str = Field(..., max_length=50)
    stress_level: int = Field(..., ge=1, le=10)
    note: Optional[str] = Field(None, max_length=500)

class QuizResultCreateRequest(BaseModel):
    quiz_type: str = Field(..., max_length=20)
    score: int = Field(..., ge=0, le=30)
    severity: str = Field(..., max_length=100)
    advice: Optional[str] = Field(None, max_length=1000)


@app.get("/api/sessions", tags=["Chat Sessions CRUD"])
async def get_all_sessions():
    """[READ ALL] Lấy danh sách tất cả các cuộc trò chuyện đã lưu."""
    sessions_list = list(db_sessions.values())
    sessions_list.sort(key=lambda x: x.get("updatedAt", ""), reverse=True)
    return {"status": "success", "count": len(sessions_list), "data": sessions_list}

@app.post("/api/sessions", tags=["Chat Sessions CRUD"], status_code=201)
async def create_session(req: SessionCreateRequest):
    """[CREATE] Tạo một phiên trò chuyện mới."""
    session_id = f"sess_{int(time.time() * 1000)}"
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    session_data = {
        "id": session_id,
        "title": req.title,
        "createdAt": now_str,
        "updatedAt": now_str,
        "messages": req.messages if req.messages else []
    }
    db_sessions[session_id] = session_data
    return {"status": "success", "message": "Đã tạo phiên chat mới thành công", "data": session_data}

@app.get("/api/sessions/{session_id}", tags=["Chat Sessions CRUD"])
async def get_session_by_id(session_id: str):
    """[READ ONE] Lấy thông tin chi tiết một phiên trò chuyện theo ID."""
    if session_id not in db_sessions:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên trò chuyện.")
    return {"status": "success", "data": db_sessions[session_id]}

@app.put("/api/sessions/{session_id}", tags=["Chat Sessions CRUD"])
async def update_session(session_id: str, req: SessionUpdateRequest):
    """[UPDATE] Cập nhật tiêu đề hoặc tin nhắn của phiên chat."""
    if session_id not in db_sessions:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên trò chuyện.")
    sess = db_sessions[session_id]
    if req.title is not None:
        sess["title"] = req.title
    if req.messages is not None:
        sess["messages"] = req.messages
    sess["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {"status": "success", "message": "Đã cập nhật phiên chat", "data": sess}

@app.delete("/api/sessions/{session_id}", tags=["Chat Sessions CRUD"])
async def delete_session(session_id: str):
    """[DELETE] Xóa một phiên trò chuyện khỏi hệ thống."""
    if session_id not in db_sessions:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên trò chuyện.")
    del db_sessions[session_id]
    return {"status": "success", "message": f"Đã xóa thành công phiên chat {session_id}"}


@app.get("/api/moods", tags=["Mood Logs CRUD"])
async def get_all_mood_logs():
    """[READ ALL] Lấy toàn bộ nhật ký cảm xúc & mức độ áp lực."""
    return {"status": "success", "count": len(db_moods), "data": db_moods}

@app.post("/api/moods", tags=["Mood Logs CRUD"], status_code=201)
async def create_mood_log(req: MoodCreateRequest):
    """[CREATE] Ghi nhận nhật ký tâm trạng mới."""
    mood_id = f"mood_{int(time.time() * 1000)}"
    entry = {
        "id": mood_id,
        "mood": req.mood,
        "stressLevel": req.stress_level,
        "note": req.note,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    db_moods.insert(0, entry)
    return {"status": "success", "message": "Đã ghi nhận nhật ký cảm xúc", "data": entry}

@app.delete("/api/moods/{mood_id}", tags=["Mood Logs CRUD"])
async def delete_mood_log(mood_id: str):
    """[DELETE] Xóa một bản ghi nhật ký cảm xúc."""
    global db_moods
    db_moods = [m for m in db_moods if m.get("id") != mood_id]
    return {"status": "success", "message": f"Đã xóa bản ghi tâm trạng {mood_id}"}


@app.get("/api/quizzes/results", tags=["Quiz Results CRUD"])
async def get_all_quiz_results():
    """[READ ALL] Lấy lịch sử kết quả trắc nghiệm tâm lý (GAD-7 / PHQ-9)."""
    return {"status": "success", "count": len(db_quiz_results), "data": db_quiz_results}

@app.post("/api/quizzes/results", tags=["Quiz Results CRUD"], status_code=201)
async def create_quiz_result(req: QuizResultCreateRequest):
    """[CREATE] Lưu bản ghi kết quả đánh giá trắc nghiệm mới."""
    result_id = f"quiz_{int(time.time() * 1000)}"
    record = {
        "id": result_id,
        "quizType": req.quiz_type,
        "score": req.score,
        "severity": req.severity,
        "advice": req.advice,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    db_quiz_results.insert(0, record)
    return {"status": "success", "message": "Đã lưu kết quả trắc nghiệm", "data": record}

@app.delete("/api/quizzes/results/{result_id}", tags=["Quiz Results CRUD"])
async def delete_quiz_result(result_id: str):
    """[DELETE] Xóa một kết quả trắc nghiệm."""
    global db_quiz_results
    db_quiz_results = [q for q in db_quiz_results if q.get("id") != result_id]
    return {"status": "success", "message": f"Đã xóa kết quả trắc nghiệm {result_id}"}



static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=FileResponse)
async def serve_index():
    """Phục vụ file index.html qua FileResponse tối ưu I/O."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file, media_type="text/html")
    return HTMLResponse("<h1>Đang khởi tạo ứng dụng An Nhiên...</h1>")


if __name__ == "__main__":
    import socket

    import uvicorn

    def is_port_available(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", p)) != 0

    target_port = int(os.getenv("PORT", 5000))
    if not is_port_available(target_port):
        logger.warning(f"Cong {target_port} dang bi chiem dung, tu dong chuyen sang cong moi...")
        for fallback in range(target_port + 1, target_port + 10):
            if is_port_available(fallback):
                target_port = fallback
                break

    print("\n============================================================")
    print(f"AN NHIEN SERVER DA SAN SANG TAI: http://localhost:{target_port}")
    print(f"XEM TAI LIEU REST API (SWAGGER UI): http://localhost:{target_port}/docs")
    print("============================================================\n")

    uvicorn.run("server:app", host="0.0.0.0", port=target_port, reload=False)

