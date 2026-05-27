#!/usr/bin/env node

/**
 * Palette Comparison Generator for BIG Phase 3B.
 *
 * Generates a single HTML page showing 3 palette variants (A, B, C) for each
 * of the 3 concepts, with mini-mockup hero (stacked/split toggle), role-based
 * color mapping, and swatches.
 *
 * Usage:
 *   node lib/palette-comparison.mjs <session_dir> <brand>
 *
 * Expects a JSON config at: <session_dir>/.tmp-palette-comparison-config.json
 *
 * Config format:
 * {
 *   "brandName": "BrandName",
 *   "concepts": [
 *     {
 *       "number": 1,
 *       "name": "Concept Name",
 *       "palettes": [
 *         {
 *           "variant": "A",
 *           "harmony": "Complémentaire",
 *           "chosenGamuts": "olives + verts chauds",
 *           "atmosphere": "Sombre-texturé",
 *           "mode": "SOMBRE" | "CLAIR",
 *           "colors": [
 *             {"role": "Primary", "name": "Mousse", "hex": "#2D4A3E"},
 *             {"role": "Secondary", "name": "Argile", "hex": "#D4A574"},
 *             {"role": "Accent", "name": "Cuivre", "hex": "#B87333"},
 *             {"role": "Bg dark", "name": "Humus", "hex": "#1A1A1A"},
 *             {"role": "Bg light", "name": "Lin", "hex": "#F5F0EB"},
 *             {"role": "Text primary", "name": "Encre", "hex": "#1C1C1C"},
 *             {"role": "Text secondary", "name": "Pierre", "hex": "#6B6B6B"}
 *           ]
 *         }
 *       ]
 *     }
 *   ]
 * }
 *
 * Output:
 *   {session_dir}/{brand}-palette-comparison.html
 */

import path from 'path';
import fs from 'fs';

const [,, sessionDir, brand] = process.argv;

if (!sessionDir || !brand) {
  console.error('Usage: node palette-comparison.mjs <session_dir> <brand>');
  process.exit(1);
}

