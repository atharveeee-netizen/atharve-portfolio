# Contributing to Atharve Dahima's Portfolio

Thank you for your interest in contributing to or reviewing this portfolio repository.

---

## Code of Conduct

All contributors and collaborators must follow our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all discussions with kindness, rigor, and respect.

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/atharveeee-netizen/atharve-portfolio.git
cd atharve-portfolio
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Launch the Local Development Server

```bash
npm run dev
```

The Vite dev server will start at `http://localhost:5173`. Multi-page application routing automatically maps clean routes (such as `/projects`, `/about`, `/labtour`) to their corresponding HTML documents.

### 4. Build for Production

```bash
npm run build
```

This compiles static assets into `dist/` ready for Vercel edge deployment.

---

## Contribution Guidelines

1. **Design & Tone Fidelity:**
   - Adhere to the voice bible: measured, close to the metal, and precise.
   - Avoid generic marketing clichés or AI-generated filler text.
   - State real engineering metrics (e.g. flight endurance in minutes, laser wavelength in nm, bit error rate).

2. **Asset Standards:**
   - Store high-resolution photography and engineering schematics in `docs/assets/`.
   - Ensure all image formats are web-optimized (PNG, WEBP, or SVG).

3. **Writing Conventions:**
   - Strictly avoid en-dashes and em-dashes across all documentation and templates. Use colons, commas, parentheses, or standard hyphens instead.

4. **Pull Requests:**
   - Ensure `npm run test` passes locally.
   - Detail the motivation for the change and include before/after screenshots for visual updates.

---

## Attribution & License

By submitting a Pull Request, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
