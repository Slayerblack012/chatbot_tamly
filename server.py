import base64
import binascii
import json
import logging
import os
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional

from core.runtime import add_project_venv_to_path, find_available_port

add_project_venv_to_path()

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.bot_engine import (
    AUTH_FAILURE_MESSAGE,
    CounselorEngine,
    get_fallback_message,
    sanitize_messages_for_gemini,
)
from core.crisis import CRISIS_RESPONSE, is_crisis_message, latest_user_message
from core.knowledge_base import (
    ASSESSMENT_QUIZZES,
    AUDIO_TRACKS,
    BREATHING_REFERENCES,
    COGNITIVE_DISTORTIONS,
    PSYCHOEDU_ARTICLES,
    PSYCHOLOGICAL_FACILITIES,
)

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
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_and_privacy_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.url.path in ("/static/sw.js", "/static/manifest.webmanifest"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

    csp_directives = [
        "default-src 'self' https: data: blob: 'unsafe-inline'",
        "script-src 'self' 'unsafe-inline' https: cdn.jsdelivr.net",
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
    for known_ip, timestamps in list(request_history.items()):
        if not timestamps or now - timestamps[-1] >= RATE_LIMIT_WINDOW:
            request_history.pop(known_ip, None)
    valid_timestamps = [t for t in request_history[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(valid_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        request_history[client_ip] = valid_timestamps
        logger.warning("Rate limit triggered.")
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
    logger.error("Lỗi khởi tạo CounselorEngine (%s).", type(exc).__name__)
    raise RuntimeError("GEMINI_API_KEY không hợp lệ hoặc thiếu. Kiểm tra file .env") from None


def b64_decode_json(encoded_str: str) -> Dict[str, Any]:
    try:
        raw_bytes = base64.b64decode(encoded_str, validate=True)
        payload = json.loads(raw_bytes.decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        logger.warning("Lỗi giải mã Base64 payload (%s).", type(exc).__name__)
        raise HTTPException(status_code=400, detail="Dữ liệu truyền tải không hợp lệ.")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Dữ liệu truyền tải không hợp lệ.")
    return payload


def b64_encode_text(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


class Base64Payload(BaseModel):
    p: str = Field(..., min_length=1, max_length=150000)


class TTSRequest(BaseModel):
    text: str = Field(..., max_length=200)


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
    """Trả về dữ liệu giáo dục tâm lý, trắc nghiệm và danh bạ cơ sở khám (đã đóng gói)."""
    payload_data = {
        "distortions": COGNITIVE_DISTORTIONS,
        "articles": PSYCHOEDU_ARTICLES,
        "quizzes": ASSESSMENT_QUIZZES,
        "facilities": PSYCHOLOGICAL_FACILITIES,
        "audio_tracks": AUDIO_TRACKS,
        "breathing_references": BREATHING_REFERENCES,
    }
    encoded = b64_encode_text(json.dumps(payload_data, ensure_ascii=False))
    return {"d": encoded}


@app.get("/api/facilities", tags=["Psychological Facilities Directory"])
async def get_facilities(location: Optional[str] = None):
    """Return directory entries with field-level verification; unverified details remain withheld."""
    facilities = PSYCHOLOGICAL_FACILITIES
    if location:
        loc = location.strip().lower()
        facilities = [
            f for f in facilities
            if f.get("location") == loc
            or loc in str(f.get("city") or "").lower()
            or loc in str(f.get("province") or "").lower()
        ]
    return {
        "status": "success",
        "location": location or "all",
        "count": len(facilities),
        "data": facilities
    }


@app.post("/api/chat")
async def chat_stream(payload: Base64Payload, request: Request):
    """Stream chat responses and intercept configured crisis phrases before provider use."""
    client_ip = get_client_ip(request)
    check_rate_limit(client_ip)

    data = b64_decode_json(payload.p)
    raw_messages = data.get("messages", [])
    if not isinstance(raw_messages, list) or len(raw_messages) == 0:
        raise HTTPException(status_code=400, detail="Danh sách tin nhắn trống.")
    if any(not isinstance(message, dict) for message in raw_messages):
        raise HTTPException(status_code=400, detail="Danh sách tin nhắn không hợp lệ.")

    if len(raw_messages) > 30:
        raise HTTPException(status_code=400, detail="Quá nhiều tin nhắn (tối đa 30)")
    total_chars = sum(len(str(m.get("content", ""))) for m in raw_messages)
    if total_chars > 50000:
        raise HTTPException(status_code=400, detail="Nội dung hội thoại quá dài")

    recent_raw = raw_messages[-30:]
    clean_messages = sanitize_messages_for_gemini(recent_raw)
    if not clean_messages:
        raise HTTPException(status_code=400, detail="Nội dung tin nhắn không hợp lệ.")

    if is_crisis_message(latest_user_message(recent_raw)):
        async def crisis_event_generator():
            encoded = b64_encode_text(CRISIS_RESPONSE)
            yield f"data: {json.dumps({'d': encoded, 'f': 0})}\n\n"
            yield f"data: {json.dumps({'d': '', 'f': 1})}\n\n"

        return StreamingResponse(
            crisis_event_generator(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"}
        )

    if not engine.is_ready():
        engine.reload()

    if not engine.is_ready():
        async def not_ready_gen():
            msg = b64_encode_text(AUTH_FAILURE_MESSAGE)
            yield f"data: {json.dumps({'d': msg, 'f': 1})}\n\n"
        return StreamingResponse(not_ready_gen(), media_type="text/event-stream")

    mode = str(data.get("mode", "empathy"))[:20]
    raw_mood_context = data.get("mood_context")
    raw_temp = data.get("temperature", 0.65)

    try:
        temperature = max(0.0, min(2.0, float(raw_temp)))
    except (ValueError, TypeError):
        temperature = 0.65

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
            logger.error("Lỗi trong async event_generator (%s).", type(exc).__name__)
            err_msg = b64_encode_text(get_fallback_message(exc))
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
async def generate_summary(payload: Base64Payload, request: Request):
    """Generate a summary from Base64-encoded conversation data."""
    client_ip = get_client_ip(request)
    check_rate_limit(client_ip)

    data = b64_decode_json(payload.p)
    raw_messages = data.get("messages", [])
    if not isinstance(raw_messages, list) or len(raw_messages) < 2:
        raise HTTPException(status_code=400, detail="Cuộc trò chuyện quá ngắn.")
    if any(not isinstance(message, dict) for message in raw_messages):
        raise HTTPException(status_code=400, detail="Danh sách tin nhắn không hợp lệ.")

    clean_messages = sanitize_messages_for_gemini(raw_messages[-30:])
    if len(clean_messages) < 2:
        raise HTTPException(status_code=400, detail="Cuộc trò chuyện quá ngắn.")
    if not engine.is_ready():
        raise HTTPException(status_code=503, detail="Dịch vụ chưa sẵn sàng.")

    summary_text = await engine.async_generate_session_summary(clean_messages)
    return {"d": b64_encode_text(summary_text)}



@app.delete("/api/privacy/data", tags=["Privacy"])
async def delete_server_data():
    """Confirm that no chat, mood, or assessment records are retained by this application server."""
    return {
        "status": "complete",
        "server_records_deleted": 0,
        "server_retains_health_records": False,
        "note": "The app server does not store user chat, mood, or quiz records. Data already sent to the AI provider is outside this endpoint's control."
    }


@app.post("/api/tts", tags=["Voice Engine"])
async def get_vietnamese_tts(payload: TTSRequest):
    """Request Vietnamese speech from the external TTS service without caching the text."""
    cleaned_text = payload.text.strip()
    if not cleaned_text:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp văn bản cần đọc")

    try:
        import httpx
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(
                "https://translate.google.com/translate_tts",
                params={"ie": "UTF-8", "tl": "vi", "client": "tw-ob", "q": cleaned_text},
                headers={"User-Agent": "Mozilla/5.0"}
            )
            if resp.status_code == 200 and len(resp.content) > 500:
                return Response(content=resp.content, media_type="audio/mpeg")
    except Exception:
        logger.warning("Không thể tải TTS từ nhà cung cấp.")

    raise HTTPException(status_code=502, detail="Không thể tạo giọng đọc lúc này")




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    static_dir = os.path.join(os.path.dirname(BASE_DIR), "static")
os.makedirs(static_dir, exist_ok=True)


@app.get("/static/audio/{audio_name}", tags=["Audio Attribution"])
async def get_attributed_audio(audio_name: str):
    track = next((item for item in AUDIO_TRACKS if item["file"] == audio_name), None)
    if not track or not track["publishable"]:
        raise HTTPException(status_code=404, detail="Tệp âm thanh đang bị chặn do chưa xác minh nguồn và giấy phép.")
    return FileResponse(os.path.join(static_dir, "audio", track["file"]), media_type="audio/mpeg")


app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=FileResponse)
@app.get("/api", response_class=FileResponse)
@app.get("/api/index.py", response_class=FileResponse)
async def serve_index():
    """Phục vụ file index.html qua FileResponse tối ưu I/O."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file, media_type="text/html")
    return HTMLResponse("<h1>Đang khởi tạo ứng dụng An Nhiên...</h1>")


if __name__ == "__main__":
    import uvicorn

    target_port = int(os.getenv("PORT", 8000))
    available_port = find_available_port(target_port)
    if available_port != target_port:
        logger.warning("Cổng %s đang bị chiếm, chuyển sang cổng %s.", target_port, available_port)
        target_port = available_port

    print("\n============================================================")
    print(f"AN NHIEN SERVER DA SAN SANG TAI: http://localhost:{target_port}")
    print(f"XEM TAI LIEU REST API (SWAGGER UI): http://localhost:{target_port}/docs")
    print("============================================================\n")

    uvicorn.run("server:app", host="0.0.0.0", port=target_port, reload=False)

