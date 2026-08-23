# AN NHIÊN TÂM LÝ - NỀN TẢNG THAM VẤN & ĐỒNG HÀNH CẢM XÚC

Nền tảng tham vấn tâm lý, thấu cảm và chăm sóc sức khỏe tinh thần được xây dựng trên **FastAPI Backend (Async SSE Streaming)** và **Vanilla Web Single Page Application (SPA)**, tích hợp mô hình ngôn ngữ lớn **Google Gemini API** (`gemini-2.5-flash`, `gemini-2.0-flash`).

---

## 1. BÀI TOÁN & MỤC TIÊU CỐT LÕI (PROBLEM STATEMENT)

### 1.1. Thực Trạng & Nỗi Đau Thực Tế (Pain Points)
- **Gia tăng áp lực tâm lý trong xã hội hiện đại**: Học sinh, sinh viên và người đi làm đối mặt với áp lực học tập, thi cử, kỳ vọng gia đình, môi trường công sở quá tải, dẫn đến kiệt sức (burnout), lo âu và suy nghĩ quá mức (overthinking).
- **Rào cản tiếp cận tham vấn tâm lý truyền thống**: Chi phí tham vấn với chuyên gia cao; sự e ngại bị định kiến xã hội hoặc phán xét; thiếu người lắng nghe chân thành vào các khung giờ đêm muộn.
- **Hạn chế của các chatbot thông thường**: Phần lớn chatbot chỉ trả lời máy móc, lặp lại các câu an ủi sáo rỗng vô thưởng vô phạt hoặc liệt kê bài giảng khô khan, không đi vào bản chất vấn đề tâm lý.

### 1.2. Định Nghĩa Bài Toán Kỹ Thuật & Nghiệp Vụ
Dự án được xây dựng nhằm giải quyết 4 bài toán kỹ thuật và khoa học hành vi then chốt:

1. **Tham Vấn Tâm Lý Chuẩn Mực (Cognitive & Affective Alignment)**:
   - Nhận diện chính xác cơ chế phòng vệ của bản ngã và 8 bẫy tư duy nhận thức (Cognitive Distortions).
   - Kết hợp phương pháp **Liệu pháp Nhận thức - Hành vi (CBT)**, **Chủ nghĩa Khắc kỷ (Stoicism)** và **Chánh niệm (Mindfulness)** để đưa ra lời khuyên chân thực, đúng bản chất và có tính chuyển hóa nội lực.
   - *Quy tắc Zero Emoji*: Áp dụng nghiêm ngặt cho **lời thoại tham vấn của AI** (để giữ sự trang trọng, điềm đạm, lắng đọng), trong khi giao diện người dùng (UI) vẫn sử dụng icon trực quan, thân thiện.

2. **Tối Ưu Độ Trễ & Xử Lý Bất Đồng Bộ (Non-blocking Async SSE Streaming)**:
   - Đạt tốc độ phản hồi tức thì với thời gian sinh ký tự đầu tiên (**Time-To-First-Token < 1s**) qua `client.aio.chats.create` và Server-Sent Events (SSE).
   - Xử lý bất đồng bộ hoàn toàn (Async I/O), không làm nghẽn Event Loop khi phục vụ nhiều người dùng đồng thời.
   - Tự động cắt tỉa ngữ cảnh (Context Window Slicing) lấy ~20 tin nhắn gần nhất trong payload để tối ưu token.

3. **Bảo Mật Quyền Riêng Tư & An Ninh Mạng (Zero-Trust Privacy & Security)**:
   - Dữ liệu trao đổi giữa Client và Server được **đóng gói bảo vệ / làm mờ (Base64 Payload Obfuscation)** nhằm ngăn chặn nghe lén cơ bản và ẩn hoàn toàn thông tin công nghệ/API key.
   - Thiết lập đầy đủ các Header an ninh: `Content-Security-Policy` (CSP), `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`.
   - Khử trùng mã HTML/Markdown qua `DOMPurify` theo cơ chế **Fail-Closed** chống triệt để tấn công XSS.

4. **Tự Đánh Giá & Giáo Dục Tâm Lý Chủ Động (Psychoeducation & Screening)**:
   - Cung cấp công cụ tự phản tư với 2 thang đo chuẩn hóa quốc tế: **GAD-7** (Generalized Anxiety Disorder) và **PHQ-9** (Patient Health Questionnaire - Depression).
   - Tích hợp tính năng **Can thiệp khủng hoảng khẩn cấp (Crisis Intervention)**: Tự động hiển thị hotline hỗ trợ 111 / 115 / Đường dây Ngày Mai 096 306 1414 khi nhận diện nguy cơ tự hại.
   - Lưu trữ phiên an toàn trên trình duyệt (`localStorage`) và hỗ trợ **Xuất Nhật Ký Hội Thoại** dạng văn bản.

---

## 2. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

