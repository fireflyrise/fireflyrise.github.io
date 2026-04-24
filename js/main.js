/* =========================================================================
   Firefly Rise — Main JS
   ========================================================================= */

/* ── Adaptive Favicon (swap on prefers-color-scheme) ──
   Chrome ignores media="(prefers-color-scheme:...)" on <link rel="icon">.
   Safari and Firefox honor it but Chrome picks first/last regardless.
   Using matchMedia is the only approach that works reliably everywhere. */
(function setAdaptiveFavicon() {
  var link = document.getElementById('favicon');
  if (!link) return;
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  var lightHref = '/images/favicon-light-background.png';
  var darkHref  = '/images/favicon-dark-background.png';
  function update(e) {
    link.href = (e && e.matches) ? darkHref : (mq.matches ? darkHref : lightHref);
  }
  update();
  if (mq.addEventListener) mq.addEventListener('change', update);
  else if (mq.addListener) mq.addListener(update); // older Safari
})();

/* ── Footer year ── */
(function () {
  var yearEl = document.getElementById('footer-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();

/* ── Hamburger Menu ── */
(function () {
  var hamburger = document.getElementById('hamburger');
  var menu = document.getElementById('nav-menu');
  if (!hamburger || !menu) return;

  hamburger.addEventListener('click', function () {
    menu.classList.toggle('open');
    var isOpen = menu.classList.contains('open');
    hamburger.setAttribute('aria-expanded', String(isOpen));
  });

  // Mobile: toggle dropdowns via parent button
  document.querySelectorAll('.nav-parent').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (window.innerWidth <= 860) {
        e.preventDefault();
        var li = btn.parentElement;
        var wasOpen = li.classList.contains('open');
        // Close all other open dropdowns
        document.querySelectorAll('.nav-menu > li.open').forEach(function (openLi) {
          if (openLi !== li) openLi.classList.remove('open');
        });
        li.classList.toggle('open', !wasOpen);
      }
    });
  });
})();

/* ── FAQs Accordion ── */
(function () {
  document.querySelectorAll('.faq-question').forEach(function (button) {
    button.addEventListener('click', function () {
      var isOpen = button.getAttribute('aria-expanded') === 'true';
      var answer = button.nextElementSibling;

      document.querySelectorAll('.faq-question[aria-expanded="true"]').forEach(function (openBtn) {
        if (openBtn !== button) {
          openBtn.setAttribute('aria-expanded', 'false');
          if (openBtn.nextElementSibling) openBtn.nextElementSibling.hidden = true;
        }
      });

      button.setAttribute('aria-expanded', String(!isOpen));
      if (answer) answer.hidden = isOpen;
    });
  });
})();

