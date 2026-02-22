// webui/pages/settings.js

export function settingsPage(content) {

  content.innerHTML = `
    <div class="card">
      <h2>Settings</h2>

      <div style="display:flex;flex-direction:column;gap:12px;margin-top:12px;">

        <label style="display:flex;align-items:center;gap:8px;">
          <input type="checkbox" id="darkToggle" />
          Dark Mode
        </label>

        <label style="display:flex;align-items:center;gap:8px;">
          <input type="checkbox" id="compactToggle" />
          Compact Mode
        </label>

        <div class="msg dim"></div>

      </div>
    </div>
  `;

  const msg = content.querySelector(".msg");

  /* ===============================
     Load Preferences
  =============================== */

  const prefs = JSON.parse(localStorage.getItem("sf_preferences") || "{}");

  const darkToggle = content.querySelector("#darkToggle");
  const compactToggle = content.querySelector("#compactToggle");

  if (prefs.dark_mode) {
    darkToggle.checked = true;
    document.body.classList.add("dark-mode");
  }

  if (prefs.compact_mode) {
    compactToggle.checked = true;
    document.body.classList.add("compact-mode");
  }

  /* ===============================
     Save Preferences
  =============================== */

  function savePrefs(updated) {
    const merged = { ...prefs, ...updated };
    localStorage.setItem("sf_preferences", JSON.stringify(merged));
  }

  /* ===============================
     Toggle Handlers
  =============================== */

  darkToggle.addEventListener("change", () => {

    const enabled = darkToggle.checked;

    document.body.classList.toggle("dark-mode", enabled);

    savePrefs({ dark_mode: enabled });

    msg.textContent = enabled
      ? "Dark mode enabled"
      : "Dark mode disabled";
  });

  compactToggle.addEventListener("change", () => {

    const enabled = compactToggle.checked;

    document.body.classList.toggle("compact-mode", enabled);

    savePrefs({ compact_mode: enabled });

    msg.textContent = enabled
      ? "Compact mode enabled"
      : "Compact mode disabled";
  });
}