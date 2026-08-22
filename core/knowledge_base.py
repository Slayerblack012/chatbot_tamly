"""
Co so du lieu kien thuc giao duc tam ly (Psychoeducation), bay tu duy CBT va bo cau hoi danh gia.
Toan bo du lieu duoc chuan hoa, khong su dung emoji.
"""

COGNITIVE_DISTORTIONS = [
    {
        "id": "all_or_nothing",
        "name": "Tư duy Trắng - Đen (All-or-Nothing)",
        "icon": "[01]",
        "description": "Nhìn nhận mọi việc theo hai cực tuyệt đối: hoàn hảo hoặc thất bại hoàn toàn, không có vùng xám ở giữa.",
        "example": "'Nếu mình không đạt điểm tối đa môn này, mình là kẻ vô dụng hoàn toàn.'",
        "reframing": "Cuộc sống có nhiều sắc độ. Việc chưa đạt điểm tuyệt đối không phủ nhận toàn bộ nỗ lực và giá trị của bạn."
    },
    {
        "id": "catastrophizing",
        "name": "Thảm kịch hóa (Catastrophizing)",
        "icon": "[02]",
        "description": "Tự động dự đoán kịch bản tồi tệ nhất có thể xảy ra và phóng đại hậu quả của nó vượt xa thực tế.",
        "example": "'Mình làm bài thuyết trình bị vấp một câu, chắc chắn cả lớp sẽ cười nhạo và thầy sẽ đánh trượt mình.'",
        "reframing": "Hãy tự hỏi: Điều tồi tệ nhất thực tế có thể xảy ra là gì? Và nếu nó xảy ra, mình có cách nào khắc phục không?"
    },
    {
        "id": "mind_reading",
        "name": "Đọc suy nghĩ người khác (Mind Reading)",
        "icon": "[03]",
        "description": "Tự suy diễn người khác đang có suy nghĩ tiêu cực hoặc phán xét về mình mà không có bằng chứng cụ thể.",
        "example": "'Họ không trả lời tin nhắn ngay, chắc là họ ghét mình lắm rồi.'",
        "reframing": "Người khác có thể đang bận rộn hoặc mệt mỏi. Bạn không thể biết chính xác suy nghĩ của họ nếu chưa hỏi trực tiếp."
    },
    {
        "id": "emotional_reasoning",
        "name": "Lý luận theo cảm xúc (Emotional Reasoning)",
        "icon": "[04]",
        "description": "Tin rằng cảm xúc tiêu cực của mình là sự thật khách quan ('Mình cảm thấy lo sợ nên chắc chắn việc này rất nguy hiểm').",
        "example": "'Mình cảm thấy mình bất tài, vậy nên mình thật sự là người kém cỏi.'",
        "reframing": "Cảm xúc là phản ứng tự nhiên tạm thời của não bộ, không phải là sự thật bất biến về năng lực của bạn."
    },
    {
        "id": "should_statements",
        "name": "Mệnh lệnh 'Phải / Nên' (Should Statements)",
        "icon": "[05]",
        "description": "Tạo áp lực khắt khe lên bản thân hoặc người khác bằng những quy chuẩn cứng nhắc ('Mình phải luôn mạnh mẽ', 'Mình không được phép sai sót').",
        "example": "'Mình không bao giờ được để điểm số tụt dốc, mình phải luôn đứng đầu.'",
        "reframing": "Thay 'mình phải' bằng 'mình mong muốn' hoặc 'mình sẽ cố gắng hết sức trong khả năng hôm nay'."
    },
    {
        "id": "personalization",
        "name": "Tự quy trách nhiệm (Personalization)",
        "icon": "[06]",
        "description": "Tự gánh hết trách nhiệm về những sự việc tiêu cực nằm ngoài tầm kiểm soát của bản thân.",
        "example": "'Nhóm không hoàn thành tốt bài tập lớn là do lỗi của một mình mình.'",
        "reframing": "Một kết quả là sự tác động của nhiều yếu tố và nhiều cá nhân. Bạn chỉ chịu trách nhiệm cho phần việc của chính bạn."
    },
    {
        "id": "overgeneralization",
        "name": "Khái quát hóa quá mức (Overgeneralization)",
        "icon": "[07]",
        "description": "Xem một biến cố tiêu cực đơn lẻ là khuôn mẫu thất bại vĩnh viễn không thể thay đổi.",
        "example": "'Mình vừa rớt phỏng vấn, từ nay chắc mình chẳng bao giờ xin được việc đâu.'",
        "reframing": "Một lần từ chối chỉ là một trải nghiệm học hỏi, không định nghĩa tương lai của bạn."
    },
    {
        "id": "mental_filter",
        "name": "Màng lọc tiêu cực (Mental Filter)",
        "icon": "[08]",
        "description": "Chỉ chăm chú nhìn vào một chi tiết tiêu cực nhỏ và phớt lờ toàn bộ những mặt tích cực khác.",
        "example": "'Nhận được 9 lời khen và 1 lời góp ý, nhưng cả ngày chỉ dằn vặt về lời góp ý đó.'",
        "reframing": "Hãy lùi lại một bước để nhìn toàn cảnh bức tranh, ghi nhận cả những điểm tích cực bạn đã làm tốt."
    },
]

