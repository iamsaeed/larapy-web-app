/**
 * Application bootstrap and shared utilities
 */

// Global utilities can be added here
window.utils = {
  // Add any global utility functions here
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  formatDate(date) {
    return new Date(date).toLocaleDateString();
  }
};

// You can add other shared functionality here
console.log('Larapy application bootstrap loaded');