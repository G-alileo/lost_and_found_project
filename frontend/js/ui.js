// UI utilities for CampusFound
// Header and footer injection disabled - using inline HTML instead

(function () {
  // Utility functions for UI components can be added here
  
  // Example: Show notification function
  window.showNotification = function(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification-popup ${type === 'error' ? 'bg-red-500' : type === 'success' ? 'bg-green-500' : 'bg-blue-500'} text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.remove();
    }, 3000);
  };
  
  // Example: Loading state helper
  window.setLoadingState = function(element, loading) {
    if (loading) {
      element.disabled = true;
      element.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
      element.disabled = false;
      element.classList.remove('opacity-50', 'cursor-not-allowed');
    }
  };
})();
