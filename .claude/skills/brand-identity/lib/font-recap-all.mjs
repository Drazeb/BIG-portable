#!/usr/bin/env node

/**
 * Font Recap All — Unified font selection overview for BIG Phase 3B.
 *
 * Generates a single HTML page showing the 3 concepts side by side with
 * their chosen fonts (display + body) and backups, all rendered in the
 * actual Google Fonts. Allows the user to visually compare at a glance.
 *
 * Usage:
 *   node lib/font-recap-all.mjs <session_dir> <brand>
 *
 * Expects a JSON config at: <session_dir>/.tmp-font-recap-config.json
 *
 * Config format:
 * {
 *   "brandName": "Atelier Vermeil",
 *   "concepts": [
 *     {
 *       "number": 1,
 *       "name": "Le Chantier Radieux",
 *       "intention": "2-3 phrases résumant l'intention créative",
 *       "display": ["Instrument Serif", "Playfair Display", "DM Serif Text"],
 *       "body": ["DM Sans", "Inter", "Source Sans 3"]
 *     }
 *   ]
 * }
 *
 * Output:
 *   <session_dir>/<brand>-font-recap-all.html
 */

import path from 'path';
import fs from 'fs';

const [,, sessionDir, brand] = process.argv;

if (!sessionDir || !brand) {
  console.error('Usage: node font-recap-all.mjs <session_dir> <brand>');
  process.exit(1);
}

const configPath = path.join(sessionDir, '.tmp-font-recap-config.json');
if (!fs.existsSync(configPath)) {
  console.error(`Config not found: ${configPath}`);
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
const { brandName, concepts } = config;

// Collect all unique font families for Google Fonts loading
const allFonts = new Set();
for (const c of concepts) {
  for (const f of [...c.display, ...c.body]) {
    allFonts.add(f);
  }
}

const googleFontsLinks = [...allFonts]
  .map(f => `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=${encodeURIComponent(f)}:wght@400;700&display=swap">`)
  .join('\n  ');

const bodyText = `La marque ${brandName} accompagne ses partenaires dans une démarche exigeante, où chaque détail compte. Notre approche combine rigueur opérationnelle et vision stratégique pour des résultats mesurables.`;

function renderFontBlock(fontName, role, isBackup, isDisplay) {
  const size = isDisplay
    ? (isBackup ? '24px' : '36px')
    : (isBackup ? '14px' : '16px');
  const weight = isDisplay ? '700' : '400';
  const sampleText = isDisplay ? brandName : bodyText;
  const bgStyle = isBackup ? 'background: #fafaf8; border: 1px solid #f0ede8; border-radius: 6px; padding: 12px 16px;' : 'padding: 12px 16px;';
  const label = isBackup ? `<div style="font: 11px/1.4 system-ui; color: #9ca3af; margin-top: 4px;">${fontName}</div>` : '';
  const roleTag = isBackup
    ? `<span style="font: 10px/1 system-ui; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em;">backup</span>`
    : `<span style="font: 10px/1 system-ui; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">${role} ★</span>`;

  return `
      <div style="${bgStyle} margin-bottom: 8px;">
        ${roleTag}
        <div style="font-family: '${fontName}', serif; font-size: ${size}; font-weight: ${weight}; line-height: 1.3; margin-top: 6px; color: #1a1a1a;">
          ${sampleText}
        </div>
        ${label}
      </div>`;
}

function renderConcept(concept) {
  const [displayMain, ...displayBackups] = concept.display;
  const [bodyMain, ...bodyBackups] = concept.body;

  const intentionBlock = concept.intention
    ? `<div style="padding: 16px 20px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; border-left: 4px solid #6b7280; margin-bottom: 20px;">
        <div style="font: 10px/1 system-ui; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-bottom: 8px;">C${concept.number} — ${concept.name}</div>
        <div style="font: 12px/1.6 system-ui; color: #374151;">${concept.intention}</div>
      </div>`
    : '';

  return `
    <div style="background: #fff; border-radius: 12px; padding: 28px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
      ${intentionBlock}
      <h2 style="font: 600 14px/1.3 system-ui; color: #1a1a1a; margin: 0 0 20px 0;">Concept ${concept.number} — ${concept.name}</h2>

      <h3 style="font: 600 11px/1 system-ui; text-transform: uppercase; letter-spacing: 0.08em; color: #6b7280; margin: 0 0 10px 0;">Display</h3>
      ${renderFontBlock(displayMain, 'display', false, true)}
      ${displayBackups.map(f => renderFontBlock(f, 'display', true, true)).join('')}

      <h3 style="font: 600 11px/1 system-ui; text-transform: uppercase; letter-spacing: 0.08em; color: #6b7280; margin: 20px 0 10px 0;">Body</h3>
      ${renderFontBlock(bodyMain, 'body', false, false)}
      ${bodyBackups.map(f => renderFontBlock(f, 'body', true, false)).join('')}
    </div>`;
}

const html = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Font Recap — ${brandName}</title>
  ${googleFontsLinks}
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #f5f3f0; font-family: system-ui, sans-serif; padding: 40px 32px; }
    .header { text-align: center; margin-bottom: 32px; }
    .header h1 { font: 600 20px/1.3 system-ui; color: #1a1a1a; }
    .header p { font: 13px/1.4 system-ui; color: #9ca3af; margin-top: 4px; }
    .grid { display: grid; grid-template-columns: repeat(${concepts.length}, 1fr); gap: 24px; max-width: 1400px; margin: 0 auto; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Sélection typographique — ${brandName}</h1>
    <p>Choix principaux ★ et backups pour chaque concept</p>
  </div>
  <div class="grid">
    ${concepts.map(renderConcept).join('\n    ')}
  </div>
</body>
</html>`;

const outputPath = path.join(sessionDir, `${brand}-font-recap-all.html`);
fs.writeFileSync(outputPath, html, 'utf-8');
console.log(`✓ Font recap written: ${outputPath}`);
