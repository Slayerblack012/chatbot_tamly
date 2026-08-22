# AN NHIÊN TÂM LÝ - NỀN TẢNG TƯ VẤN & ĐỒNG HÀNH CẢM XÚC

Nền tảng tham vấn tâm lý, thấu cảm và chăm sóc sức khỏe tinh thần được xây dựng trên nền tảng **FastAPI Backend** và **Vanilla Web Single Page Application (SPA)**, tích hợp mô hình ngôn ngữ lớn **Google Gemini API** với phản hồi thời gian thực qua **Server-Sent Events (SSE)**.

---

## 1. BÀI TOÁN & MỤC TIÊU CỐT LÕI (PROBLEM STATEMENT)

### 1.1. Thực Trạng & Nỗi Đau Thực Tế (Pain Points)
- **Gia tăng áp lực tâm lý trong xã hội hiện đại**: Học sinh, sinh viên và người đi làm đối mặt với áp lực học tập, thi cử, kỳ vọng gia đình, môi trường công sở quá tải, dẫn đến kiệt sức (burnout), lo âu và suy nghĩ quá mức (overthinking).
- **Rào cản tiếp cận tham vấn tâm lý truyền thống**: Chi phí tham vấn với chuyên gia thường cao; sự e ngại bị định kiến xã hội hoặc phán xét; thiếu người lắng nghe chân thành vào các khung giờ đêm muộn.
- **Hạn chế của các chatbot thông thường**: Phần lớn chatbot trên thị trường chỉ trả lời máy móc, lặp lại các câu an ủi sáo rỗng vô thưởng vô phạt hoặc liệt kê bài giảng khô khan, không đi vào bản chất vấn đề tâm lý.

### 1.2. Định Nghĩa Bài Toán Kỹ Thuật & Nghiệp Vụ (Problem Definition)
Dự án được xây dựng nhằm giải quyết 4 bài toán kỹ thuật và khoa học hành vi then chốt:

1. **Bài toán Tham vấn Tâm lý Chuẩn mực & Không Sáo rỗng (Cognitive & Affective Alignment)**:
   - Xây dựng hệ thống hội thoại có khả năng đọc vị chính xác cơ chế phòng vệ của bản ngã, nhận diện 8 bẫy tư duy nhận thức (Cognitive Distortions).
   - Kết hợp phương pháp **Liệu pháp Nhận thức - Hành vi (CBT)**, **Chủ nghĩa Khắc kỷ (Stoicism)** và **Chánh niệm (Mindfulness)** để đưa ra lời khuyên chân thực, đúng bản chất và có tính chuyển hóa nội lực mà không dùng emoji hay lời nói ru ngủ giả tạo.

2. **Bài toán Tối ưu Độ trễ & Tiêu thụ Tài nguyên (Latency & Token Optimization)**:
   - Đạt tốc độ phản hồi tức thì với thời gian sinh ký tự đầu tiên (**Time-To-First-Token < 1s**) qua giao thức Server-Sent Events (SSE).
   - Xử lý bài toán phình to ngữ cảnh (Context Window Inflation) bằng cơ chế tự động khóa phiên và chuyển sang chế độ ngủ (Sleep Mode) sau 60 phút không thao tác, giúp tiết kiệm 100% token nhàn rỗi.

3. **Bài toán Bảo mật Quyền Riêng Tư Tuyệt Đối (Zero-Trust Privacy & Security)**:
   - Dữ liệu tâm sự của người dùng được mã hóa chuỗi Base64 trên đường truyền mạng nhằm chống nghe lén và chống dịch ngược thông tin công nghệ khi bật Developer Tools (F12).
   - Không lưu trữ vĩnh viễn nội dung nhạy cảm trên ổ đĩa máy chủ; tự động kích hoạt màn hình che phủ bảo mật khi người dùng rời thiết bị.

4. **Bài toán Tự Đánh Giá & Giáo Dục Tâm Lý Chủ Động (Psychoeducation & Screening)**:
   - Cung cấp công cụ tự phản tư với thang đo chuẩn hóa quốc tế **GAD-7 (Generalized Anxiety Disorder 7-item)** và kho học liệu tâm lý ứng dụng giúp người dùng chủ động thấu hiểu chính mình.

---

## 2. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

```
[ Frontend Client: Single Page App ]
    │ (Base64 Encrypted Payload & Zero Emojis)
    ▼
[ FastAPI Backend Engine ] ──> [ Rate Limiting & Security Headers ]
    │
    ├──> [ Core Engine: Google GenAI SDK (Chats API) ]
    │        ├── Model chinh: gemini-3.5-flash-lite (TTFT < 1s)
    │        └── Fallback: gemini-flash-lite-latest, gemini-3.1-flash-lite
    │
    ├──> [ Tri thức Tâm lý: CBT (8 Bẫy tư duy), GAD-7, Chánh niệm ]
    └──> [ Tự động ngủ bảo mật sau 1 giờ không hoạt động ]
```

---

## 3. TÍNH NĂNG NỔI BẬT

1. **Trí Tuệ Tâm Lý Sâu Sắc & Lời Khuyên Chân Thực**:
   - Vận dụng Liệu pháp Nhận thức - Hành vi (CBT), Chủ nghĩa Khắc kỷ (Stoicism) và Chánh niệm (Mindfulness).
   - Nguyên tắc phản hồi: Đúng bản chất, dứt khoát, không dùng văn mẫu sáo rỗng, không sử dụng emoji, mang lại giá trị chuyển hóa nội lực thực sự.

