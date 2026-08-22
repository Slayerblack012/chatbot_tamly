"""
Server Backend cho An Nhiên Edu-Psychology Platform (Encrypted Payload & Zero Tech Disclosure).
Hỗ trợ Base64 payload encoding, Rate Limiting, Security Headers & Ẩn hoàn toàn thông tin công nghệ/API.
"""

import os
import time
import json
import base64
import asyncio
from collections import defaultdict
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.bot_engine import CounselorEngine
from core.knowledge_base import COGNITIVE_DISTORTIONS, PSYCHOEDU_ARTICLES, ASSESSMENT_QUIZZES

load_dotenv()

app = FastAPI(
    title="An Nhien Platform",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 2. Middleware xóa sạch thông tin Server & thêm Security Headers
@app.middleware("http")
async def security_and_privacy_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Xóa header tiết lộ công nghệ máy chủ
    if "Server" in response.headers:
        del response.headers["Server"]
    return response

# 3. Rate Limiting in-memory chống DoS / Spam
RATE_LIMIT_WINDOW = 60
MAX_REQUESTS_PER_WINDOW = 45
request_history: Dict[str, List[float]] = defaultdict(list)

def check_rate_limit(client_ip: str):
    now = time.time()
    request_history[client_ip] = [t for t in request_history[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(request_history[client_ip]) >= MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(
            status_code=429,
            detail="Yêu cầu quá nhanh. Vui lòng thử lại sau giây lát."
        )
    request_history[client_ip].append(now)

# Khởi tạo Engine (API Key quản lý bí mật 100% trong .env máy chủ)
engine = CounselorEngine()

# Helpers mã hóa & giải mã Base64
def b64_decode_json(encoded_str: str) -> Dict[str, Any]:
    try:
        raw_bytes = base64.b64decode(encoded_str.encode("utf-8"))
        return json.loads(raw_bytes.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Dữ liệu truyền tải không hợp lệ.")

def b64_encode_text(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


class EncryptedPayload(BaseModel):
    p: str = Field(..., min_length=1, max_length=150000)


@app.get("/api/health")
async def health_check():
    """Endpoint kiểm tra trạng thái chung (không tiết lộ công nghệ)."""
    return {
        "status": "ready" if engine.is_ready() else "not_configured"
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
    """Xử lý chat thời gian thực qua Base64 Encoded SSE Stream."""
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    if not engine.is_ready():
        async def not_ready_gen():
            msg = b64_encode_text("⚠️ Hệ thống đang bảo trì kết nối. Bạn vui lòng thử lại sau.")
            yield f"data: {json.dumps({'d': msg, 'f': 1})}\n\n"
        return StreamingResponse(not_ready_gen(), media_type="text/event-stream")

    # Giải mã Base64
    data = b64_decode_json(payload.p)
    raw_messages = data.get("messages", [])
    mode = data.get("mode", "empathy")
    mood_context = data.get("mood_context")
    temperature = data.get("temperature", 0.8)

    # Validation cơ bản
    if not isinstance(raw_messages, list) or len(raw_messages) == 0:
        raise HTTPException(status_code=400, detail="Danh sách tin nhắn trống.")

    # Giới hạn số lượng & độ dài tin nhắn
    clean_messages = []
    for m in raw_messages[-50:]:
        role = "user" if m.get("role") == "user" else "model"
        content = str(m.get("content", ""))[:6000]
        if content:
            clean_messages.append({"role": role, "content": content})

    async def event_generator():
        try:
            stream = engine.stream_chat(
                messages=clean_messages,
                mode=mode,
                mood_context=mood_context,
                temperature=temperature
            )
            for chunk in stream:
                if chunk:
                    encoded_chunk = b64_encode_text(chunk)
                    yield f"data: {json.dumps({'d': encoded_chunk, 'f': 0})}\n\n"
                    await asyncio.sleep(0)

            yield f"data: {json.dumps({'d': '', 'f': 1})}\n\n"
        except Exception as exc:
            err_str = str(exc).lower()
            if any(kw in err_str for kw in ["429", "resource_exhausted", "quota", "rate limit", "too many requests"]):
                err_msg = b64_encode_text("☕ **An Nhiên xin lỗi bạn nhé...**\n\nHiện tại mình đang cần vài phút tĩnh dưỡng và nạp lại năng lượng do số lượng cuộc trò chuyện trong phiên vượt quá giới hạn của hệ thống.\n\n🌿 Trong lúc chờ đợi, bạn hãy thử hít thở thật sâu, uống một ngụm nước ấm hoặc ghé qua tab **🧘 Thư Giãn & Tĩnh Tâm** để thả lỏng một chút nhé. Mình sẽ sớm quay lại cùng bạn! 💛✨")
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
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    if not engine.is_ready():
        raise HTTPException(status_code=503, detail="Dịch vụ chưa sẵn sàng.")

    data = b64_decode_json(payload.p)
    raw_messages = data.get("messages", [])
    clean_messages = []
    for m in raw_messages[-50:]:
        role = "user" if m.get("role") == "user" else "model"
        content = str(m.get("content", ""))[:6000]
        if content:
            clean_messages.append({"role": role, "content": content})

    summary_text = engine.generate_session_summary(clean_messages)
    return {"d": b64_encode_text(summary_text)}


# Phục vụ Static Files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Đang khởi tạo...</h1>"
