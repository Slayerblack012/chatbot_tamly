# 🕊️ An Nhiên Edu-Psychology Platform 2.0

**An Nhiên Edu-Psychology** là nền tảng web tư vấn và giáo dục tâm lý học đường chuyên nghiệp (FastAPI + HTML5/CSS/JavaScript thuần), tích hợp mô hình **Gemini 2.5 Flash** cùng liệu pháp Nhận thức - Hành vi (CBT), Chánh niệm (Mindfulness) và các công cụ chăm sóc cảm xúc tương tác.

---

## 🌟 4 Phân Hệ Chuyên Nghiệp

1. 💬 **Tư Vấn AI Trực Tuyến (AI Counseling Hub)**:
   - Streaming câu trả lời tức thì dạng SSE (Server-Sent Events) siêu mượt.
   - 3 Chế độ: 🕊️ *Thấu cảm & Lắng nghe*, 🧩 *Tái định hình tư duy CBT*, 🧘 *Chánh niệm & Tĩnh tâm*.
   - Check-in cảm xúc & thanh đo căng thẳng (1-10) để cá nhân hóa cuộc trò chuyện.
   - Đúc kết phiên trò chuyện & xuất nhật ký Markdown (.md).

2. 📚 **Góc Giáo Dục Tâm Lý (Psychoeducation Hub)**:
   - Thư viện 8 bẫy tư duy tiêu cực (CBT Cognitive Distortions) kèm ví dụ thực tế và câu hỏi hóa giải.
   - Mô hình Tam giác nhận thức (Suy nghĩ ➡️ Cảm xúc ➡️ Hành vi).
   - Cẩm nang vượt qua áp lực học tập, thi cử và cơ chế chống Overthinking.

3. 📝 **Trắc Nghiệm Tự Đánh Giá (Self-Assessment Quizzes)**:
   - Bài test đánh giá mức độ Lo âu chuẩn hóa GAD-7 (7 câu hỏi).
   - Thang điểm trực quan, phân tích mức độ và gợi ý giải pháp.
   - Nút gửi trực tiếp kết quả sang cho An Nhiên để bắt đầu phiên tư vấn chuyên sâu.

4. 🧘 **Phòng Thư Giãn & Tập Trung Học Tập (Study & Relaxation Studio)**:
   - Bài tập thở Chánh niệm tương tác: Thở 4-7-8 & Thở hộp (Box Breathing).
   - Kỹ thuật Neo cảm xúc 5-4-3-2-1 ngắt cơn hoảng loạn.
   - Trình phát âm thanh thiên nhiên (Mưa rơi, Suối rừng, Sóng biển).

---

## 🚀 Cách Khởi Chạy Siêu Đơn Giản

### 👉 Khởi chạy Web App:
Mở Terminal tại thư mục `tamly-chatbot` và gõ:
```powershell
python run.py
```
> Trình duyệt sẽ tự động mở trang web tại `http://localhost:8000`. Không cần Streamlit, không hỏi email, khởi động trong 1 giây!

*Hoặc trên Windows, bạn chỉ cần click đúp vào file `run.bat`.*

### 🔑 Cấu hình API Key:
- Điền API Key vào file `.env` (`GEMINI_API_KEY=your_key`)
- Hoặc bấm vào biểu tượng **⚙️ Cài đặt** ở góc trên thanh điều hướng web để dán key vào trực tiếp.
