(function () {
  async function ensureAdmin() {
    try {
      await window.api.users.me();
    } catch {
      // Try pinging stats; if unauthorized, prompt admin login
      try {
        await window.api.admin.stats();
      } catch {
        alert("Please login as admin via session.");
      }
    }
  }

  async function loadStats() {
    const s = await window.api.admin.stats();
    document.getElementById("statLost").textContent = s.total_lost;
    document.getElementById("statFound").textContent = s.total_found;
    document.getElementById("statMatches").textContent = s.total_matches;
    document.getElementById("statUnclaimed").textContent = s.unclaimed_count;

    const barCtx = document.getElementById("barChart");
    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: ["Lost", "Found", "Matches"],
        datasets: [
          {
            label: "Counts",
            data: [s.total_lost, s.total_found, s.total_matches],
            backgroundColor: ["#3b82f6", "#10b981", "#f59e0b"],
          },
        ],
      },
    });
    const pieCtx = document.getElementById("pieChart");
    const catLabels = (s.top_categories || []).map((c) => c.name);
    const catData = (s.top_categories || []).map((c) => c.count);
    new Chart(pieCtx, {
      type: "pie",
      data: {
        labels: catLabels,
        datasets: [
          {
            data: catData,
            backgroundColor: [
              "#3b82f6",
              "#10b981",
              "#ef4444",
              "#8b5cf6",
              "#f59e0b",
            ],
          },
        ],
      },
    });
  }

  async function loadCategories() {
    const list = document.getElementById("categoryList");
    const data = await window.api.categories.list();
    list.innerHTML = data
      .map(
        (c) => `
      <li class="flex items-center justify-between border rounded px-3 py-2">
        <span>${c.name}</span>
        <div class="flex gap-2">
          <button data-id="${c.id}" class="text-blue-600 underline editCat">Edit</button>
          <button data-id="${c.id}" class="text-red-600 underline delCat">Delete</button>
        </div>
      </li>
    `
      )
      .join("");
    list.onclick = async (e) => {
      const del = e.target.closest(".delCat");
      const edit = e.target.closest(".editCat");
      if (del) {
        await window.api.categories.remove(del.getAttribute("data-id"));
        loadCategories();
      } else if (edit) {
        const id = edit.getAttribute("data-id");
        const name = prompt("New category name");
        if (name) {
          await window.api.categories.update(id, name);
          loadCategories();
        }
      }
    };
  }

  async function wireAddCategory() {
    const btn = document.getElementById("addCategoryBtn");
    btn.addEventListener("click", async () => {
      const name = document.getElementById("newCategoryName").value.trim();
      if (!name) return;
      await window.api.categories.create(name);
      document.getElementById("newCategoryName").value = "";
      loadCategories();
    });
  }

  ensureAdmin();
  loadStats();
  loadCategories();
  wireAddCategory();
})();
