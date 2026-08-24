# AN NHIÊN TÂM LÝ — HỆ THỐNG TRỢ LÝ THAM VẤN & CHĂM SÓC SỨC KHỎE TINH THẦN

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/AI%20Model-Gemini%202.5%20Flash-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![CI/CD Status](https://img.shields.io/badge/CI%2FCD-Pipeline%20Passing-success?logo=github-actions&logoColor=white)](https://github.com/Slayerblack012/chatbot_tamly/actions)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff%20Compliant-black?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Unit Tests](https://img.shields.io/badge/Tests-22%2F22%20Passed-brightgreen?logo=pytest&logoColor=white)](https://pytest.org/)
[![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-059669)](https://www.w3.org/WAI/standards-guidelines/wcag/)
[![Docker](https://img.shields.io/badge/Docker-Ready%20(Non--root)-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An Nhiên Tâm Lý** là nền tảng trợ lý tham vấn tâm lý, thấu cảm và chăm sóc sức khỏe tinh thần toàn diện dành cho người Việt. Hệ thống kết hợp sức mạnh của **Mô hình Ngôn ngữ Lớn (LLM - Google Gemini 2.5 Flash)** với các cơ sở khoa học của **Liệu pháp Nhận thức - Hành vi (CBT)**, **Chánh niệm (Mindfulness)**, **Thang đo trắc nghiệm chuẩn hóa (GAD-7, PHQ-9, DASS-21)** và **Công nghệ Âm thanh Hướng dẫn Độc lập Thiết bị**.

---

## MỤC LỤC
1. [Bối Cảnh & Mục Tiêu Kỹ Thuật](#1-bối-cảnh--mục-tiêu-kỹ-thuật)
2. [Tính Năng Cốt Lõi (Core Features)](#2-tính-năng-cốt-lõi-core-features)
3. [Kiến Trúc Hệ Thống (System Architecture)](#3-kiến-trúc-hệ-thống-system-architecture)
4. [Ngăn Xếp Công Nghệ (Tech Stack)](#4-ngăn-xếp-công-nghệ-tech-stack)
5. [Cấu Trúc Thư Mục Dự Án (Directory Layout)](#5-cấu-trúc-thư-mục-dự-án-directory-layout)
6. [Tài Liệu REST API (API Specifications)](#6-tài-liệu-rest-api-api-specifications)
7. [Hướng Dẫn Cài Đặt & Chạy Cục Bộ (Local Setup)](#7-hướng-dẫn-cài-đặt--chạy-cục-bộ-local-setup)
8. [Kiểm Thử Tự Động & Đảm Bảo Chất Lượng (QA & Testing)](#8-kiểm-thử-tự-động--đảm-bảo-chất-lượng-qa--testing)
9. [Triển Khai Môi Trường Sản Xuất (Production Deployment)](#9-triển-khai-môi-trường-sản-xuất-production-deployment)
10. [Bảo Mật & Quyền Riêng Tư (Security & Privacy)](#10-bảo-mật--quyền-riêng-tư-security--privacy)

---

## 1. BỐI CẢNH & MỤC TIÊU KỸ THUẬT

### 1.1. Nỗi Đau Thực Tế (Pain Points)
- **Áp lực thế hệ & kiệt sức số**: Học sinh, sinh viên và người lao động trẻ đối diện với hội chứng kiệt sức (*burnout*), suy nghĩ quá mức (*overthinking*) và bất an xã hội.
- **Rào cản tiếp cận tham vấn truyền thống**: Chi phí cao, tâm lý sợ định kiến/phán xét, thiếu nguồn hỗ trợ thấu cảm vào khung giờ đêm muộn.
- **Hạn chế của Chatbot thế hệ cũ**: Đưa ra các câu an ủi sáo rỗng, thiếu tính chuyên môn tâm lý, không nhận diện được các bẫy méo mó nhận thức.

### 1.2. Giải Pháp Kỹ Thuật Đạt Được
- **Phản hồi thời gian thực dưới 1 giây (TTFT < 1s)** qua giao thức Server-Sent Events (SSE) bất đồng bộ.
- **Quy tắc Zero-Emoji trong lời thoại tham vấn**: AI phản hồi điềm đạm, lắng đọng, giữ khoảng lặng tôn trọng người dùng.
- **Hệ thống Can thiệp Khủng hoảng Chủ động (Crisis Intervention)**: Tự động phát hiện nguy cơ tự hại để đưa ra cứu trợ khẩn cấp.
- **Tương thích 100% đa thiết bị**: Chạy trơn tru trên mọi nền tảng không phụ thuộc cấu hình phần cứng.

---

## 2. TÍNH NĂNG CỐT LÕI (CORE FEATURES)

### 2.1. Động Cơ Tham Vấn AI Đa Phong Cách (Multi-Persona Engine)
- **Thấu Cảm (Empathy Mode - Mặc định)**: Lắng nghe không phán xét, phản chiếu cảm xúc (*Emotion Reflection*).
- **Tái Cấu Trúc Nhận Thức (CBT Mode)**: Nhận diện 8 bẫy tư duy sai lệch, đặt câu hỏi Socrates để chuyển hóa góc nhìn.
- **Chánh Niệm & Tĩnh Tâm (Mindfulness Mode)**: Hướng tâm trí về thực tại (*Grounding*), làm dịu phản ứng thần kinh chiến-hay-biến (*Fight-or-Flight*).
- **Ngữ cảnh thông minh**: Tự động nhận diện thời gian trong ngày (Sáng, Trưa, Chiều, Đêm khuya) để mở lời phù hợp.

### 2.2. Can Thiệp Khủng Hoảng (Crisis Safety Net)
- Tích hợp bộ lọc từ khóa nguy cấp theo thời gian thực (*Tự tử, kết thúc cuộc sống, tự hại, bế tắc cùng cực*).
- Kích hoạt **Banner cứu hộ khẩn cấp 24/7** hiển thị trực tiếp đường dây nóng miễn phí: **Tổng đài 111**, **Cấp cứu 115**, **Đường dây Ngày Mai (096 306 1414)**.

### 2.3. Bộ Tự Đánh Giá & Biểu Đồ Radar Tâm Lý (Psychometric Suite)
- **3 Thang đo chuẩn hóa quốc tế**:
  - **GAD-7**: Thang đo Rối loạn Lo âu Lan tỏa.
  - **PHQ-9**: Thang đo Mức độ Trầm cảm.
  - **DASS-21**: Thang đo Trầm cảm - Lo âu - Căng thẳng.
- **Biểu đồ Radar SVG Đa Chiều**: Tự động tổng hợp điểm số trên 5 trục cảm xúc (*Lo âu, Trầm cảm, Căng thẳng, Thể chất, Tự ti*) với biểu đồ lưới SVG thuần cực nhẹ.
- **CRUD Quản lý Lịch sử**: Lưu trữ phiên đánh giá cục bộ và đồng bộ API.

### 2.4. Góc Tĩnh Tâm & Động Cơ Âm Thanh Giọng Nữ Chuẩn
- **2 Phương pháp thở khoa học**:
  - **Thở 4-7-8 (Tiến sĩ Andrew Weil)**: Hít 4s -> Giữ 7s -> Thở 8s (Hạ cortisol, hỗ trợ ngủ sâu).
  - **Thở Đều 4-4-4-4 (Box Breathing - Navy SEALs)**: Hít 4s -> Giữ 4s -> Thở 4s -> Nghỉ 4s (Tập trung tinh thần).
- **Động cơ Giọng Nữ Tiếng Việt Chuẩn 100%**:
  - Tích hợp bộ tệp âm thanh giọng nữ studio tiếng Việt độc lập thiết bị (`/static/audio/tts/`), không bị lỗi giọng nam tiếng Anh trên máy tính Windows.
  - Hỗ trợ endpoint `/api/tts` dự phòng tự động nạp giọng nói trực tuyến.
- **Tiếng Chuông Thiền Tây Tạng (Tibetan Singing Bowl Synthesizer)**:
  - Tổng hợp sóng âm hài âm tự nhiên (*432Hz & 528Hz*) bằng **Web Audio API** chạy 100% offline.
- **Mốc thời gian tùy chọn**: `1 Phút`, `3 Phút (Chuẩn)`, `5 Phút`, `10 Phút`, `Tự do` kèm thanh tiến trình và bộ đếm chu kỳ.
- **Không gian âm thanh thư giãn**: Tích hợp tiếng Mưa rơi, Sóng biển, Tiếng chim rừng.
- **Kỹ thuật Neo Cảm Xúc 5-4-3-2-1**: Cắt đứt cơn hoảng loạn bằng 5 giác quan.

### 2.5. Giao Diện & Chuyển Động GPU 120 FPS (Celestial Theme)
- **Chuyển đổi Dark/Light Mode 3D**: Vòng tròn tỏa sáng góc nhấp chuột kết hợp **View Transitions API** và bụi sao phát sáng chuyển động 100% trên GPU compositor thread.
- **Hệ thống Font chữ chuẩn mực**:
  - Tiêu đề & Nhãn: **Outfit** (Đậm nét, hiện đại).
  - Thân bài & Nhập liệu: **Plus Jakarta Sans** (Độ tương phản cao, nét chữ công thái học).
- **Chế độ Bảo vệ Riêng tư (Auto-Idle Lock)**: Tự động khóa màn hình sau 1 giờ không hoạt động để bảo mật câu chuyện cá nhân.

---

## 3. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

```
                              ┌───────────────────────────────────────────────────┐
                              │           NGƯỜI DÙNG / TRÌNH DUYỆT                 │
                              │   (Mobile, Tablet, Desktop - WCAG 2.1 AA UI)     │
                              └─────────────────────────┬─────────────────────────┘
                                                        │
                              ┌─────────────────────────▼─────────────────────────┐
                              │           FRONTEND SINGLE PAGE APP (SPA)          │
                              │   - Vanilla ES6+ (Zero NPM Bloat)                 │
                              │   - Fail-Closed DOMPurify & Marked Markdown        │
                              │   - Web Audio API (Singing Bowl Synth 432Hz)      │
                              │   - Dedicated Vietnamese Female Audio Engine      │
                              │   - View Transitions API + GPU Particles          │
                              └─────────────────────────┬─────────────────────────┘
                                                        │ HTTP / Async SSE Streaming
                                                        │ (Base64 Obfuscated Payload)
                              ┌─────────────────────────▼─────────────────────────┐
                              │            FASTAPI BACKEND GATEWAY                │
                              │   - Security Headers (CSP, Nosniff, XSS, Frame)   │
                              │   - In-Memory Sliding Window Rate Limiter         │
                              │   - GZip Middleware Compression                   │
                              └──────┬──────────────────────┬───────────────┬─────┘
                                     │                      │               │
            ┌────────────────────────▼────────┐ ┌───────────▼─────────┐   ┌▼────────────────────┐
            │   AI CHAT STREAMING ENGINE      │ │   PSYCHOEDUCATION   │   │  AUDIO TTS ENGINE   │
            │ - Google GenAI Async SDK        │ │ - 8 CBT Distortions │   │ - Local Studio MP3s │
            │ - Gemini 2.5 Flash Primary      │ │ - GAD-7, PHQ-9, DASS│   │ - Dynamic TTS Cache │
            │ - Auto-Fallback (2.0 / 1.5)     │ │ - SVG Radar Chart   │   └─────────────────────┘
            │ - Crisis Keyword Interceptor    │ └─────────────────────┘
            └─────────────────────────────────┘
```

---

## 4. NGĂN XẾP CÔNG NGHỆ (TECH STACK)

| Phân Hệ | Công Nghệ Sử Dụng | Mục Đích & Điểm Vượt Trội |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.11 / 3.12, FastAPI, Uvicorn | Xử lý bất đồng bộ cao độ (*High Throughput Async I/O*), độ trễ thấp |
| **AI LLM Engine** | Google GenAI SDK (`google-genai`), Gemini 2.5 Flash | Khả năng thấu cảm tự nhiên, xử lý ngữ cảnh dài, TTFT < 1s |
| **Frontend Core** | Semantic HTML5, Vanilla CSS3 (Custom Properties), ES6+ JS | Không cồng kềnh, tải trang tức thì dưới 100ms, hoạt động ổn định |
| **Bảo Mật Frontend** | DOMPurify, Marked.js (Self-hosted) | Lọc sạch mã độc XSS theo cơ chế Fail-Closed an toàn tuyệt đối |
| **Âm Thanh & Tĩnh Tâm** | Web Audio API, Studio Vietnamese Female Audio | Chuông thiền 432Hz tự tổng hợp + Giọng nữ tiếng Việt chuẩn 100% |
| **Kiểm Định Mã Nguồn** | Ruff Linter & Formatter | Kiểm tra định dạng và chất lượng code siêu tốc |
| **Kiểm Thử Tự Động** | Pytest, Pytest-Asyncio, HTTPX | Bộ 22 bài kiểm thử tự động bao phủ API, Engine và Logic |
| **Container & CI/CD** | Docker (Multi-stage, Non-root user), GitHub Actions | Pipeline tự động kiểm tra code, test và build Docker image |
| **Cloud Hosting** | Render.com | Tự động triển khai từ nhánh `main` qua `render.yaml` |

---

## 5. CẤU TRÚC THƯ MỤC DỰ ÁN (DIRECTORY LAYOUT)

```
tamly-chatbot/
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD Pipeline (Lint, Test, Docker Dry-run)
│
├── api/
│   └── index.py               # Điểm nạp chuẩn (Entrypoint) cho Serverless & Cloud Deployments
│
├── core/
│   ├── __init__.py
│   ├── bot_engine.py          # Lõi kết nối Gemini Async SDK, Auto-Fallback & Cắt tỉa Context
│   ├── knowledge_base.py      # Dữ liệu CBT 8 bẫy tư duy, bài học tâm lý, GAD-7, PHQ-9, DASS-21
│   └── prompts.py             # Hệ thống Prompt tâm lý chuyên sâu (Zero Emoji Bot Dialog)
│
├── static/
│   ├── audio/
│   │   ├── tts/               # Bộ âm thanh giọng nữ tiếng Việt chuẩn (intro, inhale, hold, exhale, completed)
│   │   ├── rain.mp3           # Âm thanh thư giãn: Tiếng mưa rơi
│   │   ├── ocean_waves.mp3    # Âm thanh thư giãn: Sóng biển êm dịu
│   │   └── forest_birds.mp3   # Âm thanh thư giãn: Tiếng chim rừng
│   ├── css/
│   │   └── style.css          # Hệ thống CSS Design Tokens, Theme 3D GPU, Radar SVG, Responsive Grid
│   ├── js/
│   │   ├── vendor/
│   │   │   ├── marked.min.js  # Thư viện render Markdown tự lưu trữ (Offline)
│   │   │   └── purify.min.js  # Thư viện khử trùng XSS DOMPurify tự lưu trữ (Offline)
│   │   └── app.js             # Logic Frontend: SSE Streaming, Base64, Web Audio Synth, Voice Manager
│   ├── favicon.svg            # Biểu tượng thương hiệu SVG
│   └── index.html             # Giao diện Single Page Application thuần Việt
│
├── tests/
│   ├── __init__.py
│   ├── test_bot_engine.py     # 6 Tests: Prompt building, Context Sanitization, Candidate Models
│   ├── test_knowledge.py      # 4 Tests: Cấu trúc dữ liệu CBT, GAD-7, PHQ-9, Articles
│   └── test_server.py         # 12 Tests: API Routes, Base64 Decode, Rate Limit, Proxy IP, TTS Cache
│
├── .dockerignore              # Danh sách loại trừ khi đóng gói container
├── .env.example               # Mẫu cấu hình biến môi trường chuẩn
├── .gitignore                 # Danh sách loại trừ khỏi Git (Bảo mật .env)
├── Dockerfile                 # Khởi tạo container Python 3.12 non-root với Healthcheck
├── Procfile                   # Cấu hình process chạy trên máy chủ đám mây
├── pyproject.toml             # Cấu hình Ruff Linter & Pytest
├── README.md                  # Tài liệu kỹ thuật dự án
├── render.yaml                # Cấu hình tự động triển khai hạ tầng Render Web Service
├── requirements.txt           # Danh sách thư viện Python phụ thuộc
├── run.bat                    # Script khởi chạy nhanh 1 chạm trên Windows
├── run.py                     # Script khởi chạy kèm tự động dò tìm cổng trống & mở trình duyệt
└── server.py                  # Máy chủ FastAPI, Middleware bảo mật, Rate Limiter & CRUD APIs
```

---

## 6. TÀI LIỆU REST API (API SPECIFICATIONS)

Hệ thống cung cấp giao diện Swagger UI tương tác tại: `http://localhost:8000/docs`

| Phương Thức | Đường Dẫn (Endpoint) | Chức Năng | Mô Tả & Tham Số |
| :---: | :--- | :--- | :--- |
| `POST` | `/api/chat` | **Hội Thoại AI (Streaming)** | Nhận payload Base64 `{"p": "<base64>"}` và trả về stream văn bản Server-Sent Events (SSE) |
| `GET` | `/api/health` | **Kiểm Tra Trạng Thái** | Trả về trạng thái server, Gemini readiness và phiên bản (`status: ok`) |
| `GET` | `/api/tts` | **Đọc Giọng Nữ Tiếng Việt** | Trả về file audio stream `audio/mpeg` cho tham số `?text=...` (Kèm bộ đệm in-memory) |
| `GET` | `/api/knowledge/distortions` | **8 Bẫy Tư Duy CBT** | Danh sách định nghĩa, ví dụ và câu hỏi phản tư cho 8 bẫy nhận thức |
| `GET` | `/api/knowledge/articles` | **Bài Viết Tâm Lý** | Kho bài đọc giáo dục tâm lý theo danh mục |
| `GET` | `/api/knowledge/quizzes` | **Dữ Liệu Trắc Nghiệm** | Câu hỏi và thang điểm cho GAD-7, PHQ-9, DASS-21 |
| `GET` | `/api/quizzes/results` | **Lấy Lịch Sử Đánh Giá** | Danh sách kết quả trắc nghiệm đã lưu |
| `POST` | `/api/quizzes/results` | **Lưu Kết Quả Trắc Nghiệm** | Thêm mới một bản ghi điểm số trắc nghiệm |
| `DELETE`| `/api/quizzes/results/{id}` | **Xóa Kết Quả Trắc Nghiệm** | Xóa bản ghi trắc nghiệm theo ID |

---

## 7. HƯỚNG DẪN CÀI ĐẶT & CHẠY CỤC BỘ (LOCAL SETUP)

### Bước 1: Yêu cầu tiên quyết
- **Python 3.11** hoặc **Python 3.12** đã được cài đặt trên hệ thống.
- Git để quản lý mã nguồn.

### Bước 2: Clone kho lưu trữ
```bash
git clone https://github.com/Slayerblack012/chatbot_tamly.git
cd chatbot_tamly
```

### Bước 3: Tạo môi trường ảo & Cài đặt thư viện
```bash
# Trên Windows
python -m venv .venv
.venv\Scripts\activate

# Trên macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Nâng cấp pip và cài đặt thư viện
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Cấu hình biến môi trường
Tạo file `.env` tại thư mục gốc của dự án:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
```
> *(Nhận API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/)).*

### Bước 5: Khởi chạy ứng dụng

- **Khởi chạy Giao diện Web (Khuyên dùng)**:
  ```bash
  python run.py
  ```
  *(Script sẽ tự động kiểm tra cổng khả dụng và mở trình duyệt tại `http://localhost:8000`).*

- **Khởi chạy qua Uvicorn trực tiếp**:
  ```bash
  uvicorn server:app --host 127.0.0.1 --port 8000 --reload
  ```

- **Khởi chạy Chế độ Dòng lệnh (CLI Terminal)**:
  ```bash
  python main.py
  ```

---

## 8. KIỂM THỬ TỰ ĐỘNG & ĐẢM BẢO CHẤT LƯỢNG (QA & TESTING)

Dự án áp dụng quy trình kiểm soát chất lượng nghiêm ngặt trước mỗi commit:

```bash
# 1. Kiểm tra Linter & Định dạng mã nguồn (Ruff)
ruff check .

# 2. Tự động sửa lỗi định dạng nếu có
ruff check --fix .

# 3. Kiểm tra tính toàn vẹn gói phụ thuộc
python -m pip check

# 4. Chạy toàn bộ 22 bài kiểm thử tự động (Unit Test Suite)
pytest -v
```

---

## 9. TRIỂN KHAI MÔI TRƯỜNG SẢN XUẤT (PRODUCTION DEPLOYMENT)

### Cách 1: Tự động qua Render Cloud (Khuyên dùng)
Dự án đã tích hợp sẵn tệp cấu hình hạ tầng [`render.yaml`](file:///d:/AI_md_siking/tamly-chatbot/render.yaml):
1. Đẩy mã nguồn lên GitHub.
2. Tại [Render Dashboard](https://dashboard.render.com/) -> Chọn **New Blueprint Instance** -> Chọn repository `chatbot_tamly`.
3. Điền giá trị `GEMINI_API_KEY` tại mục biến môi trường.
4. Render sẽ tự động build và cấp phát HTTPS miễn phí.

### Cách 2: Triển khai với Docker Container
```bash
# Xây dựng Docker image
docker build -t an-nhien-tam-ly:latest .

# Khởi chạy container với biến môi trường
docker run -d \
  --name an-nhien-app \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your_api_key_here" \
  --restart unless-stopped \
  an-nhien-tam-ly:latest
```

---

## 10. BẢO MẬT & QUYỀN RIÊNG TƯ (SECURITY & PRIVACY)

- **Ngăn Chặn Nghe Lén Payload**: Dữ liệu gửi từ Client lên Server được mã hóa Base64 Obfuscation, hạn chế việc quét chuỗi trần (*Plaintext Inspection*).
- **Bộ Header An Ninh Chuẩn Doanh Nghiệp**:
  - `Content-Security-Policy`: Khóa chặt miền tài nguyên hợp lệ, chống nhúng script độc hại.
  - `X-Content-Type-Options: nosniff`: Chống tấn công MIME type sniffing.
  - `X-Frame-Options: SAMEORIGIN`: Chống tấn công Clickjacking.
  - `X-XSS-Protection: 1; mode=block`: Kích hoạt bộ lọc XSS của trình duyệt.
- **Fail-Closed DOMPurify**: Khử trùng 100% nội dung HTML/Markdown trước khi chèn vào DOM.
- **Giới Hạn Tần Suất Yêu Cầu (Rate Limiting)**: Chống Spam và DoS với thuật toán Sliding Window (Tối đa 45 requests/phút/IP), hỗ trợ nhận diện IP thật qua Proxy/Cloudflare.
- **Khóa Phiên Tự Động (Auto-Lock)**: Tự động che mờ và khóa nội dung sau 60 phút không tương tác để bảo vệ quyền riêng tư nếu người dùng rời khỏi thiết bị.
