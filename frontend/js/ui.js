(function () {
  function header() {
    return `
    <header class="bg-white shadow">
      <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <a href="./index.html" class="text-xl font-semibold">Lost & Found</a>
        <nav class="flex gap-4 text-sm">
          <a href="./index.html" class="hover:underline">Home</a>
          <a href="./browse.html" class="hover:underline">Browse</a>
          <a href="./report-lost.html" class="hover:underline">Report Lost</a>
          <a href="./report-found.html" class="hover:underline">Report Found</a>
          <a href="./user-dashboard.html" class="hover:underline">Dashboard</a>
          <a href="./admin-dashboard.html" class="hover:underline">Admin</a>
          <a href="./login.html" class="hover:underline">Login</a>
          <a href="./register.html" class="hover:underline">Register</a>
        </nav>
      </div>
    </header>`;
  }

  function footer() {
    return `<footer class="border-t py-6 text-center text-sm text-gray-500">© Campus Lost & Found</footer>`;
  }

  function inject() {
    const h = document.createElement("div");
    h.innerHTML = header();
    document.body.prepend(h.firstElementChild);
    const f = document.createElement("div");
    f.innerHTML = footer();
    document.body.appendChild(f.firstElementChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
