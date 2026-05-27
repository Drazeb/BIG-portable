#!/usr/bin/env node

/**
 * Font Pool Contact Sheet Generator
 *
 * Generates a visual contact sheet showing all fonts in a pool,
 * each identified by number only (no font name visible).
 * Single-column layout optimized for multimodal LLM processing:
 * slightly soft resolution forces the LLM to scan all fonts
 * instead of committing early (reduces primacy bias).
 *
 * Usage:
 *   node lib/font-pool-contact-sheet.mjs <output_dir> <pool_name>
 *
 * Expects a JSON config at: <output_dir>/.tmp-pool-config.json
 *
 * Config format:
 * {
 *   "fonts": ["Font Name 1", "Font Name 2", ...],
 *   "sampleText": "Ag Stratégie & Vision 2026"
 * }
 *
 * Output:
 *   {output_dir}/font-pool-{pool_name}.png
 *   {output_dir}/font-pool-{pool_name}.html
 *   {output_dir}/font-pool-{pool_name}-mapping.json  (number → font name)
 */

import puppeteer from 'puppeteer';
import { pathToFileURL, fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const [,, outputDir, poolName] = process.argv;

if (!outputDir || !poolName) {
  console.error('Usage: node font-pool-contact-sheet.mjs <output_dir> <pool_name>');
  process.exit(1);
}

const configPath = path.join(outputDir, '.tmp-pool-config.json');
if (!fs.existsSync(configPath)) {
  console.error(`Config not found: ${configPath}`);
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
const fonts = config.fonts;
const sampleText = config.sampleText || 'Ag Stratégie & Vision 2026';
// Split mode: generate 2 planches (A/B) with larger text for better LLM readability
const splitMode = config.split === true || fonts.length > 30;

// Load font source map (Google Fonts / Fontshare / local self-host)
// Path: ref/font-source-map.json relative to skill root
const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SOURCE_MAP_PATH = path.join(SKILL_ROOT, 'ref', 'font-source-map.json');
let sourceMap = {};
if (fs.existsSync(SOURCE_MAP_PATH)) {
  sourceMap = JSON.parse(fs.readFileSync(SOURCE_MAP_PATH, 'utf-8'));
} else {
  console.warn(`⚠ Source map not found at ${SOURCE_MAP_PATH} — defaulting all fonts to 'google'`);
}

// Local fonts directory (for Velvetyne, GitHub OFL, etc.)
const LOCAL_FONTS_DIR = path.join(SKILL_ROOT, 'lib', 'fonts');

function getFontSource(fontName) {
  return sourceMap[fontName] || 'google';
}

function fontshareSlug(fontName) {
  // "Cabinet Grotesk" → "cabinet-grotesk", "Bespoke Sans" → "bespoke-sans"
  return fontName.toLowerCase().replace(/\s+/g, '-');
}

// Validate all fonts have known source ; abort if 'local' fonts not self-hosted yet
function preflightCheck(fonts) {
  const unknown = [];
  const localMissing = [];
  for (const f of fonts) {
    const src = sourceMap[f];
    if (!src) {
      unknown.push(f);
    } else if (src === 'local') {
      // Check that .woff2 file exists
      const slug = fontshareSlug(f);
      const woff2Path = path.join(LOCAL_FONTS_DIR, `${slug}.woff2`);
      if (!fs.existsSync(woff2Path)) localMissing.push(f);
    }
  }
  if (unknown.length > 0) {
    console.error(`❌ Fontes sans source map (ajouter à ref/font-source-map.json) : ${unknown.join(', ')}`);
    process.exit(2);
  }
  if (localMissing.length > 0) {
    console.error(`❌ Fontes 'local' manquantes dans ${LOCAL_FONTS_DIR} : ${localMissing.join(', ')}`);
    console.error(`   Self-host les .woff2 nécessaires (ex: ${fontshareSlug(localMissing[0])}.woff2) avant de relancer.`);
    process.exit(2);
  }
}
// Tags: optional array of category tags (e.g. ["SERIF", "SANS", "MONO"]) displayed next to numbers
// When tags.length == fonts.length, tags are indexed locally (tag[0] = first font)
// When tags.length > fonts.length, tags are indexed globally (tag[startNum-1] = first font)
const tags = config.tags || [];
// Optional startNum override from config (for sub-planches)
const configStartNum = config.startNum || null;

// Viewport tuned for "good enough" resolution — not too sharp (causes primacy bias)
// not too blurry (causes bad choices). 2400px with 48px font → ~80px per row after
// Claude's internal downscaling. Tested across 6 concepts × 3 approaches.
const VIEWPORT_WIDTH = 2400;

function buildFontsStylesheets(fonts) {
  // Bucketise par source
  const buckets = { google: [], fontshare: [], local: [] };
  for (const f of fonts) {
    const src = getFontSource(f);
    buckets[src].push(f);
  }

  const links = [];

  // Google Fonts CDN
  if (buckets.google.length > 0) {
    const families = buckets.google.map(f => `family=${encodeURIComponent(f)}:wght@400;700`);
    const url = `https://fonts.googleapis.com/css2?${families.join('&')}&display=swap`;
    links.push(`<link href="${url}" rel="stylesheet">`);
  }

  // Fontshare CDN
  if (buckets.fontshare.length > 0) {
    const families = buckets.fontshare.map(f => `f[]=${fontshareSlug(f)}@400,700`);
    const url = `https://api.fontshare.com/v2/css?${families.join('&')}&display=swap`;
    links.push(`<link href="${url}" rel="stylesheet">`);
  }

  // Local self-host (@font-face inline)
  if (buckets.local.length > 0) {
    const faces = buckets.local.map(f => {
      const slug = fontshareSlug(f);
      const woff2Url = pathToFileURL(path.join(LOCAL_FONTS_DIR, `${slug}.woff2`)).href;
      return `@font-face { font-family: '${f}'; src: url('${woff2Url}') format('woff2'); font-weight: 400 700; font-display: swap; }`;
    }).join('\n      ');
    links.push(`<style>\n      ${faces}\n    </style>`);
  }

  return links.join('\n  ');
}

function generateHtml(fonts, sampleText, { label, startNum = 1, fontSize = 48, lightFontSize = 28, fontTags = [] } = {}) {
  const stylesheets = buildFontsStylesheets(fonts);

  const rows = fonts.map((font, i) => {
    const num = startNum + i;
    // If tags array length matches fonts array length, index locally; otherwise index globally
    const tag = fontTags.length === fonts.length ? (fontTags[i] || '') : (fontTags[startNum + i - 1] || '');
    const tagHtml = tag ? `<span class="tag">${tag}</span>` : '';
    return `
    <div class="row">
      <div class="num">${String(num).padStart(2, '0')}${tagHtml}</div>
      <div class="sample" style="font-family:'${font}',serif; font-weight:700">
        ${sampleText}
      </div>
      <div class="sample-light" style="font-family:'${font}',serif; font-weight:400">
        abcdefghijklmnopqrstuvwxyz 0123456789
      </div>
    </div>`;
  }).join('');

  const displayLabel = label || poolName;

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Font Pool — ${displayLabel}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://api.fontshare.com">
  <link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
  ${stylesheets}
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #FFFFFF; color: #1A1A1A;
      padding: 24px 32px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .header {
      font-size: 11px; text-transform: uppercase; letter-spacing: 2px;
      color: #999; margin-bottom: 20px; padding-bottom: 12px;
      border-bottom: 1px solid #E5E7EB;
    }
    .row {
      display: grid;
      grid-template-columns: 60px 1fr 1fr;
      gap: 24px;
      align-items: baseline;
      padding: 14px 0;
      border-bottom: 1px solid #F5F5F5;
    }
    .num {
      font-size: 20px; font-weight: 700; color: #BBB;
      font-family: monospace;
      padding-top: 8px;
    }
    .tag {
      display: inline-block;
      font-size: 14px; font-weight: 700;
      color: #FFF; background: #888;
      padding: 3px 10px; border-radius: 4px;
      margin-left: 10px; vertical-align: middle;
      letter-spacing: 1.5px;
    }
    .sample {
      font-size: ${fontSize}px; line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .sample-light {
      font-size: ${lightFontSize}px; line-height: 1.4;
      color: #666;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  </style>
</head>
<body>
  <div class="header">Font Pool ${displayLabel} — ${fonts.length} fonts (#${String(startNum).padStart(2,'0')}–#${String(startNum + fonts.length - 1).padStart(2,'0')}) — sample: "${sampleText}"</div>
  ${rows}
</body>
</html>`;
}

async function generateSheet(browser, sheetFonts, sampleText, outputDir, fileName, opts = {}) {
  const html = generateHtml(sheetFonts, sampleText, opts);
  const htmlPath = path.join(outputDir, `${fileName}.html`);
  fs.writeFileSync(htmlPath, html, 'utf-8');
  console.log(`  ✓ ${fileName}.html`);

  const page = await browser.newPage();
  const rowHeight = opts.fontSize ? Math.round(opts.fontSize * 2.2) : 85;
  const estimatedHeight = sheetFonts.length * rowHeight + 80;
  await page.setViewport({ width: VIEWPORT_WIDTH, height: estimatedHeight });

  const fileUrl = pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

  await page.waitForFunction(() => document.fonts.ready, { timeout: 15000 })
    .catch(() => console.warn('  ⚠ Fonts timeout — continuing'));

  await new Promise(resolve => setTimeout(resolve, 2000));

  // STRICT FONT-LOADING CHECK — verify each expected font is actually loaded
  const failures = await page.evaluate((expectedFonts) => {
    return expectedFonts.filter(font => {
      // Check at both weights we actually use (400 and 700)
      const ok400 = document.fonts.check(`400 16px "${font}"`);
      const ok700 = document.fonts.check(`700 16px "${font}"`);
      return !ok400 && !ok700;
    });
  }, sheetFonts);

  if (failures.length > 0) {
    await page.close();
    throw new Error(`❌ ${failures.length}/${sheetFonts.length} fontes NON CHARGÉES dans ${fileName}: ${failures.join(', ')}`);
  }
  console.log(`  ✓ chargement vérifié : ${sheetFonts.length}/${sheetFonts.length} fontes OK`);

  const pngPath = path.join(outputDir, `${fileName}.png`);
  await page.screenshot({ fullPage: true, path: pngPath });
  console.log(`  ✓ ${fileName}.png`);

  await page.close();
}

async function main() {
  console.log(`Generating contact sheet for pool ${poolName} (${fonts.length} fonts, split=${splitMode})...`);

  // Preflight: verify all fonts have known source + 'local' fonts are self-hosted
  preflightCheck(fonts);
  const sourceCounts = fonts.reduce((acc, f) => {
    const s = getFontSource(f);
    acc[s] = (acc[s] || 0) + 1;
    return acc;
  }, {});
  console.log(`  → sources : ${Object.entries(sourceCounts).map(([k,v]) => `${v} ${k}`).join(', ')}`);

  // Write unified mapping file (number → font name) — always covers ALL fonts
  const mapping = {};
  fonts.forEach((f, i) => { mapping[String(i + 1).padStart(2, '0')] = f; });
  const mappingPath = path.join(outputDir, `font-pool-${poolName}-mapping.json`);
  fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2), 'utf-8');
  console.log(`  ✓ font-pool-${poolName}-mapping.json`);

  const browser = await puppeteer.launch({
    headless: 'new',
    protocolTimeout: 120000,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    if (splitMode) {
      // Split into 2 planches with larger text
      const mid = Math.ceil(fonts.length / 2);
      const fontsA = fonts.slice(0, mid);
      const fontsB = fonts.slice(mid);
      const splitFontSize = 72;
      const splitLightFontSize = 40;

      await generateSheet(browser, fontsA, sampleText, outputDir, `font-pool-${poolName}-A`, {
        label: `${poolName} (planche A)`, startNum: 1, fontSize: splitFontSize, lightFontSize: splitLightFontSize, fontTags: tags
      });
      await generateSheet(browser, fontsB, sampleText, outputDir, `font-pool-${poolName}-B`, {
        label: `${poolName} (planche B)`, startNum: mid + 1, fontSize: splitFontSize, lightFontSize: splitLightFontSize, fontTags: tags
      });
    } else {
      // Single planche (original behavior)
      await generateSheet(browser, fonts, sampleText, outputDir, `font-pool-${poolName}`, {
        label: poolName, startNum: configStartNum || 1, fontTags: tags
      });
    }
  } catch (err) {
    console.error('Erreur Puppeteer:', err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }

  console.log('Contact sheet terminée.');
}

main();
