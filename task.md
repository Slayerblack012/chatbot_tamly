
═══════════════════════════════════════════════════════════════════════════
ĐÓNG VAI: SENIOR FULL-STACK DEVELOPER & SOLUTION ARCHITECT (10 NĂM KINH NGHIỆM)
═══════════════════════════════════════════════════════════════════════════

Bạn là một lập trình viên cấp cao với 10 năm kinh nghiệm, chuyên về:

- Ứng dụng web chăm sóc sức khỏe tinh thần (Mental Health Tech)
- Crisis Intervention Systems & Safety Protocols
- UX/UI cho đối tượng học sinh (Gen Z, 12-18 tuổi)
- Privacy, Data Protection & GDPR Compliance
- NLP, Prompt Engineering cho AI Chatbot
- Medical/Healthcare Compliance (HIPAA-equivalent)

═══════════════════════════════════════════════════════════════════════════
BỐI CẢNH DỰ ÁN
═══════════════════════════════════════════════════════════════════════════

Dự án: Ứng dụng web hỗ trợ sức khỏe tinh thần cho học sinh Việt Nam.
Đối tượng người dùng: Học sinh cấp 2 và cấp 3 (12-18 tuổi).
Tính năng hiện có:

1. Trò chuyện (AI Chatbot)
2. Hiểu về cảm xúc
3. Tự đánh giá (PHQ-9)
4. Cơ sở khám
5. Tĩnh tâm (nhạc, kỹ thuật thở)
6. Quyền riêng tư

Mục tiêu: Hoàn thành 8 tasks trong checklist dưới đây với chất lượng production-ready, an toàn, và tuân thủ các tiêu chuẩn đạo đức y tế.

═══════════════════════════════════════════════════════════════════════════
DANH SÁCH 8 TASKS CẦN IMPLEMENT
═══════════════════════════════════════════════════════════════════════════

🔴 [P0 - CRITICAL] TASK 1: Crisis Detection - Trò chuyện
─────────────────────────────────────────────────────────
Yêu cầu: Bật khung khẩn cấp (crisis modal) khi học sinh nói GIÁN TIẾP
về tự tử/tổn thương.
Ví dụ trigger phrases:

- "ngủ không dậy nữa"
- "mọi người nhẹ nhõm khi không có mình"
- "không muốn tồn tại nữa"
- "muốn biến mất"
- "mọi chuyện sẽ ổn khi mình không ở đây"
  Output: Hiển thị crisis modal với thông điệp hỗ trợ khẩn cấp.

🔴 [P0 - CRITICAL] TASK 2: Crisis Response - Hiển thị Hotline
──────────────────────────────────────────────────────────────
Yêu cầu: Khi phát hiện nguy cơ:

- Đưa số điện thoại 111 / 115 / Đường dây Ngày Mai lên ĐẦU câu trả lời
- Hỏi THẲNG về sự an toàn của học sinh (direct safety check)
- Không vòng vo, không đưa lời khuyên chung chung
  Output: Template response ưu tiên hotline + câu hỏi an toàn.

🟠 [P1 - HIGH] TASK 3: System Prompt Refinement - Trò chuyện
─────────────────────────────────────────────────────────────
Yêu cầu sửa câu lệnh hệ thống (system prompt) của AI chatbot:

- BỎ hoàn toàn lời khuyên "nghỉ học 1-2 ngày"
- KHÔNG chê bai, phán xét người khác (phụ huynh, giáo viên, bạn bè)
- RÚT NGẮN câu trả lời (max 150-200 từ, dễ đọc trên mobile)
- Giọng điệu: ấm áp, không giáo điều, không sáo rỗng
  Output: System prompt mới + ví dụ before/after.

🟠 [P1 - HIGH] TASK 4: Privacy Controls - Quyền riêng tư
──────────────────────────────────────────────────────────
Yêu cầu:
  a) Thêm nút "Xóa HẲN lịch sử" (hard delete, không soft delete)
  b) Sửa câu marketing "hoàn toàn an toàn và riêng tư"
     → Thay bằng giải thích MINH BẠCH dữ liệu được gửi đi đâu,
       lưu ở đâu, ai có quyền truy cập, thời gian lưu trữ.
Output: UI component + backend API xóa dữ liệu + Privacy policy text mới.

🟠 [P1 - HIGH] TASK 5: PHQ-9 Question 9 Logic - Tự đánh giá
────────────────────────────────────────────────────────────
Yêu cầu:
  a) Khi câu 9 PHQ-9 > 0 (ý nghĩ tự làm hại bản thân):
     - SỬA lời khuyên "không có biểu hiện trầm cảm" → phải KHỚP với
       khung cảnh báo crisis
     - Trigger logic giống Task 1 & 2
  b) Ghi NGUỒN bản dịch tiếng Việt của thang đo PHQ-9
  c) Ghi rõ disclaimer: "Đây là công cụ SÀNG LỌC, KHÔNG PHẢI chẩn đoán y khoa"
Output: Conditional logic + UI warning + disclaimer component.

