(function () {
  let currentConversation = null;
  let messagePollingInterval = null;
  let unreadCountInterval = null;

  // Initialize chat functionality
  async function initChat() {
    await updateUnreadBadge();
    startUnreadCountPolling();
  }

  // Update unread message badge
  async function updateUnreadBadge() {
    try {
      const count = await api.chat.getUnreadCount();
      const badges = document.querySelectorAll('.chat-unread-badge');
      
      badges.forEach(badge => {
        if (count > 0) {
          badge.textContent = count > 99 ? '99+' : count;
          badge.classList.remove('hidden');
        } else {
          badge.classList.add('hidden');
        }
      });
    } catch (error) {
      console.error('Error updating unread badge:', error);
    }
  }

  // Start polling for unread count
  function startUnreadCountPolling() {
    if (unreadCountInterval) clearInterval(unreadCountInterval);
    unreadCountInterval = setInterval(updateUnreadBadge, 5000); // Every 5 seconds
  }

  // Stop polling for unread count
  function stopUnreadCountPolling() {
    if (unreadCountInterval) {
      clearInterval(unreadCountInterval);
      unreadCountInterval = null;
    }
  }

  // Load conversations list
  async function loadConversations() {
    const container = document.getElementById('conversationsList');
    if (!container) return;

    try {
      container.innerHTML = `
        <div class="flex items-center justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      `;

      const conversations = await api.chat.getConversations();

      if (conversations.length === 0) {
        container.innerHTML = `
          <div class="text-center py-12">
            <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">No conversations yet</h3>
            <p class="text-gray-600 dark:text-gray-400">Start a conversation from the Browse page or when you find a match</p>
          </div>
        `;
        return;
      }

      container.innerHTML = conversations.map(conv => {
        const otherUser = conv.lost_user.id === window.currentUserId ? conv.found_user : conv.lost_user;
        const lastMessageTime = conv.last_message ? formatTime(conv.last_message.created_at) : '';
        const unreadBadge = conv.unread_count > 0 ? 
          `<span class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">${conv.unread_count}</span>` : '';

        return `
          <div class="conversation-item p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-200 cursor-pointer" 
               data-conversation-id="${conv.id}">
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0">
                ${otherUser.profile_picture ? 
                  `<img src="${otherUser.profile_picture}" alt="${otherUser.username}" class="w-12 h-12 rounded-full">` :
                  `<div class="w-12 h-12 rounded-full bg-primary flex items-center justify-center">
                    <span class="text-white font-semibold text-lg">${otherUser.username.charAt(0).toUpperCase()}</span>
                  </div>`
                }
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <h4 class="text-sm font-semibold text-gray-900 dark:text-white truncate">${otherUser.username}</h4>
                  ${unreadBadge}
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
                  <span class="font-medium ${conv.lost_report.report_type === 'lost' ? 'text-red-500' : 'text-green-500'}">
                    ${conv.lost_report.report_type === 'lost' ? '🔍' : '✅'} ${conv.lost_report.title}
                  </span>
                  ↔
                  <span class="font-medium ${conv.found_report.report_type === 'found' ? 'text-green-500' : 'text-red-500'}">
                    ${conv.found_report.report_type === 'found' ? '✅' : '🔍'} ${conv.found_report.title}
                  </span>
                </p>
                ${conv.last_message ? `
                  <p class="text-sm text-gray-600 dark:text-gray-400 truncate">
                    <span class="font-medium">${conv.last_message.sender}:</span> ${conv.last_message.content}
                  </p>
                  <p class="text-xs text-gray-400 mt-1">${lastMessageTime}</p>
                ` : ''}
              </div>
            </div>
          </div>
        `;
      }).join('');

      // Add click handlers
      document.querySelectorAll('.conversation-item').forEach(item => {
        item.addEventListener('click', () => {
          const conversationId = item.dataset.conversationId;
          openConversation(conversationId);
        });
      });

    } catch (error) {
      console.error('Error loading conversations:', error);
      container.innerHTML = `
        <div class="text-center py-12">
          <p class="text-red-500">Failed to load conversations. Please try again.</p>
        </div>
      `;
    }
  }

  // Open a conversation
  async function openConversation(conversationId) {
    currentConversation = conversationId;
    
    // Show chat window
    const chatWindow = document.getElementById('chatWindow');
    const conversationsList = document.getElementById('conversationsListContainer');
    
    if (chatWindow) {
      chatWindow.classList.remove('hidden');
      if (conversationsList) conversationsList.classList.add('hidden');
      
      await loadConversationDetails(conversationId);
      await loadMessages(conversationId);
      startMessagePolling(conversationId);
      
      // Focus message input
      const messageInput = document.getElementById('messageInput');
      if (messageInput) messageInput.focus();
    }
  }

  // Load conversation details
  async function loadConversationDetails(conversationId) {
    try {
      const conversation = await api.chat.getConversation(conversationId);
      const otherUser = conversation.lost_user.id === window.currentUserId ? 
        conversation.found_user : conversation.lost_user;
      
      const headerContainer = document.getElementById('chatHeader');
      if (headerContainer) {
        headerContainer.innerHTML = `
          <div class="flex items-center space-x-3">
            <button id="backToChatList" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            ${otherUser.profile_picture ? 
              `<img src="${otherUser.profile_picture}" alt="${otherUser.username}" class="w-10 h-10 rounded-full">` :
              `<div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
                <span class="text-white font-semibold">${otherUser.username.charAt(0).toUpperCase()}</span>
              </div>`
            }
            <div>
              <h3 class="font-semibold text-gray-900 dark:text-white">${otherUser.username}</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                ${conversation.lost_report.title} ↔ ${conversation.found_report.title}
              </p>
            </div>
          </div>
        `;
        
        // Add back button handler
        document.getElementById('backToChatList')?.addEventListener('click', closeConversation);
      }
    } catch (error) {
      console.error('Error loading conversation details:', error);
    }
  }

  // Load messages
  async function loadMessages(conversationId) {
    const container = document.getElementById('messagesContainer');
    if (!container) return;

    try {
      const messages = await api.chat.getMessages(conversationId);
      
      if (messages.length === 0) {
        container.innerHTML = `
          <div class="text-center py-8">
            <p class="text-gray-500 dark:text-gray-400">No messages yet. Start the conversation!</p>
          </div>
        `;
        return;
      }

      container.innerHTML = messages.map(msg => {
        const isOwnMessage = msg.sender.id === window.currentUserId;
        return `
          <div class="flex ${isOwnMessage ? 'justify-end' : 'justify-start'} mb-4">
            <div class="max-w-xs lg:max-w-md">
              ${!isOwnMessage ? `
                <div class="flex items-center space-x-2 mb-1">
                  ${msg.sender.profile_picture ? 
                    `<img src="${msg.sender.profile_picture}" alt="${msg.sender.username}" class="w-6 h-6 rounded-full">` :
                    `<div class="w-6 h-6 rounded-full bg-gray-400 flex items-center justify-center">
                      <span class="text-white text-xs">${msg.sender.username.charAt(0).toUpperCase()}</span>
                    </div>`
                  }
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-400">${msg.sender.username}</span>
                </div>
              ` : ''}
              <div class="${isOwnMessage ? 
                'bg-primary text-white' : 
                'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'} 
                rounded-lg px-4 py-2">
                <p class="text-sm break-words">${escapeHtml(msg.content)}</p>
              </div>
              <p class="text-xs text-gray-400 mt-1 ${isOwnMessage ? 'text-right' : ''}">
                ${formatTime(msg.created_at)}
              </p>
            </div>
          </div>
        `;
      }).join('');

      // Scroll to bottom
      container.scrollTop = container.scrollHeight;
      
      // Update unread badge
      await updateUnreadBadge();
      
    } catch (error) {
      console.error('Error loading messages:', error);
      container.innerHTML = `
        <div class="text-center py-8">
          <p class="text-red-500">Failed to load messages. Please try again.</p>
        </div>
      `;
    }
  }

  // Send message
  async function sendMessage(conversationId, content) {
    if (!content.trim()) return;

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessageBtn');
    
    try {
      if (messageInput) messageInput.disabled = true;
      if (sendButton) sendButton.disabled = true;

      await api.chat.sendMessage(conversationId, content.trim());
      
      if (messageInput) messageInput.value = '';
      await loadMessages(conversationId);
      
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      if (messageInput) messageInput.disabled = false;
      if (sendButton) sendButton.disabled = false;
      if (messageInput) messageInput.focus();
    }
  }

  // Start polling for new messages
  function startMessagePolling(conversationId) {
    stopMessagePolling();
    messagePollingInterval = setInterval(() => {
      if (currentConversation === conversationId) {
        loadMessages(conversationId);
      }
    }, 3000); // Poll every 3 seconds
  }

  // Stop polling for messages
  function stopMessagePolling() {
    if (messagePollingInterval) {
      clearInterval(messagePollingInterval);
      messagePollingInterval = null;
    }
  }

  // Close conversation
  function closeConversation() {
    stopMessagePolling();
    currentConversation = null;
    
    const chatWindow = document.getElementById('chatWindow');
    const conversationsList = document.getElementById('conversationsListContainer');
    
    if (chatWindow) chatWindow.classList.add('hidden');
    if (conversationsList) conversationsList.classList.remove('hidden');
  }

  // Create conversation from reports
  async function createConversation(lostReportId, foundReportId) {
    try {
      const conversation = await api.chat.createConversation(lostReportId, foundReportId);
      // Redirect to messages page with conversation opened
      window.location.href = `./messages.html?conversation=${conversation.id}`;
    } catch (error) {
      console.error('Error creating conversation:', error);
      alert('Failed to start conversation. Please try again.');
    }
  }

  // Create conversation from a single report (simple flow)
  async function createConversationFromReport(reportId) {
    try {
      const conversation = await api.chat.createConversationFromReport(reportId);
      // Redirect to messages page with conversation opened
      window.location.href = `./messages.html?conversation=${conversation.id}`;
    } catch (error) {
      console.error('Error creating conversation:', error);
      const errorMsg = error.response?.data?.non_field_errors?.[0] || 
                       error.response?.data?.detail || 
                       'Failed to start conversation. Please try again.';
      alert(errorMsg);
    }
  }

  // Utility functions
  function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    if (diff < 604800000) return `${Math.floor(diff / 86400000)}d ago`;
    
    return date.toLocaleDateString();
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Expose public API
  window.chatApp = {
    initChat,
    loadConversations,
    openConversation,
    closeConversation,
    sendMessage,
    createConversation,
    createConversationFromReport,
    updateUnreadBadge,
    startUnreadCountPolling,
    stopUnreadCountPolling,
  };

  // Initialize on page load if user is logged in
  document.addEventListener('DOMContentLoaded', () => {
    const tokens = JSON.parse(localStorage.getItem('tokens') || '{}');
    if (tokens.access) {
      initChat();
    }
  });

  // Cleanup on page unload
  window.addEventListener('beforeunload', () => {
    stopMessagePolling();
    stopUnreadCountPolling();
  });
})();
