#!/usr/bin/env node

/**
 * Font + Palette Specimen Generator for BIG Phase 3B visual verification.
 *
 * Generates HTML specimens showing font pairings + palette swatches + text on
 * colored backgrounds, then captures screenshots via Puppeteer for multimodal
 * validation by the subagent.
 *
 * Usage:
 *   node lib/font-palette-specimen.mjs <session_dir> <brand>
 *
 * Expects a JSON config at: <session_dir>/.tmp-specimen-config.json
 *
 * Config format:
 * {
 *   "concepts": [
 *     {
 *       "number": 1,
 *       "name": "Concept Name",
 *       "brandName": "BrandName",
 *       "displayFont": "Playfair Display",
 *       "displayWeight": "700",
 *       "bodyFont": "Inter",
 *       "bodyWeight": "400",
 *       "mode": "SOMBRE" | "CLAIR",
 *       "colors": [
 *         {"role": "Primary", "name": "Name", "hex": "#2D4A3E"},
 *         {"role": "Secondary", "name": "Name", "hex": "#D4A574"},
 *         {"role": "Accent", "name": "Name", "hex": "#B87333"},
 *         {"role": "Bg dark", "name": "Name", "hex": "#1A1A1A"},
 *         {"role": "Bg light", "name": "Name", "hex": "#F5F0EB"},
 *         {"role": "Text primary", "name": "Name", "hex": "#1C1C1C"},
 *         {"role": "Text secondary", "name": "Name", "hex": "#6B6B6B"}
 *       ],
 *       "gamutScan": [
 *         {"gamut": "roses terreux", "affinity": "FAIBLE", "reason": "..."},
 *         {"gamut": "olives", "affinity": "FORTE", "reason": "..."}
 *       ],
 *       "chosenGamuts": "olives + verts chauds",
 *       "harmony": "Analogue",
 *       "atmosphere": "Labo d'alchimie"
 *     }
 *   ]
 * }
 *
 * Output:
 *   {session_dir}/{brand}-specimen-c{N}.html  (one HTML per concept)
 *   {session_dir}/{brand}-specimen-c{N}.png   (one screenshot per concept, 1200px wide)
 */