/* ── Hero / Quote Modal (Multi-step Lead Capture) ── */
(function () {
  var overlay = document.getElementById('hero-modal');
  if (!overlay) return;

  var triggers = document.querySelectorAll('[data-modal="hero-modal"]');
  var closeBtn = overlay.querySelector('.modal-close');
  var stepEls = overlay.querySelectorAll('.modal-step');
  var dots = overlay.querySelectorAll('.modal-progress-dots span');
  var labelEl = overlay.querySelector('.modal-progress-label');
  var totalSteps = 3;

  // Config — localized strings injected via data attributes on overlay
  var cfg = overlay.dataset;
  var lang = cfg.lang || 'en';
  var spanishRegion = cfg.spanishRegion || '';
  var webhookUrl = cfg.webhook || '';
  var businessName = cfg.business || 'Firefly Rise';
  var step1Question = cfg.step1Q || 'What marketing service are you interested in?';
  var step2Question = cfg.step2Q || 'What type of home service business do you run?';

  var currentStep = 1;
  var state = { step1: null, step2: null };

  function setStep(n) {
    currentStep = n;
    stepEls.forEach(function (el) { el.classList.remove('active'); });
    var target = overlay.querySelector('[data-step="' + n + '"]');
    if (target) target.classList.add('active');

    dots.forEach(function (dot, i) {
      dot.classList.remove('active', 'done');
      if (i === n - 1) dot.classList.add('active');
      else if (i < n - 1) dot.classList.add('done');
    });

    if (labelEl) {
      if (lang === 'es') {
        labelEl.textContent = 'Paso ' + n + ' de ' + totalSteps;
      } else {
        labelEl.textContent = 'Step ' + n + ' of ' + totalSteps;
      }
    }
  }

  function openModal() {
    overlay.classList.add('modal-visible');
    document.body.classList.add('modal-open');
    setStep(1);
    // Reset success/error state
    overlay.querySelector('.modal-success').classList.remove('active');
    overlay.querySelector('.modal-error-state').classList.remove('active');
    overlay.querySelector('.modal-form').style.display = '';
  }
  function closeModal() {
    overlay.classList.remove('modal-visible');
    document.body.classList.remove('modal-open');
  }

  triggers.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.preventDefault();
      openModal();
    });
  });
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('modal-visible')) closeModal();
  });

  // Track selections
  overlay.querySelectorAll('input[name="step1"]').forEach(function (r) {
    r.addEventListener('change', function () { state.step1 = r.value; });
  });
  overlay.querySelectorAll('input[name="step2"]').forEach(function (r) {
    r.addEventListener('change', function () { state.step2 = r.value; });
  });

  // Phone auto-formatter — formats as user types: (XXX) XXX-XXXX
  function formatUSPhone(raw) {
    var d = (raw || '').replace(/\D/g, '');
    // Drop a leading "1" country code if pasted (e.g. 16028290009 → 6028290009)
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    d = d.slice(0, 10);
    if (d.length === 0) return '';
    if (d.length <= 3) return '(' + d;
    if (d.length <= 6) return '(' + d.slice(0, 3) + ') ' + d.slice(3);
    return '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);
  }
  var phoneInput = overlay.querySelector('#modal-phone');
  if (phoneInput) {
    phoneInput.addEventListener('input', function () {
      // Skip formatting on backspace at end so user can clear naturally
      this.value = formatUSPhone(this.value);
    });
    phoneInput.addEventListener('paste', function (e) {
      // Let the paste land, then reformat on the next tick
      var self = this;
      setTimeout(function () { self.value = formatUSPhone(self.value); }, 0);
    });
  }

  // Next / Back buttons
  overlay.querySelectorAll('[data-action="next"]').forEach(function (b) {
    b.addEventListener('click', function () {
      var errEl = overlay.querySelector('[data-step="' + currentStep + '"] .modal-error');
      if (errEl) errEl.classList.remove('visible');

      if (currentStep === 1 && !state.step1) {
        if (errEl) { errEl.textContent = lang === 'es' ? 'Por favor selecciona una opción.' : 'Please select an option.'; errEl.classList.add('visible'); }
        return;
      }
      if (currentStep === 2 && !state.step2) {
        if (errEl) { errEl.textContent = lang === 'es' ? 'Por favor selecciona una opción.' : 'Please select an option.'; errEl.classList.add('visible'); }
        return;
      }
      setStep(currentStep + 1);
    });
  });
  overlay.querySelectorAll('[data-action="back"]').forEach(function (b) {
    b.addEventListener('click', function () { setStep(Math.max(1, currentStep - 1)); });
  });

  // Submit
  var submitBtn = overlay.querySelector('[data-action="submit"]');
  if (submitBtn) {
    submitBtn.addEventListener('click', function () {
      var nameEl = overlay.querySelector('#modal-name');
      var phoneEl = overlay.querySelector('#modal-phone');
      var emailEl = overlay.querySelector('#modal-email');
      var hpEl = overlay.querySelector('#modal-website');
      var errEl = overlay.querySelector('[data-step="3"] .modal-error');
      errEl.classList.remove('visible');

      var name = (nameEl.value || '').trim();
      var phone = (phoneEl.value || '').trim();
      var email = (emailEl.value || '').trim();
      var honeypot = hpEl ? (hpEl.value || '').trim() : '';

      // Honeypot — bots auto-fill the hidden "website" field; humans never see it.
      // Show the success state so the bot thinks it worked, but never POST or burn a Pabbly task.
      if (honeypot) {
        if (window.console && console.log) {
          console.log('[FireflyRise] Honeypot tripped, dropping submission silently.');
        }
        overlay.querySelector('.modal-form').style.display = 'none';
        var hpSuccess = overlay.querySelector('.modal-success');
        var hpNameSlot = hpSuccess.querySelector('.success-name');
        if (hpNameSlot) hpNameSlot.textContent = (name.split(' ')[0] || '');
        hpSuccess.classList.add('active');
        setTimeout(function () {
          if (overlay.classList.contains('modal-visible')) closeModal();
        }, 6000);
        return;
      }

      if (!name || !phone || !email) {
        errEl.textContent = lang === 'es' ? 'Por favor completa todos los campos.' : 'Please fill in all fields.';
        errEl.classList.add('visible');
        return;
      }
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      var phoneDigits = phone.replace(/\D/g, '');
      if (!emailOk) {
        errEl.textContent = lang === 'es' ? 'Por favor ingresa un correo válido.' : 'Please enter a valid email address.';
        errEl.classList.add('visible');
        return;
      }
      if (phoneDigits.length < 7) {
        errEl.textContent = lang === 'es' ? 'Por favor ingresa un teléfono válido.' : 'Please enter a valid phone number.';
        errEl.classList.add('visible');
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = lang === 'es' ? 'Enviando...' : 'Sending...';

      var payload = {
        source: 'hero_modal',
        business: businessName,
        language: lang,
        spanish_region: spanishRegion,
        page_path: window.location.pathname,
        step1_question: step1Question,
        step1_answer: state.step1,
        step2_question: step2Question,
        step2_answer: state.step2,
        full_name: name,
        phone: phone,
        email: email,
        submitted_at: new Date().toISOString()
      };

      var showSuccess = function () {
        overlay.querySelector('.modal-form').style.display = 'none';
        var success = overlay.querySelector('.modal-success');
        var firstName = name.split(' ')[0];
        var nameSlot = success.querySelector('.success-name');
        if (nameSlot) nameSlot.textContent = firstName;
        success.classList.add('active');
        setTimeout(function () {
          if (overlay.classList.contains('modal-visible')) closeModal();
        }, 6000);
      };
      var showError = function () {
        overlay.querySelector('.modal-form').style.display = 'none';
        overlay.querySelector('.modal-error-state').classList.add('active');
      };

      // If webhook is the placeholder, still show success for UX parity
      if (!webhookUrl || webhookUrl.indexOf('REPLACE') !== -1 || webhookUrl.indexOf('PLACEHOLDER') !== -1) {
        console.log('[FireflyRise] Modal submission (webhook placeholder):', payload);
        showSuccess();
        submitBtn.disabled = false;
        submitBtn.textContent = lang === 'es' ? 'Obtener Mi Cotización Gratis' : 'Get My Free Quote';
        return;
      }

      fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (r.ok) { showSuccess(); } else { showError(); }
      }).catch(function () {
        showError();
      }).finally(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = lang === 'es' ? 'Obtener Mi Cotización Gratis' : 'Get My Free Quote';
      });
    });
  }

  setStep(1);
})();

/* ── IntersectionObserver fade-in ── */
(function () {
  if (!('IntersectionObserver' in window)) return;
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(function (el) { observer.observe(el); });
})();
