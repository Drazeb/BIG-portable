#!/usr/bin/env node

/**
 * Hero fold check for BIG style-tiles.
 *
 * Verifies that key hero elements (title, subtitle, CTA) are fully visible
 * within the 1440×900 viewport (above the fold / no scroll).
 *
 * Usage:
 *   node lib/hero-fold-check.mjs <session_dir> <brand> [concept_numbers...]
 *
 * Output:
 *   {session_dir}/{brand}-hero-fold.md
 */

import puppeteer from 'puppeteer';
import { pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const [,, sessionDir, brand, ...conceptArgs] = process.argv;

if (!sessionDir || !brand) {
  console.error('Usage: node hero-fold-check.mjs <session_dir> <brand> [concept_numbers...]');
  process.exit(1);
}

const concepts = conceptArgs.length > 0
  ? conceptArgs.map(Number)
  : [1, 2, 3];

const VIEWPORT_WIDTH = 1440;
const VIEWPORT_HEIGHT = 900;
const NAVIGATION_TIMEOUT = 120000;
const PROTOCOL_TIMEOUT = 300000;
const FONT_WAIT_TIMEOUT = 10000;

async function checkHeroFold(browser, htmlPath, conceptNum) {
  const page = await browser.newPage();
  await page.setViewport({ width: VIEWPORT_WIDTH, height: VIEWPORT_HEIGHT });

  const fileUrl = pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: NAVIGATION_TIMEOUT });

  await page.waitForFunction(() => document.fonts.ready, { timeout: FONT_WAIT_TIMEOUT })
    .catch(() => {});

  await new Promise(resolve => setTimeout(resolve, 1000));

  // Find the hero section and its key elements
  const heroData = await page.evaluate((viewportH) => {
    // Find the hero/first section
    const hero = document.querySelector(
      'section:first-of-type, [class*="hero"], [class*="voice"], header + section, header + div, body > section:first-child, body > div:first-child > section:first-child'
    );

    if (!hero) {
      return { found: false, message: 'No hero section found' };
    }

    const heroRect = hero.getBoundingClientRect();

    // Find key elements within the hero
    const elements = [];

    // Title: h1, or largest heading, or element with class containing "title"
    const titleCandidates = hero.querySelectorAll('h1, h2, [class*="title"], [class*="heading"]');
    for (const el of titleCandidates) {
      const rect = el.getBoundingClientRect();
      if (rect.height === 0) continue;
      const text = el.textContent.trim().substring(0, 60);
      elements.push({
        type: 'title',
        tag: el.tagName.toLowerCase(),
        text,
        top: Math.round(rect.top),
        bottom: Math.round(rect.bottom),
        visible: rect.bottom <= viewportH,
        overflow: rect.bottom > viewportH ? Math.round(rect.bottom - viewportH) : 0,
      });
    }

    // Subtitle / body text
    const subtitleCandidates = hero.querySelectorAll('p, [class*="subtitle"], [class*="description"]');
    for (const el of subtitleCandidates) {
      const rect = el.getBoundingClientRect();
      if (rect.height === 0) continue;
      const fontSize = parseFloat(getComputedStyle(el).fontSize);
      if (fontSize < 12) continue; // skip tiny text
      const text = el.textContent.trim().substring(0, 60);
      elements.push({
        type: 'subtitle',
        tag: el.tagName.toLowerCase(),
        text,
        top: Math.round(rect.top),
        bottom: Math.round(rect.bottom),
        visible: rect.bottom <= viewportH,
        overflow: rect.bottom > viewportH ? Math.round(rect.bottom - viewportH) : 0,
      });
    }

    // CTA buttons/links
    const ctaCandidates = hero.querySelectorAll('a, button, [class*="cta"], [class*="button"]');
    for (const el of ctaCandidates) {
      const rect = el.getBoundingClientRect();
      if (rect.height === 0) continue;
      const text = el.textContent.trim().substring(0, 40);
      if (text.length < 2) continue;
      elements.push({
        type: 'cta',
        tag: el.tagName.toLowerCase(),
        text,
        top: Math.round(rect.top),
        bottom: Math.round(rect.bottom),
        visible: rect.bottom <= viewportH,
        overflow: rect.bottom > viewportH ? Math.round(rect.bottom - viewportH) : 0,
      });
    }

    return {
      found: true,
      heroBottom: Math.round(heroRect.bottom),
      heroOverflow: heroRect.bottom > viewportH ? Math.round(heroRect.bottom - viewportH) : 0,
      viewportHeight: viewportH,
      elements,
    };
  }, VIEWPORT_HEIGHT);

  await page.close();
  return heroData;
}

function generateReport(results) {
  let md = `# Rapport Hero Fold — ${brand}\n\n`;
  md += `> Viewport : ${VIEWPORT_WIDTH}×${VIEWPORT_HEIGHT}px. Tout élément dont le bord inférieur dépasse ${VIEWPORT_HEIGHT}px est invisible sans scroll.\n\n`;

  let hasIssues = false;

  for (const { conceptNum, data } of results) {
    md += `## Concept ${conceptNum}\n\n`;

    if (!data.found) {
      md += `⚠ Pas de section hero détectée.\n\n`;
      continue;
    }

    const overflowing = data.elements.filter(el => !el.visible);

    if (overflowing.length === 0) {
      md += `✓ Tous les éléments du hero sont visibles sans scroll.\n\n`;
    } else {
      hasIssues = true;
      md += `**${overflowing.length} élément(s) invisible(s) sans scroll :**\n\n`;
      md += `| Type | Tag | Texte | Position bas | Débordement |\n`;
      md += `|------|-----|-------|-------------|-------------|\n`;
      for (const el of overflowing) {
        const truncText = el.text.length > 40 ? el.text.substring(0, 40) + '...' : el.text;
        md += `| ${el.type} | \`${el.tag}\` | ${truncText} | ${el.bottom}px | **+${el.overflow}px** sous le fold |\n`;
      }
      md += `\n`;

      if (data.heroOverflow > 0) {
        md += `La section hero elle-même dépasse le viewport de **${data.heroOverflow}px** (bas du hero : ${data.heroBottom}px).\n\n`;
      }
    }
  }

  if (!hasIssues) {
    md += `---\n\n**Aucun problème de fold détecté.**\n`;
  }

  return md;
}

async function main() {
  console.log(`Hero fold check for ${brand} (concepts: ${concepts.join(', ')})...`);

  const browser = await puppeteer.launch({
    headless: 'new',
    protocolTimeout: PROTOCOL_TIMEOUT,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const results = [];
  let exitCode = 0;

  try {
    for (const num of concepts) {
      const htmlFile = path.join(sessionDir, `${brand}-style-tile-concept-${num}.html`);
      if (!fs.existsSync(htmlFile)) {
        console.warn(`  ⚠ ${path.basename(htmlFile)} not found — skipping`);
        continue;
      }
      console.log(`  Checking concept ${num}...`);
      const data = await checkHeroFold(browser, htmlFile, num);
      const overflowing = data.found ? data.elements.filter(el => !el.visible).length : 0;
      console.log(`  → ${overflowing} element(s) below fold`);
      results.push({ conceptNum: num, data });
    }
  } catch (err) {
    console.error('Erreur hero-fold-check:', err.message);
    exitCode = 1;
  } finally {
    await browser.close();
  }

  const report = generateReport(results);
  const reportPath = path.join(sessionDir, `${brand}-hero-fold.md`);
  fs.writeFileSync(reportPath, report, 'utf-8');
  console.log(`  ✓ ${brand}-hero-fold.md`);

  process.exit(exitCode);
}

main();
