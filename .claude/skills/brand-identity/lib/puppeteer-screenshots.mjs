#!/usr/bin/env node

/**
 * Puppeteer screenshot capture for BIG DA Check (Phase 4bis).
 *
 * Usage:
 *   node lib/puppeteer-screenshots.mjs <session_dir> <brand> [concept_numbers...]
 *
 * Examples:
 *   node lib/puppeteer-screenshots.mjs /path/to/outputs/brand-session brand 1 2 3
 *   node lib/puppeteer-screenshots.mjs /path/to/outputs/brand-session brand 2
 *
 * Output files per concept:
 *   {session_dir}/screenshot-c{N}-full.png   (full page, 1440px wide)
 *   {session_dir}/screenshot-c{N}-hero.png   (viewport 1440×900, above-the-fold)
 */

import puppeteer from 'puppeteer';
import { pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const [,, sessionDir, brand, ...conceptArgs] = process.argv;

if (!sessionDir || !brand) {
  console.error('Usage: node puppeteer-screenshots.mjs <session_dir> <brand> [concept_numbers...]');
  process.exit(1);
}

const concepts = conceptArgs.length > 0
  ? conceptArgs.map(Number)
  : [1, 2, 3];

const VIEWPORT_WIDTH = 1440;
const VIEWPORT_HEIGHT = 900;
const FONT_WAIT_TIMEOUT = 10000;
const ANIMATION_DELAY = 2000;
const NAVIGATION_TIMEOUT = 120000;   // 2min — fichiers HTML lourds (base64 images) sur Google Drive
const PROTOCOL_TIMEOUT = 300000;     // 5min — fullPage screenshot de pages volumineuses

async function captureStyleTile(browser, htmlPath, conceptNum) {
  const page = await browser.newPage();
  await page.setViewport({ width: VIEWPORT_WIDTH, height: VIEWPORT_HEIGHT });

  // pathToFileURL encode les chemins Google Drive avec espaces
  const fileUrl = pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: NAVIGATION_TIMEOUT });

  // Attendre le chargement des Google Fonts
  await page.waitForFunction(() => document.fonts.ready, { timeout: FONT_WAIT_TIMEOUT })
    .catch(() => console.warn(`  ⚠ Fonts timeout concept ${conceptNum} — continuing`));

  // Délai pour les animations CSS
  await new Promise(resolve => setTimeout(resolve, ANIMATION_DELAY));

  // Hero screenshot (viewport seul, above-the-fold)
  const heroPath = path.join(sessionDir, `screenshot-c${conceptNum}-hero.png`);
  await page.screenshot({ fullPage: false, path: heroPath });
  console.log(`  ✓ screenshot-c${conceptNum}-hero.png`);

  // Full-page screenshot
  const fullPath = path.join(sessionDir, `screenshot-c${conceptNum}-full.png`);
  await page.screenshot({ fullPage: true, path: fullPath });
  console.log(`  ✓ screenshot-c${conceptNum}-full.png`);

  await page.close();
}

async function main() {
  console.log(`Capturing screenshots for ${brand} (concepts: ${concepts.join(', ')})...`);

  const browser = await puppeteer.launch({
    headless: 'new',
    protocolTimeout: PROTOCOL_TIMEOUT,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  let exitCode = 0;
  try {
    for (const num of concepts) {
      const htmlFile = path.join(sessionDir, `${brand}-style-tile-concept-${num}.html`);
      if (!fs.existsSync(htmlFile)) {
        console.warn(`  ⚠ ${path.basename(htmlFile)} not found — skipping`);
        continue;
      }
      await captureStyleTile(browser, htmlFile, num);
    }
  } catch (err) {
    console.error('Erreur Puppeteer:', err.message);
    exitCode = 1;
  } finally {
    await browser.close();
  }

  console.log('Capture terminée.');
  process.exit(exitCode);
}

main();
