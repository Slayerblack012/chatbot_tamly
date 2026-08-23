/**
 * AN NHIÊN TÂM LÝ - CLIENT SCRIPT
 * Bảo mật: DOMPurify Fail-closed, UTF-8 Base64 Obfuscation, Role Alternation Auto-Recovery,
 * Can thiệp Khủng hoảng (Crisis Alert & PHQ-9 Item 9 trigger), GAD-7 & PHQ-9, Real Health Check,
 * Dark Mode Toggle, Stop Stream AbortController, Smart Scroll & Drawer Backdrop.
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
  // 1. B1 & C1: DARK MODE THEME CONTROLLER
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
  // 2. CRISIS KEYWORD DETECTION
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
  // 3. APP STATE & PERSISTENCE
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

  // B3: Mobile Drawer & Backdrop logic
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
  // 4. CHAT FLOW & SMART STREAMING (B2: NÚT DỪNG, B4: SMART SCROLL)
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

  // B4: Smart Scroll - chỉ auto-scroll nếu người dùng đang ở gần đáy (~140px)
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

    // Nếu đang stream mà bấm nút -> Hủy stream (B2)
    if (state.isStreaming) {
      if (currentAbortController) {
        currentAbortController.abort();
      }
      setStreamingState(false);
      return;
    }

    const trimmedText = text.trim();
    closeSidebar();

    // Kiểm tra từ khóa khủng hoảng để hiển thị hotline ngay
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
      // Giới hạn 20 tin nhắn gần nhất để payload không bị phình to
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

  // Clear Chat & Reset LocalStorage
  document.getElementById("btn-clear-chat").addEventListener("click", () => {
    if (confirm("Bạn có chắc chắn muốn xóa toàn bộ lịch sử trò chuyện này và bắt đầu lại?")) {
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

  // Export Chat to Text File
  const btnExportChat = document.getElementById("btn-export-chat");
  if (btnExportChat) {
    btnExportChat.addEventListener("click", () => {
      if (state.messages.length <= 1) {
        alert("Chưa có nội dung trò chuyện để xuất.");
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

  // Summarize Session
  document.getElementById("btn-summarize").addEventListener("click", async () => {
    if (state.messages.length < 3) {
      alert("Hãy trò chuyện thêm một vài câu để An Nhiên có thể đúc kết cho bạn nhé.");
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
      alert("Không thể tạo đúc kết lúc này.");
    } finally {
      btn.textContent = "📝 Đúc Kết Lời Nhắn Nhủ";
    }
  });

  renderMessages();

  // =========================================================================
  // 5. KNOWLEDGE & PSYCHOEDUCATION (B5: SKELETON REPLACEMENT)
  // =========================================================================
  async function loadKnowledge() {
    try {
      const res = await fetch("/api/knowledge");
      const dataJson = await res.json();
      const data = JSON.parse(decodeB64(dataJson.d));
      state.allQuizzes = data.quizzes;

      // Render Distortion Cards with Escaped Values
      const grid = document.getElementById("distortion-grid");
      if (grid && data.distortions) {
        grid.innerHTML = data.distortions.map(d => `
          <div class="distortion-card">
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
      }

      // Render Articles
      const artContainer = document.getElementById("articles-container");
      if (artContainer && data.articles) {
        artContainer.innerHTML = data.articles.map(a => `
          <div style="background:var(--card-bg); border:1px solid var(--border-color); border-radius:var(--radius-lg); padding:24px; box-shadow:var(--shadow-sm);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:var(--primary-light); color:var(--primary); font-size:0.8rem; font-weight:700; padding:4px 12px; border-radius:var(--radius-full);">${escapeHTML(a.category)}</span>
              <span style="font-size:0.8rem; color:var(--text-muted);">${escapeHTML(a.readTime)}</span>
            </div>
            <h3 style="font-family:var(--font-heading); font-size:1.25rem; color:var(--indigo-dark); margin-bottom:12px;">${escapeHTML(a.title)}</h3>
            <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom:14px;">${escapeHTML(a.summary)}</p>
            <div style="background:var(--bg-page); padding:16px; border-radius:var(--radius-md); font-size:0.9rem; line-height:1.7;">
              ${renderSafeMarkdown(a.content)}
            </div>
          </div>
        `).join("");
      }

      // Setup initial Quiz Data
      selectQuizType(state.activeQuizType);
    } catch (e) {
      console.warn("Không thể nạp tri thức tâm lý:", e);
    }
  }
  loadKnowledge();

  // =========================================================================
  // 6. SELF-ASSESSMENT QUIZ (A2: NO DOUBLE ESCAPE, C4: PHQ-9 CÂU 9 >= 1)
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
    // A2: Gán textContent trực tiếp, không qua escapeHTML để không bị double-escape & < >
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

    // C4: Kiểm tra câu số 9 của PHQ-9 (index 8) về suy nghĩ tự hại / tự tử
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
  // 7. RELAXATION BREATHING
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
  // 8. AUTO-IDLE & PRIVACY SLEEP MODE (1 HOUR TIMEOUT)
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
