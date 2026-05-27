#!/usr/bin/env node

/**
 * Gamut Visual Generator for BIG Phase 3B-0a.
 *
 * Generates a single HTML page showing authorized and excluded chromatic gamuts
 * produced by the chromatic router, with territory context and Ventre Mou info.
 *
 * Usage:
 *   node lib/gamut-visual.mjs <session_dir> <brand>
 *
 * Expects a JSON config at: <session_dir>/.tmp-gamut-visual-config.json
 *
 * Config format:
 * {
 *   "brandName": "Camille",
 *   "cursorB": 2,
 *   "cursorBLabel": "Distinction",
 *   "territories": {
 *     "principal": { "name": "Dévoilement Stratégique", "keywords": ["Chirurgicale", "Lucide", ...] },
 *     "secondaire": { "name": "Cap Long Terme", "keywords": ["Projection", ...] },
 *     "tertiaire": { "name": "Autorité Sans Costume", "keywords": ["Artisanale-premium", ...] }
 *   },
 *   "ventreMouChromatique": [
 *     { "element": "Bleu comme couleur primaire (électrique, roi, marine ou cyan)", "frequency": "4/4" },
 *     { "element": "Gradient bleu-violet", "frequency": "2/4" }
 *   ],
 *   "analyzedKeywords": ["Chirurgicale", "Lucide", ...],
 *   "authorized": [
 *     { "gamut": "Terres brûlées profondes", "reason": "...", "source": "TERRITOIRE", "swatches": ["#8B4513", "#A0522D", "#D2691E"] },
 *     { "gamut": "Bleus tech", "reason": "...", "source": "[SECTORIEL]", "swatches": ["#0066FF", "#0033CC"] }
 *   ],
 *   "excluded": [
 *     { "gamut": "Bleus tech / corporate", "reason": "...", "swatches": ["#0066FF", "#0033CC"] }
 *   ]
 * }
 *
 * Output:
 *   {session_dir}/{brand}-gamuts-visual.html
 */

import path from 'path';
import fs from 'fs';

const [,, sessionDir, brand] = process.argv;

if (!sessionDir || !brand) {
  console.error('Usage: node gamut-visual.mjs <session_dir> <brand>');
  process.exit(1);
}