PSYCHOEDU_ARTICLES = [
    {
        "id": "cognitive_triangle",
        "title": "Mô Hình Tam Giác Nhận Thức (CBT Cognitive Triangle)",
        "category": "Cốt Lõi Tâm Lý Học",
        "readTime": "3 phút đọc",
        "summary": "Hiểu rõ mối quan hệ mật thiết giữa Suy nghĩ -> Cảm xúc -> Hành vi để làm chủ tâm trạng.",
        "content": """
### Tam Giác Nhận Thức Là Gì?
Trong Liệu pháp Nhận thức - Hành vi (CBT), các nhà tâm lý học phát hiện ra rằng **không phải sự việc bên ngoài khiến bạn đau khổ, mà chính cách bạn diễn giải (suy nghĩ về) sự việc đó tạo nên cảm xúc của bạn.**

1. **Suy nghĩ (Thoughts)**: Những câu thoại nội tâm bạn tự nói với chính mình khi gặp một tình huống.
2. **Cảm xúc (Emotions)**: Cảm giác phát sinh (lo âu, thất vọng, vui mừng, bình an).
3. **Hành vi (Behaviors)**: Phản ứng thực tế (trì hoãn, thu mình, hành động đối phó hoặc đối mặt).

*Quy luật chuyển dịch*: Khi bạn thay đổi **Suy nghĩ** thành góc nhìn thực tế và tích cực hơn, **Cảm xúc** sẽ dịu đi và **Hành vi** sẽ trở nên hiệu quả hơn.
"""
    },
    {
        "id": "study_stress_coping",
        "title": "Cẩm Nang Quản Lý Căng Thẳng Học Đường & Thi Cử",
        "category": "Học Sinh & Sinh Viên",
        "readTime": "4 phút đọc",
        "summary": "Các bước thực hành tâm lý giúp vượt qua áp lực điểm số, thi cử và kỳ vọng gia đình.",
        "content": """
### Áp Lực Học Tập & Cách Tháo Gỡ:
1. **Phân biệt Áp lực lành mạnh (Eustress) & Áp lực kiệt sức (Distress)**:
   - Một chút căng thẳng vừa phải giúp bạn tập trung và tăng năng suất.
   - Nhưng khi tim đập nhanh kéo dài, mất ngủ và sợ hãi, cơ thể đang báo động kiệt sức.

2. **Kỹ thuật Pomodoro Cảm Xúc**:
   - Học tập trung trong 25 phút.
   - Dành 5 phút nghỉ ngơi: đứng dậy, vươn vai, uống một ngụm nước ấm, thở chậm 3 nhịp.
   - Không lướt mạng xã hội trong 5 phút nghỉ để não bộ thực sự được thả lỏng.

3. **Tách Biệt Điểm Số & Giá Trị Bản Thân**:
   - Điểm số chỉ phản ánh mức độ nắm kiến thức ở một thời điểm, không phản ánh phẩm giá của bạn.
"""
    },
    {
        "id": "panic_and_overthinking",
        "title": "Hiểu Về Cơ Chế Suy Nghĩ Miên Man (Overthinking)",
        "category": "Sức Khỏe Tinh Thần",
        "readTime": "3 phút đọc",
        "summary": "Tại sao não bộ lại liên tục nghĩ ngợi vào ban đêm và cách ngắt mạch suy nghĩ lặp lại.",
        "content": """
### Não Bộ Hoạt Động Thế Nào Khi Bạn Suy Nghĩ Miên Man?
Hạch hạnh nhân (Amygdala) - trung tâm cảnh báo nguy hiểm trong não - bị kích hoạt quá mức, khiến não hiểu nhầm các suy nghĩ tưởng tượng là mối đe dọa thực tế.

**3 Bước Ngắt Mạch Suy Nghĩ:**
1. **Ghi nhận**: Tự nhủ 'Tâm trí mình đang bật chế độ lo xa.'
2. **Kỹ thuật 5-4-3-2-1**: Đưa sự chú ý về các giác quan thực tại xung quanh.
3. **Viết xả (Brain Dump)**: Viết toàn bộ suy nghĩ trong đầu ra một tờ giấy rồi gấp lại, hẹn sáng mai xem xét.
"""
    }
]