```
[ Frontend Client: Vanilla SPA ]
     │ (Base64 Obfuscated Payload & CSP Protected)
     ▼
[ FastAPI Backend Engine ] ──> [ Rate Limiter (IP Proxy Aware) & Security Headers ]
     │
     ├──> [ Core Engine: Google GenAI Async SDK (aio.chats) ]
     │        ├── Model chính: gemini-2.5-flash (TTFT < 1s, Cached)
     │        └── Fallback tự động: gemini-2.0-flash, gemini-1.5-flash
     │
     ├──> [ Tri Thức Tâm Lý: CBT (8 Bẫy tư duy), GAD-7, PHQ-9, Chánh niệm ]
     └──> [ Can thiệp khủng hoảng & Tự động khóa phiên sau 1 giờ ]
```

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```
tamly-chatbot/
│
├── core/
│   ├── __init__.py
│   ├── bot_engine.py         # Quản lý kết nối Gemini SDK Async, Auto-Fallback & Caching
│   ├── knowledge_base.py     # Dữ liệu 8 bẫy tư duy CBT, bài đọc tâm lý, GAD-7 & PHQ-9
│   └── prompts.py            # Hệ thống Prompt tâm lý sâu sắc (Zero Emoji Bot Dialog)
│
├── static/
│   ├── css/
│   │   └── style.css         # Hệ thống thiết kế CSS thuần, Responsive, Crisis Banner
│   ├── js/
│   │   └── app.js            # Xử lý Async SSE Reader, Base64, Fail-closed DOMPurify, Export
│   └── index.html            # Giao diện Single Page Application (SPA)
│
├── tests/
│   ├── __init__.py
│   ├── test_server.py        # Test API endpoints, Base64 decoding, Rate limiting, CSP
│   ├── test_bot_engine.py    # Test engine async, role merging, prompt builders
│   └── test_knowledge.py     # Test bộ dữ liệu CBT, GAD-7, PHQ-9
│
├── server.py                 # FastAPI Backend Server, Middleware bảo mật, Rate Limiter
├── main.py                   # Giao diện dòng lệnh Terminal (CLI)
├── run.py                    # Script khởi chạy 1-click tự động mở trình duyệt
├── run.bat                   # File Batch khởi động nhanh trên Windows
├── requirements.txt          # Danh sách thư viện Python
├── pyproject.toml            # Cấu hình chuẩn cho Ruff Linter & Pytest
├── Dockerfile                # Cấu hình Docker non-root user & Healthcheck
├── .dockerignore             # Chống sao chép file bí mật vào container
├── Procfile                  # Cấu hình khởi chạy cho Render / Railway
├── .gitignore                # Bảo mật file .env và loại trừ file tạm
├── .env.example              # Mẫu cấu hình biến môi trường
└── README.md                 # Tài liệu hướng dẫn sử dụng và triển khai
```

---

## 4. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY CỤC BỘ (LOCAL)

### Bước 1: Chuẩn bị môi trường
Yêu cầu máy tính đã cài đặt **Python 3.10 trở lên**.

### Bước 2: Cài đặt thư viện
Mở Terminal hoặc PowerShell tại thư mục dự án và chạy:
```powershell
pip install -r requirements.txt
```

### Bước 3: Cấu hình Gemini API Key
Tạo file `.env` tại thư mục gốc với nội dung:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```
*(Bạn có thể lấy API Key tại [Google AI Studio](https://aistudio.google.com/)).*

### Bước 4: Khởi chạy ứng dụng
- **Cách 1 (Giao diện Web - Khuyên dùng)**:
  ```powershell
  python run.py
  ```
  *(Hoặc nhấp đúp trực tiếp vào file `run.bat` trên Windows. Hệ thống sẽ tự động mở trình duyệt tại `http://localhost:8000`).*

- **Cách 2 (Giao diện Dòng lệnh CLI)**:
  ```powershell
  python main.py
  ```

### Bước 5: Chạy Kiểm Thử Tự Động (Automated Testing & Linting)
```powershell
# Chạy Linter
ruff check .

# Chạy toàn bộ Test Suite
pytest -v
```

---

## 5. HƯỚNG DẪN TRIỂN KHAI (DEPLOYMENT)

> [!NOTE]
> Giao thức **Server-Sent Events (SSE)** yêu cầu kết nối TCP dạng long-lived streaming. Các nền tảng Serverless thông thường (như AWS Lambda hoặc Vercel Python Serverless) thường có cơ chế buffer response khiến trải nghiệm stream từng ký tự bị gián đoạn. Vì vậy, **Render.com, Railway hoặc Docker Container** là các giải pháp được khuyến nghị hàng đầu.

### Cách 1: Triển khai lên Render.com (Khuyên Dùng)
1. Đẩy mã nguồn lên tài khoản GitHub của bạn.
2. Truy cập [Render.com](https://render.com/) -> Chọn **New Web Service**.
3. Kết nối với GitHub Repository của dự án.
4. Cấu hình Render:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT --no-server-header`
5. Thêm biến môi trường tại mục **Environment Variables**:
   - `GEMINI_API_KEY`: API Key của bạn
   - `GEMINI_MODEL`: `gemini-2.5-flash`

### Cách 2: Triển khai với Docker
```bash
docker build -t an-nhien-tam-ly .
docker run -d -p 8000:8000 -e GEMINI_API_KEY="your_api_key" an-nhien-tam-ly
```

---

## 6. ĐƯỜNG DÂY NÓNG CAN THIỆP KHỦNG HOẢNG & RANH GIỚI Y TẾ
- **Tổng đài Quốc gia Bảo vệ Trẻ em & Thanh thiếu niên**: `111` (Miễn phí 24/7)
- **Cấp cứu Y tế Khẩn cấp**: `115`
- **Đường dây nóng Ngày Mai (Hỗ trợ trầm cảm & khủng hoảng tâm lý)**: `096 306 1414`
- **Ranh Giới Y Tế**: Nền tảng An Nhiên đóng vai trò là Người Bạn Tri Kỷ & Trợ Lý Tham Vấn Cảm Xúc, không thay thế cho chẩn đoán y khoa hay điều trị tâm thần lâm sàng từ bác sĩ chuyên khoa.

---
