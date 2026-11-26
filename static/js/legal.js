(() => {
  const storageKey = "an_nhien_theme_mode";
  const storageSalt = "AnNhien_Secured_v2_9988_Salt";
  const requestedTheme = new URLSearchParams(window.location.search).get("theme");

  function getSavedTheme() {
    try {
      const saved = localStorage.getItem(storageKey);
      if (!saved) return "light";
      if (saved === "dark" || saved === "light") return saved;
      if (!saved.startsWith("AN_ENC:")) return "light";

      const encoded = window.atob(saved.slice(7));
      let decoded = "";
      for (let i = 0; i < encoded.length; i++) {
        decoded += String.fromCharCode(
          encoded.charCodeAt(i) ^ storageSalt.charCodeAt(i % storageSalt.length)
        );
      }
      return JSON.parse(decoded) === "dark" ? "dark" : "light";
    } catch {
      return "light";
    }
  }

  const theme = requestedTheme === "dark" || requestedTheme === "light"
    ? requestedTheme
    : getSavedTheme();
  document.documentElement.dataset.theme = theme;

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('a[href^="/static/privacy-policy.html"], a[href^="/static/terms-of-use.html"]')
      .forEach((link) => {
        const url = new URL(link.href, window.location.href);
        url.searchParams.set("theme", theme);
        link.href = `${url.pathname}${url.search}${url.hash}`;
      });
  });
})();
