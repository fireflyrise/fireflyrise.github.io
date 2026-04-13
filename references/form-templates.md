# Form Templates Reference

## Home Services (Plumbing, HVAC, Electrical, etc.)

### Step 1 — Service Type
```html
<div class="form-step" id="step-1">
  <h3>What do you need help with?</h3>
  <div class="service-grid">
    <label class="service-card">
      <input type="radio" name="service" value="Emergency Repair">
      <span>🔧 Emergency Repair</span>
    </label>
    <label class="service-card">
      <input type="radio" name="service" value="Installation">
      <span>🏠 New Installation</span>
    </label>
    <label class="service-card">
      <input type="radio" name="service" value="Maintenance">
      <span>🔍 Maintenance / Tune-Up</span>
    </label>
    <label class="service-card">
      <input type="radio" name="service" value="Estimate">
      <span>📋 Free Estimate</span>
    </label>
  </div>
</div>
```

### Step 2 — Contact Info
```html
<div class="form-step" id="step-2" style="display:none">
  <h3>How can we reach you?</h3>
  <input type="text" id="name" placeholder="Your Name" required>
  <input type="tel" id="phone" placeholder="Phone Number" required>
  <input type="email" id="email" placeholder="Email Address" required>
</div>
```

### Step 3 — Details + Submit
```html
<div class="form-step" id="step-3" style="display:none">
  <h3>Tell us a bit more</h3>
  <textarea id="message" placeholder="Describe the issue or job..." rows="4"></textarea>
  <select id="preferred_time">
    <option value="">Preferred contact time</option>
    <option value="Morning (8am–12pm)">Morning (8am–12pm)</option>
    <option value="Afternoon (12pm–5pm)">Afternoon (12pm–5pm)</option>
    <option value="Evening (5pm–8pm)">Evening (5pm–8pm)</option>
    <option value="ASAP">ASAP / Emergency</option>
  </select>
  <button type="button" id="submit-btn">Get My Free Quote →</button>
</div>
```

---

## Flower Delivery / Gift Services

### Step 1 — Occasion
Options: Birthday, Anniversary, Sympathy, Just Because, Corporate, Wedding

### Step 2 — Delivery Info
Name, Phone, Email, Delivery Address, Delivery Date

### Step 3 — Message + Submit
Personal message for card, budget range selector, submit

---

## Digital Marketing Agency / Professional Services

### Step 1 — Project Type
Options: New Website, SEO / Traffic, Google Ads, Social Media, Full Package

### Step 2 — Business Info
Name, Business Name, Phone, Email, Website URL

### Step 3 — Goals + Submit
Monthly budget range, biggest challenge textarea, submit

---

## General Contractor / Remodeling

### Step 1 — Project Type
Options: Kitchen Remodel, Bathroom, Addition, New Construction, Repair / Other

### Step 2 — Contact
Name, Phone, Email, Property Address

### Step 3 — Timeline + Budget
Estimated start date, rough budget range, project description, submit
