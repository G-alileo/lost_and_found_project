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
      const data = await api.chat.getUnreadCount();
      const count = data.unread_count || 0;
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

      const response = await api.chat.getConversations();
      console.log('Loaded conversations:', response);
      console.log('Current user ID:', window.currentUserId);

      // Handle paginated response (results array) or plain array
      const conversations = response.results || response;

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

      // Update conversation count (use total count from pagination or array length)
      const countBadge = document.getElementById('conversationCount');
      if (countBadge) {
        countBadge.textContent = response.count || conversations.length;
      }

      container.innerHTML = conversations.map(conv => {
        try {
          // Safely get other user
          const otherUser = conv.lost_user?.id === window.currentUserId ? conv.found_user : conv.lost_user;
          if (!otherUser) {
            console.error('Could not determine other user for conversation:', conv);
            return '';
          }

          const lastMessageTime = conv.last_message ? formatTime(conv.last_message.created_at) : '';
          const unreadBadge = conv.unread_count > 0 ? 
            `<span class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">${conv.unread_count}</span>` : '';

          // Get the primary report (for single-item conversations)
          const report = conv.lost_report || conv.found_report;
          if (!report) {
            console.error('Conversation has no reports:', conv);
            return '';
          }
          
          const reportType = report.report_type;
          const reportIcon = reportType === 'lost' ? '🔍 Lost' : '✅ Found';
          const reportColor = reportType === 'lost' ? 'text-red-600' : 'text-green-600';

          return `
          <div class="conversation-item p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg hover:border-primary transition-all duration-200 cursor-pointer" 
               data-conversation-id="${conv.id}">
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                ${otherUser.profile_picture ? 
                  `<img src="${otherUser.profile_picture}" alt="${otherUser.username}" class="w-12 h-12 rounded-full object-cover border-2 border-gray-200 dark:border-gray-600">` :
                  `<div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                    <span class="text-white font-semibold text-lg">${otherUser.username.charAt(0).toUpperCase()}</span>
                  </div>`
                }
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <h4 class="text-sm font-semibold text-gray-900 dark:text-white truncate">${otherUser.username}</h4>
                  ${unreadBadge}
                </div>
                <p class="text-xs ${reportColor} dark:${reportColor} font-medium mb-2 flex items-center">
                  <span class="mr-1">${reportIcon}:</span>
                  <span class="truncate">${report.title}</span>
                </p>
                ${conv.last_message ? `
                  <p class="text-sm text-gray-600 dark:text-gray-400 truncate">
                    ${conv.last_message.content}
                  </p>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">${lastMessageTime}</p>
                ` : `<p class="text-xs text-gray-400 italic">No messages yet</p>`}
              </div>
            </div>
          </div>
        `;
        } catch (err) {
          console.error('Error rendering conversation:', conv, err);
          return '';
        }
      }).filter(html => html).join(''); // Remove empty strings

      // Add click handlers
      document.querySelectorAll('.conversation-item').forEach(item => {
        item.addEventListener('click', () => {
          const conversationId = item.dataset.conversationId;
          openConversation(conversationId);
        });
      });

    } catch (error) {
      console.error('Error loading conversations:', error);
      console.error('Error details:', error.response || error.message);
      container.innerHTML = `
        <div class="text-center py-12">
          <p class="text-red-500 mb-2">Failed to load conversations.</p>
          <button onclick="window.chatApp.loadConversations()" class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover">
            Try Again
          </button>
        </div>
      `;
    }
  }

  // Open a conversation
  async function openConversation(conversationId) {
    currentConversation = conversationId;
    // Store globally for message form access
    window.currentConversationId = conversationId;
    
    // Show chat window
    const chatWindow = document.getElementById('chatWindow');
    const conversationsList = document.getElementById('conversationsListContainer');
    
    if (chatWindow) {
      chatWindow.classList.remove('hidden');
      
      // Only hide conversations list on mobile
      if (conversationsList && window.innerWidth < 768) {
        conversationsList.classList.add('hidden');
      }
      
      // Highlight active conversation
      document.querySelectorAll('.conversation-item').forEach(item => {
        if (item.dataset.conversationId === conversationId) {
          item.classList.add('bg-blue-50', 'dark:bg-gray-700', 'border-primary');
        } else {
          item.classList.remove('bg-blue-50', 'dark:bg-gray-700', 'border-primary');
        }
      });
      
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
      
      // Get the primary report
      const report = conversation.lost_report || conversation.found_report;
      const reportType = report.report_type;
      const reportIcon = reportType === 'lost' ? '🔍' : '✅';
      const reportLabel = reportType === 'lost' ? 'Lost Item' : 'Found Item';
      
      const headerContainer = document.getElementById('chatHeader');
      if (headerContainer) {
        headerContainer.innerHTML = `
          <div class="flex items-center justify-between w-full">
            <div class="flex items-center space-x-3">
              <button id="backToChatList" class="md:hidden p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
                <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
              </button>
              ${otherUser.profile_picture ? 
                `<img src="${otherUser.profile_picture}" alt="${otherUser.username}" class="w-12 h-12 rounded-full object-cover border-2 border-primary">` :
                `<div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
                  <span class="text-white font-semibold text-lg">${otherUser.username.charAt(0).toUpperCase()}</span>
                </div>`
              }
              <div>
                <h3 class="font-bold text-gray-900 dark:text-white text-lg">${otherUser.username}</h3>
                <p class="text-xs text-gray-600 dark:text-gray-400 flex items-center mt-0.5">
                  <span class="mr-1">${reportIcon}</span>
                  <span class="font-medium">${reportLabel}:</span>
                  <span class="ml-1 truncate max-w-xs">${report.title}</span>
                </p>
              </div>
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
          <div class="flex ${isOwnMessage ? 'justify-end' : 'justify-start'} mb-4 animate-fadeIn">
            <div class="max-w-xs lg:max-w-md xl:max-w-lg">
              ${!isOwnMessage ? `
                <div class="flex items-center space-x-2 mb-2">
                  ${msg.sender.profile_picture ? 
                    `<img src="${msg.sender.profile_picture}" alt="${msg.sender.username}" class="w-8 h-8 rounded-full object-cover border-2 border-gray-200 dark:border-gray-600">` :
                    `<div class="w-8 h-8 rounded-full bg-gradient-to-br from-gray-400 to-gray-500 flex items-center justify-center shadow-md">
                      <span class="text-white font-semibold text-sm">${msg.sender.username.charAt(0).toUpperCase()}</span>
                    </div>`
                  }
                  <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">${msg.sender.username}</span>
                </div>
              ` : ''}
              <div class="${isOwnMessage ? 
                'bg-gradient-to-br from-primary to-accent text-white shadow-md' : 
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-600 shadow-sm'} 
                rounded-2xl ${isOwnMessage ? 'rounded-tr-sm' : 'rounded-tl-sm'} px-5 py-3">
                <p class="text-sm leading-relaxed break-words">${escapeHtml(msg.content)}</p>
              </div>
              <div class="flex items-center ${isOwnMessage ? 'justify-end' : 'justify-start'} mt-1 px-1">
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  ${formatTime(msg.created_at)}
                </p>
              </div>
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
    window.currentConversationId = null;
    
    const chatWindow = document.getElementById('chatWindow');
    const conversationsList = document.getElementById('conversationsListContainer');
    
    if (chatWindow) chatWindow.classList.add('hidden');
    
    // On mobile: show conversations list again
    if (window.innerWidth < 768 && conversationsList) {
      conversationsList.classList.remove('hidden');
    }
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
