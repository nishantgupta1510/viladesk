# VilaDesk (Phase 1 Gatekeeper Platform)
### Micro-Township & Villa Society Gatekeeper Platform for Tier-2 Cities (Jaipur)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/nishantgupta1510/viladesk)

A specialized management and security system designed for horizontal gated communities, duplex rows, and small villa societies (10 to 200 units).

---

## 🌟 What is Built in Phase 1

1. **Horizontal Township Schema (`schema.sql` & `viladesk.db`)**:
   * No `Tower -> Floor -> Unit` apartment model.
   * Native support for **Occupied Villas** (Owner vs. Tenant contact routing + family member approvals), **Vacant Investor Plots** (with differential maintenance calculation), and **Under-Construction Plots** (contractor passes and labor tracking).
   * Seeded with 25 realistic plots for **Defined World City, Narsinghpura, Ajmer Road, NH-8, Jaipur, 302026** (including Plot 79).

2. **24x7 Interactive Live Demo Showcase (`/demo` & `/`)**:
   * Light & positive vibe theme (crisp white, fresh mint, sunshine gold).
   * Side-by-side live simulator: Guard Tablet on left (`/guard`), Resident WhatsApp phone on right (`/whatsapp`).
   * 5 1-Click Interactive Test Scenarios: Swiggy (Plot 79), Amazon Courier (Plot 14), Uber Cab, Night QR Kiosk, and Fast-Track Passcode `1177`.

3. **Builder Proposal Presentation Deck (`/proposal` & `/download/proposal-deck`)**:
   * 10-slide high-impact presentation in light positive theme created for builder pitches.
   * Slide-by-slide script, deployment timelines, Phase 1 requirements checklist, and monetization roadmap.
   * Downloadable as native `.pptx` (`VilaDesk_Builder_Proposal_Deck.pptx`).

4. **Guard Lite PWA (`/guard`)**:
   * Ultra-lightweight, high-contrast mobile interface designed for budget Android devices.
   * **Hindi & English Speech-to-Text Input**: Guard holds mic button and speaks (*"Plot 79 Courier 9829011079"*) to auto-select plot, category, and phone number.
   * **Mandatory Visitor Phone Input**: Numeric keypad with +91 prefix and validation.
   * **Leave at Gate Chime**: Audible notification and visual alert when resident instructs delivery left at gate.
   * **Currently Inside Carousel**: 1-tap checkout for departing visitors with overstay alerts.

5. **Guardless / Night QR Kiosk (`/kiosk`)**:
   * For societies with unstaffed gates or night hours (8 PM - 8 AM).
   * Visitors scan the weatherproof QR board at the gate on their smartphone.
   * Selects target plot and phone number -> Rings the resident via WhatsApp.
   * Real-time polling with dedicated **"Leave Package at Gate"** screen.

6. **Resident WhatsApp Simulator (`/whatsapp`)**:
   * Demonstrates the zero-app barrier: **residents do not need to install an app**.
   * Interactive buttons: `[ ✅ प्रवेश दें / Allow ]`, `[ ❌ रोकें / Deny ]`, and `[ 📦 गेट पर रखें / Leave at Gate ]`.
   * Real Meta WhatsApp Cloud API integration with webhook callbacks.

7. **Society Admin & Layout Map (`/admin`)**:
   * Interactive visual representation of the township's horizontal streets.
   * Live metrics: Occupied vs. Vacant vs. Construction count.
   * Real-time live activity stream of visitors inside and full audit log.

---

## 🚀 How to Run Locally

```bash
cd /Users/nishantgupta/.gemini/antigravity/scratch/viladesk
python3 server.py
```

The server starts on `http://localhost:8080`.

### Available Routes
* **Interactive 24x7 Demo:** [http://localhost:8080/demo](http://localhost:8080/demo)
* **Builder Proposal Deck:** [http://localhost:8080/proposal](http://localhost:8080/proposal)
* **Guard Lite App (Hindi/Voice):** [http://localhost:8080/guard](http://localhost:8080/guard)
* **Night QR Kiosk (Self-Service):** [http://localhost:8080/kiosk](http://localhost:8080/kiosk)
* **Resident WhatsApp Simulator:** [http://localhost:8080/whatsapp](http://localhost:8080/whatsapp)
* **Admin Dashboard & Township Map:** [http://localhost:8080/admin](http://localhost:8080/admin)
* **Gate Sign (Print Ready):** [http://localhost:8080/print-board](http://localhost:8080/print-board)

---

## ☁️ Persistent Cloud Deployment (Option A)

Deploy to Render in 1 click:

1. Click the **[Deploy to Render](https://render.com/deploy?repo=https://github.com/nishantgupta1510/viladesk)** button above.
2. Sign in with GitHub (`nishantgupta1510`).
3. Render automatically reads `render.yaml` and launches your 24x7 persistent web service (e.g. `https://viladesk.onrender.com`).
4. Set Meta WhatsApp Webhook URL to `https://<your-service>.onrender.com/api/whatsapp/webhook` with token `viladesk_secret_verify_token_2026`.