2. **Phản Hồi Siêu Tốc (Real-time SSE Streaming)**:
   - Tối ưu hóa với mô hình `gemini-3.5-flash-lite`, thời gian nhận token đầu tiên (**TTFT**) chỉ từ **0.6s - 1.0s**.
   - Chuẩn hóa theo phương thức `client.chats.create` và `chat.send_message_stream`, triệt tiêu hoàn toàn các cảnh báo Automatic Function Calling (AFC).

3. **Bảo Mật & Mã Hóa Gói Tin (Base64 Payload Obfuscation)**:
   - Toàn bộ dữ liệu truyền tải giữa Client và Server đều được đóng gói và mã hóa chuỗi Base64.
   - Ẩn hoàn toàn thông tin công nghệ (FastAPI, Gemini, Model name, API Key).
   - Tích hợp Security Headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`.
   - Khử trùng 100% mã HTML/Markdown bằng `DOMPurify 3.0` chống tấn công XSS.

4. **Tự Động Nghỉ Ngơi & Khóa Bảo Mật Sau 1 Giờ (Idle Timeout)**:
   - Nhận diện thao tác trên cả Máy tính lẫn Điện thoại (chạm cảm ứng, cuộn trang, gõ phím).
   - Nếu không có tương tác trong 60 phút, hệ thống tự động khóa bảo mật, làm mờ nội dung cũ để bảo vệ quyền riêng tư và reset token về 0 khi bắt đầu phiên mới.

5. **Giao Diện Đa Thiết Bị Chuẩn Responsive**:
   - **Mobile (< 768px)**: Thanh điều hướng dưới đáy (Mobile Bottom Navigation Bar), ngăn kéo cảm xúc trượt (Drawer), chiều cao co giãn linh hoạt `100dvh`.
   - **Desktop / Tablet**: Bố cục 2 cột chuyên nghiệp, công cụ check-in cảm xúc, bài tập thở chánh niệm và âm thanh thư giãn.

---

## 4. CẤU TRÚC THƯ MỤC DỰ ÁN

```
tamly-chatbot/
│
├── core/
│   ├── __init__.py
│   ├── bot_engine.py         # Quản lý kết nối Gemini SDK, Chat stream, Auto Fallback
│   ├── knowledge_base.py     # Dữ liệu 8 bẫy tư duy CBT, bài đọc tâm lý, bài test GAD-7
│   └── prompts.py            # Hệ thống Prompt tâm lý sâu sắc (Zero Emoji)
│
├── static/
│   ├── css/
│   │   └── style.css         # Hệ thống thiết kế CSS thuần, Responsive, Hiệu ứng thở
│   ├── js/
│   │   └── app.js            # Xử lý SSE Reader, Base64 encode/decode, 1h Idle Sleep
│   └── index.html            # Giao diện Single Page Application (SPA)
│
├── server.py                 # FastAPI Backend Server, Middleware bảo mật, Rate Limiter
├── main.py                   # Giao diện dòng lệnh Terminal (CLI)
├── run.py                    # Script khởi chạy 1-click tự động mở trình duyệt
├── run.bat                   # File Batch khởi động nhanh trên Windows
├── requirements.txt          # Danh sách thư viện Python
├── Dockerfile                # Cấu hình đóng gói Docker Container
├── Procfile                  # Cấu hình khởi chạy cho Render / Railway / Heroku
├── vercel.json               # Cấu hình cho nền tảng Vercel
├── .gitignore                # Bảo mật file .env và loại trừ file tạm
├── .env.example              # Mẫu cấu hình biến môi trường
└── README.md                 # Tài liệu mô tả bài toán và hướng dẫn sử dụng
```

---

## 5. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY CỤC BỘ (LOCAL)

### Bước 1: Chuẩn bị môi trường
Yêu cầu máy tính đã cài đặt **Python 3.10 trở lên**.

### Bước 2: Cài đặt các thư viện cần thiết
Mở Terminal hoặc PowerShell tại thư mục dự án và chạy:
```powershell
pip install -r requirements.txt
```

### Bước 3: Cấu hình Gemini API Key
Tạo file `.env` tại thư mục gốc với nội dung:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Bạn có thể lấy API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/)).*

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

---

## 6. HƯỚNG DẪN TRIỂN KHAI LÊN CLOUD (DEPLOYMENT)

### Cách 1: Triển khai lên Render.com (Khuyên Dùng)
1. Đẩy mã nguồn lên tài khoản GitHub của bạn.
2. Truy cập [Render.com](https://render.com/) -> Chọn **New Web Service**.
3. Kết nối với GitHub Repository của dự án.
4. Render sẽ tự động nhận diện cấu hình:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Thêm biến môi trường tại mục **Environment Variables**:
   - Key: `GEMINI_API_KEY`
   - Value: `API_Key_cua_ban`
6. Nhấn **Create Web Service** và nhận đường link sử dụng công khai.

### Cách 2: Triển khai với Docker
```bash
docker build -t an-nhien-tam-ly .
docker run -d -p 8000:8000 -e GEMINI_API_KEY="your_api_key" an-nhien-tam-ly
```

---

## 7. THÔNG TIN BẢO MẬT & RANH GIỚI Y TẾ
- **Bảo Mật Quyền Riêng Tư**: Toàn bộ nội dung trao đổi chỉ tồn tại trong phiên duyệt web của người dùng và không được lưu trữ vĩnh viễn trên máy chủ cục bộ.
- **Ranh Giới Y Tế**: Hệ thống đóng vai trò là Người Bạn Tri Kỷ & Trợ Lý Tham Vấn Cảm Xúc, không thay thế cho chẩn đoán y khoa hay điều trị tâm thần lâm sàng từ bác sĩ chuyên khoa.

---
*Phát triển bởi đội ngũ An Nhiên Tâm Lý.*
