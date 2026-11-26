# AN NHIÊN TÂM LÝ — HỆ THỐNG TRỢ LÝ THAM VẤN & CHĂM SÓC SỨC KHỎE TINH THẦN

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![CI/CD Status](https://img.shields.io/badge/CI%2FCD-Pipeline%20Passing-success?logo=github-actions&logoColor=white)](https://github.com/Slayerblack012/chatbot_tamly/actions)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff%20Compliant-black?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Unit Tests](https://img.shields.io/badge/Tests-pytest-brightgreen?logo=pytest&logoColor=white)](https://pytest.org/)
[![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-059669)](https://www.w3.org/WAI/standards-guidelines/wcag/)
[![Docker](https://img.shields.io/badge/Docker-Ready%20(Non--root)-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An Nhiên Tâm Lý** là ứng dụng hỗ trợ cảm xúc dành cho người Việt, hướng đến học sinh. Ứng dụng không chẩn đoán hoặc thay thế dịch vụ y tế. Các câu hỏi PHQ-9/GAD-7 chỉ là công cụ sàng lọc; bản PHQ-9 tiếng Việt hiện tại chưa được xác minh là bản dịch chuẩn hóa.

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
- **Áp lực học đường & kiệt sức số**: Học sinh đối diện với áp lực học tập, thi cử, suy nghĩ quá mức (*overthinking*) và bất an xã hội.
- **Rào cản tiếp cận tham vấn truyền thống**: Chi phí cao, tâm lý sợ định kiến/phán xét, thiếu nguồn hỗ trợ thấu cảm vào khung giờ đêm muộn.
- **Hạn chế của Chatbot thế hệ cũ**: Đưa ra các câu an ủi sáo rỗng, thiếu tính chuyên môn tâm lý, không nhận diện được các bẫy méo mó nhận thức.

### 1.2. Giải Pháp Kỹ Thuật Đạt Được
- **Phản hồi streaming** qua giao thức Server-Sent Events (SSE) bất đồng bộ; độ trễ phụ thuộc mạng và nhà cung cấp.
- **Quy tắc Zero-Emoji trong lời thoại tham vấn**: AI phản hồi điềm đạm, lắng đọng, giữ khoảng lặng tôn trọng người dùng.
- **Hỗ trợ khủng hoảng theo luật từ khóa**: Kiểm tra một số cách diễn đạt gián tiếp ở trình duyệt và máy chủ, sau đó hiển thị thông tin hỗ trợ cùng câu hỏi kiểm tra an toàn. Đây không phải công cụ triage lâm sàng.
- **Giao diện thích ứng**: Hỗ trợ trình duyệt phổ biến; cần kiểm thử trên thiết bị mục tiêu trước phát hành.

---

## 2. TÍNH NĂNG CỐT LÕI (CORE FEATURES)

### 2.1. Động Cơ Tham Vấn AI Đa Phong Cách (Multi-Persona Engine)
- **Thấu Cảm (Empathy Mode - Mặc định)**: Lắng nghe không phán xét, phản chiếu cảm xúc (*Emotion Reflection*).
- **Tái Cấu Trúc Nhận Thức (CBT Mode)**: Nhận diện 8 bẫy tư duy sai lệch, đặt câu hỏi Socrates để chuyển hóa góc nhìn.
- **Chánh Niệm & Tĩnh Tâm (Mindfulness Mode)**: Hướng tâm trí về thực tại (*Grounding*), làm dịu phản ứng thần kinh chiến-hay-biến (*Fight-or-Flight*).
- **Ngữ cảnh thông minh**: Tự động nhận diện thời gian trong ngày (Sáng, Trưa, Chiều, Đêm khuya) để mở lời phù hợp.

### 2.2. Can Thiệp Khủng Hoảng (Crisis Safety Net)
- Bộ dò luật từ khóa xử lý một số câu trực tiếp/gián tiếp ở trình duyệt và máy chủ; đây không phải phát hiện đầy đủ mọi nguy cơ.
- Câu trả lời khẩn cấp hiển thị **111**, **115**, **Đường dây Ngày Mai (096 306 1414)** trước câu hỏi kiểm tra an toàn. Cần xác minh số và khả năng hoạt động trước production.

### 2.3. Bộ Tự Đánh Giá & Biểu Đồ Radar Tâm Lý (Psychometric Suite)
- **Công cụ tự sàng lọc**:
  - **GAD-7**: Thang đo Rối loạn Lo âu Lan tỏa.
  - **PHQ-9**: Công cụ sàng lọc triệu chứng trầm cảm; bản tiếng Việt trong ứng dụng chưa được thẩm định.
- **Biểu đồ Radar SVG Đa Chiều**: Tự động tổng hợp điểm số trên 5 trục cảm xúc (*Lo âu, Trầm cảm, Căng thẳng, Thể chất, Tự ti*) với biểu đồ lưới SVG thuần cực nhẹ.
- Lịch sử hội thoại chỉ lưu trên trình duyệt; ứng dụng không lưu kết quả sàng lọc trên máy chủ.

### 2.4. Góc Tĩnh Tâm & Âm Thanh
- **Bài tập thở có nguồn tham khảo**: thở 4-7-8 và box breathing; đây là bài tập tự nguyện, dừng nếu thấy khó chịu.
- **Giọng đọc tiếng Việt**: endpoint `/api/tts` chuyển văn bản qua dịch vụ ngoài; có thể không khả dụng và không nên gửi thông tin nhận dạng.
- **Tiếng Chuông Thiền Tây Tạng (Tibetan Singing Bowl Synthesizer)**:
  - Tổng hợp sóng âm hài âm tự nhiên (*432Hz & 528Hz*) bằng **Web Audio API** chạy 100% offline.
- **Mốc thời gian tùy chọn**: `1 Phút`, `3 Phút (Chuẩn)`, `5 Phút`, `10 Phút`, `Tự do` kèm thanh tiến trình và bộ đếm chu kỳ.
- **Không gian âm thanh**: các tệp nhạc đang bị chặn khỏi giao diện/API vì repo chưa có bằng chứng nguồn và giấy phép.
- **Kỹ thuật neo cảm xúc 5-4-3-2-1**: Bài tập tự nguyện đưa sự chú ý về giác quan; không thay thế hỗ trợ chuyên môn.

### 2.5. Giao Diện & Chuyển Động GPU 120 FPS (Celestial Theme)
- **Chuyển đổi Dark/Light Mode 3D**: Vòng tròn tỏa sáng góc nhấp chuột kết hợp **View Transitions API** và bụi sao phát sáng chuyển động 100% trên GPU compositor thread.
- **Bảng màu thương hiệu bất biến**: Mọi giao diện phải giữ bảng màu An Nhiên; chỉ được chuyển giữa các bộ màu sáng/tối đã duyệt. Xem [quy tắc design system](docs/design-system.md).
- **Hệ thống Font chữ chuẩn mực**:
  - Tiêu đề & Nhãn: **Outfit** (Đậm nét, hiện đại).
  - Thân bài & Nhập liệu: **Plus Jakarta Sans** (Độ tương phản cao, nét chữ công thái học).
- **Chế độ Bảo vệ Riêng tư (Auto-Idle Lock)**: Tự động khóa màn hình sau 1 giờ không hoạt động để bảo mật câu chuyện cá nhân.

### 2.6. Danh Bạ Cơ Sở Khám & Tham Vấn Tâm Lý Uy Tín (Mental Health Directory)
- **Danh bạ Đồng Nai có đối chiếu theo từng trường**: chỉ địa chỉ, liên hệ, giờ làm và chuyên môn đã đối chiếu từ nguồn chính thức mới được hiển thị; các mục chưa xác minh được giữ ẩn.

---

## 3. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

```
                              ┌───────────────────────────────────────────────────┐
                              │           NGƯỜI DÙNG / TRÌNH DUYỆT                 │
                              │   (Mobile-first UI; cần audit WCAG trước release) │
                              └─────────────────────────┬─────────────────────────┘
                                                        │
                              ┌─────────────────────────▼─────────────────────────┐
                              │           FRONTEND SINGLE PAGE APP (SPA)          │
                              │   - Vanilla ES6+ (Zero NPM Bloat)                 │
                              │   - Fail-Closed DOMPurify & Marked Markdown        │
                              │   - Crisis dialog + hard-delete local history     │
                              │   - License-gated audio metadata                 │
                              │   - View Transitions API + GPU Particles          │
                              └─────────────────────────┬─────────────────────────┘
                                                        │ HTTP / Async SSE Streaming
                                                        │ (Base64 transport encoding; not encryption)
                              ┌─────────────────────────▼─────────────────────────┐
                              │            FASTAPI BACKEND GATEWAY                │
                              │   - Security Headers (CSP, Nosniff, Frame)        │
                              │   - In-Memory Sliding Window Rate Limiter         │
                              │   - GZip Middleware Compression                   │
                              └──────┬──────────────────────┬───────────────┬─────┘
                                     │                      │               │
            ┌────────────────────────▼────────┐ ┌───────────▼─────────┐   ┌▼────────────────────┐
            │   AI CHAT STREAMING ENGINE      │ │   PSYCHOEDUCATION   │   │  AUDIO TTS ENGINE   │
            │ - Configured external AI       │ │ - CBT and education │   │ - TTS provider      │
            │ - Configured model              │ │ - GAD-7 / PHQ-9     │   │ - Bundled tracks    │
            │ - Crisis response before AI    │ │ - Verification flags│   │   blocked           │
            │                                 │ └─────────────────────┘   └─────────────────────┘
            └─────────────────────────────────┘
```

---

## 4. NGĂN XẾP CÔNG NGHỆ (TECH STACK)

| Phân Hệ | Công Nghệ Sử Dụng | Mục Đích & Điểm Vượt Trội |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.11 / 3.12, FastAPI, Uvicorn | Xử lý bất đồng bộ cao độ (*High Throughput Async I/O*), độ trễ thấp |
| **AI Engine** | External AI service, configured model | AI handles ordinary chat; crisis branch bypasses external processing |
| **Frontend Core** | Semantic HTML5, Vanilla CSS3 (Custom Properties), ES6+ JS | Không cồng kềnh, tải trang tức thì dưới 100ms, hoạt động ổn định |
| **Bảo Mật Frontend** | DOMPurify, Marked.js (Self-hosted) | Sanitization and CSP are defense-in-depth, not a security guarantee |
| **Âm Thanh & Tĩnh Tâm** | Web Audio API, source/license metadata | Bundled tracks blocked until licensing evidence is recorded |
| **Kiểm Định Mã Nguồn** | Ruff Linter & Formatter | Kiểm tra định dạng và chất lượng code siêu tốc |
| **Kiểm Thử Tự Động** | Pytest, Pytest-Asyncio, HTTPX | Tests cover API, crisis, screening metadata, facilities and licensing gates |
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
│   ├── bot_engine.py          # Kết nối dịch vụ AI, Auto-Fallback & Cắt tỉa Context
│   ├── crisis.py              # Rule-based crisis detector and fixed safety response
│   ├── knowledge_base.py      # CBT, screening, sourced articles, facility/audio metadata
│   └── prompts.py             # Short, non-judgmental counselor prompt
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
│   ├── privacy-policy.html    # User-facing privacy notice (draft)
│   ├── terms-of-use.html      # Terms (draft)
│   └── index.html             # Giao diện Single Page Application thuần Việt
│
├── docs/
│   ├── crisis-runbook.md      # Crisis service operations and incident response
│   ├── design-system.md       # Immutable An Nhiên brand color and UI rules
│   └── implementation-plan.md # Priorities, architecture, risks and test strategy
│
├── tests/
│   ├── __init__.py
│   ├── test_crisis.py         # Rule-based safety detection and response tests
│   ├── test_bot_engine.py     # Prompt building, context sanitization and model fallback
│   ├── test_knowledge.py      # Screening, references, facilities and audio compliance metadata
│   └── test_server.py         # API, privacy deletion, crisis SSE and facility tests
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
└── server.py                  # FastAPI, crisis SSE, privacy endpoint and read-only APIs
```

---

## 6. TÀI LIỆU REST API (API SPECIFICATIONS)

Hệ thống cung cấp giao diện Swagger UI tương tác tại: `http://localhost:8000/docs`

| Phương Thức | Đường Dẫn (Endpoint) | Chức Năng | Mô Tả & Tham Số |
| :---: | :--- | :--- | :--- |
| `POST` | `/api/chat` | **Chat / crisis response** | Nhận Base64-encoded JSON `{"p": "<base64>"}` và trả SSE; crisis phrases nhận phản hồi cố định trước khi gọi AI |
| `POST` | `/api/summary` | **Đúc kết cuộc trò chuyện** | Gửi nội dung được chọn đến dịch vụ xử lý AI bên ngoài để tóm tắt |
| `GET` | `/api/health` | **Kiểm tra trạng thái** | Trả về `ready` hoặc `maintenance` |
| `GET` | `/api/knowledge` | **Dữ liệu giáo dục** | Bài viết, sàng lọc, tham khảo, facility/audio metadata |
| `GET` | `/api/facilities` | **Danh bạ cơ sở khám** | Hỗ trợ lọc theo `?location=bien_hoa`; mỗi trường dữ liệu có trạng thái xác minh riêng |
| `DELETE` | `/api/privacy/data` | **Xác nhận phạm vi xóa** | Xác nhận máy chủ ứng dụng không lưu lịch sử trò chuyện, cảm xúc hoặc kết quả sàng lọc; việc xóa trên thiết bị được thực hiện riêng |
| `POST` | `/api/tts` | **Đọc tiếng Việt** | Nội dung chỉ được gửi để thực hiện yêu cầu đọc thành tiếng; không lưu trong lịch sử của ứng dụng |
| `GET` | `/static/audio/{file}` | **Âm thanh có attribution** | Chỉ phân phối tệp có license/source đã xác minh; tệp hiện tại trả 404 |

Các API công khai `/api/sessions`, `/api/moods` và `/api/quizzes/results` đã bị gỡ vì chúng dùng chung bộ nhớ tiến trình và không xác thực người dùng.

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
Tạo file `.env` tại thư mục gốc và cấu hình thông tin truy cập dịch vụ xử lý AI theo cấu hình triển khai. Không đưa giá trị bí mật vào mã nguồn hoặc tài liệu công khai.
```env
PORT=8000
```

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

# 4. Chạy bộ kiểm thử tự động
pytest -v
```

Kế hoạch ưu tiên, sơ đồ phụ thuộc, kiến trúc, rủi ro và các cổng kiểm tra phát hành được ghi tại [docs/implementation-plan.md](docs/implementation-plan.md).

---

## 9. TRIỂN KHAI MÔI TRƯỜNG SẢN XUẤT (PRODUCTION DEPLOYMENT)

### Cách 1: Tự động qua Render Cloud
Dự án có tệp cấu hình hạ tầng [`render.yaml`](render.yaml):
1. Đẩy mã nguồn lên GitHub.
2. Tại [Render Dashboard](https://dashboard.render.com/) -> Chọn **New Blueprint Instance** -> Chọn repository `chatbot_tamly`.
3. Cấu hình thông tin truy cập dịch vụ xử lý AI tại mục biến môi trường bảo mật.
4. Render sẽ tự động build và cấp phát HTTPS miễn phí.

### Cách 2: Triển khai với Docker Container
```bash
# Xây dựng Docker image
docker build -t an-nhien-tam-ly:latest .

# Khởi chạy container với cấu hình môi trường riêng
docker run -d \
  --name an-nhien-app \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  an-nhien-tam-ly:latest
```

---

## 10. BẢO MẬT & QUYỀN RIÊNG TƯ

- Ứng dụng không đăng tải công khai nội dung trò chuyện, thông tin cảm xúc hoặc kết quả sàng lọc.
- Lịch sử được lưu trên trình duyệt của thiết bị đang dùng và có thể bị người có quyền truy cập thiết bị xem. Cách lưu hiện tại không phải mã hóa bảo mật; người dùng có thể xóa bằng nút “Xóa HẲN lịch sử”.
- Để cung cấp tính năng trò chuyện/tóm tắt và đọc thành tiếng, nội dung liên quan có thể được chuyển đến dịch vụ xử lý trí tuệ nhân tạo hoặc giọng nói bên ngoài. Đơn vị xử lý và thời hạn lưu cụ thể cần được xác minh trước khi phát hành; ứng dụng không kiểm soát việc lưu giữ của các dịch vụ này.
- Máy chủ ứng dụng không lưu lịch sử trò chuyện, nhật ký cảm xúc hoặc kết quả sàng lọc. Địa chỉ kết nối và thời điểm truy cập được giữ tạm thời trong bộ nhớ để giới hạn yêu cầu. Hệ thống lưu trữ của đơn vị vận hành có thể có bản ghi riêng; cần xác minh thời hạn lưu và cấu hình trước khi phát hành.
- Nút xóa lịch sử chỉ xóa dữ liệu trên trình duyệt của thiết bị hiện tại; không xóa bản sao lưu của trình duyệt, bản ghi vận hành hoặc bản sao đã được dịch vụ bên ngoài nhận.
- **Security headers**:
  - `Content-Security-Policy`: Khóa chặt miền tài nguyên hợp lệ, chống nhúng script độc hại.
  - `X-Content-Type-Options: nosniff`: Chống tấn công MIME type sniffing.
  - `X-Frame-Options: SAMEORIGIN`: Chống tấn công Clickjacking.
  - `X-XSS-Protection: 1; mode=block`: Kích hoạt bộ lọc XSS của trình duyệt.
- **DOMPurify**: Làm sạch Markdown/HTML; đây là một lớp phòng vệ, không phải bảo đảm an toàn tuyệt đối.
- **Giới Hạn Tần Suất Yêu Cầu (Rate Limiting)**: Chống Spam và DoS với thuật toán Sliding Window (Tối đa 45 requests/phút/IP), hỗ trợ nhận diện IP thật qua Proxy/Cloudflare.
- **Danh bạ và media**: chỉ thông tin cơ sở đã đối chiếu theo từng trường được hiển thị; tệp nhạc chưa có giấy phép bị chặn khỏi giao diện và dịch vụ.
- Ứng dụng hiện chưa đáp ứng/được chứng nhận HIPAA, GDPR, tiêu chuẩn Bộ Y tế, WCAG 2.1 AA hay uptime 99.9%. Các trang [privacy](static/privacy-policy.html) và [terms](static/terms-of-use.html) là bản dự thảo cần chuyên gia pháp lý rà soát trước phát hành.
- Xem [runbook khủng hoảng](docs/crisis-runbook.md) để biết quy trình kiểm tra và xử lý sự cố.
