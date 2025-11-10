(function () {
  const BASE_URL = "http://localhost:8000/api/";

  function getTokens() {
    try {
      const tokens = JSON.parse(localStorage.getItem("tokens") || "{}");
      console.log('API: Getting tokens:', { access: !!tokens.access, refresh: !!tokens.refresh });
      return tokens;
    } catch {
      console.log('API: Error parsing tokens, returning empty object');
      return {};
    }
  }
  function setTokens(tokens) {
    console.log('API: Setting tokens:', { access: !!tokens?.access, refresh: !!tokens?.refresh });
    localStorage.setItem("tokens", JSON.stringify(tokens || {}));
  }
  function clearTokens() {
    console.log('API: Clearing tokens');
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
      console.log('API: Response interceptor - Status:', error.response?.status, 'URL:', original?.url);
      
      if (error.response && error.response.status === 401 && !original._retry) {
        original._retry = true;
        const { refresh } = getTokens();
        console.log('API: 401 error, attempting token refresh. Has refresh token:', !!refresh);
        
        if (!refresh) {
          console.log('API: No refresh token available, clearing tokens');
          clearTokens();
          return Promise.reject(error);
        }
        
        if (refreshing) {
          console.log('API: Already refreshing, queuing request');
          return new Promise((resolve, reject) =>
            queue.push({ resolve, reject })
          );
        }
        
        refreshing = true;
        try {
          console.log('API: Attempting token refresh');
          const res = await axios.post(BASE_URL + "auth/token/refresh/", {
            refresh,
          });
          console.log('API: Token refresh successful');
          
          const tokens = getTokens();
          tokens.access = res.data.access;
          setTokens(tokens);
          
          queue.forEach((p) => p.resolve());
          queue = [];
          
          console.log('API: Retrying original request with new token');
          return instance(original);
        } catch (e) {
          console.error('API: Token refresh failed:', e.response?.status, e.response?.data);
          queue.forEach((p) => p.reject(e));
          queue = [];
          
          // Only clear tokens if refresh actually failed (not network errors)
          if (e.response?.status === 401) {
            console.log('API: Refresh token invalid, clearing all tokens');
            clearTokens();
          }
          return Promise.reject(e);
        } finally {
          refreshing = false;
        }
      }
      return Promise.reject(error);
    }
  );

  async function login(username, password) {
    console.log('API: Attempting login for username:', username);
    const { data } = await instance.post("auth/token/", { username, password });
    console.log('API: Login successful, setting tokens');
    console.log('API: Tokens received:', { access: !!data.access, refresh: !!data.refresh });
    setTokens({ access: data.access, refresh: data.refresh });
    
    // Verify tokens were stored
    const storedTokens = getTokens();
    console.log('API: Tokens stored successfully:', { access: !!storedTokens.access, refresh: !!storedTokens.refresh });
    
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

  async function logout() {
    try {
      await instance.post("auth/logout/");
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      clearTokens();
    }
  }

  window.api = {
    auth: { login, register, adminLogin, logout },
    users: {
      async me() {
        console.log('API: Attempting to get user info');
        const { data } = await instance.get("users/me/");
        console.log('API: User info retrieved:', data);
        return data;
      },
      async update(formData) {
        const { data } = await instance.put("users/me/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        return data;
      },
      async updateProfile(formData) {
        const { data } = await instance.patch("users/me/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        return data;
      },
      async changePassword(payload) {
        const { data } = await instance.post("users/change-password/", payload);
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
    subcategories: {
      async list(params) {
        // params can include { category: id }
        const { data } = await instance.get("subcategories/", { params });
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
    dashboard: {
      async stats() {
        const { data } = await instance.get("dashboard/stats/");
        return data;
      },
      async reports() {
        const { data } = await instance.get("dashboard/reports/");
        return data;
      },
      async matches() {
        const { data } = await instance.get("dashboard/matches/");
        return data;
      },
      async notifications() {
        const { data } = await instance.get("dashboard/notifications/");
        return data;
      },
      async markNotificationRead(id) {
        const { data } = await instance.post(`dashboard/notifications/${id}/read/`);
        return data;
      },
      async confirmMatch(id) {
        const { data } = await instance.post(`dashboard/matches/${id}/confirm/`);
        return data;
      },
      async rejectMatch(id) {
        const { data } = await instance.post(`dashboard/matches/${id}/reject/`);
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
    chat: {
      async getConversations() {
        const { data } = await instance.get("chat/conversations/");
        return data;
      },
      async createConversation(lostReportId, foundReportId) {
        const { data } = await instance.post("chat/conversations/", {
          lost_report_id: lostReportId,
          found_report_id: foundReportId,
        });
        return data;
      },
      async createConversationFromReport(reportId) {
        const { data } = await instance.post("chat/conversations/", {
          report_id: reportId,
        });
        return data;
      },
      async getConversation(conversationId) {
        const { data } = await instance.get(`chat/conversations/${conversationId}/`);
        return data;
      },
      async getMessages(conversationId) {
        const { data } = await instance.get(`chat/conversations/${conversationId}/messages/`);
        return data;
      },
      async sendMessage(conversationId, content) {
        const { data } = await instance.post(
          `chat/conversations/${conversationId}/send_message/`,
          { content }
        );
        return data;
      },
      async getUnreadCount() {
        const { data } = await instance.get("chat/conversations/unread_count/");
        return data;
      },
      async markMessageRead(messageId) {
        const { data } = await instance.post(`chat/messages/${messageId}/mark_read/`);
        return data;
      },
    },
  };
})();