import puppeteer from 'puppeteer';
import { pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const [,, sessionDir, brand] = process.argv;

if (!sessionDir || !brand) {
  console.error('Usage: node font-palette-specimen.mjs <session_dir> <brand>');
  process.exit(1);
}

const configPath = path.join(sessionDir, '.tmp-specimen-config.json');
if (!fs.existsSync(configPath)) {
  console.error(`Config not found: ${configPath}`);
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

const VIEWPORT_WIDTH = 1200;
const FONT_WAIT_TIMEOUT = 10000;

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

/** Extract flat palette array from colors (for readability tests) */
function flatPalette(colors) {
  return colors.map(c => c.hex);
}

/** Builds Google Fonts URL for all concepts */
function buildFontsUrl(concepts) {
  const families = new Set();
  for (const c of concepts) {
    const dw = c.displayWeight || '400;700';
    const bw = c.bodyWeight || '400;700';
    families.add(`family=${encodeURIComponent(c.displayFont)}:wght@${dw}`);
    families.add(`family=${encodeURIComponent(c.bodyFont)}:wght@${bw}`);
  }
  return `https://fonts.googleapis.com/css2?${[...families].join('&')}&display=swap`;
}

// ── Mockup (role-based, aligned with palette-comparison.mjs) ──

function mockupHtml(concept) {
  const { name, displayFont, bodyFont, colors, atmosphere, chosenGamuts, harmony, brandName, mode } = concept;
  const brandLabel = brandName || 'Brand';
  const isDark = (mode || '').toUpperCase() === 'SOMBRE';

  // Role-based color mapping
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

  // Gradient
  const gradC1 = findColor(colors, 'primary');
  const gradC2 = findColor(colors, 'secondary');
  const gradC3 = accentCol;
  const gradient = `linear-gradient(135deg, ${gradC1} 0%, ${gradC2} 50%, ${gradC3} 100%)`;
  const rgbaLabel = isDark ? '255,255,255' : '0,0,0';

  const modeLabel = isDark ? 'SOMBRE' : 'CLAIR';

  // Swatch strip for mockup footer
  const palette = flatPalette(colors);
  const swatchStrip = palette.map(hex =>
    `<div style="width:20px;height:20px;border-radius:4px;background:${hex};${luminance(hex) > 0.85 ? 'border:1px solid #ccc;' : luminance(hex) < 0.05 ? 'border:1px solid #333;' : ''}"></div>`
  ).join('');

  const intentionBlock = concept.intentionCreative ? `
  <div style="margin-bottom:24px;padding:20px 24px;background:#fff;border:1px solid #e5e7eb;border-radius:10px;border-left:4px solid #6b7280;max-width:calc(100% - 380px);">
    <div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#9ca3af;margin-bottom:8px;">Intention créative — Concept ${concept.number}</div>
    <div style="font-size:14px;line-height:1.65;color:#374151;">${concept.intentionCreative}</div>
  </div>` : '';

  return `
  ${intentionBlock}
  <div class="mockup-section">
    <div class="mockup-label">Aperçu — Impression visuelle générale</div>
    <div class="mockup-card" id="mockup-${concept.number}">
      <div class="mockup-chrome" style="background:${chromeBg};">
        <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
        <div class="toggle-switch" onclick="toggleMockup(${concept.number}, this)">
          <span class="opt active" data-mode="stacked">Stack</span>
          <span class="opt" data-mode="split">Split</span>
        </div>
      </div>

      <!-- STACKED (default) -->
      <div class="hero-stacked" style="background:${bgPage};color:${textMain};">
        <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 24px;">
          <div style="font-family:'${displayFont}',serif;font-weight:700;font-size:16px;color:${navBrand};">${brandLabel}</div>
          <div style="display:flex;gap:16px;">
            <div style="width:32px;height:4px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
            <div style="width:32px;height:4px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
            <div style="width:32px;height:4px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
          </div>
        </div>
        <div style="padding:24px;text-align:center;">
          <div style="font-family:'${displayFont}',serif;font-weight:700;font-size:36px;line-height:1.1;margin-bottom:12px;color:${titleCol};">${name}</div>
          <div style="height:4px;border-radius:2px;background:${accentCol};width:50%;opacity:0.5;margin:0 auto 6px;"></div>
          <div style="height:4px;border-radius:2px;background:${accentCol};width:30%;opacity:0.3;margin:0 auto 16px;"></div>
          <div style="height:3px;background:${textMain};opacity:0.12;width:70%;margin:0 auto 5px;"></div>
          <div style="height:3px;background:${textMain};opacity:0.12;width:80%;margin:0 auto 5px;"></div>
          <div style="height:3px;background:${textMain};opacity:0.12;width:55%;margin:0 auto 16px;"></div>
          <div style="display:inline-block;padding:10px 24px;border-radius:3px;font-size:12px;font-weight:700;letter-spacing:0.5px;background:${ctaBg};color:${ctaText};font-family:'${bodyFont}',sans-serif;">DÉCOUVRIR</div>
        </div>
        <div style="margin:0 24px;height:120px;border-radius:8px;background:${gradient};opacity:0.65;position:relative;">
          <div style="position:absolute;bottom:10px;right:12px;font-size:9px;color:rgba(${rgbaLabel},0.4);letter-spacing:1px;text-transform:uppercase;">Visuel hero</div>
        </div>
        <div style="margin:20px 24px;padding:20px;border-radius:6px;background:${invBg};color:${invText};">
          <div style="font-family:'${displayFont}',serif;font-weight:700;font-size:18px;margin-bottom:8px;color:${invHeading};">Section inversée</div>
          <div style="font-family:'${bodyFont}',sans-serif;font-size:12px;opacity:0.7;line-height:1.6;">Contenu sur fond ${isDark ? 'clair' : 'sombre'}</div>
        </div>
        <div style="display:flex;gap:4px;padding:0 24px 20px;">${swatchStrip}</div>
      </div>

      <!-- SPLIT -->
      <div class="hero-split" style="background:${bgPage};color:${textMain};">
        <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 24px;">
          <div style="font-family:'${displayFont}',serif;font-weight:700;font-size:16px;color:${navBrand};">${brandLabel}</div>
          <div style="display:flex;gap:16px;">
            <div style="width:32px;height:4px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
            <div style="width:32px;height:4px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
            <div style="width:32px;height:4px;border-radius:2px;background:${textMain};opacity:0.3;"></div>
          </div>
        </div>
        <div style="display:flex;min-height:200px;">
          <div style="flex:1;padding:24px;display:flex;flex-direction:column;justify-content:center;">
            <div style="font-family:'${displayFont}',serif;font-weight:700;font-size:28px;line-height:1.1;margin-bottom:12px;color:${titleCol};">${name}</div>
            <div style="height:4px;border-radius:2px;background:${accentCol};width:70%;opacity:0.5;margin-bottom:6px;"></div>
            <div style="height:4px;border-radius:2px;background:${accentCol};width:45%;opacity:0.3;margin-bottom:14px;"></div>
            <div style="height:3px;background:${textMain};opacity:0.12;width:90%;margin-bottom:4px;"></div>
            <div style="height:3px;background:${textMain};opacity:0.12;width:100%;margin-bottom:4px;"></div>
            <div style="height:3px;background:${textMain};opacity:0.12;width:70%;margin-bottom:14px;"></div>
            <div style="display:inline-block;padding:10px 24px;border-radius:3px;font-size:12px;font-weight:700;letter-spacing:0.5px;background:${ctaBg};color:${ctaText};font-family:'${bodyFont}',sans-serif;align-self:flex-start;">DÉCOUVRIR</div>
          </div>
          <div style="flex:1;background:${gradient};opacity:0.65;position:relative;">
            <div style="position:absolute;bottom:10px;right:12px;font-size:9px;color:rgba(${rgbaLabel},0.4);letter-spacing:1px;text-transform:uppercase;">Visuel hero</div>
          </div>
        </div>
        <div style="margin:20px 24px;padding:20px;border-radius:6px;background:${invBg};color:${invText};">
          <div style="font-family:'${displayFont}',serif;font-weight:700;font-size:18px;margin-bottom:8px;color:${invHeading};">Section inversée</div>
          <div style="font-family:'${bodyFont}',sans-serif;font-size:12px;opacity:0.7;line-height:1.6;">Contenu sur fond ${isDark ? 'clair' : 'sombre'}</div>
        </div>
        <div style="display:flex;gap:4px;padding:0 24px 20px;">${swatchStrip}</div>
      </div>
    </div>

    ${atmosphere || chosenGamuts || harmony ? `
    <div class="params-strip">
      ${atmosphere ? `<div class="param"><span class="param-label">Registre</span><span class="param-value">${atmosphere} · ${modeLabel}</span></div>` : ''}
      ${atmosphere && harmony ? '<div class="param-sep"></div>' : ''}
      ${harmony ? `<div class="param"><span class="param-label">Harmonie</span><span class="param-value">${harmony}</span></div>` : ''}
      ${harmony && chosenGamuts ? '<div class="param-sep"></div>' : ''}
      ${chosenGamuts ? `<div class="param"><span class="param-label">Gammes</span><span class="param-value">${chosenGamuts}</span></div>` : ''}
    </div>` : ''}
  </div>`;
}

// ── Specimen content (fonts + readability tests) ──

function conceptHtml(concept) {
  const { number, name, displayFont, bodyFont, colors } = concept;
  const palette = flatPalette(colors);

  const swatches = colors.map(c => {
    const isLight = luminance(c.hex) > 0.85;
    const border = isLight ? 'border:1px solid #ddd;' : '';
    return `
    <div class="swatch-col">
      <div class="swatch" style="background:${c.hex};color:${contrastText(c.hex)};${border}">
        <span class="swatch-label">${c.hex}</span>
      </div>
      <div class="swatch-name">${c.name}</div>
      <div class="swatch-role">${c.role}</div>
    </div>`;
  }).join('');

  // Readability tests
  const sorted = [...palette].sort((a, b) => luminance(a) - luminance(b));
  const dark = sorted[0];
  const light = sorted[sorted.length - 1];

  const textOnDarkRows = palette.map(textColor => `
    <div class="combo-row" style="background:${dark}; color:${textColor}">
      <span class="combo-swatch" style="background:${textColor}"></span>
      <span class="combo-text" style="font-family:'${displayFont}',serif; font-size:28px; font-weight:700">
        Titre ${textColor}
      </span>
      <span class="combo-body" style="font-family:'${bodyFont}',sans-serif; font-size:15px">
        Corps de texte — lisibilité sur fond sombre
      </span>
    </div>
  `).join('');

  const textOnLightRows = palette.map(textColor => `
    <div class="combo-row" style="background:${light}; color:${textColor}">
      <span class="combo-swatch" style="background:${textColor}"></span>
      <span class="combo-text" style="font-family:'${displayFont}',serif; font-size:28px; font-weight:700">
        Titre ${textColor}
      </span>
      <span class="combo-body" style="font-family:'${bodyFont}',sans-serif; font-size:15px">
        Corps de texte — lisibilité sur fond clair
      </span>
    </div>
  `).join('');

  const bgCombos = palette.slice(0, 3).map(bg => `
    <div class="text-on-bg" style="background:${bg}; color:${contrastText(bg)}">
      <h3 style="font-family:'${displayFont}',serif; font-size:28px; margin:0 0 8px; font-weight:700">
        Titre sur ${bg}
      </h3>
      <p style="font-family:'${bodyFont}',sans-serif; font-size:15px; line-height:1.6; margin:0">
        Le renard brun rapide saute par-dessus le chien paresseux.
        Corps de texte sur fond coloré — vérification de lisibilité et d'harmonie.
      </p>
    </div>
  `).join('');

  return `
  <div class="concept">
    <div class="concept-header">CONCEPT ${number} — "${name}"</div>

    <div class="font-section">
      <div class="font-label">Display — ${displayFont}</div>
      <h1 style="font-family:'${displayFont}',serif; font-size:56px; font-weight:700; margin:0 0 4px; line-height:1.1">
        ${displayFont}
      </h1>
      <h2 style="font-family:'${displayFont}',serif; font-size:36px; font-weight:400; margin:0 0 4px; line-height:1.2">
        AaBbCcDdEeFfGg 0123456789
      </h2>
      <p style="font-family:'${displayFont}',serif; font-size:24px; font-weight:700; margin:0; line-height:1.4; color:#555">
        Le design est l'ambassadeur silencieux de votre marque — Paul Rand
      </p>
    </div>

    <div class="font-section">
      <div class="font-label">Body — ${bodyFont}</div>
      <p style="font-family:'${bodyFont}',sans-serif; font-size:16px; font-weight:400; line-height:1.7; margin:0 0 8px">
        ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 &amp;@€!?#%
      </p>
      <p style="font-family:'${bodyFont}',sans-serif; font-size:16px; font-weight:400; line-height:1.7; margin:0">
        Le renard brun rapide saute par-dessus le chien paresseux. Un paragraphe complet en corps de texte
        pour juger la lisibilité, le rythme, la couleur typographique et l'espacement entre les lettres.
        Les chiffres 0123456789 et la ponctuation : virgule, point-virgule ; deux-points : point d'exclamation !
      </p>
    </div>

    <div class="pairing-section">
      <div class="font-label">Pairing — ${displayFont} + ${bodyFont}</div>
      <h3 style="font-family:'${displayFont}',serif; font-size:32px; font-weight:700; margin:0 0 12px; line-height:1.2">
        Un titre en display suivi de body text
      </h3>
      <p style="font-family:'${bodyFont}',sans-serif; font-size:16px; font-weight:400; line-height:1.7; margin:0">
        Ce paragraphe montre le contraste entre le titre et le corps de texte. Le pairing typographique
        crée une hiérarchie visuelle qui guide l'oeil du lecteur. On vérifie ici que les deux familles
        cohabitent harmonieusement et que le contraste est suffisant sans être discordant.
      </p>
    </div>

    ${concept.gamutScan ? `
    <div class="font-label" style="margin-top:32px">Scan des gammes chromatiques</div>
    <div class="gamut-scan">
      <div class="gamut-chosen">Gammes choisies : <strong>${concept.chosenGamuts || '—'}</strong> · Harmonie : <strong>${concept.harmony || '—'}</strong></div>
      <table class="gamut-table">
        <thead><tr><th>Gamme</th><th>Affinité</th><th>Justification</th></tr></thead>
        <tbody>
          ${concept.gamutScan.map(g => `
            <tr class="gamut-${g.affinity.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')}">
              <td class="gamut-name">${g.gamut}</td>
              <td class="gamut-affinity"><span class="badge-${g.affinity.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')}">${g.affinity}</span></td>
              <td class="gamut-reason">${g.reason}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>` : ''}

    <div class="font-label" style="margin-top:32px">Palette</div>
    <div class="palette-grid">${swatches}</div>

    <div class="font-label" style="margin-top:32px">Lisibilité — chaque couleur sur fond sombre (${dark})</div>
    <div class="combo-grid">${textOnDarkRows}</div>

    <div class="font-label" style="margin-top:24px">Lisibilité — chaque couleur sur fond clair (${light})</div>
    <div class="combo-grid">${textOnLightRows}</div>

    <div class="font-label" style="margin-top:32px">Texte sur fonds colorés</div>
    <div class="bg-combos">${bgCombos}</div>
  </div>`;
}

// ── Full HTML ──

function generateSingleHtml(concept) {
  const fontsUrl = buildFontsUrl([concept]);
  const mockup = mockupHtml(concept);
  const content = conceptHtml(concept);

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Specimen — ${concept.name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="${fontsUrl}" rel="stylesheet">
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0; padding: 32px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #FAFAFA; color: #1A1A1A;
    }

    /* ============ TOGGLE SWITCH ============ */
    .toggle-switch {
      margin-left: auto; display: flex; align-items: center;
      background: rgba(255,255,255,0.2); border-radius: 10px; padding: 2px;
      cursor: pointer; user-select: none;
      font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .toggle-switch .opt {
      padding: 2px 8px; border-radius: 8px; color: rgba(255,255,255,0.5); transition: all 0.15s;
    }
    .toggle-switch .opt.active {
      background: rgba(255,255,255,0.9); color: #333; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* ============ MOCK-UP PREVIEW ============ */
    .mockup-section { margin-bottom: 32px; }
    .mockup-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #AAA; margin-bottom: 12px; }
    .mockup-card { border-radius: 12px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.08); max-width: 560px; }
    .mockup-chrome { height: 32px; display: flex; align-items: center; padding: 0 12px; gap: 6px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; }
    .dot-r { background: #ff5f57; }
    .dot-y { background: #febc2e; }
    .dot-g { background: #28c840; }

    /* Hero toggle */
    .hero-stacked { display: block; }
    .hero-split { display: none; }
    .mockup-card.mode-split .hero-stacked { display: none; }
    .mockup-card.mode-split .hero-split { display: block; }

    .params-strip { display: flex; align-items: center; gap: 16px; margin-top: 16px; padding: 12px 16px; background: #fff; border: 1px solid #E5E7EB; border-radius: 8px; max-width: 560px; }
    .param { display: flex; flex-direction: column; gap: 2px; }
    .param-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #AAA; }
    .param-value { font-size: 13px; font-weight: 600; color: #333; }
    .param-sep { width: 1px; height: 28px; background: #E5E7EB; }

    /* ============ SPECIMEN ============ */
    .concept {
      background: #FFFFFF; border: 1px solid #E5E7EB;
      border-radius: 12px; padding: 32px;
    }
    .concept-header {
      font-size: 13px; text-transform: uppercase; letter-spacing: 2px;
      color: #888; margin-bottom: 24px; padding-bottom: 12px;
      border-bottom: 1px solid #F0F0F0;
    }
    .font-section { margin-bottom: 24px; }
    .pairing-section {
      margin-top: 24px; padding: 24px;
      background: #F8F9FA; border-radius: 8px;
    }
    .font-label {
      font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px;
      color: #AAA; margin-bottom: 10px;
    }
    .palette-grid {
      display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; margin-top: 8px;
    }
    .swatch-col { display: flex; flex-direction: column; gap: 2px; }
    .swatch {
      height: 56px; border-radius: 8px;
      display: flex; align-items: flex-end; padding: 6px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .swatch-label { font-size: 10px; font-family: monospace; }
    .swatch-name { font-size: 10px; font-weight: 600; color: #333; text-align: center; }
    .swatch-role { font-size: 8px; color: #BBB; text-align: center; }
    .gamut-scan { margin-top: 8px; }
    .gamut-chosen {
      font-size: 13px; color: #555; margin-bottom: 12px;
      padding: 8px 12px; background: #F8F9FA; border-radius: 6px;
    }
    .gamut-table {
      width: 100%; border-collapse: collapse; font-size: 13px;
    }
    .gamut-table th {
      text-align: left; padding: 6px 10px; border-bottom: 2px solid #E5E7EB;
      font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #888;
    }
    .gamut-table td { padding: 6px 10px; border-bottom: 1px solid #F0F0F0; }
    .gamut-name { font-weight: 600; }
    .gamut-reason { color: #666; font-style: italic; }
    .badge-forte { background: #D4EDDA; color: #155724; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .badge-moderee { background: #FFF3CD; color: #856404; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .badge-faible { background: #F8D7DA; color: #721C24; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .gamut-forte td { background: #F8FFF8; }
    .gamut-moderee td { background: #FFFEF8; }
    .gamut-faible td { background: #FFF8F8; }
    .bg-combos {
      display: flex; flex-direction: column; gap: 10px; margin-top: 8px;
    }
    .text-on-bg {
      padding: 20px 28px; border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .combo-grid {
      display: flex; flex-direction: column; gap: 2px; margin-top: 8px;
      border-radius: 8px; overflow: hidden;
    }
    .combo-row {
      display: flex; align-items: center; gap: 16px;
      padding: 12px 20px;
    }
    .combo-swatch {
      width: 20px; height: 20px; border-radius: 4px; flex-shrink: 0;
      border: 1px solid rgba(128,128,128,0.3);
    }
    .combo-text { flex-shrink: 0; }
    .combo-body { opacity: 0.85; }
  </style>
</head>
<body>
  ${mockup}
  ${content}
  <script>
  function toggleMockup(num, sw) {
    const card = document.getElementById('mockup-' + num);
    const isSplit = card.classList.toggle('mode-split');
    sw.querySelector('[data-mode="stacked"]').classList.toggle('active', !isSplit);
    sw.querySelector('[data-mode="split"]').classList.toggle('active', isSplit);
  }
  </script>
</body>
</html>`;
}

// ── Main ──

async function main() {
  console.log(`Generating font+palette specimens for ${brand} (${config.concepts.length} concepts)...`);

  const browser = await puppeteer.launch({
    headless: 'new',
    protocolTimeout: 120000,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  let exitCode = 0;
  try {
    for (const concept of config.concepts) {
      const num = concept.number;

      const html = generateSingleHtml(concept);
      const htmlPath = path.join(sessionDir, `${brand}-specimen-c${num}.html`);
      fs.writeFileSync(htmlPath, html, 'utf-8');
      console.log(`  ✓ ${brand}-specimen-c${num}.html`);

      const page = await browser.newPage();
      await page.setViewport({ width: VIEWPORT_WIDTH, height: 2200 });

      const fileUrl = pathToFileURL(htmlPath).href;
      await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

      await page.waitForFunction(() => document.fonts.ready, { timeout: FONT_WAIT_TIMEOUT })
        .catch(() => console.warn(`  ⚠ Fonts timeout concept ${num} — continuing`));

      await new Promise(resolve => setTimeout(resolve, 1000));

      const screenshotPath = path.join(sessionDir, `${brand}-specimen-c${num}.png`);
      try {
        await page.screenshot({ fullPage: false, path: screenshotPath });
        console.log(`  ✓ ${brand}-specimen-c${num}.png`);
      } catch (ssErr) {
        console.warn(`  ⚠ Screenshot timeout concept ${num} — HTML ok, continuing`);
      }

      await page.close();
    }
  } catch (err) {
    console.error('Erreur Puppeteer:', err.message);
    exitCode = 1;
  } finally {
    await browser.close();
  }

  console.log('Specimen terminé.');
  process.exit(exitCode);
}

main();
