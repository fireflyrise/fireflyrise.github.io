# Section Snippets Reference

## Trust Bar / Social Proof Strip
A horizontal bar of 3–5 icons + stats placed below the hero.

```html
<section class="trust-bar">
  <div class="trust-item"><span class="trust-number">15+</span><span class="trust-label">Years in Business</span></div>
  <div class="trust-item"><span class="trust-number">2,400+</span><span class="trust-label">Jobs Completed</span></div>
  <div class="trust-item"><span class="trust-number">4.9★</span><span class="trust-label">Google Rating</span></div>
  <div class="trust-item"><span class="trust-number">2hr</span><span class="trust-label">Avg Response Time</span></div>
  <div class="trust-item"><span class="trust-number">Licensed</span><span class="trust-label">& Insured</span></div>
</section>
```

## Mobile Sticky CTA Bar
Fixed bottom bar on mobile only. Hidden on desktop.

```html
<div class="mobile-cta-bar">
  <a href="tel:PHONE" class="btn-call">📞 Call Now</a>
  <a href="#contact" class="btn-quote">Get a Free Quote</a>
</div>
```
```css
.mobile-cta-bar {
  display: flex;
  position: fixed;
  bottom: 0; left: 0; right: 0;
  z-index: 999;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.15);
}
.mobile-cta-bar a {
  flex: 1;
  text-align: center;
  padding: 14px;
  font-weight: 700;
  font-size: 0.95rem;
  text-decoration: none;
}
.btn-call { background: var(--color-accent); color: #fff; }
.btn-quote { background: var(--color-primary); color: var(--color-cta-text); }
@media (min-width: 768px) { .mobile-cta-bar { display: none; } }
/* Add bottom padding to body so content isn't hidden behind bar on mobile */
@media (max-width: 767px) { body { padding-bottom: 60px; } }
```

## IntersectionObserver Fade-In
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
```
CSS: `.fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.5s, transform 0.5s; } .fade-in.visible { opacity: 1; transform: none; }`

## Hamburger Nav (mobile)
```javascript
document.getElementById('hamburger').addEventListener('click', () => {
  document.getElementById('nav-menu').classList.toggle('open');
});
```

## Accordion FAQ
```javascript
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    item.classList.toggle('open');
  });
});
```

## Smooth progress bar for multi-step form
```javascript
function updateProgress(step, total) {
  const pct = ((step - 1) / (total - 1)) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
  document.getElementById('step-label').textContent = `Step ${step} of ${total}`;
}
```

## Container Pattern (use on every section)
```html
<section class="services-section">
  <div class="container">
    <!-- section content here -->
  </div>
</section>
```
```css
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 var(--space-sm);
}
```

## Responsive Grid Patterns

### Service Cards (1 → 2 → 3 columns)
```css
.services-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-md);
}
@media (min-width: 600px) {
  .services-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .services-grid { grid-template-columns: repeat(3, 1fr); }
}
```

### Testimonials (1 → 3 columns)
```css
.testimonials-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-md);
}
@media (min-width: 768px) {
  .testimonials-grid { grid-template-columns: repeat(3, 1fr); }
}
```

## Hamburger Nav (mobile)
```html
<nav class="site-nav">
  <div class="container nav-inner">
    <div class="nav-logo">LOGO</div>
    <button class="hamburger" id="hamburger" aria-label="Open menu">☰</button>
    <div class="nav-menu" id="nav-menu">
      <a href="#services">Services</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
      <a href="tel:PHONE" class="nav-cta">📞 PHONE</a>
    </div>
  </div>
</nav>
```
```css
.site-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--color-bg-white);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.nav-inner {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: var(--space-sm);
}
.hamburger { display: block; background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.nav-menu {
  display: none; flex-direction: column;
  position: absolute; top: 100%; left: 0; right: 0;
  background: var(--color-bg-white);
  padding: var(--space-sm);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.nav-menu.open { display: flex; }
.nav-menu a { padding: var(--space-xs) 0; font-size: 1rem; text-decoration: none; color: var(--color-text); }
.nav-cta { color: var(--color-primary) !important; font-weight: 700; }
@media (min-width: 768px) {
  .hamburger { display: none; }
  .nav-menu { display: flex; flex-direction: row; position: static; box-shadow: none; padding: 0; gap: var(--space-md); align-items: center; }
}
```
```javascript
document.getElementById('hamburger').addEventListener('click', () => {
  document.getElementById('nav-menu').classList.toggle('open');
});
```

## Global Spacing & Typography Base
```css
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&family=Open+Sans:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Open Sans', sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  color: var(--color-text-dark);
  margin: 0;
}

/* Headings — set ONCE globally, never override per-section */
h1, h2, h3, h4 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  text-transform: capitalize;
  text-align: left;
  margin-top: 0;
  line-height: 1.2;
}

/* Fixed sizes — ALL h2 tags same size, ALL h3 tags same size across the entire page */
h1 { font-size: clamp(2rem, 5vw, 3.5rem); }
h2 { font-size: clamp(1.5rem, 3vw, 2.25rem); }
h3 { font-size: clamp(1.1rem, 2vw, 1.4rem); }
h4 { font-size: 1.1rem; }

/* Text color based on section background — apply via parent section class */
.section-light h1, .section-light h2, .section-light h3, .section-light h4,
.section-light p, .section-light li { color: var(--color-text-dark); }

.section-dark h1, .section-dark h2, .section-dark h3, .section-dark h4,
.section-dark p, .section-dark li { color: var(--color-text-light); }

p { max-width: 65ch; }
section { padding: var(--space-xl) var(--space-sm); }
@media (min-width: 768px) {
  section { padding: var(--space-2xl) var(--space-lg); }
}
img { max-width: 100%; height: auto; display: block; }
```
