#!/usr/bin/env node

/**
 * Grid Visual Generator — mini-app chromatic-router-v2 (Étage 1).
 *
 * Fork minimal de .claude/skills/brand-identity/lib/gamut-visual.mjs.
 * Réutilise escHtml / luminance / buildSwatches / buildSourceTags / buildTerritoryBlock
 * et le look (cartes contexte, pills, badges). NOUVEAU : un layout MATRICE
 * (une rangée par territoire × trois colonnes d'aptitude : base | dominante | accent).
 *
 * On LIT immédiatement l'hypothèse : si la colonne « accent » de la rangée du
 * territoire énergique est peuplée de couleurs qui claquent, l'énergie survit.
 *
 * Usage :
 *   node lib/grid-visual.mjs <run_dir> <brand>
 * Lit  : <run_dir>/.tmp-grid-visual-config.json
 * Écrit: <run_dir>/01-grid-visual.html
 *
 * Config :
 * {
 *   "brandName": "...", "cursorB": 3, "cursorBLabel": "ZAG",
 *   "territories": { "principal": {name,keywords}, "secondaire": {...}, "tertiaire": {...} },
 *   "ventreMouChromatique": [{element,frequency}],
 *   "analyzedKeywords": [...],
 *   "grid": [
 *     { "role": "Principal", "name": "Maîtrise Tranquille",
 *       "gammes": [{gamut, aptitude, keyword, source, swatches:[hex]}] },
 *     { "role": "Secondaire", ... }, { "role": "Tertiaire", ... }
 *   ],
 *   "excluded": [{gamut, reason}]
 * }
 */

import path from 'path';
import fs from 'fs';

