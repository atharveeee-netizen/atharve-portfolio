<div align="center">

<img src="assets/img/og-card.png" width="720" alt="atharveeee portfolio banner" />

# atharveeee
### **Personal Portfolio Web Application**
*A multi-page static site built with fluid inertia motion, darkroom aesthetics, and Web Audio feedback.*

[![Live Site](https://img.shields.io/badge/Live%20Site-atharveeee.vercel.app-00FFA3.svg?style=for-the-badge)](https://atharveeee.vercel.app)
[![Deployed on Vercel](https://img.shields.io/badge/Deployment-Vercel%20Edge-black.svg?style=for-the-badge&logo=vercel)](https://vercel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](index.html)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](assets/styles.css)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)](assets/app.js)
[![Motion: Lenis](https://img.shields.io/badge/Scroll-Lenis%20Inertia-000000)](https://github.com/darkroomengineering/lenis)
[![Bundler: Vite 8](https://img.shields.io/badge/Bundler-Vite%208.0-646CFF?logo=vite&logoColor=white)](vite.config.js)

[**Live Demo**](https://atharveeee.vercel.app) | [**Architecture**](#architecture--technical-approach) | [**Interaction & Motion Engine**](#interaction--motion-engine) | [**Audio System**](#audio-architecture--soundscape) | [**Routing & Multi-Page Setup**](#routing--multi-page-architecture) | [**Design System**](#design-system--css-architecture) | [**Local Setup**](#local-development)

</div>

---

## Overview

This repository contains the complete source code for **[atharveeee.vercel.app](https://atharveeee.vercel.app)**.

The site is built as an uncompromising, high-performance static Multi-Page Application (MPA). Rather than relying on heavy client-side JavaScript frameworks, it is authored in clean, semantic HTML5, modular Vanilla CSS, and modern ES6+ JavaScript. The result is instantaneous page loads, zero hydration lag, full search indexability, and 60 FPS animation physics.

---

## Architecture & Technical Approach

The codebase prioritizes performance, visual craft, and zero runtime bloat:

```text
                        Browser / Client
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
   [Semantic HTML5 MPA]                 [Audio & Motion Core]
   - index.html (Home)                  - Lenis inertia scrolling
   - about.html (Background)            - IntersectionObserver reveals
   - projects.html (Work)               - Per-char text roll hover
   - labtour.html (Photo Essay)         - Web Audio click/hover FX
   - how-it-works.html (Workflow)       - Reduced-motion fallbacks
   - contact.html (Direct Form)
            |                                     |
            +------------------+------------------+
                               |
                               v
                   [Vite 8 Multi-Page Server]
                   - Clean URL dev rewrites
                   - Hot module replacement
                               |
                               v
                   [Vercel Global Edge CDN]
                   - vercel.json extensionless routes
                   - Sub-50ms Time to First Byte (TTFB)
```

### Key Engineering Decisions

* **Zero Framework Bloat:** No React, Next.js, or Vue runtime overhead. Pages ship clean HTML and lightweight vanilla modules.
* **Inertia Smooth Scrolling:** High-precision scroll physics powered by Lenis, calibrated with natural deceleration.
* **Progressive Enhancement:** Works smoothly across all modern desktop and mobile browsers, with explicit `prefers-reduced-motion` compliance.
* **Clean URL Routing:** Uses custom Vite dev middleware locally and edge rewrites in production to deliver clean URLs without `.html` extensions.

---

## Interaction & Motion Engine

All kinetic behaviors are orchestrated through standalone, highly optimized scripts:

### 1. Lenis Smooth Scroll (`assets/app.js`)
Smooth inertia scrolling is initialized via a lightweight Lenis instance:
* **Duration:** 1.15 seconds with custom easing curve.
* **Wheel Multiplier:** 1.0 for predictable desktop navigation.
* **Touch Multiplier:** 1.4 for tactile mobile momentum.
* Automatically disabled when the user enables `prefers-reduced-motion: reduce`.

### 2. Viewport Reveal Pipeline (`assets/app.js`)
Content reveals use a robust `IntersectionObserver` system:
* **Immediate Above-The-Fold Check:** Elements already inside the viewport on initial page load execute immediately without entrance delays.
* **Root Margin Offset:** Configured with `0px 0px -8% 0px` to trigger reveals slightly ahead of scroll boundary entry.
* **Built-in Failsafe:** A global 1.6-second timer automatically reveals any un-triggered elements to guarantee no content remains hidden if an observer stalls.

### 3. Kinetic Button Hover Animation (`assets/btn-hover.js`)
Call-to-action buttons feature a custom, three-part micro-interaction:
1. **Per-Character Text Roll:** The label text is dynamically parsed into stacked character spans (`.fx-char__a` and `.fx-char__b`). On hover, the primary letter rolls upward out of frame while the clone rolls in from below with a staggered `0.01s` delay per character and a `cubic-bezier(.16, 1, .3, 1)` transition curve.
2. **Forward-Looping Arrow:** Inside the clipped icon box, the leading arrow translates out to the right while a second arrow enters seamlessly from the left.
3. **Background Wipe:** A soft, hardware-accelerated fill rises smoothly from bottom to top.

---

## Audio Architecture & Soundscape

The portfolio features an integrated sonic layer designed to reward user interactions:

* **Audio Gate Modal:** On first visit, a clean introductory prompt offers the choice to enter with or without sound ("This site carries a soundtrack. Your call.").
* **Tactile Micro-Feedback:** Buttons and interactive elements trigger subtle audio cues (`btn-in.mp3`, `btn-out.mp3`, and `btn-in-2.mp3`) on mouse enter, mouse leave, and click events.
* **Non-Blocking Execution:** Sound assets load asynchronously and fail silently if audio context initialization is blocked by browser autoplay policies.
* **State Persistence:** Audio preferences remain consistent across page transitions.

---

## Routing & Multi-Page Architecture

The site runs as a multi-page application with clean, search-friendly URLs:

### Local Development (Vite)
Vite's development server is configured with custom middleware in `vite.config.js`:

```javascript
import { defineConfig } from 'vite';

export default defineConfig({
  appType: 'mpa',
  plugins: [
    {
      name: 'rewrite-all',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          if (!req.url.includes('.') && req.url !== '/' && !req.url.startsWith('/@')) {
            req.url += '.html';
          }
          next();
        });
      }
    }
  ]
});
```

This rewrites incoming requests such as `/projects` or `/about` directly to their matching HTML file on disk without requiring manual browser file extensions.

### Production (Vercel)
Production deployments use `vercel.json` to handle clean URL routing:

```json
{
  "cleanUrls": true,
  "trailingSlash": false
}
```

---

## Design System & CSS Architecture

The visual aesthetic uses a focused, monochrome darkroom theme:

### Color System
* **Background Deep:** `#0c0f12` and `#121619`
* **Surface Panels:** `#141a21` and `#1e242b`
* **Text Primary:** `#f4f4f4`
* **Text Muted:** `#8d8d8d`
* **Accents & Borders:** `#25303d` and `#525252`

### Stylesheet Modularization
* **`assets/styles.css`:** Core CSS custom properties, global resets, typography tokens, custom scrollbars, and navigation header layout.
* **`assets/pages.css`:** Structural layout systems, responsive grid templates, and view wrappers across individual pages.
* **`assets/gallery.css`:** Interactive project cards, thumbnail frames, modal overlays, and hover transitions.

### Hardware Acceleration
Animations strictly target GPU-accelerated CSS properties (`transform` and `opacity`) with explicit `will-change: transform` hints, eliminating layout recalculations and repaint thrashing.

---

## Project Structure

```text
atharve-portfolio/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.yml          # Structured bug report form
|   |   |-- feature_request.yml     # Feature & UX suggestion form
|   |   |-- hardware_inquiry.yml    # Collaboration & contact form
|   |   `-- config.yml              # Issue template configuration
|   |-- workflows/
|   |   `-- ci.yml                  # Automated Vite build & dash verification
|   `-- pull_request_template.md    # PR review checklist
|
|-- assets/                         # Core runtime styling, scripts, and audio
|   |-- audio/                      # Background soundtrack audio files
|   |-- img/                        # Branding images, icons, and hero graphics
|   |   |-- curated/                # Visual engravings and historical illustrations
|   |   `-- og-card.png             # Social preview card and hero image
|   |-- app.js                      # Lenis scroll controller and reveal engine
|   |-- btn-hover.js                # Per-character button text roll and arrow loops
|   |-- gallery.js                  # Gallery filtering and interactive views
|   |-- partials.js                 # Shared header and footer partial injectors
|   |-- styles.css                  # Global tokens, reset, and base typography
|   |-- pages.css                   # Page layout structures
|   |-- gallery.css                 # Project showcase and grid styles
|   |-- btn-in.mp3                  # Button hover audio trigger
|   |-- btn-out.mp3                 # Button mouse leave audio trigger
|   `-- btn-in-2.mp3                # Button click feedback audio trigger
|
|-- projects/                       # In-depth case-study subpages
|   |-- f450-multirotor-drone.html
|   |-- laser-lifi-network.html
|   |-- pcb-design.html
|   |-- cryogenic-electronics.html
|   |-- embedded-flight-controller.html
|   |-- face-detection-drone.html
|   |-- computer-vision-pipeline.html
|   |-- autonomous-tracking.html
|   |-- publications.html
|   `-- certificates.html
|
|-- index.html                      # Entry landing page with audio gate
|-- about.html                      # Background and story page
|-- projects.html                   # Case study gallery directory
|-- labtour.html                    # Workshop photo essay
|-- how-it-works.html               # Process and engagement workflow
|-- contact.html                    # Direct contact page with WhatsApp integration
|-- privacy-policy.html             # Privacy policy statement
|-- terms-conditions.html           # Terms and conditions
|
|-- CITATION.cff                    # Citation metadata for portfolio code
|-- CODE_OF_CONDUCT.md              # Contributor Covenant Code of Conduct v2.1
|-- CONTRIBUTING.md                 # Local setup and contribution guidelines
|-- LICENSE                         # MIT License
|-- package.json                    # Node scripts and dependencies
|-- vercel.json                     # Production edge routing rules
`-- vite.config.js                  # Multi-page development server config
```

---

## Local Development

### Prerequisites
* **Node.js**: v18.0.0 or higher
* **npm**: v9.0.0 or higher

### 1. Clone the Repository
```bash
git clone https://github.com/atharveeee-netizen/atharve-portfolio.git
cd atharve-portfolio
```

### 2. Install Dependencies
```bash
npm install --ignore-scripts
```

### 3. Run Development Server
```bash
npm run dev
```
The local server will start at `http://localhost:5173`. Any page can be opened cleanly (for example `http://localhost:5173/about` or `http://localhost:5173/projects`).

### 4. Build for Production
```bash
npm run build
```
Compiles and bundles static assets into `dist/`.

### 5. Preview Production Build
```bash
npm run preview
```

---

## Production Deployment

The project is pre-configured for zero-configuration deployments on **Vercel**:

```bash
# Deploy to preview
npx vercel

# Deploy directly to production
npx vercel --prod
```

---

## License

Released under the **MIT License**. Copyright (c) 2026 Atharve Dahima. All rights reserved.
