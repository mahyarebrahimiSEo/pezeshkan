/**
 * Pezeshkan Medical Ecosystem & Magazine - 2026 Minimalist Circular Preloader
 * Apple / Linear Aesthetics - Pure PEZESHK-ON Wordmark & Smooth Circular Motion
 */

(function () {
  'use strict';

  function getPreloaderHTML(isMag) {
    var editorialBadgeHTML = isMag
      ? '<div class="pez-mag-editorial-badge" aria-hidden="true">' +
          '<svg class="pez-mag-editorial-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>' +
            '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>' +
            '<line x1="9" y1="7" x2="15" y2="7"></line>' +
            '<line x1="9" y1="11" x2="13" y2="11"></line>' +
            '<path d="m15 15 3-3 2 2-3 3h-2v-2z"></path>' +
          '</svg>' +
        '</div>'
      : '';

    var subtextHTML = isMag
      ? '<span class="pez-preloader-mag-label">' +
          '<svg class="pez-pencil-mini" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path>' +
            '<path d="m15 5 4 4"></path>' +
          '</svg>' +
          '<span>مجله سلامت و دانشنامه بالینی</span>' +
        '</span>'
      : '<span class="pez-preloader-subtext">CLINICAL ECOSYSTEM</span>';

    return (
      '<div id="pezeshkanPreloader" class="pez-preloader' + (isMag ? ' pez-preloader-mag' : '') + '" role="status" aria-live="polite" aria-label="Loading PEZESHK-ON">' +
        '<div class="pez-preloader-bg-glow" aria-hidden="true"></div>' +
        '<div class="pez-preloader-centerpiece">' +
          editorialBadgeHTML +
          '<div class="pez-circular-spinner-wrap" aria-hidden="true">' +
            '<svg class="pez-circular-spinner" viewBox="0 0 60 60">' +
              '<defs>' +
                '<linearGradient id="pezSpinnerGradient" x1="0%" y1="0%" x2="100%" y2="100%">' +
                  '<stop offset="0%" stop-color="#0066FF"/>' +
                  '<stop offset="50%" stop-color="#38BDF8"/>' +
                  '<stop offset="100%" stop-color="#00E5FF"/>' +
                '</linearGradient>' +
              '</defs>' +
              '<circle class="spinner-track" cx="30" cy="30" r="24" fill="none" stroke-width="3"/>' +
              '<circle class="spinner-arc" cx="30" cy="30" r="24" fill="none" stroke-width="3.5" stroke-linecap="round"/>' +
            '</svg>' +
            '<div class="spinner-center-dot"></div>' +
          '</div>' +
          '<div class="pez-preloader-brand-box">' +
            '<span class="pez-preloader-wordmark">PEZESHK-ON</span>' +
            subtextHTML +
          '</div>' +
        '</div>' +
      '</div>'
    );
  }

  function initClinicalPreloader(options) {
    if (typeof window !== 'undefined' && window.location && window.location.search.indexOf('nopreloader') !== -1) {
      return;
    }
    if (window.__pezeshkanPreloaderInitialized) return;
    window.__pezeshkanPreloaderInitialized = true;

    options = options || {};
    var isMag = typeof options.isMag === 'boolean' ? options.isMag : (
      window.location.pathname.indexOf('/mag') === 0
    );

    var preloader = document.getElementById('pezeshkanPreloader');
    if (!preloader) {
      var wrapper = document.createElement('div');
      wrapper.innerHTML = getPreloaderHTML(isMag);
      preloader = wrapper.firstElementChild;
      if (document.body) {
        document.body.prepend(preloader);
      } else if (document.documentElement) {
        document.documentElement.appendChild(preloader);
      }
    }

    var startTime = performance.now();
    var isDismissed = false;

    function dismiss() {
      if (isDismissed) return;
      if (typeof window !== 'undefined' && window.location && window.location.search.indexOf('freeze') !== -1) return;
      isDismissed = true;

      // Allow minimum pleasant viewing time (~350ms) for smooth visual ergonomics
      var elapsed = performance.now() - startTime;
      var remainingDelay = Math.max(0, 350 - elapsed);

      setTimeout(function () {
        if (preloader) {
          preloader.classList.add('is-loaded');
        }

        try {
          window.dispatchEvent(new CustomEvent('pezeshkan:preloader-dismissed'));
        } catch (e) {}

        setTimeout(function () {
          if (preloader && preloader.parentNode) {
            preloader.parentNode.removeChild(preloader);
          }
        }, 550);
      }, remainingDelay);
    }

    if (document.readyState === 'complete') {
      dismiss();
    } else {
      window.addEventListener('load', dismiss);
    }

    // Safety timeout: Never hold longer than 1100ms
    setTimeout(dismiss, 1100);
  }

  if (document.readyState === 'loading') {
    if (document.body) {
      initClinicalPreloader();
    } else {
      document.addEventListener('DOMContentLoaded', function () {
        initClinicalPreloader();
      });
    }
  } else {
    initClinicalPreloader();
  }

  window.initClinicalPreloader = initClinicalPreloader;
})();