const configPath = path.join(sessionDir, '.tmp-gamut-visual-config.json');
if (!fs.existsSync(configPath)) {
  console.error(`Config not found: ${configPath}`);
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// ── Helpers ──

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function luminance(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const toLinear = (c) => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}

// ── Builders ──

function buildTerritoryBlock(role, label, color, t) {
  const pills = t.keywords.map(k => `<span class="kw-pill">${escHtml(k)}</span>`).join('');
  return `
    <div class="territory-block">
      <div class="territory-label" style="color:${color};">${label}</div>
      <div class="territory-name">${escHtml(t.name)}</div>
      <div class="territory-keywords">${pills}</div>
    </div>`;
}

function buildVmItems(items) {
  return items.map(v => `
    <div class="vm-item">
      <span class="vm-freq">${escHtml(v.frequency)}</span>
      <span>${escHtml(v.element)}</span>
    </div>`).join('');
}

function vmModeNote(b) {
  if (b === 1) return 'Mode B=1 (Mimétisme) : inclusion obligatoire — gammes sectorielles forcées en autorisées';
  if (b === 3) return 'Mode B=3 (ZAG) : exclusion obligatoire — gammes sectorielles forcées en exclues';
  return 'Mode B=2 (Distinction) : inclusion conditionnelle — autorisées uniquement si cohérentes avec les territoires';
}

function buildSwatches(hexList) {
  if (!hexList || hexList.length === 0) return '';
  if (hexList.length === 1) {
    const isLight = luminance(hexList[0]) > 0.85;
    const border = isLight ? 'border:1px solid #ddd;' : '';
    return `<div class="gamut-swatches"><div class="gs" style="background:${hexList[0]};${border}"></div></div>`;
  }
  return `<div class="gamut-swatches">${hexList.map(h => {
    const isLight = luminance(h) > 0.85;
    const border = isLight ? 'border:1px solid #ddd;' : '';
    return `<div class="gs" style="background:${h};${border}"></div>`;
  }).join('')}</div>`;
}

function buildSourceTags(source) {
  // Parse the source string and emit one badge per tag.
  // Supported tags (cumulable) : TERRITOIRE, [SECTORIEL], [SLOP_RISQUE]
  if (!source) return '';
  const upper = String(source).toUpperCase();
  const tags = [];
  if (upper.includes('TERRITOIRE')) {
    tags.push(`<span class="tag-source tag-territoire">Territoire</span>`);
  }
  if (upper.includes('[SECTORIEL]')) {
    tags.push(`<span class="tag-source tag-sectoriel">Sectoriel</span>`);
  }
  if (upper.includes('[SLOP_RISQUE]')) {
    tags.push(`<span class="tag-source tag-slop-risque" title="Zone training-defaults LLM — vigilance requise sur les hex choisis en aval">Slop risque</span>`);
  }
  return tags.join('');
}

function buildGamutCard(g, kind) {
  // kind = 'authorized' | 'excluded' | 'nonApplicable'
  const cls = kind === 'excluded' ? 'gamut-card excluded'
            : kind === 'nonApplicable' ? 'gamut-card non-applicable'
            : 'gamut-card';
  const sourceTags = kind === 'authorized' ? buildSourceTags(g.source) : '';
  return `
    <div class="${cls}">
      ${buildSwatches(g.swatches || [])}
      <div class="gamut-info">
        <div class="gamut-name">${escHtml(g.gamut)} ${sourceTags}</div>
        <div class="gamut-reason">${escHtml(g.reason)}</div>
      </div>
    </div>`;
}

// ── Full HTML ──

function generateHtml() {
  const { brandName, cursorB, cursorBLabel, territories, ventreMouChromatique, analyzedKeywords, authorized, excluded, nonApplicable } = config;

  const territoriesHtml = [
    buildTerritoryBlock('principal', 'Principal — donne le ton dominant', '#2563EB', territories.principal),
    buildTerritoryBlock('secondaire', 'Secondaire — apporte de la profondeur', '#7C3AED', territories.secondaire),
    buildTerritoryBlock('tertiaire', 'Tertiaire — touche distinctive', '#0891B2', territories.tertiaire),
  ].join('');

  const vmHtml = ventreMouChromatique && ventreMouChromatique.length > 0
    ? `<div class="context-card">
        <div class="context-card-header">Ventre Mou sectoriel — éléments chromatiques</div>
        <div class="vm-grid">${buildVmItems(ventreMouChromatique)}</div>
        <div class="vm-label-note">${vmModeNote(cursorB)}</div>
       </div>`
    : '';

  const keywordsHtml = (analyzedKeywords || []).map(k => `<span class="analyzed-kw">${escHtml(k)}</span>`).join('');

  const authorizedHtml = (authorized || []).map(g => buildGamutCard(g, 'authorized')).join('');
  const excludedHtml = (excluded || []).map(g => buildGamutCard(g, 'excluded')).join('');
  const nonApplicableHtml = (nonApplicable || []).map(g => buildGamutCard(g, 'nonApplicable')).join('');

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gammes chromatiques — ${escHtml(brandName)}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #F5F5F5; color: #1A1A1A; padding: 32px;
      max-width: 1200px; margin: 0 auto;
    }
    .page-title { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
    .page-subtitle { font-size: 14px; color: #888; margin-bottom: 32px; }

    .context-card {
      background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;
      padding: 20px 24px; margin-bottom: 16px;
    }
    .context-card-header {
      font-size: 10px; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #9CA3AF; margin-bottom: 12px;
    }

    .territory-block { margin-bottom: 14px; }
    .territory-block:last-child { margin-bottom: 0; }
    .territory-label {
      font-size: 10px; font-weight: 700; letter-spacing: .08em;
      text-transform: uppercase; margin-bottom: 6px;
    }
    .territory-name { font-size: 15px; font-weight: 600; color: #1A1A1A; margin-bottom: 4px; }
    .territory-keywords { display: flex; flex-wrap: wrap; gap: 6px; }
    .kw-pill {
      font-size: 11px; padding: 3px 10px; border-radius: 20px;
      background: #F3F4F6; color: #4B5563; font-weight: 500;
    }

    .vm-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px; }
    .vm-item {
      display: flex; align-items: flex-start; gap: 10px;
      font-size: 13px; line-height: 1.5; color: #374151;
      padding: 10px 14px; background: #FEF3C7; border-radius: 8px;
      border-left: 3px solid #F59E0B;
    }
    .vm-freq {
      font-size: 10px; font-weight: 700; color: #D97706;
      white-space: nowrap; flex-shrink: 0;
      background: #FDE68A; padding: 2px 8px; border-radius: 10px;
    }
    .vm-label-note { font-size: 11px; color: #9CA3AF; margin-top: 8px; font-style: italic; }

    .section-divider { border: none; border-top: 1px solid #E5E7EB; margin: 32px 0; }

    .gamut-section-header {
      font-size: 18px; font-weight: 700; margin-bottom: 16px;
      display: flex; align-items: center; gap: 10px;
    }
    .count { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
    .count-authorized { background: #ECFDF5; color: #059669; }
    .count-excluded { background: #FEF2F2; color: #DC2626; }
    .count-non-applicable { background: #F3F4F6; color: #6B7280; }

    .analyzed-keywords { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 24px; }
    .analyzed-kw {
      font-size: 12px; padding: 4px 12px; border-radius: 20px;
      background: #EFF6FF; color: #2563EB; font-weight: 600;
    }
    .kw-header {
      margin-bottom: 8px; font-size: 11px; font-weight: 600;
      text-transform: uppercase; letter-spacing: .1em; color: #9CA3AF;
    }

    .gamuts-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 12px;
      margin-bottom: 32px;
    }
    .gamut-card {
      background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px;
      padding: 16px 18px; display: flex; gap: 14px; align-items: flex-start;
      transition: box-shadow 0.15s;
    }
    .gamut-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .gamut-card.excluded { background: #FFFFFF; border-left: 4px solid #DC2626; }
    .gamut-card.non-applicable { background: #FFFFFF; border-left: 4px solid #D1D5DB; }
    .gamut-card.non-applicable .gamut-reason { font-style: italic; }

    .gamut-swatches { display: flex; flex-direction: column; gap: 3px; flex-shrink: 0; }
    .gs {
      width: 42px; height: 42px; border-radius: 6px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .gamut-info { flex: 1; min-width: 0; }
    .gamut-name {
      font-size: 14px; font-weight: 700; color: #1A1A1A; margin-bottom: 4px;
      display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    }
    .tag-source {
      font-size: 9px; font-weight: 700; letter-spacing: .06em;
      padding: 2px 8px; border-radius: 4px; text-transform: uppercase;
    }
    .tag-territoire { background: #ECFDF5; color: #059669; }
    .tag-sectoriel { background: #FEF3C7; color: #D97706; }
    .tag-slop-risque {
      background: #FEE2E2; color: #B91C1C;
      border: 1px solid #FCA5A5;
      cursor: help;
    }
    .gamut-reason { font-size: 12px; line-height: 1.5; color: #6B7280; }

    .gamut-card.excluded .gamut-name { text-decoration: line-through; text-decoration-color: #DC2626; text-decoration-thickness: 1px; }

    .accent-note {
      padding: 14px 20px; background: #F0FDF4; border: 1px solid #BBF7D0;
      border-radius: 10px; font-size: 13px; color: #166534; line-height: 1.5;
      margin-bottom: 32px;
    }
    .accent-note strong { font-weight: 700; }

    .instructions {
      margin-top: 24px; padding: 20px; background: #FFFFFF;
      border: 1px solid #E5E7EB; border-radius: 12px;
      font-size: 14px; color: #555; line-height: 1.6;
    }
    .instructions strong { color: #1A1A1A; }

    @media (max-width: 700px) {
      body { padding: 16px; }
      .gamuts-grid { grid-template-columns: 1fr; }
      .vm-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <div class="page-title">Gammes chromatiques — ${escHtml(brandName)}</div>
  <div class="page-subtitle">Routeur chromatique · Phase 3B-0a · Curseur B=${cursorB} (${escHtml(cursorBLabel)})</div>

  <div class="context-card">
    <div class="context-card-header">Territoires créatifs (décontaminés)</div>
    ${territoriesHtml}
  </div>

  ${vmHtml}

  <hr class="section-divider">

  <div class="kw-header">Mots-clés dominants analysés</div>
  <div class="analyzed-keywords">${keywordsHtml}</div>

  <hr class="section-divider">

  <div class="gamut-section-header">
    Gammes recommandées
    <span class="count count-authorized">${(authorized || []).length} gamme${(authorized || []).length > 1 ? 's' : ''}</span>
  </div>
  <div class="gamuts-grid">${authorizedHtml}</div>

  ${(nonApplicable && nonApplicable.length > 0) ? `
  <div class="gamut-section-header">
    Gammes non recommandées
    <span class="count count-non-applicable">${nonApplicable.length} gamme${nonApplicable.length > 1 ? 's' : ''}</span>
  </div>
  <div class="gamuts-grid">${nonApplicableHtml}</div>
  ` : ''}

  <div class="gamut-section-header">
    Gammes fortement non recommandées
    <span class="count count-excluded">${(excluded || []).length} gamme${(excluded || []).length > 1 ? 's' : ''}</span>
  </div>
  <div class="gamuts-grid">${excludedHtml}</div>

  <div class="accent-note">
    <strong>Accent libre</strong> — toute gamme, y compris exclue, peut être utilisée en accent si elle sert le concept narratif.
  </div>

  <div class="instructions">
    <strong>Validation :</strong> Ces gammes vous conviennent ? Si vous voulez ajuster (autoriser une gamme exclue, exclure une gamme autorisée), indiquez-le maintenant.<br>
    Répondez <strong>"OK"</strong> pour valider et continuer.
  </div>

</body>
</html>`;
}

// ── Main ──

const html = generateHtml();
const outputPath = path.join(sessionDir, `${brand}-gamuts-visual.html`);
fs.writeFileSync(outputPath, html, 'utf-8');
console.log(`  ✓ ${brand}-gamuts-visual.html`);
