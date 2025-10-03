(function () {
  const BASE_URL = "http://localhost:8000/api/";

  function getTokens() {
    try {
      return JSON.parse(localStorage.getItem("tokens") || "{}");
    } catch {
      return {};
    }
  }
  function setTokens(tokens) {
    localStorage.setItem("tokens", JSON.stringify(tokens || {}));
  }
  function clearTokens() {
    localStorage.removeItem("tokens");
  }

  // Default: do NOT send cookies. We'll opt-in for admin/session endpoints.
  const instance = axios.create({ baseURL: BASE_URL, withCredentials: false });

  instance.interceptors.request.use((config) => {
    const { access } = getTokens();
    if (access && !config.withCredentials) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }
    // CSRF for session-auth admin writes (assumes csrftoken cookie present)
    if (!config.headers["X-CSRFToken"]) {
      const csrftoken = document.cookie
        .split("; ")
        .find((r) => r.startsWith("csrftoken="))
        ?.split("=")[1];
      if (csrftoken) config.headers["X-CSRFToken"] = csrftoken;
    }
    return config;
  });

  let refreshing = false;
  let queue = [];
  instance.interceptors.response.use(
    (r) => r,
    async (error) => {
      const original = error.config;
      if (error.response && error.response.status === 401 && !original._retry) {
        original._retry = true;
        const { refresh } = getTokens();
        if (!refresh) {
          clearTokens();
          return Promise.reject(error);
        }
        if (refreshing) {
          return new Promise((resolve, reject) =>
            queue.push({ resolve, reject })
          );
        }
        refreshing = true;
        try {
          const res = await axios.post(BASE_URL + "auth/token/refresh/", {
            refresh,
          });
          const tokens = getTokens();
          tokens.access = res.data.access;
          setTokens(tokens);
          queue.forEach((p) => p.resolve());
          queue = [];
          return instance(original);
        } catch (e) {
          queue.forEach((p) => p.reject(e));
          queue = [];
          clearTokens();
          return Promise.reject(e);
        } finally {
          refreshing = false;
        }
      }
      return Promise.reject(error);
    }
  );

  async function login(username, password) {
    const { data } = await instance.post("auth/token/", { username, password });
    setTokens({ access: data.access, refresh: data.refresh });
    return data;
  }

  async function register(payload) {
    const { data } = await instance.post("auth/register/", payload);
    return data;
  }

  async function adminLogin(username, password) {
    const { data } = await instance.post(
      "auth/admin-login/",
      { username, password },
      { withCredentials: true }
    );
    return data;
  }

  window.api = {
    auth: { login, register, adminLogin },
    users: {
      async me() {
        const { data } = await instance.get("users/me/");
        return data;
      },
      async update(formData) {
        const { data } = await instance.put("users/me/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        return data;
      },
    },
    categories: {
      async list() {
        const { data } = await instance.get("categories/");
        return data;
      },
      async create(name) {
        const { data } = await instance.post(
          "categories/",
          { name },
          { withCredentials: true }
        );
        return data;
      },
      async update(id, name) {
        const { data } = await instance.put(
          `categories/${id}/`,
          { name },
          { withCredentials: true }
        );
        return data;
      },
      async remove(id) {
        const { data } = await instance.delete(`categories/${id}/`, {
          withCredentials: true,
        });
        return data;
      },
    },
    reports: {
      async list(params) {
        const { data } = await instance.get("reports/", { params });
        return data;
      },
      async get(id) {
        const { data } = await instance.get(`reports/${id}/`);
        return data;
      },
      async create(formData) {
        const { data } = await instance.post("reports/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        return data;
      },
      async update(id, formData) {
        const { data } = await instance.put(`reports/${id}/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        return data;
      },
      async remove(id) {
        const { data } = await instance.delete(`reports/${id}/`);
        return data;
      },
      async findMatches(id) {
        const { data } = await instance.post(`reports/${id}/find_matches/`);
        return data;
      },
    },
    matches: {
      async list(params) {
        const { data } = await instance.get("matches/", { params });
        return data;
      },
      async get(id) {
        const { data } = await instance.get(`matches/${id}/`);
        return data;
      },
      async confirm(id) {
        const { data } = await instance.post(
          `matches/${id}/confirm/`,
          {},
          { withCredentials: true }
        );
        return data;
      },
      async reject(id) {
        const { data } = await instance.post(
          `matches/${id}/reject/`,
          {},
          { withCredentials: true }
        );
        return data;
      },
    },
    notifications: {
      async list() {
        const { data } = await instance.get("notifications/");
        return data;
      },
      async markRead(id) {
        const { data } = await instance.post(`notifications/${id}/mark-read/`);
        return data;
      },
    },
    admin: {
      async stats() {
        const { data } = await instance.get("admin/stats/", {
          withCredentials: true,
        });
        return data;
      },
    },
  };
})();