ASSESSMENT_QUIZZES = {
    "gad7": {
        "title": "Bảng Đánh Giá Mức Độ Lo Âu & Áp Lực",
        "subtitle": "Dựa trên thang đo chuẩn hóa quốc tế GAD-7 (Generalized Anxiety Disorder)",
        "description": "Trong 2 tuần qua, bạn có thường xuyên bị làm phiền bởi những vấn đề sau đây không?",
        "options": [
            {"label": "Hoàn toàn không", "score": 0},
            {"label": "Vài ngày", "score": 1},
            {"label": "Hơn một nửa số ngày", "score": 2},
            {"label": "Gần như mỗi ngày", "score": 3},
        ],
        "questions": [
            "Cảm thấy bồn chồn, lo lắng hoặc bứt rứt không yên.",
            "Không thể ngừng hoặc kiểm soát được sự lo lắng của bản thân.",
            "Lo lắng quá nhiều về những điều khác nhau trong cuộc sống / học tập.",
            "Gặp khó khăn trong việc thả lỏng và thư giãn.",
            "Cảm thấy đứng ngồi không yên đến mức khó có thể ngồi im một chỗ.",
            "Dễ cảm thấy cáu kỉnh, bực bội hoặc khó chịu.",
            "Cảm thấy sợ hãi như thể có điều gì tồi tệ sắp sửa xảy ra.",
        ],
        "brackets": [
            {
                "range": (0, 4),
                "level": "Mức độ Lo âu Tối thiểu (Bình thường)",
                "color": "#10B981",
                "advice": "Tâm lý của bạn đang ở trạng thái ổn định và cân bằng. Hãy tiếp tục duy trì lối sống lành mạnh, ăn ngủ điều độ và dành thời gian cho sở thích cá nhân."
            },
            {
                "range": (5, 9),
                "level": "Mức độ Lo âu Nhẹ",
                "color": "#F59E0B",
                "advice": "Bạn đang có một chút áp lực và bồn chồn. Hãy thử áp dụng bài tập thở chậm 4-7-8, giảm bớt caffeine và chia sẻ cùng An Nhiên hoặc bạn bè."
            },
            {
                "range": (10, 14),
                "level": "Mức độ Lo âu Trung bình",
                "color": "#F97316",
                "advice": "Mức độ căng thẳng đang ảnh hưởng rõ rệt đến chất lượng cuộc sống. Hãy dành nhiều thời gian hơn để nghỉ ngơi, thực hành chánh niệm và cùng An Nhiên tháo gỡ từng vấn đề."
            },
            {
                "range": (15, 21),
                "level": "Mức độ Lo âu Đáng Chú Ý (Cao)",
                "color": "#EF4444",
                "advice": "Bạn đang phải chịu đựng áp lực rất lớn. Ngoài việc thực hành các bài tập thư giãn với An Nhiên, bạn nên cân nhắc chia sẻ với người thân đáng tin cậy hoặc tham vấn chuyên gia tâm lý học đường/y tế."
            }
        ]
    }
}
