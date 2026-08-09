/**
 * Jehovah Jireh Choir – ULK | Main JavaScript
 * Handles: scroll effects, back-to-top, scroll reveal, ad tracking
 */

// ── Back to top button ────────────────────────────────────────────────────────
const backToTop = document.getElementById('back-to-top');
if (backToTop) {
  window.addEventListener('scroll', () => {
    backToTop.classList.toggle('show', window.scrollY > 400);
  }, { passive: true });
}

// ── Scroll Reveal ─────────────────────────────────────────────────────────────
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
);
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Animated counters ─────────────────────────────────────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = parseInt(el.dataset.duration || '2000', 10);
  const start = performance.now();
  const update = (timestamp) => {
    const elapsed = timestamp - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
    el.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = '1';
        animateCounter(entry.target);
      }
    });
  },
  { threshold: 0.5 }
);
document.querySelectorAll('[data-counter]').forEach(el => counterObserver.observe(el));

// ── Ad impression tracking ────────────────────────────────────────────────────
document.querySelectorAll('[data-ad-id]').forEach(el => {
  const adId = el.dataset.adId;
  const csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');
  const csrf = csrfEl ? csrfEl.value : '';
  // Track impression
  fetch(`/advertising/track/${adId}/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'is_click=0',
  }).catch(() => {});
  // Track click
  el.addEventListener('click', () => {
    fetch(`/advertising/track/${adId}/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'is_click=1',
    }).catch(() => {});
  });
});

// ── HTMX indicator ────────────────────────────────────────────────────────────
document.body.addEventListener('htmx:beforeRequest', () => {
  document.body.classList.add('htmx-loading');
});
document.body.addEventListener('htmx:afterRequest', () => {
  document.body.classList.remove('htmx-loading');
});

// ── Confirm delete ─────────────────────────────────────────────────────────────
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', (e) => {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// ── Social share ──────────────────────────────────────────────────────────────
window.shareContent = function(platform, url, title) {
  url = url || window.location.href;
  title = title || document.title;
  const encoded = encodeURIComponent;
  const links = {
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encoded(url)}`,
    twitter: `https://twitter.com/intent/tweet?url=${encoded(url)}&text=${encoded(title)}`,
    whatsapp: `https://wa.me/?text=${encoded(title + ' ' + url)}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encoded(url)}`,
  };
  if (platform === 'copy') {
    navigator.clipboard.writeText(url).then(() => {
      showToast('Link copied to clipboard!', 'success');
    });
    return;
  }
  if (links[platform]) {
    window.open(links[platform], '_blank', 'width=600,height=400,noopener,noreferrer');
  }
};

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `fixed top-20 right-4 z-[9999] px-5 py-3 rounded-xl text-white text-sm font-medium shadow-lg ${
    type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600'
  }`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.5s'; setTimeout(() => toast.remove(), 500); }, 3000);
}

// ── Lazy load images not handled by browser ───────────────────────────────────
if ('loading' in HTMLImageElement.prototype) {
  // Browser supports lazy loading natively
} else {
  // Fallback: load lazily with IntersectionObserver
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  const lazyObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src || img.src;
        lazyObserver.unobserve(img);
      }
    });
  });
  lazyImages.forEach(img => lazyObserver.observe(img));
}

// ── Keyboard accessibility for custom interactive elements ────────────────────
document.querySelectorAll('[role="button"]:not(button)').forEach(el => {
  if (!el.getAttribute('tabindex')) el.setAttribute('tabindex', '0');
  el.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      el.click();
    }
  });
});

console.log('%cJehovah Jireh Choir – ULK', 'color:#DCA928;font-size:18px;font-weight:bold;');
console.log('%cWe Worship. We Evangelize. We Transform Lives.', 'color:#123F78;font-size:12px;');
