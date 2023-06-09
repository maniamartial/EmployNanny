  window.addEventListener('DOMContentLoaded', function() {
    var loadingOverlay = document.querySelector('.loading-overlay');
    loadingOverlay.style.display = 'flex';

    window.addEventListener('load', function() {
      loadingOverlay.style.display = 'none';
    });
  });