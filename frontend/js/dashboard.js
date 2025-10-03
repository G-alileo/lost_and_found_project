(function () {
  async function load() {
    try {
      const me = await window.api.users.me();
    } catch {
      alert("Please login first");
      location.href = "./login.html";
      return;
    }

    // Load my reports (reuse reports list filtered client-side for now)
    const all = await window.api.reports.list({});
    const myContainer = document.getElementById("myReports");
    myContainer.innerHTML = (all.results || [])
      .map(
        (r) => `
      <div class="border rounded p-3">
        <div class="text-xs text-gray-500">${
          r.report_type?.toUpperCase() || ""
        }</div>
        <div class="font-semibold">${r.title}</div>
      </div>
    `
      )
      .join("");

    // Load notifications
    const notifs = await window.api.notifications.list();
    const unread = (notifs || []).filter((n) => !n.is_read).length;
    document.getElementById("unreadCount").textContent = unread;
    const notifContainer = document.getElementById("notifications");
    notifContainer.innerHTML = (notifs || [])
      .slice(0, 8)
      .map(
        (n) => `
      <div class="border rounded p-3 ${n.is_read ? "" : "bg-yellow-50"}">
        <div class="text-sm">${n.message}</div>
        <button data-id="${
          n.id
        }" class="mt-2 text-xs text-blue-600 underline markRead">Mark read</button>
      </div>
    `
      )
      .join("");

    notifContainer.addEventListener("click", async (e) => {
      const btn = e.target.closest(".markRead");
      if (!btn) return;
      const id = btn.getAttribute("data-id");
      await window.api.notifications.markRead(id);
      load();
    });

    // Load matches
    const matches = await window.api.matches.list({});
    const matchesContainer = document.getElementById("matches");
    matchesContainer.innerHTML = (matches.results || matches || [])
      .map(
        (m) => `
      <div class="border rounded p-3">
        <div class="text-sm">Confidence: ${(m.confidence_score * 100).toFixed(
          0
        )}%</div>
        <div class="text-xs text-gray-600">Status: ${m.status}</div>
      </div>
    `
      )
      .join("");
  }

  load();
})();