const [, , runDir, brand] = process.argv;
if (!runDir || !brand) {
  console.error('Usage: node grid-visual.mjs <run_dir> <brand>');
  process.exit(1);
}
const configPath = path.join(runDir, '.tmp-grid-visual-config.json');
if (!fs.existsSync(configPath)) {
  console.error(`Config not found: ${configPath}`);
  process.exit(1);
}
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// ── Helpers (repris de gamut-visual.mjs) ──
function escHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function luminance(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const toLinear = (c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}
function buildSwatches(hexList) {
  if (!hexList || hexList.length === 0) {
    return `<div class="gamut-swatches gs-empty" title="Pas de match catalogue — swatch indisponible">—</div>`;
  }
  return `<div class="gamut-swatches">${hexList.map((h) => {
    const border = luminance(h) > 0.85 ? 'border:1px solid #ddd;' : '';
    return `<div class="gs" style="background:${h};${border}"></div>`;
  }).join('')}</div>`;
}
function buildSourceTags(source) {
  if (!source) return '';
  const upper = String(source).toUpperCase();
  const tags = [];
  if (upper.includes('TERRITOIRE')) tags.push(`<span class="tag-source tag-territoire">Territoire</span>`);
  if (upper.includes('[SECTORIEL]')) tags.push(`<span class="tag-source tag-sectoriel">Sectoriel</span>`);
  if (upper.includes('[SLOP_RISQUE]')) tags.push(`<span class="tag-source tag-slop-risque" title="Zone training-defaults LLM">Slop risque</span>`);
  return tags.join('');
}
function buildTerritoryBlock(label, color, t) {
  if (!t) return '';
  const pills = (t.keywords || []).map((k) => `<span class="kw-pill">${escHtml(k)}</span>`).join('');
  return `
    <div class="territory-block">
      <div class="territory-label" style="color:${color};">${label}</div>
      <div class="territory-name">${escHtml(t.name)}</div>
      <div class="territory-keywords">${pills}</div>
    </div>`;
}
function buildVmItems(items) {
  return (items || []).map((v) => `
    <div class="vm-item"><span class="vm-freq">${escHtml(v.frequency)}</span><span>${escHtml(v.element)}</span></div>`).join('');
}
function vmModeNote(b) {
  if (b === 1) return 'Mode B=1 (Mimétisme) : inclusion obligatoire des gammes sectorielles';
  if (b === 3) return 'Mode B=3 (ZAG) : exclusion obligatoire des gammes sectorielles';
  return 'Mode B=2 (Distinction) : inclusion conditionnelle';
}

// ── Matrice territoire × aptitude ──
const APTITUDES = ['base', 'dominante', 'accent'];
const APT_LABEL = { base: 'Base — fonds & textes', dominante: 'Dominante — identité', accent: 'Accent — éclat' };

function buildGammeChip(g) {
  return `
    <div class="chip">
      ${buildSwatches(g.swatches || [])}
      <div class="chip-info">
        <div class="chip-name">${escHtml(g.gamut)} ${buildSourceTags(g.source)}</div>
        ${g.keyword ? `<div class="chip-kw">${escHtml(g.keyword)}</div>` : ''}
      </div>
    </div>`;
}

function buildMatrixRow(row) {
  const cells = APTITUDES.map((apt) => {
    const gammes = (row.gammes || []).filter((g) => (g.aptitude || '').toLowerCase() === apt);
    const inner = gammes.length
      ? gammes.map(buildGammeChip).join('')
      : `<div class="cell-empty">—</div>`;
    const emptyCls = gammes.length ? '' : ' is-empty';
    return `<td class="cell cell-${apt}${emptyCls}">${inner}</td>`;
  }).join('');
  return `
    <tr>
      <th class="row-head">
        <div class="row-role">${escHtml(row.role)}</div>
        <div class="row-name">${escHtml(row.name)}</div>
      </th>
      ${cells}
    </tr>`;
}

function generateHtml() {
  const { brandName, cursorB, cursorBLabel, territories, ventreMouChromatique, analyzedKeywords, grid, excluded } = config;

  const territoriesHtml = [
    buildTerritoryBlock('Principal — donne le ton dominant', '#2563EB', territories?.principal),
    buildTerritoryBlock('Secondaire — apporte de la profondeur', '#7C3AED', territories?.secondaire),
    buildTerritoryBlock('Tertiaire — touche distinctive', '#0891B2', territories?.tertiaire),
  ].join('');

  const vmHtml = (ventreMouChromatique && ventreMouChromatique.length)
    ? `<div class="context-card">
         <div class="context-card-header">Ventre Mou sectoriel — éléments chromatiques</div>
         <div class="vm-grid">${buildVmItems(ventreMouChromatique)}</div>
         <div class="vm-label-note">${vmModeNote(cursorB)}</div>
       </div>` : '';

  const keywordsHtml = (analyzedKeywords || []).map((k) => `<span class="analyzed-kw">${escHtml(k)}</span>`).join('');
  const headerCells = APTITUDES.map((a) => `<th class="col-head col-${a}">${APT_LABEL[a]}</th>`).join('');
  const matrixRows = (grid || []).map(buildMatrixRow).join('');
  const excludedHtml = (excluded || []).map((g) => `
    <div class="excl-card">
      ${buildSwatches(g.swatches || [])}
      <div class="excl-info"><div class="excl-name">${escHtml(g.gamut)} ${buildSourceTags(g.source)}</div><div class="excl-reason">${escHtml(g.reason || '')}</div></div>
    </div>`).join('');

  return `<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grille chromatique — ${escHtml(brandName)}</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #F5F5F5; color: #1A1A1A; padding: 32px; max-width: 1280px; margin: 0 auto; }
  .page-title { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
  .page-subtitle { font-size: 14px; color: #888; margin-bottom: 28px; }
  .context-card { background: #FFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; }
  .context-card-header { font-size: 10px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #9CA3AF; margin-bottom: 12px; }
  .territory-block { margin-bottom: 14px; } .territory-block:last-child { margin-bottom: 0; }
  .territory-label { font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 6px; }
  .territory-name { font-size: 15px; font-weight: 600; margin-bottom: 4px; }
  .territory-keywords { display: flex; flex-wrap: wrap; gap: 6px; }
  .kw-pill { font-size: 11px; padding: 3px 10px; border-radius: 20px; background: #F3F4F6; color: #4B5563; font-weight: 500; }
  .vm-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px; }
  .vm-item { display: flex; align-items: flex-start; gap: 10px; font-size: 13px; line-height: 1.5; color: #374151; padding: 10px 14px; background: #FEF3C7; border-radius: 8px; border-left: 3px solid #F59E0B; }
  .vm-freq { font-size: 10px; font-weight: 700; color: #D97706; white-space: nowrap; flex-shrink: 0; background: #FDE68A; padding: 2px 8px; border-radius: 10px; }
  .vm-label-note { font-size: 11px; color: #9CA3AF; margin-top: 8px; font-style: italic; }
  .section-divider { border: none; border-top: 1px solid #E5E7EB; margin: 28px 0; }
  .kw-header { margin-bottom: 8px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; color: #9CA3AF; }
  .analyzed-keywords { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 24px; }
  .analyzed-kw { font-size: 12px; padding: 4px 12px; border-radius: 20px; background: #EFF6FF; color: #2563EB; font-weight: 600; }

  .matrix { width: 100%; border-collapse: separate; border-spacing: 8px; }
  .col-head { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: #6B7280; padding: 8px 12px; text-align: left; vertical-align: bottom; }
  .col-base { color: #6B7280; } .col-dominante { color: #B45309; } .col-accent { color: #BE185D; }
  .row-head { width: 200px; text-align: left; vertical-align: top; padding: 14px 14px; background: #FFF; border: 1px solid #E5E7EB; border-radius: 10px; }
  .row-role { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: #9CA3AF; margin-bottom: 4px; }
  .row-name { font-size: 14px; font-weight: 700; }
  .cell { vertical-align: top; padding: 10px; border-radius: 10px; min-width: 220px; background: #FFF; border: 1px solid #E5E7EB; }
  .cell-base { background: #FBFBFB; }
  .cell-dominante { background: #FFFBF5; border-color: #FDE9C8; }
  .cell-accent { background: #FFF5F9; border-color: #FBD5E5; }
  .cell.is-empty { background: repeating-linear-gradient(45deg,#FAFAFA,#FAFAFA 6px,#F0F0F0 6px,#F0F0F0 12px); }
  .cell-empty { color: #C0C0C0; font-size: 20px; text-align: center; padding: 14px 0; }

  .chip { display: flex; gap: 10px; align-items: flex-start; padding: 8px; border-radius: 8px; margin-bottom: 8px; background: #FFF; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
  .chip:last-child { margin-bottom: 0; }
  .gamut-swatches { display: flex; flex-direction: column; gap: 2px; flex-shrink: 0; }
  .gs { width: 30px; height: 30px; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.12); }
  .gs-empty { width: 30px; height: 30px; border-radius: 5px; border: 1px dashed #D1D5DB; color: #C0C0C0; display: flex; align-items: center; justify-content: center; font-size: 14px; }
  .chip-info { flex: 1; min-width: 0; }
  .chip-name { font-size: 12px; font-weight: 700; line-height: 1.3; display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
  .chip-kw { font-size: 11px; color: #9CA3AF; margin-top: 3px; }
  .tag-source { font-size: 8px; font-weight: 700; letter-spacing: .05em; padding: 2px 6px; border-radius: 4px; text-transform: uppercase; }
  .tag-territoire { background: #ECFDF5; color: #059669; }
  .tag-sectoriel { background: #FEF3C7; color: #D97706; }
  .tag-slop-risque { background: #FEE2E2; color: #B91C1C; border: 1px solid #FCA5A5; }

  .excl-section-header { font-size: 16px; font-weight: 700; margin: 28px 0 14px; display: flex; align-items: center; gap: 10px; }
  .count { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
  .count-excluded { background: #FEF2F2; color: #DC2626; }
  .count-nonret { background: #F3F4F6; color: #6B7280; }
  .excl-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; }
  .excl-card { background: #FFF; border: 1px solid #E5E7EB; border-left: 4px solid #DC2626; border-radius: 8px; padding: 12px 14px; display: flex; gap: 12px; align-items: flex-start; }
  .excl-info { flex: 1; min-width: 0; }
  .excl-name { font-size: 13px; font-weight: 700; text-decoration: line-through; text-decoration-color: #DC2626; }
  .excl-reason { font-size: 12px; color: #6B7280; margin-top: 4px; }
  .nonret-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 8px; opacity: 0.78; }
  .nonret-card { background: #FAFAFA; border: 1px solid #ECECEC; border-radius: 8px; padding: 8px 10px; display: flex; gap: 10px; align-items: center; }
  .nonret-name { font-size: 12px; color: #6B7280; }
  .legend { margin-top: 24px; padding: 16px 20px; background: #FFF; border: 1px solid #E5E7EB; border-radius: 12px; font-size: 13px; color: #555; line-height: 1.6; }
  .legend strong { color: #1A1A1A; }
</style></head><body>

  <div class="page-title">Grille chromatique — ${escHtml(brandName)}</div>
  <div class="page-subtitle">Routeur v2 (mini-app de test) · territoire × aptitude · Curseur B=${cursorB} (${escHtml(cursorBLabel)})</div>

  <div class="context-card">
    <div class="context-card-header">Territoires créatifs (décontaminés)</div>
    ${territoriesHtml}
  </div>
  ${vmHtml}

  <hr class="section-divider">
  <div class="kw-header">Mots-clés dominants analysés</div>
  <div class="analyzed-keywords">${keywordsHtml}</div>

  <hr class="section-divider">
  <table class="matrix">
    <thead><tr><th class="row-head" style="background:transparent;border:none;"></th>${headerCells}</tr></thead>
    <tbody>${matrixRows}</tbody>
  </table>

  ${excludedHtml ? `<div class="excl-section-header">Gammes exclues <span class="count count-excluded">${(excluded || []).length}</span></div><div class="excl-grid">${excludedHtml}</div>` : ''}

  <div class="legend">
    <strong>Lecture :</strong> chaque rangée = un territoire ; chaque colonne = une aptitude fonctionnelle.
    L'hypothèse du test : la colonne <strong>Accent</strong> de la rangée du territoire énergique doit être
    peuplée de couleurs qui claquent (l'énergie survit), et chacune des trois colonnes doit avoir au moins une gamme.<br>
    Swatches = hex indicatifs du catalogue (pas la palette finale). « — » = pas de match catalogue (gamme hors-catalogue).
  </div>

</body></html>`;
}

const html = generateHtml();
const outputPath = path.join(runDir, `${brand}-grid-visual.html`);
fs.writeFileSync(outputPath, html, 'utf-8');
console.log(`  ✓ ${brand}-grid-visual.html`);
