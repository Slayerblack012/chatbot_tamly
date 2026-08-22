/**
 * AN NHIEN TAM LY - APP SCRIPT (ZERO EMOJI & BASE64 PAYLOAD ENCRYPTED)
 */

document.addEventListener("DOMContentLoaded", () => {
  // =========================================================================
  // 0. BASE64 UTF-8 ENCODING & DECODING HELPERS (PEP64 / OBFUSCATION)
  // =========================================================================
  function encodeB64(str) {
    try {
      return window.btoa(unescape(encodeURIComponent(str)));
    } catch (e) {
      return window.btoa(str);
    }
  }

  function decodeB64(str) {
    try {
      return decodeURIComponent(escape(window.atob(str)));
    } catch (e) {
      return window.atob(str);
    }
  }

  // =========================================================================
  // 1. APP STATE
  // =========================================================================
  const state = {
    messages: [
      {
        role: "model",
        content: "Chào bạn, mình là **An Nhiên Tâm Lý**. Không gian ở đây hoàn toàn an toàn và riêng tư. Dù bạn đang gặp áp lực học tập, chuyện tình cảm hay những băn khoăn khó nói, mình luôn ở đây để lắng nghe và cùng bạn tháo gỡ dứt khoát. Hôm nay bạn đang bận lòng chuyện gì, hãy chia sẻ cùng mình nhé."
      }
    ],
    mode: "empathy",
    currentMood: "Bình yên",
    stressLevel: 4,
    isStreaming: false,
    quizState: {
      currentQuestion: 0,
      answers: [],
      quizData: null
    },
    breathingInterval: null,
    breathingActive: false,
    breathingMode: "478"
  };

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

  if (btnToggleSidebar && chatSidebar) {
    btnToggleSidebar.addEventListener("click", () => chatSidebar.classList.add("open"));
  }
  if (btnCloseSidebar && chatSidebar) {
    btnCloseSidebar.addEventListener("click", () => chatSidebar.classList.remove("open"));
  }

  // Safe Markdown
  function renderSafeMarkdown(rawMarkdown) {
    if (!rawMarkdown) return "";
    let html = window.marked ? window.marked.parse(rawMarkdown) : rawMarkdown;
    return window.DOMPurify ? window.DOMPurify.sanitize(html) : html;
  }

  // Render Messages
  function renderMessages() {
    chatMessagesEl.innerHTML = "";
    state.messages.forEach(msg => appendMessageToDOM(msg.role, msg.content));
    scrollToBottom();
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

  function scrollToBottom() {
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
  }

  // Chat Streaming with Base64 Obfuscated Transmission
  async function sendMessage(text) {
    if (!text || !text.trim() || state.isStreaming) return;
    const trimmedText = text.trim();

    if (chatSidebar) chatSidebar.classList.remove("open");

    state.messages.push({ role: "user", content: trimmedText });
    appendMessageToDOM("user", trimmedText);
    chatInput.value = "";
    scrollToBottom();

    state.isStreaming = true;
    const assistantBubble = appendMessageToDOM("assistant", '<div class="typing-wave"><span></span><span></span><span></span></div>');
    scrollToBottom();

    let fullText = "";
    let hasReceivedFirstChunk = false;

    try {
      // Mã hóa toàn bộ payload thành Base64 trước khi gửi
      const rawPayload = JSON.stringify({
        messages: state.messages,
        mode: state.mode,
        mood_context: {
          mood_name: state.currentMood,
          stress_level: state.stressLevel
        }
      });

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ p: encodeB64(rawPayload) })
      });

      if (!response.ok) {
        throw new Error(`Lỗi kết nối (${response.status})`);
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
                // Giải mã Base64 chunk từ server
                if (parsed.d) {
                  const chunkText = decodeB64(parsed.d);
                  fullText += chunkText;
                  if (!hasReceivedFirstChunk) {
                    hasReceivedFirstChunk = true;
                  }
                  assistantBubble.innerHTML = renderSafeMarkdown(fullText);
                  scrollToBottom();
                }
              } catch (e) {}
            }
          }
        }
      }

      state.messages.push({ role: "model", content: fullText });
    } catch (err) {
      assistantBubble.innerHTML = `*(Kết nối gián đoạn. Bạn thử gửi lại nhé.)*`;
    } finally {
      state.isStreaming = false;
    }
  }

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(chatInput.value);
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

  document.getElementById("btn-clear-chat").addEventListener("click", () => {
    state.messages = [
      {
        role: "model",
        content: "Chào bạn, mình đã sẵn sàng cho một phiên trò chuyện mới. Hãy chia sẻ bất kỳ điều gì bạn muốn nhé."
      }
    ];
    renderMessages();
    if (chatSidebar) chatSidebar.classList.remove("open");
  });

  // Summarize Session with Base64
  document.getElementById("btn-summarize").addEventListener("click", async () => {
    if (state.messages.length < 3) {
      alert("Hãy trò chuyện thêm một vài câu để An Nhiên có thể đúc kết cho bạn nhé.");
      return;
    }
    const btn = document.getElementById("btn-summarize");
    btn.textContent = "Đang đúc kết...";
    try {
      const rawPayload = JSON.stringify({ messages: state.messages });
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
        renderMessages();
        if (chatSidebar) chatSidebar.classList.remove("open");
      }
    } catch (e) {
      alert("Không thể tạo đúc kết lúc này.");
    } finally {
      btn.textContent = "Đúc Kết Lời Nhắn Nhủ";
    }
  });

  renderMessages();

  // Load Knowledge
  async function loadKnowledge() {
    try {
      const res = await fetch("/api/knowledge");
      const dataJson = await res.json();
      const data = JSON.parse(decodeB64(dataJson.d));

      const grid = document.getElementById("distortion-grid");
      if (grid && data.distortions) {
        grid.innerHTML = data.distortions.map(d => `
          <div class="distortion-card">
            <div>
              <div class="dist-badge"><span class="dist-icon-label">${d.icon}</span> <span class="dist-title">${d.name}</span></div>
              <p class="dist-desc">${d.description}</p>
              <div class="dist-example"><strong>Ví dụ:</strong> ${d.example}</div>
            </div>
            <div class="dist-reframe">
              <strong>Góc nhìn hóa giải:</strong> ${d.reframing}
            </div>
          </div>
        `).join("");
      }

      const artContainer = document.getElementById("articles-container");
      if (artContainer && data.articles) {
        artContainer.innerHTML = data.articles.map(a => `
          <div style="background:white; border:1px solid var(--border-color); border-radius:var(--radius-lg); padding:24px; box-shadow:var(--shadow-sm);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:var(--primary-light); color:var(--primary); font-size:0.8rem; font-weight:700; padding:4px 12px; border-radius:var(--radius-full);">${a.category}</span>
              <span style="font-size:0.8rem; color:var(--text-muted);">${a.readTime}</span>
            </div>
            <h3 style="font-family:var(--font-heading); font-size:1.25rem; color:var(--indigo-dark); margin-bottom:12px;">${a.title}</h3>
            <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom:14px;">${a.summary}</p>
            <div style="background:#F8FAFC; padding:16px; border-radius:var(--radius-md); font-size:0.9rem; line-height:1.7;">
              ${renderSafeMarkdown(a.content)}
            </div>
          </div>
        `).join("");
      }

      if (data.quizzes && data.quizzes.gad7) {
        state.quizState.quizData = data.quizzes.gad7;
      }
    } catch (e) {}
  }
  loadKnowledge();

  // Quiz Logic
  const quizIntroView = document.getElementById("quiz-intro-view");
  const quizStepView = document.getElementById("quiz-step-view");
  const quizResultView = document.getElementById("quiz-result-view");
  const btnStartQuiz = document.getElementById("btn-start-quiz");
  const quizStepIndicator = document.getElementById("quiz-step-indicator");
  const quizProgressFill = document.getElementById("quiz-progress-fill");
  const quizProgressPercent = document.getElementById("quiz-progress-percent");
  const quizQuestionText = document.getElementById("quiz-question-text");
  const quizOptionsList = document.getElementById("quiz-options-list");

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
        <span>${opt.label}</span>
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

    let bracket = qData.brackets[0];
    for (const b of qData.brackets) {
      if (totalScore >= b.range[0] && totalScore <= b.range[1]) {
        bracket = b;
        break;
      }
    }

    const badge = document.getElementById("quiz-score-badge");
    badge.textContent = `Tổng Điểm: ${totalScore} / 21`;
    badge.style.backgroundColor = bracket.color;

    document.getElementById("quiz-level-text").textContent = bracket.level;
    document.getElementById("quiz-level-text").style.color = bracket.color;
    document.getElementById("quiz-advice-text").innerHTML = `
      <strong>Lời khuyên & Định hướng:</strong><br>${bracket.advice}
    `;

    document.getElementById("btn-discuss-result").onclick = () => {
      const prompt = `Mình vừa làm bài trắc nghiệm lo âu GAD-7 và đạt ${totalScore}/21 điểm (${bracket.level}). An Nhiên có thể tư vấn và hướng dẫn mình cách cải thiện tâm trạng lúc này không?`;
      activateTab("tab-chat");
      sendMessage(prompt);
    };

    document.getElementById("btn-retake-quiz").onclick = () => {
      quizResultView.style.display = "none";
      quizIntroView.style.display = "block";
    };
  }

  // Relaxation Breathing
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
    btnToggleBreathe.textContent = "Bắt Đầu";
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
  // 6. AUTO-IDLE & PRIVACY SLEEP MODE (1 HOUR TIMEOUT ON DESKTOP & MOBILE)
  // =========================================================================
  const IDLE_TIMEOUT_MS = 60 * 60 * 1000; // 60 phút (1 giờ)
  let lastActiveTimestamp = Date.now();
  let isSleeping = false;
  const sleepOverlay = document.getElementById("sleep-overlay");
  const btnWakeUp = document.getElementById("btn-wake-up");

  function recordActivity() {
    if (!isSleeping) {
      lastActiveTimestamp = Date.now();
    }
  }

  // Lắng nghe mọi tương tác trên Desktop lẫn Mobile (chạm màn hình, vuốt, gõ bàn phím)
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
    // Reset cuộc trò chuyện mới để tiết kiệm token tối đa
    state.messages = [
      {
        role: "model",
        content: "Chào bạn, mình là **An Nhiên Tâm Lý**. Phiên trò chuyện mới đã sẵn sàng. Bạn đang cảm thấy thế nào rồi?"
      }
    ];
    renderMessages();
    activateTab("tab-chat");
  }

  if (btnWakeUp) {
    btnWakeUp.addEventListener("click", wakeUp);
  }

  // Định kỳ kiểm tra sau mỗi 15 giây
  setInterval(() => {
    if (!isSleeping && (Date.now() - lastActiveTimestamp >= IDLE_TIMEOUT_MS)) {
      putToSleep();
    }
  }, 15000);

  // Khi mở lại điện thoại hoặc quay lại tab trình duyệt sau hơn 1 giờ
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && !isSleeping) {
      if (Date.now() - lastActiveTimestamp >= IDLE_TIMEOUT_MS) {
        putToSleep();
      }
    }
  });

});
