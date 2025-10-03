// User dropdown functionality
function initializeUserDropdown() {
  const userMenuButton = document.getElementById('userMenuButton');
  const userDropdown = document.getElementById('userDropdown');
  const dropdownArrow = document.getElementById('dropdownArrow');

  if (!userMenuButton || !userDropdown || !dropdownArrow) {
    return; // Elements not found, skip initialization
  }

  userMenuButton.addEventListener('click', function(e) {
    e.stopPropagation();
    const isOpen = !userDropdown.classList.contains('hidden');
    
    if (isOpen) {
      closeDropdown();
    } else {
      openDropdown();
    }
  });

  function openDropdown() {
    userDropdown.classList.remove('hidden');
    dropdownArrow.style.transform = 'rotate(180deg)';
  }

  function closeDropdown() {
    userDropdown.classList.add('hidden');
    dropdownArrow.style.transform = 'rotate(0deg)';
  }

  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!userMenuButton.contains(e.target) && !userDropdown.contains(e.target)) {
      closeDropdown();
    }
  });

  // Logout functionality
  document.getElementById('logoutBtn')?.addEventListener('click', async function() {
    try {
      await window.api.auth.logout();
      window.showNotification('Logged out successfully', 'success');
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    } catch (error) {
      console.error('Logout failed:', error);
      window.showNotification('Logout failed. Please try again.', 'error');
    }
  });

  // Edit Profile functionality
  document.getElementById('editProfileBtn')?.addEventListener('click', function() {
    openEditProfileModal();
  });

  // Change Password functionality
  document.getElementById('changePasswordBtn')?.addEventListener('click', function() {
    openChangePasswordModal();
  });
}

// Profile editing modal functions
function openEditProfileModal() {
  // Create modal HTML
  const modalHTML = `
    <div id="editProfileModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Edit Profile</h3>
          <button id="closeEditModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form id="editProfileForm" class="space-y-4">
          <div>
            <label class="form-label">Username</label>
            <input id="editUsername" type="text" class="input-field w-full" required>
          </div>
          
          <div>
            <label class="form-label">Email</label>
            <input id="editEmail" type="email" class="input-field w-full" required>
          </div>
          
          <div>
            <label class="form-label">Bio</label>
            <textarea id="editBio" class="input-field w-full resize-none" rows="3" placeholder="Tell us about yourself..."></textarea>
          </div>
          
          <div>
            <label class="form-label">Profile Picture</label>
            <input id="editAvatar" type="file" accept="image/*" class="input-field w-full">
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" id="cancelEdit" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // Populate current user data
  const currentUser = window.currentUser;
  if (currentUser) {
    document.getElementById('editUsername').value = currentUser.username || '';
    document.getElementById('editEmail').value = currentUser.email || '';
    document.getElementById('editBio').value = currentUser.bio || '';
  }
  
  // Add event listeners
  document.getElementById('closeEditModal').addEventListener('click', closeEditProfileModal);
  document.getElementById('cancelEdit').addEventListener('click', closeEditProfileModal);
  document.getElementById('editProfileForm').addEventListener('submit', handleProfileUpdate);
}

function closeEditProfileModal() {
  const modal = document.getElementById('editProfileModal');
  if (modal) {
    modal.remove();
  }
}

async function handleProfileUpdate(e) {
  e.preventDefault();
  
  const formData = new FormData();
  formData.append('username', document.getElementById('editUsername').value);
  formData.append('email', document.getElementById('editEmail').value);
  formData.append('bio', document.getElementById('editBio').value);
  
  const avatarFile = document.getElementById('editAvatar').files[0];
  if (avatarFile) {
    formData.append('avatar', avatarFile);
  }
  
  try {
    const updatedUser = await window.api.users.updateProfile(formData);
    window.currentUser = updatedUser;
    
    // Update UI across all pages
    if (typeof showUserMenu === 'function') {
      showUserMenu(updatedUser);
    }
    
    closeEditProfileModal();
    window.showNotification('Profile updated successfully!', 'success');
  } catch (error) {
    console.error('Profile update failed:', error);
    window.showNotification('Failed to update profile. Please try again.', 'error');
  }
}

function openChangePasswordModal() {
  const modalHTML = `
    <div id="changePasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Change Password</h3>
          <button id="closePasswordModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form id="changePasswordForm" class="space-y-4">
          <div>
            <label class="form-label">Current Password</label>
            <input id="currentPassword" type="password" class="input-field w-full" required>
          </div>
          
          <div>
            <label class="form-label">New Password</label>
            <input id="newPassword" type="password" class="input-field w-full" required>
          </div>
          
          <div>
            <label class="form-label">Confirm New Password</label>
            <input id="confirmPassword" type="password" class="input-field w-full" required>
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" id="cancelPassword" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Change Password</button>
          </div>
        </form>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // Add event listeners
  document.getElementById('closePasswordModal').addEventListener('click', closeChangePasswordModal);
  document.getElementById('cancelPassword').addEventListener('click', closeChangePasswordModal);
  document.getElementById('changePasswordForm').addEventListener('submit', handlePasswordChange);
}

function closeChangePasswordModal() {
  const modal = document.getElementById('changePasswordModal');
  if (modal) {
    modal.remove();
  }
}

async function handlePasswordChange(e) {
  e.preventDefault();
  
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  
  if (newPassword !== confirmPassword) {
    window.showNotification('New passwords do not match', 'error');
    return;
  }
  
  try {
    await window.api.users.changePassword({
      current_password: currentPassword,
      new_password: newPassword
    });
    
    closeChangePasswordModal();
    window.showNotification('Password changed successfully!', 'success');
  } catch (error) {
    console.error('Password change failed:', error);
    window.showNotification('Failed to change password. Please check your current password.', 'error');
  }
}

// Initialize dropdown when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeUserDropdown);