const configPath = path.join(sessionDir, '.tmp-palette-comparison-config.json');
if (!fs.existsSync(configPath)) {
  console.error(`Config not found: ${configPath}`);
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// ── Tolérance aux clés FR (fallback) ──
// Le contrat documenté est en anglais (harmony / chosenGamuts / atmosphere / mode),
// mais l'orchestrateur peut faussement les franciser. On normalise ici et on émet
// un avertissement pour que la cause soit corrigée à la source.
const FR_TO_EN_KEYS = {
  harmonie: 'harmony',
  gammes: 'chosenGamuts',
  registre: 'atmosphere',
  atmosphère: 'atmosphere',
  modeFond: 'mode',
};
let frKeysSeen = false;
for (const concept of (config.concepts || [])) {
  for (const palette of (concept.palettes || [])) {
    for (const [frKey, enKey] of Object.entries(FR_TO_EN_KEYS)) {
      if (palette[frKey] !== undefined && palette[enKey] === undefined) {
        palette[enKey] = palette[frKey];
        frKeysSeen = true;
      }
    }
  }
}
if (frKeysSeen) {
  console.warn('  ⚠ Config contient des clés FR (harmonie/gammes/registre/modeFond). Normalisées en EN, mais l\'orchestrateur doit utiliser harmony/chosenGamuts/atmosphere/mode.');
}

// ── Helpers ──

function luminance(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const toLinear = (c) => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}

function contrastText(bgHex) {
  return luminance(bgHex) > 0.4 ? '#1A1A1A' : '#FFFFFF';
}

/**
 * Find a color by role (case-insensitive partial match).
 * Falls back to first color if not found.
 */
function findColor(colors, ...rolePatterns) {
  for (const pattern of rolePatterns) {
    const p = pattern.toLowerCase();
    const found = colors.find(c => c.role.toLowerCase().includes(p));
    if (found) return found.hex;
  }
  return colors[0].hex;
}

// ── Mockup builder (role-based) ──

function buildMockup(palette, conceptName, brandName, mode) {
  const { colors } = palette;
  const isDark = (mode || '').toUpperCase() === 'SOMBRE';

  // Map roles to mockup elements
  const bgPage    = isDark ? findColor(colors, 'bg dark', 'primary dark') : findColor(colors, 'bg light', 'surface', 'neutral light');
  const textMain  = isDark ? findColor(colors, 'bg light', 'neutral light', 'surface') : findColor(colors, 'text primary');
  const titleCol  = isDark ? findColor(colors, 'accent') : findColor(colors, 'primary');
  const navBrand  = titleCol;
  const accentCol = findColor(colors, 'accent');
  const ctaBg     = accentCol;
  const ctaText   = contrastText(ctaBg);
  const chromeBg  = isDark ? findColor(colors, 'primary base', 'primary') : findColor(colors, 'secondary');

  // Inverted block
  const invBg      = isDark ? findColor(colors, 'bg light', 'neutral light', 'surface') : findColor(colors, 'bg dark', 'primary dark');
  const invText    = isDark ? findColor(colors, 'text primary', 'primary dark') : findColor(colors, 'bg light', 'neutral light', 'surface');
  const invHeading = isDark ? findColor(colors, 'accent') : findColor(colors, 'secondary', 'accent');

  // Gradient: primary → secondary → accent
  const gradC1 = findColor(colors, 'primary');
  const gradC2 = findColor(colors, 'secondary');
  const gradC3 = accentCol;

  const navLinks = `
    <div style="display:flex;gap:12px;">
      <div style="width:24px;height:3px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
      <div style="width:24px;height:3px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
      <div style="width:24px;height:3px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
    </div>`;

  const navBar = `
    <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 16px;">
      <div style="font-weight:700;font-size:13px;color:${navBrand};">${brandName}</div>
      ${navLinks}
    </div>`;

  const accentLines = `
    <div style="height:3px;border-radius:2px;background:${accentCol};width:50%;opacity:0.5;margin:0 auto 4px;"></div>
    <div style="height:3px;border-radius:2px;background:${accentCol};width:30%;opacity:0.3;margin:0 auto 12px;"></div>`;

  const bodyLines = `
    <div style="height:2px;background:${textMain};opacity:0.1;width:70%;margin:0 auto 4px;"></div>
    <div style="height:2px;background:${textMain};opacity:0.1;width:80%;margin:0 auto 4px;"></div>
    <div style="height:2px;background:${textMain};opacity:0.1;width:55%;margin:0 auto 12px;"></div>`;

  const bodyLinesLeft = `
    <div style="height:2px;background:${textMain};opacity:0.1;width:90%;margin-bottom:3px;"></div>
    <div style="height:2px;background:${textMain};opacity:0.1;width:100%;margin-bottom:3px;"></div>
    <div style="height:2px;background:${textMain};opacity:0.1;width:70%;margin-bottom:10px;"></div>`;

  const accentLinesLeft = `
    <div style="height:3px;border-radius:2px;background:${accentCol};width:70%;opacity:0.5;margin-bottom:4px;"></div>
    <div style="height:3px;border-radius:2px;background:${accentCol};width:45%;opacity:0.3;margin-bottom:10px;"></div>`;

  const ctaBtn = `<div style="display:inline-block;padding:8px 18px;border-radius:3px;font-size:10px;font-weight:700;letter-spacing:0.5px;background:${ctaBg};color:${ctaText};">DÉCOUVRIR</div>`;

  const gradient = `linear-gradient(135deg, ${gradC1} 0%, ${gradC2} 50%, ${gradC3} 100%)`;

  const heroPlaceholder = `
    <div style="margin:0 16px;height:90px;border-radius:6px;background:${gradient};opacity:0.65;position:relative;">
      <div style="position:absolute;bottom:8px;right:10px;font-size:8px;color:rgba(${isDark ? '255,255,255' : '0,0,0'},0.4);letter-spacing:1px;text-transform:uppercase;">Visuel hero</div>
    </div>`;

  const heroPlaceholderSplit = `
    <div style="flex:1;background:${gradient};opacity:0.65;position:relative;">
      <div style="position:absolute;bottom:8px;right:8px;font-size:8px;color:rgba(${isDark ? '255,255,255' : '0,0,0'},0.4);letter-spacing:1px;text-transform:uppercase;">Visuel hero</div>
    </div>`;

  const invertedBlock = `
    <div style="margin:16px;padding:14px;border-radius:4px;background:${invBg};color:${invText};">
      <div style="font-weight:700;font-size:13px;margin-bottom:4px;color:${invHeading};">Section inversée</div>
      <div style="font-size:10px;opacity:0.7;line-height:1.5;">Contenu sur fond ${isDark ? 'clair' : 'sombre'}</div>
    </div>`;

  // STACKED
  const stacked = `
    <div class="hero-stacked" style="background:${bgPage};color:${textMain};">
      ${navBar}
      <div style="padding:20px 16px 16px;text-align:center;">
        <div style="font-weight:700;font-size:24px;line-height:1.1;margin-bottom:8px;color:${titleCol};">${conceptName}</div>
        ${accentLines}
        ${bodyLines}
        ${ctaBtn}
      </div>
      ${heroPlaceholder}
      ${invertedBlock}
    </div>`;

  // SPLIT
  const split = `
    <div class="hero-split" style="background:${bgPage};color:${textMain};">
      ${navBar}
      <div style="display:flex;min-height:150px;">
        <div style="flex:1;padding:16px 14px;display:flex;flex-direction:column;justify-content:center;">
          <div style="font-weight:700;font-size:20px;line-height:1.1;margin-bottom:8px;color:${titleCol};">${conceptName}</div>
          ${accentLinesLeft}
          ${bodyLinesLeft}
          <div style="align-self:flex-start;">${ctaBtn}</div>
        </div>
        ${heroPlaceholderSplit}
      </div>
      ${invertedBlock}
    </div>`;

  return { stacked, split, chromeBg };
}

// ── Card builder ──

function paletteCardHtml(palette, isRecommended, conceptName, brandName, cardId) {
  const { variant, harmony, chosenGamuts, atmosphere, mode, colors } = palette;
  const mockup = buildMockup(palette, conceptName, brandName, mode);

  const modeLabel = (mode || '').toUpperCase() === 'SOMBRE' ? 'SOMBRE' : 'CLAIR';

  const swatches = colors.map(c => {
    const isLight = luminance(c.hex) > 0.85;
    const border = isLight ? 'border:1px solid #ddd;' : '';
    return `
      <div class="swatch-col">
        <div class="swatch-mini" style="background:${c.hex};color:${contrastText(c.hex)};${border}">
          <span class="swatch-mini-hex">${c.hex}</span>
        </div>
        <div class="swatch-mini-name">${c.name}</div>
        <div class="swatch-mini-role">${c.role}</div>
      </div>`;
  }).join('');

  return `
  <div class="palette-card ${isRecommended ? 'recommended' : ''}" id="${cardId}">
    <div class="palette-header">
      <span class="palette-variant">Palette ${variant}</span>
      ${isRecommended ? '<span class="badge-recommended">Recommandée</span>' : ''}
      <div class="toggle-switch" onclick="toggleMode('${cardId}', this)">
        <span class="opt active" data-mode="stacked">Stack</span>
        <span class="opt" data-mode="split">Split</span>
      </div>
    </div>

    <div class="mockup-card">
      <div class="mockup-chrome" style="background:${mockup.chromeBg};">
        <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
      </div>
      ${mockup.stacked}
      ${mockup.split}
    </div>

    <div class="palette-meta">
      <div class="meta-item"><span class="meta-label">Harmonie</span><span class="meta-value">${harmony}</span></div>
      <div class="meta-item"><span class="meta-label">Gammes</span><span class="meta-value">${chosenGamuts}</span></div>
      <div class="meta-item"><span class="meta-label">Atmosphère</span><span class="meta-value">${atmosphere} · ${modeLabel}</span></div>
    </div>

    <div class="swatches-row">${swatches}</div>
  </div>`;
}

function conceptRowHtml(concept) {
  const { number, name, palettes } = concept;
  const cards = palettes.map((p, i) => {
    const cardId = `card-c${number}${String.fromCharCode(97 + i)}`;
    return paletteCardHtml(p, i === 0, name, config.brandName, cardId);
  }).join('');

  const intentionBlock = concept.intentionCreative ? `
    <div style="padding:14px 20px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;border-left:4px solid #6b7280;margin-bottom:12px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#9ca3af;margin-bottom:6px;">Intention créative</div>
      <div style="font-size:12px;line-height:1.55;color:#374151;">${concept.intentionCreative}</div>
    </div>` : '';

  return `
  <div class="concept-row">
    ${intentionBlock}
    <div class="concept-label">Concept ${number} — "${name}"</div>
    <div class="palettes-row">${cards}</div>
  </div>`;
}

// ── Full HTML ──

function generateHtml() {
  const conceptRows = config.concepts.map(c => conceptRowHtml(c)).join('');

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Comparaison palettes — ${config.brandName}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #F5F5F5; color: #1A1A1A; padding: 32px;
    }
    .page-title { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
    .page-subtitle { font-size: 14px; color: #888; margin-bottom: 32px; }

    .concept-row { margin-bottom: 48px; }
    .concept-label {
      font-size: 13px; text-transform: uppercase; letter-spacing: 2px;
      color: #888; margin-bottom: 16px; padding-bottom: 8px;
      border-bottom: 1px solid #E0E0E0;
    }
    .palettes-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }

    .palette-card {
      background: #FFFFFF; border: 1px solid #E5E7EB;
      border-radius: 12px; padding: 20px;
    }
    .palette-card.recommended { border-color: #2563EB; border-width: 2px; }

    .palette-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
    .palette-variant { font-size: 16px; font-weight: 700; }
    .badge-recommended {
      font-size: 11px; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.5px; padding: 3px 10px; border-radius: 4px;
      background: #EFF6FF; color: #2563EB;
    }

    /* Toggle switch */
    .toggle-switch {
      margin-left: auto; display: flex; align-items: center;
      background: #F3F4F6; border-radius: 12px; padding: 2px;
      cursor: pointer; user-select: none;
      font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .toggle-switch .opt {
      padding: 3px 10px; border-radius: 10px; color: #9CA3AF; transition: all 0.15s;
    }
    .toggle-switch .opt.active {
      background: #FFFFFF; color: #374151; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Mockup */
    .mockup-card {
      border-radius: 8px; overflow: hidden;
      box-shadow: 0 4px 16px rgba(0,0,0,0.1);
      margin-bottom: 16px;
    }
    .mockup-chrome { height: 24px; display: flex; align-items: center; padding: 0 10px; gap: 5px; }
    .dot { width: 8px; height: 8px; border-radius: 50%; }
    .dot-r { background: #ff5f57; } .dot-y { background: #febc2e; } .dot-g { background: #28c840; }

    /* Hero toggle */
    .hero-stacked { display: block; }
    .hero-split { display: none; }
    .palette-card.mode-split .hero-stacked { display: none; }
    .palette-card.mode-split .hero-split { display: block; }

    /* Meta */
    .palette-meta {
      display: flex; flex-direction: column; gap: 4px;
      margin-bottom: 12px; padding: 10px;
      background: #F8F9FA; border-radius: 8px; font-size: 12px;
    }
    .meta-item { display: flex; justify-content: space-between; }
    .meta-label { text-transform: uppercase; letter-spacing: 0.5px; color: #999; font-size: 10px; }
    .meta-value { font-weight: 500; color: #333; }

    /* Swatches */
    .swatches-row { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
    .swatch-col { display: flex; flex-direction: column; gap: 2px; }
    .swatch-mini {
      height: 56px; border-radius: 6px; display: flex;
      align-items: flex-end; padding: 4px 5px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    .swatch-mini-hex { font-size: 8px; font-family: monospace; opacity: 0.8; }
    .swatch-mini-name {
      font-size: 9px; color: #666; text-align: center;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .swatch-mini-role {
      font-size: 8px; color: #BBB; text-align: center;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }

    .instructions {
      margin-top: 32px; padding: 20px; background: #FFFFFF;
      border: 1px solid #E5E7EB; border-radius: 12px;
      font-size: 14px; color: #555; line-height: 1.6;
    }
    .instructions strong { color: #1A1A1A; }

    @media (max-width: 900px) { .palettes-row { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="page-title">Palettes — ${config.brandName}</div>
  <div class="page-subtitle">3 directions chromatiques par concept · Stacked par défaut, utilisez le toggle pour passer en Split</div>

  ${conceptRows}

  <div class="instructions">
    <strong>Comment choisir :</strong> Indiquez votre choix par concept, par exemple : "C1→A, C2→B, C3→A".<br>
    Répondez "OK" pour garder les palettes A (recommandées) pour les 3 concepts.
  </div>

  <script>
  function toggleMode(id, sw) {
    const card = document.getElementById(id);
    const isSplit = card.classList.toggle('mode-split');
    sw.querySelector('[data-mode="stacked"]').classList.toggle('active', !isSplit);
    sw.querySelector('[data-mode="split"]').classList.toggle('active', isSplit);
  }
  </script>
</body>
</html>`;
}

// ── Main ──

const html = generateHtml();
const outputPath = path.join(sessionDir, `${brand}-palette-comparison.html`);
fs.writeFileSync(outputPath, html, 'utf-8');
console.log(`  ✓ ${brand}-palette-comparison.html`);
