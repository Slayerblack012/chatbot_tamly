/**
 * AN NHIÊN TÂM LÝ - CLIENT SCRIPT
 * Bảo mật: DOMPurify Fail-closed, UTF-8 Base64 Obfuscation, Role Alternation Auto-Recovery,
 * Can thiệp Khủng hoảng (Crisis Alert & PHQ-9 Item 9 trigger), GAD-7 & PHQ-9, Real Health Check,
 * Dark Mode Toggle, Stop Stream AbortController, Smart Scroll, Drawer Backdrop & Custom Modals (No native alert/confirm).
 */

document.addEventListener("DOMContentLoaded", () => {
  // =========================================================================
  // 0. BASE64 UTF-8 OBFUSCATION & HTML ESCAPING HELPERS
  // =========================================================================
  function encodeB64(str) {
    try {
      const bytes = new TextEncoder().encode(str);
      const binString = Array.from(bytes, (byte) => String.fromCharCode(byte)).join("");
      return window.btoa(binString);
    } catch (e) {
      return window.btoa(unescape(encodeURIComponent(str)));
    }
  }

  function decodeB64(str) {
    try {
      const binString = window.atob(str);
      const bytes = Uint8Array.from(binString, (m) => m.charCodeAt(0));
      return new TextDecoder().decode(bytes);
    } catch (e) {
      return decodeURIComponent(escape(window.atob(str)));
    }
  }

  function escapeHTML(str) {
    if (!str) return "";
    return String(str).replace(/[&<>'"]/g, 
      tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag] || tag)
    );
  }

  // Safe Markdown rendering (Fail-closed to avoid XSS if sanitizer is missing)
  function renderSafeMarkdown(rawMarkdown) {
    if (!rawMarkdown) return "";
    if (!window.DOMPurify) {
      console.warn("DOMPurify chưa sẵn sàng. Fallback sang escaped plain text.");
      return escapeHTML(rawMarkdown).replace(/\n/g, "<br>");
    }
    const html = window.marked ? window.marked.parse(rawMarkdown) : escapeHTML(rawMarkdown);
    return window.DOMPurify.sanitize(html, {
      USE_PROFILES: { html: true }
    });
  }

  // =========================================================================
  // 1. UNIVERSAL CUSTOM POPUP & CONFIRM MODAL SYSTEM
  // =========================================================================
  const appModal = document.getElementById("app-modal");
  const modalIcon = document.getElementById("modal-icon");
  const modalTitle = document.getElementById("modal-title");
  const modalSubtitle = document.getElementById("modal-subtitle");
  const modalBody = document.getElementById("modal-body");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalCancelBtn = document.getElementById("modal-cancel-btn");
  const modalPrimaryBtn = document.getElementById("modal-primary-btn");

  let currentModalAction = null;

  function openModal({ icon, title, subtitle, bodyHtml, primaryBtnText, onPrimaryClick }) {
    if (modalIcon) modalIcon.textContent = icon || "🌿";
    if (modalTitle) modalTitle.textContent = title || "An Nhiên Tâm Lý";
    if (modalSubtitle) modalSubtitle.textContent = subtitle || "";
    if (modalBody) modalBody.innerHTML = bodyHtml || "";
    if (modalCancelBtn) modalCancelBtn.style.display = "none";
    if (modalPrimaryBtn) {
      modalPrimaryBtn.textContent = primaryBtnText || "Đã Hiểu ✨";
      modalPrimaryBtn.className = "btn-send";
      currentModalAction = onPrimaryClick || null;
    }
    if (appModal) {
      appModal.style.display = "flex";
      document.body.style.overflow = "hidden";
    }
  }

  function openConfirmModal({ icon, title, subtitle, bodyHtml, confirmText, cancelText, isDanger, onConfirm }) {
    if (modalIcon) modalIcon.textContent = icon || "❓";
    if (modalTitle) modalTitle.textContent = title || "Xác Nhận";
    if (modalSubtitle) modalSubtitle.textContent = subtitle || "";
    if (modalBody) modalBody.innerHTML = bodyHtml || "";
    if (modalCancelBtn) {
      modalCancelBtn.style.display = "inline-flex";
      modalCancelBtn.textContent = cancelText || "Hủy Bỏ";
      modalCancelBtn.onclick = closeModal;
    }
    if (modalPrimaryBtn) {
      modalPrimaryBtn.textContent = confirmText || "Đồng Ý";
      modalPrimaryBtn.className = isDanger ? "btn-send btn-stop-stream" : "btn-send";
      currentModalAction = onConfirm || null;
    }
    if (appModal) {
      appModal.style.display = "flex";
      document.body.style.overflow = "hidden";
    }
  }

  function closeModal() {
    if (appModal) {
      appModal.style.display = "none";
      document.body.style.overflow = "";
      currentModalAction = null;
    }
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeModal);
  if (modalCancelBtn) modalCancelBtn.addEventListener("click", closeModal);
  if (modalPrimaryBtn) {
    modalPrimaryBtn.addEventListener("click", () => {
      const action = currentModalAction;
      closeModal();
      if (typeof action === "function") {
        action();
      }
    });
  }

  if (appModal) {
    appModal.addEventListener("click", (e) => {
      if (e.target === appModal) closeModal();
    });
  }

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && appModal && appModal.style.display === "flex") {
      closeModal();
    }
  });

  // =========================================================================
  // 2. DARK MODE THEME CONTROLLER
  // =========================================================================
  const THEME_STORAGE_KEY = "an_nhien_theme_mode";
  const btnThemeToggle = document.getElementById("btn-theme-toggle");
  const themeColorMeta = document.getElementById("theme-color-meta");

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    if (btnThemeToggle) {
      btnThemeToggle.textContent = theme === "dark" ? "☀️" : "🌙";
    }
    if (themeColorMeta) {
      themeColorMeta.setAttribute("content", theme === "dark" ? "#0F172A" : "#F8FAFC");
    }
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch (e) {}
  }

  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY) || "light";
  applyTheme(savedTheme);

  if (btnThemeToggle) {
    btnThemeToggle.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      const next = current === "dark" ? "light" : "dark";
      applyTheme(next);
    });
  }

  // =========================================================================
  // 3. CRISIS KEYWORD DETECTION
  // =========================================================================
  const CRISIS_KEYWORDS = [
    "tự tử", "tu tu", "muốn chết", "muon chet", "kết thúc cuộc sống", "ket thuc cuoc song",
    "tự hại", "tu hai", "tự làm đau", "tu lam dau", "không muốn sống", "khong muon song",
    "muốn biến mất", "muon bien mat", "chết đi cho xong", "chet di cho xong", 
    "tuyệt vọng muốn chết", "suicide", "kill myself", "cắt tay", "cat tay"
  ];

  function checkCrisisKeywords(text) {
    if (!text) return false;
    const lower = text.toLowerCase();
    return CRISIS_KEYWORDS.some(kw => lower.includes(kw));
  }

  const crisisAlertBanner = document.getElementById("crisis-alert-banner");
  const btnDismissCrisis = document.getElementById("btn-dismiss-crisis");
  if (btnDismissCrisis && crisisAlertBanner) {
    btnDismissCrisis.addEventListener("click", () => {
      crisisAlertBanner.style.display = "none";
    });
  }

  // =========================================================================
  // 4. APP STATE & PERSISTENCE
  // =========================================================================
  const STORAGE_KEY = "an_nhien_chat_session_v1";

  const DEFAULT_MESSAGES = [
    {
      role: "model",
      content: "Chào bạn, mình là **An Nhiên Tâm Lý**. Không gian ở đây hoàn toàn an toàn và riêng tư. Dù bạn đang gặp áp lực học tập, chuyện tình cảm hay những băn khoăn khó nói, mình luôn ở đây để lắng nghe và cùng bạn tháo gỡ dứt khoát. Hôm nay bạn đang bận lòng chuyện gì, hãy chia sẻ cùng mình nhé."
    }
  ];

  function loadStoredMessages() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.warn("Không thể khôi phục lịch sử từ localStorage:", e);
    }
    return DEFAULT_MESSAGES;
  }

  function saveStoredMessages(messages) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch (e) {
      console.warn("Không thể lưu lịch sử vào localStorage:", e);
    }
  }

  const state = {
    messages: loadStoredMessages(),
    mode: "empathy",
    currentMood: "Bình yên",
    stressLevel: 4,
    isStreaming: false,
    activeQuizType: "gad7",
    allQuizzes: null,
    quizState: {
      currentQuestion: 0,
      answers: [],
      quizData: null
    },
    breathingInterval: null,
    breathingActive: false,
    breathingMode: "478"
  };

  let currentAbortController = null;

  // DOM Elements
  const navTabs = document.querySelectorAll(".nav-tab-btn");
  const mobileNavBtns = document.querySelectorAll(".mobile-nav-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const chatMessagesEl = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const stressSlider = document.getElementById("stress-slider");
  const stressValDisplay = document.getElementById("stress-val-display");
  const chatGreetingTitle = document.getElementById("chat-greeting-title");

  const chatSidebar = document.getElementById("chat-sidebar");
  const btnToggleSidebar = document.getElementById("btn-toggle-sidebar");
  const btnCloseSidebar = document.getElementById("btn-close-sidebar");
  const drawerBackdrop = document.getElementById("drawer-backdrop");

  const btnSend = document.getElementById("btn-send");
  const btnSendLabel = document.getElementById("btn-send-label");
  const btnSendIcon = document.getElementById("btn-send-icon");

  // R7: Health Check Indicator Real-time
  const statusIndicator = document.getElementById("status-indicator");
  const statusText = document.getElementById("status-text");

  async function checkSystemHealth() {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      if (data.status === "ready" || data.ready === true) {
        if (statusIndicator) statusIndicator.className = "status-indicator online";
        if (statusText) statusText.textContent = "Đang Trực Tuyến";
      } else {
        if (statusIndicator) statusIndicator.className = "status-indicator maintenance";
        if (statusText) statusText.textContent = "Bảo Trì Kết Nối";
      }
    } catch (err) {
      if (statusIndicator) statusIndicator.className = "status-indicator offline";
      if (statusText) statusText.textContent = "Mất Kết Nối";
    }
  }
  checkSystemHealth();
  setInterval(checkSystemHealth, 30000);

  // Greeting
  function initGreeting() {
    const hour = new Date().getHours();
    let text = "Chào buổi sáng an lành.";
    if (hour >= 12 && hour < 18) text = "Chào buổi chiều dịu êm.";
    else if (hour >= 18 && hour < 22) text = "Chào buổi tối ấm áp.";
    else if (hour >= 22 || hour < 5) text = "Đêm đã về khuya.";
    if (chatGreetingTitle) chatGreetingTitle.textContent = text;
  }
  initGreeting();

  // Navigation Tabs
  function activateTab(targetTabId) {
    navTabs.forEach(b => {
      if (b.getAttribute("data-tab") === targetTabId) b.classList.add("active");
      else b.classList.remove("active");
    });
    mobileNavBtns.forEach(b => {
      if (b.getAttribute("data-tab") === targetTabId) b.classList.add("active");
      else b.classList.remove("active");
    });
    tabPanes.forEach(p => {
      if (p.id === targetTabId) p.classList.add("active");
      else p.classList.remove("active");
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  navTabs.forEach(btn => btn.addEventListener("click", () => activateTab(btn.getAttribute("data-tab"))));
  mobileNavBtns.forEach(btn => btn.addEventListener("click", () => activateTab(btn.getAttribute("data-tab"))));

  // Mobile Drawer & Backdrop logic
  function openSidebar() {
    if (chatSidebar) chatSidebar.classList.add("open");
    if (drawerBackdrop) drawerBackdrop.classList.add("active");
  }

  function closeSidebar() {
    if (chatSidebar) chatSidebar.classList.remove("open");
    if (drawerBackdrop) drawerBackdrop.classList.remove("active");
  }

  if (btnToggleSidebar) btnToggleSidebar.addEventListener("click", openSidebar);
  if (btnCloseSidebar) btnCloseSidebar.addEventListener("click", closeSidebar);
  if (drawerBackdrop) drawerBackdrop.addEventListener("click", closeSidebar);

  // =========================================================================
  // 5. FEATURE GUIDE POPUPS
  // =========================================================================
  const btnGuideChat = document.getElementById("btn-guide-chat");
  if (btnGuideChat) {
    btnGuideChat.addEventListener("click", () => {
      openModal({
        icon: "💬",
        title: "Hướng Dẫn Trò Chuyện Cùng An Nhiên",
        subtitle: "Không gian lắng nghe thấu cảm & tư vấn tâm lý cá nhân hóa",
        bodyHtml: `
          <div style="display:flex; flex-direction:column; gap:14px;">
            <div style="background:var(--primary-light); padding:12px 14px; border-radius:var(--radius-md); border-left:3px solid var(--primary);">
              <strong>🌿 3 Phong Cách Trò Chuyện Linh Hoạt:</strong>
              <ul style="margin-left:18px; margin-top:6px; font-size:0.88rem;">
                <li><strong>🕊️ Lắng nghe & Đồng cảm:</strong> Phù hợp khi bạn cần sự an ủi, thấu hiểu và xoa dịu cảm xúc tức thì.</li>
                <li><strong>🧩 Phân tích & Tháo gỡ nút thắt (CBT):</strong> Phân tích logic bẫy suy nghĩ và đưa ra giải pháp dứt khoát.</li>
                <li><strong>🧘 Tĩnh tâm & Thả lỏng:</strong> Hướng dẫn quay về hơi thở và tìm lại sự bình an trong tâm trí.</li>
              </ul>
            </div>
            <div>
              <strong>🎯 Cá nhân hóa theo tâm trạng:</strong>
              <p style="font-size:0.88rem; color:var(--text-muted); margin-top:4px;">
                Bạn có thể chọn biểu tượng cảm xúc và kéo thanh <em>Mức độ áp lực (1 - 10)</em> bên thanh bên trái để An Nhiên điều chỉnh giọng điệu phù hợp nhất với bạn.
              </p>
            </div>
            <div style="background:var(--bg-page); border:1px solid var(--border-color); padding:12px 14px; border-radius:var(--radius-md); font-size:0.85rem;">
              🔒 <strong>Bảo mật tuyệt đối:</strong> Cuộc trò chuyện được lưu cục bộ trên máy của bạn và không chia sẻ cho bên thứ ba.
            </div>
          </div>
        `,
        primaryBtnText: "Bắt Đầu Trò Chuyện ✨"
      });
    });
  }

  const btnGuideEdu = document.getElementById("btn-guide-edu");
  if (btnGuideEdu) {
    btnGuideEdu.addEventListener("click", () => {
      openModal({
        icon: "📚",
        title: "Liệu Pháp Nhận Thức Hành Vi (CBT)",
        subtitle: "Công cụ tâm lý học thực chứng giúp bạn làm chủ cảm xúc",
        bodyHtml: `
          <div style="display:flex; flex-direction:column; gap:14px;">
            <p>
              <strong>Liệu pháp CBT (Cognitive Behavioral Therapy)</strong> khẳng định rằng: <em>Không phải hoàn cảnh làm ta tổn thương, mà chính là cách ta diễn giải hoàn cảnh đó.</em>
            </p>
            <div style="background:var(--primary-light); padding:14px; border-radius:var(--radius-md); border:1px solid var(--border-color);">
              <h4 style="color:var(--primary); margin-bottom:6px;">Tam Giác Nhận Thức CBT:</h4>
              <p style="font-size:0.88rem; line-height:1.6;">
                <strong>Suy Nghĩ</strong> (Bẫy nhận thức) ➔ <strong>Cảm Xúc</strong> (Lo âu, buồn bã) ➔ <strong>Hành Vi</strong> (Trì hoãn, thu mình). Khi thay đổi suy nghĩ, cảm xúc của bạn sẽ tự nhiên bình an trở lại.
              </p>
            </div>
            <p style="font-size:0.88rem; color:var(--text-muted);">
              👉 Hãy nhấp vào từng thẻ <strong>8 Bẫy Suy Nghĩ Thường Gặp</strong> bên dưới để nhận diện và học cách hóa giải ngay lập tức!
            </p>
          </div>
        `,
        primaryBtnText: "Đã Hiểu CBT ✨"
      });
    });
  }

  const btnGuideQuiz = document.getElementById("btn-guide-quiz");
  if (btnGuideQuiz) {
    btnGuideQuiz.addEventListener("click", () => {
      openModal({
        icon: "📝",
        title: "Ý Nghĩa Thang Đo Tự Đánh Giá (GAD-7 & PHQ-9)",
        subtitle: "Bộ công cụ trắc nghiệm chuẩn hóa y khoa quốc tế",
        bodyHtml: `
          <div style="display:flex; flex-direction:column; gap:14px;">
            <div style="background:var(--bg-page); padding:12px 14px; border-radius:var(--radius-md); border:1px solid var(--border-color);">
              <strong>📊 Thang đo GAD-7 (Generalized Anxiety Disorder 7):</strong>
              <p style="font-size:0.88rem; color:var(--text-muted); margin-top:4px;">
                Đo lường mức độ lo âu, bồn chồn và căng thẳng trong 2 tuần qua qua 7 câu hỏi tiêu chuẩn.
              </p>
            </div>
            <div style="background:var(--bg-page); padding:12px 14px; border-radius:var(--radius-md); border:1px solid var(--border-color);">
              <strong>🌧️ Thang đo PHQ-9 (Patient Health Questionnaire 9):</strong>
              <p style="font-size:0.88rem; color:var(--text-muted); margin-top:4px;">
                Sàng lọc mức độ trầm cảm và suy giảm năng lượng với 9 câu hỏi lâm sàng.
              </p>
            </div>
            <div style="background:#FEF2F2; border:1px solid #FCA5A5; padding:12px 14px; border-radius:var(--radius-md); color:#991B1B; font-size:0.85rem;">
              ⚠️ <em>Lưu ý quan trọng:</em> Bảng tự đánh giá mang tính chất tham khảo và phản tư cảm xúc, không thay thế chẩn đoán y khoa chính thức của bác sĩ chuyên khoa tâm thần.
            </div>
          </div>
        `,
        primaryBtnText: "Tiến Hành Làm Bài 🚀"
      });
    });
  }

  const btnGuideStudio = document.getElementById("btn-guide-studio");
  if (btnGuideStudio) {
    btnGuideStudio.addEventListener("click", () => {
      openModal({
        icon: "🧘",
        title: "Khoa Học Về Nhịp Thở & Tĩnh Tâm",
        subtitle: "Kích hoạt hệ thần kinh phó giao cảm để giảm stress tức thì",
        bodyHtml: `
          <div style="display:flex; flex-direction:column; gap:14px;">
            <div>
              <strong>🌬️ Phương Pháp Thở 4-7-8 (Tiến sĩ Andrew Weil):</strong>
              <p style="font-size:0.88rem; color:var(--text-muted); margin-top:4px;">
                <strong>Hít vào 4 giây</strong> qua mũi ➔ <strong>Giữ hơi thở 7 giây</strong> ➔ <strong>Thở ra êm 8 giây</strong> qua miệng. Kỹ thuật này giúp hạ nhịp tim, giảm lượng cortisol và đưa não bộ vào trạng thái thư thái sâu.
              </p>
            </div>
            <div>
              <strong>📦 Kỹ Thuật Thở Vuông (Box Breathing - Navy SEALs):</strong>
              <p style="font-size:0.88rem; color:var(--text-muted); margin-top:4px;">
                <strong>Hít 4s - Giữ 4s - Thở 4s - Nghỉ 4s</strong>. Giúp tái tạo sự tập trung sắc bén và làm chủ tâm trí khi chịu áp lực cao.
              </p>
            </div>
          </div>
        `,
        primaryBtnText: "Tập Thở Ngay 🍃"
      });
    });
  }

  const btnGroundingCard = document.getElementById("btn-grounding-card");
  if (btnGroundingCard) {
    btnGroundingCard.addEventListener("click", () => {
      openModal({
        icon: "🌿",
        title: "Kỹ Thuật Neo Cảm Xúc 5-4-3-2-1",
        subtitle: "Cắt đứt cơn hoảng loạn và suy nghĩ miên man bằng 5 giác quan",
        bodyHtml: `
          <div style="display:flex; flex-direction:column; gap:12px; font-size:0.9rem;">
            <p>Khi cảm xúc dâng trào hoặc tâm trí bị cuốn vào lo âu, hãy nhìn xung quanh và lần lượt thực hiện:</p>
            <div style="background:var(--primary-light); padding:10px 14px; border-radius:var(--radius-md); border-left:3px solid var(--primary);">
              <strong>👀 5 ĐIỀU BẠN NHÌN THẤY:</strong> Một chiếc lá, vệt nắng, cây bút, bức tường...
            </div>
            <div style="background:var(--bg-page); padding:10px 14px; border-radius:var(--radius-md); border-left:3px solid #38BDF8;">
              <strong>🖐️ 4 ĐIỀU BẠN CẢM NHẬN ĐƯỢC:</strong> Độ mịn của áo, sự vững chắc của mặt sàn dưới chân...
            </div>
            <div style="background:var(--primary-light); padding:10px 14px; border-radius:var(--radius-md); border-left:3px solid #10B981;">
              <strong>👂 3 ÂM THANH BẠN NGHE THẤY:</strong> Tiếng quạt, tiếng xe ngoài phố, tiếng thở của chính bạn...
            </div>
            <div style="background:var(--bg-page); padding:10px 14px; border-radius:var(--radius-md); border-left:3px solid #F59E0B;">
              <strong>👃 2 MÙI HƯƠNG BẠN NGỬI THẤY:</strong> Mùi cà phê, mùi không khí trong phòng...
            </div>
            <div style="background:var(--primary-light); padding:10px 14px; border-radius:var(--radius-md); border-left:3px solid #6366F1;">
              <strong>👅 1 VỊ BẠN NẾM ĐƯỢC:</strong> Vị nước mát trong miệng, hay một ngụm trà ấm...
            </div>
          </div>
        `,
        primaryBtnText: "Đã Bình Tâm ✨"
      });
    });
  }

  // =========================================================================
  // 6. CHAT FLOW & SMART STREAMING
  // =========================================================================
  function renderMessages() {
    chatMessagesEl.innerHTML = "";
    state.messages.forEach(msg => appendMessageToDOM(msg.role, msg.content));
    forceScrollToBottom();
  }

  function appendMessageToDOM(role, content) {
    const isUser = role === "user";
    const wrapper = document.createElement("div");
    wrapper.className = `msg-wrapper ${isUser ? "user" : "assistant"}`;

    const avatar = document.createElement("div");
    avatar.className = "msg-avatar";
    avatar.textContent = isUser ? "🌱" : "🕊️";

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";
    bubble.innerHTML = renderSafeMarkdown(content);

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatMessagesEl.appendChild(wrapper);
    return bubble;
  }

  function forceScrollToBottom() {
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
  }

  function smartScrollToBottom() {
    const threshold = 140;
    const distanceToBottom = chatMessagesEl.scrollHeight - chatMessagesEl.scrollTop - chatMessagesEl.clientHeight;
    if (distanceToBottom <= threshold) {
      chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
    }
  }

  function setStreamingState(isStreaming) {
    state.isStreaming = isStreaming;
    if (isStreaming) {
      if (btnSend) {
        btnSend.classList.add("btn-stop-stream");
        btnSend.setAttribute("aria-label", "Dừng phản hồi");
      }
      if (btnSendLabel) btnSendLabel.textContent = "Dừng";
      if (btnSendIcon) btnSendIcon.textContent = "⏹️";
    } else {
      if (btnSend) {
        btnSend.classList.remove("btn-stop-stream");
        btnSend.setAttribute("aria-label", "Gửi tin nhắn");
      }
      if (btnSendLabel) btnSendLabel.textContent = "Gửi";
      if (btnSendIcon) btnSendIcon.textContent = "🕊️";
      currentAbortController = null;
    }
  }

  // Chat Streaming with Base64 Obfuscated Transmission & Context Slicing
  async function sendMessage(text) {
    if (!text || !text.trim()) return;

    if (state.isStreaming) {
      if (currentAbortController) {
        currentAbortController.abort();
      }
      setStreamingState(false);
      return;
    }

    const trimmedText = text.trim();
    closeSidebar();

    if (checkCrisisKeywords(trimmedText) && crisisAlertBanner) {
      crisisAlertBanner.style.display = "flex";
      crisisAlertBanner.scrollIntoView({ behavior: "smooth" });
    }

    state.messages.push({ role: "user", content: trimmedText });
    saveStoredMessages(state.messages);
    appendMessageToDOM("user", trimmedText);
    chatInput.value = "";
    forceScrollToBottom();

    setStreamingState(true);
    currentAbortController = new AbortController();

    const assistantBubble = appendMessageToDOM("assistant", '<div class="typing-wave"><span></span><span></span><span></span></div>');
    forceScrollToBottom();

    let fullText = "";

    try {
      const payloadMessages = state.messages.slice(-20);

      const rawPayload = JSON.stringify({
        messages: payloadMessages,
        mode: state.mode,
        mood_context: {
          mood_name: state.currentMood,
          stress_level: state.stressLevel
        }
      });

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ p: encodeB64(rawPayload) }),
        signal: currentAbortController.signal
      });

      if (!response.ok) {
        throw new Error(`Lỗi kết nối máy chủ (${response.status})`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.replace("data: ", "").trim();
            if (jsonStr) {
              try {
                const parsed = JSON.parse(jsonStr);
                if (parsed.d) {
                  const chunkText = decodeB64(parsed.d);
                  fullText += chunkText;
                  assistantBubble.innerHTML = renderSafeMarkdown(fullText);
                  smartScrollToBottom();
                }
              } catch (e) {}
            }
          }
        }
      }

      if (fullText.trim()) {
        state.messages.push({ role: "model", content: fullText });
        saveStoredMessages(state.messages);
      } else {
        const fallbackMsg = "*(An Nhiên đang gặp gián đoạn kết nối tạm thời. Bạn hãy thử gửi lại sau giây lát nhé.)*";
        assistantBubble.innerHTML = renderSafeMarkdown(fallbackMsg);
        state.messages.pop();
        saveStoredMessages(state.messages);
      }
    } catch (err) {
      if (err.name === "AbortError") {
        if (fullText.trim()) {
          state.messages.push({ role: "model", content: fullText });
          saveStoredMessages(state.messages);
        } else {
          assistantBubble.innerHTML = `*(Đã dừng câu trả lời)*`;
          state.messages.pop();
          saveStoredMessages(state.messages);
        }
      } else {
        console.error("Chat error:", err);
        const errMsg = "*(Kết nối gián đoạn. Bạn thử gửi lại tin nhắn nhé.)*";
        assistantBubble.innerHTML = errMsg;
        state.messages.pop();
        saveStoredMessages(state.messages);
      }
    } finally {
      setStreamingState(false);
    }
  }

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (state.isStreaming) {
      if (currentAbortController) currentAbortController.abort();
      setStreamingState(false);
    } else {
      sendMessage(chatInput.value);
    }
  });

  document.querySelectorAll(".chip-btn[data-prompt]").forEach(chip => {
    chip.addEventListener("click", () => sendMessage(chip.getAttribute("data-prompt")));
  });

  document.querySelectorAll(".mode-item").forEach(item => {
    item.addEventListener("click", () => {
      document.querySelectorAll(".mode-item").forEach(i => i.classList.remove("active"));
      item.classList.add("active");
      state.mode = item.getAttribute("data-mode");
    });
  });

  document.querySelectorAll(".mood-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".mood-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.currentMood = btn.getAttribute("data-mood");
    });
  });

  stressSlider.addEventListener("input", (e) => {
    state.stressLevel = parseInt(e.target.value);
    stressValDisplay.textContent = `${state.stressLevel} / 10`;
  });

  // Clear Chat with Custom Modal Confirmation (No browser native confirm dialog)
  document.getElementById("btn-clear-chat").addEventListener("click", () => {
    openConfirmModal({
      icon: "🗑️",
      title: "Bắt Đầu Lại Phiên Trò Chuyện?",
      subtitle: "Làm mới không gian lắng nghe riêng tư",
      bodyHtml: `
        <p style="font-size:0.92rem; line-height:1.6; color:var(--text-dark);">
          Bạn có chắc chắn muốn xóa toàn bộ lịch sử trò chuyện này không? Toàn bộ nội dung trao đổi sẽ được xóa sạch khỏi bộ nhớ thiết bị để bạn bắt đầu một phiên mới hoàn toàn riêng tư.
        </p>
      `,
      confirmText: "Xóa & Bắt Đầu Lại",
      cancelText: "Giữ Lại",
      isDanger: true,
      onConfirm: () => {
        state.messages = [
          {
            role: "model",
            content: "Chào bạn, mình đã sẵn sàng cho một phiên trò chuyện mới. Hãy chia sẻ bất kỳ điều gì bạn muốn nhé."
          }
        ];
        localStorage.removeItem(STORAGE_KEY);
        renderMessages();
        if (crisisAlertBanner) crisisAlertBanner.style.display = "none";
        closeSidebar();
      }
    });
  });

  // Export Chat to Text File with Custom Info Modal
  const btnExportChat = document.getElementById("btn-export-chat");
  if (btnExportChat) {
    btnExportChat.addEventListener("click", () => {
      if (state.messages.length <= 1) {
        openModal({
          icon: "ℹ️",
          title: "Chưa Có Nội Dung Để Xuất",
          subtitle: "Nhật ký hội thoại hiện đang trống",
          bodyHtml: "<p>Hãy trò chuyện một vài câu cùng An Nhiên trước khi xuất biên bản nhật ký nhé.</p>",
          primaryBtnText: "Đã Hiểu ✨"
        });
        return;
      }
      let exportText = `====================================================\n`;
      exportText += `   BIÊN BẢN TRÒ CHUYỆN - AN NHIÊN TÂM LÝ\n`;
      exportText += `   Thời gian xuất: ${new Date().toLocaleString("vi-VN")}\n`;
      exportText += `====================================================\n\n`;

      state.messages.forEach((msg) => {
        const sender = msg.role === "user" ? "BẠN" : "AN NHIÊN";
        exportText += `[${sender}]:\n${msg.content}\n\n----------------------------------------------------\n\n`;
      });

      const blob = new Blob([exportText], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `An_Nhien_Nhat_Ky_${new Date().toISOString().slice(0, 10)}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  // Summarize Session with Custom Modal Notifications
  document.getElementById("btn-summarize").addEventListener("click", async () => {
    if (state.messages.length < 3) {
      openModal({
        icon: "📝",
        title: "Cần Thêm Ngữ Cảnh",
        subtitle: "Đúc kết lời nhắn nhủ",
        bodyHtml: "<p>Hãy chia sẻ thêm một vài câu để An Nhiên có đủ ngữ cảnh đúc kết những lời nhắn nhủ ý nghĩa nhất cho bạn nhé.</p>",
        primaryBtnText: "Tiếp Tục Trò Chuyện ✨"
      });
      return;
    }
    const btn = document.getElementById("btn-summarize");
    btn.textContent = "Đang đúc kết...";
    try {
      const payloadMessages = state.messages.slice(-25);
      const rawPayload = JSON.stringify({ messages: payloadMessages });
      const res = await fetch("/api/summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ p: encodeB64(rawPayload) })
      });
      const data = await res.json();
      if (data.d) {
        const summaryText = decodeB64(data.d);
        state.messages.push({
          role: "model",
          content: `### Đúc Kết Phiên Trò Chuyện:\n\n${summaryText}`
        });
        saveStoredMessages(state.messages);
        renderMessages();
        closeSidebar();
      }
    } catch (e) {
      openModal({
        icon: "⚠️",
        title: "Thông Báo",
        subtitle: "Tạm thời gián đoạn",
        bodyHtml: "<p>Chưa thể tạo đúc kết lúc này. Bạn vui lòng thử lại sau giây lát nhé.</p>",
        primaryBtnText: "Đóng"
      });
    } finally {
      btn.textContent = "📝 Đúc Kết Lời Nhắn Nhủ";
    }
  });

  renderMessages();

  // =========================================================================
  // 7. KNOWLEDGE & PSYCHOEDUCATION (POPUP CHI TIẾT KHI CLICK THẺ)
  // =========================================================================
  async function loadKnowledge() {
    try {
      const res = await fetch("/api/knowledge");
      const dataJson = await res.json();
      const data = JSON.parse(decodeB64(dataJson.d));
      state.allQuizzes = data.quizzes;

      // Render Distortion Cards with Clickable Popup Details
      const grid = document.getElementById("distortion-grid");
      if (grid && data.distortions) {
        grid.innerHTML = data.distortions.map((d, idx) => `
          <div class="distortion-card" data-dist-idx="${idx}">
            <div>
              <div class="dist-badge">
                <span class="dist-icon-label">${escapeHTML(d.icon)}</span> 
                <span class="dist-title">${escapeHTML(d.name)}</span>
              </div>
              <p class="dist-desc">${escapeHTML(d.description)}</p>
              <div class="dist-example"><strong>Ví dụ:</strong> ${escapeHTML(d.example)}</div>
            </div>
            <div class="dist-reframe">
              <strong>Góc nhìn hóa giải:</strong> ${escapeHTML(d.reframing)}
            </div>
          </div>
        `).join("");

        grid.querySelectorAll(".distortion-card").forEach(card => {
          card.addEventListener("click", () => {
            const idx = parseInt(card.getAttribute("data-dist-idx"));
            const dist = data.distortions[idx];
            if (!dist) return;

            openModal({
              icon: dist.icon,
              title: dist.name,
              subtitle: "Nhận diện & Hóa giải bẫy nhận thức CBT",
              bodyHtml: `
                <div style="display:flex; flex-direction:column; gap:16px;">
                  <div style="font-size:0.95rem; line-height:1.6;">
                    ${escapeHTML(dist.description)}
                  </div>
                  <div style="background:#FFFBEB; border:1px solid #FDE68A; padding:14px; border-radius:var(--radius-md);">
                    <strong style="color:#92400E;">🔍 Biểu hiện thường gặp trong cuộc sống:</strong>
                    <p style="font-size:0.9rem; color:#78350F; margin-top:4px;">"${escapeHTML(dist.example)}"</p>
                  </div>
                  <div style="background:var(--primary-light); border:1px solid rgba(13,148,136,0.3); padding:14px; border-radius:var(--radius-md);">
                    <strong style="color:var(--primary);">🌿 Cách tái cấu trúc nhận thức (Cognitive Reframing):</strong>
                    <p style="font-size:0.9rem; color:#0F766E; margin-top:4px;">${escapeHTML(dist.reframing)}</p>
                  </div>
                  <div style="font-size:0.85rem; color:var(--text-muted);">
                    💡 <em>Bạn có đang gặp phải bẫy suy nghĩ này không? Hãy nhấn nút bên dưới để cùng An Nhiên tháo gỡ nhé!</em>
                  </div>
                </div>
              `,
              primaryBtnText: "💬 Thực Hành Hóa Giải Cùng An Nhiên",
              onPrimaryClick: () => {
                activateTab("tab-chat");
                sendMessage(`Mình vừa tìm hiểu về bẫy suy nghĩ "${dist.name}". An Nhiên có thể giúp mình phân tích và thực hành hóa giải bẫy suy nghĩ này trong các tình huống thực tế được không?`);
              }
            });
          });
        });
      }

      // Render Articles with Full Reading Popup
      const artContainer = document.getElementById("articles-container");
      if (artContainer && data.articles) {
        artContainer.innerHTML = data.articles.map((a, idx) => `
          <div class="article-card" data-art-idx="${idx}" style="background:var(--card-bg); border:1px solid var(--border-color); border-radius:var(--radius-lg); padding:24px; box-shadow:var(--shadow-sm); cursor:pointer; transition:transform 0.2s, box-shadow 0.2s;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:var(--primary-light); color:var(--primary); font-size:0.8rem; font-weight:700; padding:4px 12px; border-radius:var(--radius-full);">${escapeHTML(a.category)}</span>
              <span style="font-size:0.8rem; color:var(--text-muted);">${escapeHTML(a.readTime)} • 🔍 Nhấp để đọc</span>
            </div>
            <h3 style="font-family:var(--font-heading); font-size:1.25rem; color:var(--indigo-dark); margin-bottom:12px;">${escapeHTML(a.title)}</h3>
            <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom:14px;">${escapeHTML(a.summary)}</p>
            <div style="background:var(--bg-page); padding:16px; border-radius:var(--radius-md); font-size:0.9rem; line-height:1.7;">
              ${renderSafeMarkdown(a.content)}
            </div>
          </div>
        `).join("");

        artContainer.querySelectorAll(".article-card").forEach(card => {
          card.addEventListener("mouseenter", () => card.style.boxShadow = "var(--shadow-md)");
          card.addEventListener("mouseleave", () => card.style.boxShadow = "var(--shadow-sm)");
          card.addEventListener("click", () => {
            const idx = parseInt(card.getAttribute("data-art-idx"));
            const art = data.articles[idx];
            if (!art) return;

            openModal({
              icon: "📖",
              title: art.title,
              subtitle: `${art.category} • Thời gian đọc: ${art.readTime}`,
              bodyHtml: `
                <div style="display:flex; flex-direction:column; gap:16px;">
                  <div style="font-size:0.95rem; line-height:1.8;">
                    ${renderSafeMarkdown(art.content)}
                  </div>
                </div>
              `,
              primaryBtnText: "💬 Thảo Luận Bài Viết Này",
              onPrimaryClick: () => {
                activateTab("tab-chat");
                sendMessage(`Mình vừa đọc bài viết "${art.title}" trong mục Góc Nhìn Tâm Lý. An Nhiên có thể đúc kết cho mình những hành động cụ thể để áp dụng bài học này vào cuộc sống không?`);
              }
            });
          });
        });
      }

      // Setup initial Quiz Data
      selectQuizType(state.activeQuizType);
    } catch (e) {
      console.warn("Không thể nạp tri thức tâm lý:", e);
    }
  }
  loadKnowledge();

  // =========================================================================
  // 8. SELF-ASSESSMENT QUIZ
  // =========================================================================
  const quizIntroView = document.getElementById("quiz-intro-view");
  const quizIntroTitle = document.getElementById("quiz-intro-title");
  const quizIntroSubtitle = document.getElementById("quiz-intro-subtitle");
  const quizStepView = document.getElementById("quiz-step-view");
  const quizResultView = document.getElementById("quiz-result-view");
  const btnStartQuiz = document.getElementById("btn-start-quiz");
  const quizStepIndicator = document.getElementById("quiz-step-indicator");
  const quizProgressFill = document.getElementById("quiz-progress-fill");
  const quizProgressPercent = document.getElementById("quiz-progress-percent");
  const quizQuestionText = document.getElementById("quiz-question-text");
  const quizOptionsList = document.getElementById("quiz-options-list");
  const quizTypeBtns = document.querySelectorAll(".quiz-type-btn");

  function selectQuizType(type) {
    state.activeQuizType = type;
    quizTypeBtns.forEach(b => {
      if (b.getAttribute("data-quiz-type") === type) b.classList.add("active");
      else b.classList.remove("active");
    });

    if (state.allQuizzes && state.allQuizzes[type]) {
      const q = state.allQuizzes[type];
      state.quizState.quizData = q;
      if (quizIntroTitle) quizIntroTitle.textContent = q.title;
      if (quizIntroSubtitle) quizIntroSubtitle.textContent = q.subtitle;
    }

    quizStepView.style.display = "none";
    quizResultView.style.display = "none";
    quizIntroView.style.display = "block";
  }

  quizTypeBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      selectQuizType(btn.getAttribute("data-quiz-type"));
    });
  });

  btnStartQuiz.addEventListener("click", () => {
    state.quizState.currentQuestion = 0;
    state.quizState.answers = [];
    quizIntroView.style.display = "none";
    quizResultView.style.display = "none";
    quizStepView.style.display = "block";
    renderQuizStep();
  });

  function renderQuizStep() {
    const qData = state.quizState.quizData;
    if (!qData) return;

    const total = qData.questions.length;
    const curr = state.quizState.currentQuestion;

    if (curr >= total) {
      finishQuiz();
      return;
    }

    quizStepIndicator.textContent = `Câu hỏi ${curr + 1} / ${total}`;
    const percent = Math.round(((curr) / total) * 100);
    quizProgressFill.style.width = `${percent}%`;
    quizProgressPercent.textContent = `${percent}%`;
    quizQuestionText.textContent = `${curr + 1}. ${qData.questions[curr]}`;

    quizOptionsList.innerHTML = qData.options.map(opt => `
      <button class="quiz-option-btn" data-score="${opt.score}">
        <span>${escapeHTML(opt.label)}</span>
        <span style="color:var(--text-muted); font-size:0.85rem;">+${opt.score} điểm</span>
      </button>
    `).join("");

    quizOptionsList.querySelectorAll(".quiz-option-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const score = parseInt(btn.getAttribute("data-score"));
        state.quizState.answers.push(score);
        state.quizState.currentQuestion++;
        renderQuizStep();
      });
    });
  }

  function finishQuiz() {
    quizStepView.style.display = "none";
    quizResultView.style.display = "block";

    const totalScore = state.quizState.answers.reduce((a, b) => a + b, 0);
    const qData = state.quizState.quizData;
    const maxScore = qData.questions.length * 3;

    // PHQ-9 Câu 9 >= 1 Điểm trigger crisis
    const isPHQ9 = state.activeQuizType === "phq9" || (qData.id === "phq9");
    const item9Score = (isPHQ9 && state.quizState.answers.length >= 9) ? state.quizState.answers[8] : 0;

    if (item9Score >= 1 && crisisAlertBanner) {
      crisisAlertBanner.style.display = "flex";
      crisisAlertBanner.scrollIntoView({ behavior: "smooth" });
    }

    let bracket = qData.brackets[0];
    for (const b of qData.brackets) {
      if (totalScore >= b.range[0] && totalScore <= b.range[1]) {
        bracket = b;
        break;
      }
    }

    const badge = document.getElementById("quiz-score-badge");
    badge.textContent = `Tổng Điểm: ${totalScore} / ${maxScore}`;
    badge.style.backgroundColor = (item9Score >= 1 && bracket.color === "#10B981") ? "#EA580C" : bracket.color;

    document.getElementById("quiz-level-text").textContent = bracket.level;
    document.getElementById("quiz-level-text").style.color = (item9Score >= 1 && bracket.color === "#10B981") ? "#EA580C" : bracket.color;

    let adviceHtml = `<strong>Lời khuyên & Định hướng:</strong><br>${escapeHTML(bracket.advice)}`;
    if (item9Score >= 1) {
      adviceHtml += `
        <div style="margin-top:14px; padding:12px 14px; background:#FEF2F2; border:1.5px solid #FCA5A5; border-radius:8px; color:#991B1B; font-size:0.9rem; line-height:1.6;">
          ⚠️ <strong>Lưu ý an toàn quan trọng:</strong> Bạn đã ghi nhận có suy nghĩ tự làm tổn thương bản thân ở câu hỏi số 9. Bất kể tổng điểm là bao nhiêu, xin bạn hãy liên hệ ngay với người thân đáng tin cậy hoặc gọi tổng đài hỗ trợ khẩn cấp <strong>111</strong> (miễn phí 24/7), <strong>115</strong> hoặc Đường dây Ngày Mai <strong>096 306 1414</strong> để được lắng nghe và trợ giúp kịp thời.
        </div>
      `;
    }
    document.getElementById("quiz-advice-text").innerHTML = adviceHtml;

    document.getElementById("btn-discuss-result").onclick = () => {
      const quizName = qData.title || (state.activeQuizType === "phq9" ? "trầm cảm PHQ-9" : "lo âu GAD-7");
      const prompt = `Mình vừa làm bài tự đánh giá ${quizName} và đạt ${totalScore}/${maxScore} điểm (${bracket.level}). An Nhiên có thể tư vấn và hướng dẫn mình cách cải thiện tâm trạng lúc này không?`;
      activateTab("tab-chat");
      sendMessage(prompt);
    };

    document.getElementById("btn-retake-quiz").onclick = () => {
      quizResultView.style.display = "none";
      quizIntroView.style.display = "block";
    };
  }

  // =========================================================================
  // 9. RELAXATION BREATHING
  // =========================================================================
  const circleBreathe = document.getElementById("circle-breathe");
  const breatheActionText = document.getElementById("breathe-action-text");
  const breatheTimerText = document.getElementById("breathe-timer-text");
  const btnToggleBreathe = document.getElementById("btn-toggle-breathe");
  const btnMode478 = document.getElementById("btn-mode-478");
  const btnModeBox = document.getElementById("btn-mode-box");

  btnMode478.addEventListener("click", () => {
    btnMode478.classList.add("active");
    btnModeBox.classList.remove("active");
    state.breathingMode = "478";
    stopBreathing();
  });

  btnModeBox.addEventListener("click", () => {
    btnModeBox.classList.add("active");
    btnMode478.classList.remove("active");
    state.breathingMode = "box";
    stopBreathing();
  });

  btnToggleBreathe.addEventListener("click", () => {
    if (state.breathingActive) stopBreathing();
    else startBreathing();
  });

  function startBreathing() {
    state.breathingActive = true;
    btnToggleBreathe.textContent = "Dừng Bài Tập Thở";
    runBreathingCycle();
  }

  function stopBreathing() {
    state.breathingActive = false;
    clearTimeout(state.breathingInterval);
    btnToggleBreathe.textContent = "▶️ Bắt Đầu";
    circleBreathe.className = "circle-breathe";
    breatheActionText.textContent = "Sẵn sàng";
    breatheTimerText.textContent = "Nhấn Bắt Đầu";
  }

  function runBreathingCycle() {
    if (!state.breathingActive) return;

    if (state.breathingMode === "478") {
      circleBreathe.className = "circle-breathe inhale";
      breatheActionText.textContent = "Hít vào";
      breatheTimerText.textContent = "4 giây";

      state.breathingInterval = setTimeout(() => {
        if (!state.breathingActive) return;
        circleBreathe.className = "circle-breathe hold";
        breatheActionText.textContent = "Giữ hơi thở";
        breatheTimerText.textContent = "7 giây";

        state.breathingInterval = setTimeout(() => {
          if (!state.breathingActive) return;
          circleBreathe.className = "circle-breathe exhale";
          breatheActionText.textContent = "Thở ra êm";
          breatheTimerText.textContent = "8 giây";

          state.breathingInterval = setTimeout(() => runBreathingCycle(), 8000);
        }, 7000);
      }, 4000);
    } else {
      circleBreathe.className = "circle-breathe inhale";
      breatheActionText.textContent = "Hít vào";
      breatheTimerText.textContent = "4 giây";

      state.breathingInterval = setTimeout(() => {
        if (!state.breathingActive) return;
        circleBreathe.className = "circle-breathe hold";
        breatheActionText.textContent = "Giữ";
        breatheTimerText.textContent = "4 giây";

        state.breathingInterval = setTimeout(() => {
          if (!state.breathingActive) return;
          circleBreathe.className = "circle-breathe exhale";
          breatheActionText.textContent = "Thở ra";
          breatheTimerText.textContent = "4 giây";

          state.breathingInterval = setTimeout(() => {
            if (!state.breathingActive) return;
            circleBreathe.className = "circle-breathe";
            breatheActionText.textContent = "Nghỉ ngơi";
            breatheTimerText.textContent = "4 giây";

            state.breathingInterval = setTimeout(() => runBreathingCycle(), 4000);
          }, 4000);
        }, 4000);
      }, 4000);
    }
  }

  // =========================================================================
  // 10. AUTO-IDLE & PRIVACY SLEEP MODE (1 HOUR TIMEOUT)
  // =========================================================================
  const IDLE_TIMEOUT_MS = 60 * 60 * 1000;
  let lastActiveTimestamp = Date.now();
  let isSleeping = false;
  const sleepOverlay = document.getElementById("sleep-overlay");
  const btnWakeUp = document.getElementById("btn-wake-up");

  function recordActivity() {
    if (!isSleeping) {
      lastActiveTimestamp = Date.now();
    }
  }

  ["touchstart", "touchmove", "mousemove", "mousedown", "keydown", "scroll", "click"].forEach(evt => {
    window.addEventListener(evt, recordActivity, { passive: true });
  });

  function putToSleep() {
    if (isSleeping) return;
    isSleeping = true;
    if (sleepOverlay) sleepOverlay.style.display = "flex";
    stopBreathing();
    document.querySelectorAll("audio").forEach(a => a.pause());
  }

  function wakeUp() {
    isSleeping = false;
    lastActiveTimestamp = Date.now();
    if (sleepOverlay) sleepOverlay.style.display = "none";
    state.messages = [
      {
        role: "model",
        content: "Chào bạn, mình là **An Nhiên Tâm Lý**. Phiên trò chuyện mới đã sẵn sàng. Bạn đang cảm thấy thế nào rồi?"
      }
    ];
    saveStoredMessages(state.messages);
    renderMessages();
    activateTab("tab-chat");
  }

  if (btnWakeUp) {
    btnWakeUp.addEventListener("click", wakeUp);
  }

  setInterval(() => {
    if (!isSleeping && (Date.now() - lastActiveTimestamp >= IDLE_TIMEOUT_MS)) {
      putToSleep();
    }
  }, 15000);

  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && !isSleeping) {
      if (Date.now() - lastActiveTimestamp >= IDLE_TIMEOUT_MS) {
        putToSleep();
      }
    }
  });
});