🟡 [P2 - MEDIUM] TASK 6: Clinic Verification - Cơ sở khám
──────────────────────────────────────────────────────────
Yêu cầu:
  a) Gọi xác minh TỪNG số điện thoại và giờ làm việc của cơ sở khám
  b) Cập nhật địa chỉ theo ĐƠN VỊ HÀNH CHÍNH MỚI nhất của VN
  c) BỎ cụm "được thẩm định y khoa" nếu CHƯA có chuyên gia thẩm định
Output: Verification workflow + updated data + compliance flag.

🟡 [P2 - MEDIUM] TASK 7: Music & Breathing Attribution - Tĩnh tâm
─────────────────────────────────────────────────────────────────
Yêu cầu:
  a) Ghi NGUỒN và GIẤY PHÉP (license) của từng file nhạc
  b) Ghi NGUỒN các kỹ thuật thở (ví dụ: 4-7-8 breathing, box breathing)
Output: Metadata schema + attribution UI + license compliance check.

🟢 [P3 - LOW] TASK 8: Age-appropriate Content - Hiểu về cảm xúc
───────────────────────────────────────────────────────────────
Yêu cầu:
  a) Thêm TÀI LIỆU THAM KHẢO (references) cho nội dung
  b) ĐỔI các ví dụ CHƯA HỢP lứa tuổi học sinh
     (ví dụ: thay ví dụ về áp lực công việc → áp lực thi cử, bạn bè)
Output: Content audit + revised examples + reference list.

═══════════════════════════════════════════════════════════════════════════
YÊU CẦU ĐẦU RA TỪ BẠN
═══════════════════════════════════════════════════════════════════════════

Hãy trả lời theo cấu trúc sau cho TOÀN BỘ 8 TASKS:

📋 PHẦN 1: IMPLEMENTATION MASTER PLAN
────────────────────────────────────
1.1. Thứ tự ưu tiên thực hiện (với lý do dựa trên risk & impact)
1.2. Estimated effort cho từng task (S/M/L/XL + số giờ dự kiến)
1.3. Dependencies graph (task nào block task nào)
1.4. Milestones & deliverables

🏗️ PHẦN 2: TECHNICAL ARCHITECTURE
──────────────────────────────────
2.1. Kiến trúc tổng thể đề xuất (sơ đồ text-based)
2.2. Database schema changes (nếu có) - dùng SQL hoặc Prisma schema
2.3. API endpoints cần tạo/sửa (REST/GraphQL)
2.4. Component tree cho frontend
2.5. State management strategy (đặc biệt cho crisis state)

💻 PHẦN 3: CODE IMPLEMENTATION (CHO TỪNG TASK)
───────────────────────────────────────────────
Với MỖI task, hãy cung cấp:
3.x.1. Phân tích yêu cầu & edge cases
3.x.2. Code Backend (Node.js/Express hoặc framework bạn chọn)
3.x.3. Code Frontend (React/Next.js component)
3.x.4. Code Database migration (nếu cần)
3.x.5. Comments giải thích logic phức tạp
3.x.6. Ví dụ input/output

🧪 PHẦN 4: TESTING STRATEGY
────────────────────────────
4.1. Unit tests cho từng task (viết bằng Jest/Vitest)
4.2. Integration tests
4.3. Edge cases & adversarial inputs (đặc biệt cho crisis detection)
4.4. Test cases cho PHQ-9 logic
4.5. Accessibility tests (WCAG 2.1 AA)

⚠️ PHẦN 5: RISK ASSESSMENT & MITIGATION
───────────────────────────────────────
5.1. Technical risks
5.2. Legal & Compliance risks (đặc biệt với dữ liệu sức khỏe tâm thần)
5.3. UX risks (false positive crisis detection gây hoảng loạn)
5.4. Mitigation strategies cho từng risk

📚 PHẦN 6: DOCUMENTATION
────────────────────────
6.1. README update
6.2. API documentation
6.3. Runbook cho on-call khi crisis system có issue
6.4. Privacy policy & Terms of Service update

═══════════════════════════════════════════════════════════════════════════
CONSTRAINTS & NON-FUNCTIONAL REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════

- Performance: Crisis detection phải trigger trong < 500ms
- Availability: 99.9% uptime cho crisis features
- Accessibility: WCAG 2.1 AA compliant
- Mobile-first: 80% user access từ mobile
- Language: Vietnamese (có thể mở rộng English sau)
- Security: Encryption at rest & in transit, no PII logging
- Compliance: Tuân thủ hướng dẫn của Bộ Y tế VN về sức khỏe tâm thần
- Ethics: KHÔNG đưa chẩn đoán y khoa, KHÔNG thay thế bác sĩ

═══════════════════════════════════════════════════════════════════════════
HƯỚNG DẪN THỰC HIỆN
═══════════════════════════════════════════════════════════════════════════

Bắt đầu với PHẦN 1 và PHẦN 2 trước để tôi review kiến trúc.
Sau đó implement từng task theo thứ tự ưu tiên: Task 1 → Task 2 → Task 5
→ Task 3 → Task 4 → Task 6 → Task 7 → Task 8.

Với mỗi task, hãy hỏi tôi clarifying questions nếu requirement chưa rõ
trước khi viết code.

Nếu bạn hiểu yêu cầu, hãy trả lời: "Đã hiểu. Bắt đầu với PHẦN 1:
IMPLEMENTATION MASTER PLAN" và triển khai.
═══════════════════════════════════════════════════════════════════════════
