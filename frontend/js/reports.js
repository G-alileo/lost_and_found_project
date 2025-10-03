(function () {
  async function loadCategories(selectId) {
    const data = await window.api.categories.list();
    const select = document.getElementById(selectId);
    if (!select) return;
    select.innerHTML = data
      .map((c) => `<option value="${c.id}">${c.name}</option>`)
      .join("");
  }

  const fileInput = document.getElementById("image");
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      const preview = document.getElementById("preview");
      if (file) {
        preview.src = URL.createObjectURL(file);
        preview.classList.remove("hidden");
      }
    });
  }

  const reportForm = document.getElementById("reportForm");
  if (reportForm) {
    loadCategories("category");
    reportForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData();
      formData.append("title", document.getElementById("title").value.trim());
      formData.append(
        "description",
        document.getElementById("description").value.trim()
      );
      formData.append("category", document.getElementById("category").value);
      formData.append("report_type", window.reportType || "lost");
      formData.append("date_lost_found", document.getElementById("date").value);
      formData.append(
        "location",
        document.getElementById("location").value.trim()
      );
      const image = document.getElementById("image").files[0];
      if (image) formData.append("image", image);
      try {
        await window.api.reports.create(formData);
        alert("Report submitted successfully");
        location.href = "./user-dashboard.html";
      } catch (err) {
        alert("Failed to submit");
      }
    });
  }

  const applyFilters = document.getElementById("applyFilters");
  if (applyFilters) {
    loadCategories("filterCategory");
    applyFilters.addEventListener("click", async () => {
      const params = {
        type: document.getElementById("filterType").value,
        category: document.getElementById("filterCategory").value || undefined,
        q: document.getElementById("filterQ").value.trim() || undefined,
      };
      const data = await window.api.reports.list(params);
      const container = document.getElementById("list");
      container.innerHTML = (data.results || [])
        .map(
          (r) => `
        <div class="bg-white rounded shadow p-4">
          <div class="text-xs text-gray-500">${
            r.report_type?.toUpperCase() || ""
          }</div>
          <div class="font-semibold">${r.title}</div>
          <div class="text-sm text-gray-600">${r.location || ""}</div>
        </div>
      `
        )
        .join("");
    });
  }
})();
