# Perplexity Deep Research prompt v3 — Adversarial review and gap-filling on v2 typeface inventory

> Copy/paste the entire block below into Perplexity Deep Research mode. Run in English.

---

# Role

You are a **senior typography researcher and brand identity director** doing an **adversarial review** of a previous research output. Your prior v2 inventory of premium free typefaces (130 entries from Google Fonts + Fontshare for a brand identity generator) has been audited critically. Six concrete weaknesses were identified. Your mission now is to **defend, correct, or extend** the v2 output on each of these weaknesses, with verifiable evidence — not to redo the inventory from scratch.

# Posture — defensive, evidence-driven

This is not a generic research prompt. You must take a **defensive position** on each contested point: either argue with verifiable evidence why the current v2 entry is correct, or concede and correct it with replacement evidence. Vague justifications ("growing adoption", "documented usage", "cited in design community") will be rejected. **Every claim must be backed by a verifiable URL or named project from 2024-2026 elite sources.**

If you cannot find verifiable evidence for a v2 entry under challenge, **say so explicitly** and either downgrade or remove that entry. Do not invent. Do not pad.

# Context — what the v2 output produced

The v2 output (which you produced in a prior session) is a curated inventory of 108 unique typefaces (129 entries with cross-listings) restricted to **Google Fonts** and **Fontshare** distributions only. It covers 12 sensorial registers (Editorial luxury, Modern serif, Tech distinctive, Neo-grotesque, Humanist sans, Warm artisanal, Industrial bold, Slab, Expressive display, Monospace technical, Geometric expressive, Decorative statement). Each register reached ≥10 entries (some via cross-listings).

Hard-banned typefaces (do not propose under any circumstance): Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Helvetica, Arial, Source Sans 3, IBM Plex Sans, DM Sans, Times New Roman, Georgia, Garamond, Palatino, Fraunces, Cormorant (all variants), Playfair Display, DM Serif (all variants), EB Garamond. Anti-cousin clause applies — avoid close visual cousins of these families.

Source restriction: Google Fonts (`fonts.google.com`) + Fontshare (`fontshare.com`) exclusively, plus other **truly free** distribution channels (Open Foundry, Velvetyne, GitHub open-source releases, Future Fonts beta-free, foundry-direct free distributions). **No paid boutique typefaces** (no Klim, no Grilli, no Commercial Type, no Sharp Type, no ABC Dinamo, no Pangram Pangram non-Fontshare items, no Sharp Type, no Lineto).

# The 6 weaknesses identified — your defensive brief

## Weakness 1 — Missing SLOP_RISK_EMERGING tags

The v2 output tagged 8 typefaces with SLOP_RISK_EMERGING (Switzer, Cabinet Grotesk, Clash Display, General Sans, Space Grotesk, Bricolage Grotesque, Syne, Satoshi-already-excluded). The audit identified **8 additional candidates** that may warrant the tag but were not flagged.

**Your task**: for each of these 8 candidates, argue defensively. Either justify why the v2 chose NOT to tag them, with verifiable counter-evidence of distinctive deliberate usage 2024-2026, OR concede and add the SLOP_RISK_EMERGING tag with a documented saturation signal (template ecosystem adoption, listicle ubiquity, "default font" mention in design community threads).

Candidates to evaluate:

1. **Manrope** (Google Fonts) — alleged saturation as "warm Inter alternative" in SaaS templates 2024-2025
2. **Outfit** (Google Fonts) — alleged ubiquity in Webflow/Framer template ecosystems 2024
3. **Quicksand** (Google Fonts) — alleged kids/family/wellness template default since 2018
4. **Oswald** (Google Fonts) — alleged "universal poster default" since 2015
5. **Anton** (Google Fonts) — alleged condensed display default on Canva/templates
6. **Lora** (Google Fonts) — alleged "premium serif default" on Substack and Medium-likes
7. **Bodoni Moda** (Google Fonts) — alleged trajectory toward luxury-cliché (Playfair-style risk)
8. **Space Mono** (Google Fonts) — alleged crypto/dev-tool template saturation 2022-2024

**Output format for Weakness 1**:

| Typeface | Verdict (CONFIRM_TAG / DEFEND_NO_TAG / DOWNGRADE_TO_MONITOR) | Evidence | URL or named project |
|---|---|---|---|

## Weakness 2 — Weak elite-usage proof on ~20 Fontshare ITF entries

The v2 output included ~20 Fontshare entries from Indian Type Foundry (ITF) with elite-usage proof reduced to "Fontshare Originals; growing adoption" or similar vague claims. The audit flagged this as insufficient — these may be filler.

**Your task**: for each of the 20 contested ITF entries, provide either:
- A **verifiable elite usage**: a named brand 2024-2026 OR an Awwwards Site of the Day / Honorable Mention 2024-2026 with URL OR a Fonts In Use entry with the brand name OR a documented Fontshare case study.
- OR concede and recommend **REMOVE** from the inventory.

Vague claims like "documented on Inspotype", "Fontshare top-X downloaded", "growing adoption" are **rejected as proof** for this audit. We need named projects.

Contested entries:

1. **Bonny** (Fontshare ITF, Modern serif)
2. **Neco** (Fontshare ITF, Modern serif)
3. **Recia** (Fontshare ITF, Modern serif)
4. **Rowan** (Fontshare ITF, Modern serif)
5. **Sentient** (Fontshare ITF, Modern serif)
6. **Quilon** (Fontshare ITF, Humanist sans)
7. **Amulya** (Fontshare ITF, Humanist sans)
8. **Alpino** (Fontshare ITF, Humanist sans)
9. **Pally** (Fontshare ITF, Warm artisanal)
10. **Roundo** (Fontshare ITF, Warm artisanal)
11. **Pilcrow Rounded** (Fontshare ITF, Warm artisanal)
12. **Pramukh Rounded** (Fontshare ITF, Warm artisanal)
13. **Synonym** (Fontshare ITF, Tech distinctive)
14. **Tabular** (Fontshare ITF, Tech distinctive)
15. **Supreme** (Fontshare ITF, Neo-grotesque)
16. **Excon** (Fontshare ITF, Neo-grotesque)
17. **Expose** (Fontshare ITF, Neo-grotesque)
18. **Plein** (Fontshare ITF, Neo-grotesque)
19. **Bespoke Sans / Bespoke Slab / Bespoke Serif / Bespoke Stencil** (Fontshare ITF Bespoke system) — evaluate as a system if same evidence applies, else separately
20. **Boska** (Fontshare ITF, Editorial luxury / Slab)

**Output format for Weakness 2**:

| Typeface | Verdict (KEEP_VERIFIED / KEEP_DOWNGRADED / REMOVE) | Named brand or Awwwards URL or Fonts In Use entry (must be 2024-2026, must be specific) | Notes |
|---|---|---|---|

## Weakness 3 — 22 typefaces missing to reach the 130 unique target

The v2 output reached only **108 unique typefaces** (vs 130 target). The shortfall reflects the 5 genuine market gaps documented in v2 Section D.

**Your task**: for each of the 5 gaps, perform **directed research** beyond Fontshare ITF and Google Fonts heritage popular names. Search Open Foundry (open-foundry.com), Velvetyne (velvetyne.fr), GitHub open-source font releases, Future Fonts free betas, foundry-direct free distributions, and recent Google Fonts additions (post-2024). Propose 4-6 typefaces per gap, with verifiable elite usage 2024-2026.

The 5 gaps to fill:

1. **Warm artisanal standalone serifs** (3-5 typefaces) — humanist serifs with genuine craft character, not Cormorant/Garamond cousins. Avoid the anti-cousin clause violations.
2. **Decorative legible mid-point typefaces** (2-3 typefaces) — between "legible display" and "experimental". Headline-functional at moderate sizes (60-150pt) without requiring 300px minimum.
3. **High-contrast expressive display serifs beyond Bodoni Moda** (2-3 typefaces) — premium ultra-thin-stroke serifs in the Canela/Lyon Display register, but free.
4. **Humanist slab for B2B editorial** (2 typefaces) — in the Freight Text or Adelle quality tier, but free.
5. **Condensed text-rate humanist sans for news/editorial** (1-2 typefaces) — narrow text-grade sans for dense editorial columns. Author (already in v2) is partial, find more.

For each proposed typeface: name, source URL (Google Fonts / Fontshare / Open Foundry / Velvetyne / GitHub / other free), distinctive character clause, 2024-2026 elite usage proof (named project URL).

**Output format for Weakness 3**:

| Gap # | Typeface name | Source URL | Distinctive character | Elite usage proof 2024-2026 (named project URL) |
|---|---|---|---|---|

## Weakness 4 — ITF over-representation (anti-monoculture diversification)

~80% of v2 Fontshare entries come from Indian Type Foundry. Risk of typographic monoculture in the pool.

**Your task**: find **10-15 free typefaces NOT from Indian Type Foundry, NOT from Google Fonts heritage popular set, NOT already in v2**. Sources to mine:

- **Velvetyne** (velvetyne.fr) — French foundry, distinctive open-source typefaces (already partially leveraged in design community)
- **Open Foundry** (open-foundry.com) — curated open-source typefaces collection
- **GitHub open-source font repositories** (search by language/foundry)
- **Future Fonts** betas with free tier (future-fonts.com)
- **Other foundries with free tiers**: Type Network's free section, OFL-licensed typefaces from non-ITF foundries, foundry-direct free distributions
- **Google Fonts post-2023 additions** that are not yet popular (Font Discoveries, Designer Discovery, GitHub PRs to google/fonts repository)

Focus on registers under-served by ITF: Warm artisanal, Modern serif, Editorial luxury, Decorative statement.

For each: must have verifiable 2024-2026 usage by a named brand or Awwwards/Fonts In Use entry.

**Output format for Weakness 4**:

| # | Typeface name | Foundry / origin | Source URL (free distribution) | Register served | 2024-2026 elite usage proof (named project URL) |
|---|---|---|---|---|---|

## Weakness 5 — 8 borderline candidates pending arbitrage

The audit identified 8 typefaces that the v2 either excluded or didn't address, but that may legitimately enter the pool with proper context.

**Your task**: for each, argue defensively for **INCLUDE / BORDERLINE_WITH_CAVEAT / EXCLUDE** with evidence. If INCLUDE or BORDERLINE_WITH_CAVEAT, specify which register and why the inclusion does not violate the anti-cousin clause for related banned families.

Candidates:

1. **Alegreya** (Google Fonts) — old-style humanist serif, excluded by v2 due to perceived Garald-cousin proximity to banned Cormorant/Garamond. Defensible for warm-artisanal / literary register?
2. **Roboto Slab** (Google Fonts) — slab serif, family-name association with banned Roboto. Defensible if isolated to Slab register only?
3. **Hanken Grotesk** (Google Fonts) — neo-grotesque, perceived too close to Inter/DM Sans proportions. Defensible distinctive character?
4. **Plus Jakarta Sans** (Google Fonts) — flagged borderline in initial brief, not addressed in v2. Inclusion or hard exclusion?
5. **Inclusive Sans** (Google Fonts) — humanist accessibility-focused sans, not addressed in v2. Worth inclusion in Humanist sans register?
6. **Sono** (Google Fonts) — variable monospace, not addressed in v2. Worth inclusion in Monospace register?
7. **Atkinson Hyperlegible** (classic, Google Fonts) — predecessor to Atkinson Hyperlegible Next which is in v2. Worth keeping classic version separately?
8. **Big Shoulders Stencil** (Google Fonts) — stencil variant of Big Shoulders system. Worth inclusion in Decorative register?

**Output format for Weakness 5**:

| Typeface | Verdict (INCLUDE / BORDERLINE_WITH_CAVEAT / EXCLUDE) | Register if INCLUDE | Anti-cousin clause justification | Evidence |
|---|---|---|---|---|

## Weakness 6 — Real-world usage proof imbalance

The v2 output relied heavily on a French agency blog (Easyweb-agency.fr) cited 30+ times for Fontshare entries. The brief explicitly required Awwwards / Codrops Webzibition / Fonts In Use as priority sources. Tertiary listicles and agency blogs are weak proofs.

**Your task**: for the 30 most strategic typefaces of your **final consolidated v3 output** (top 5-6 per register from the consolidated v2 + v3 corrections), provide **upgraded elite-usage proof** drawn from these priority sources:

- **Awwwards** Site of the Day, Honorable Mentions, Site of the Year 2024-2026 — with URL
- **Codrops Webzibition** entries 2024-2026 — with URL
- **Fonts In Use** documented production entries with brand name and date 2024-2026 — with URL
- **The Brand Identity** brand reveal articles 2024-2026 — with URL
- **It's Nice That** brand identity coverage 2024-2026 — with URL
- **Brand New** (UnderConsideration) brand identity reveals 2024-2026 — with URL

If a typeface in your top 30 cannot be backed by at least one such priority source, mark it `WEAK_PROOF` and recommend either deeper research, downgrade, or removal.

**Output format for Weakness 6**:

| Typeface | Register | Priority source #1 (URL) | Priority source #2 (URL, optional) | Verdict (STRONG_PROOF / WEAK_PROOF) |
|---|---|---|---|---|

# Final consolidation deliverable

After processing the 6 weaknesses, produce a **final consolidated table** (the canonical v3 inventory) showing:

- Total unique typefaces (target ≥120, ideally 130-140)
- Per-register count (must remain ≥10 per register, can exceed)
- All SLOP_RISK_EMERGING tags consolidated (v2 + Weakness 1 additions)
- All ITF-filler removals or verifications applied
- All gap-fill and diversification additions integrated
- All borderline candidates resolved (INCLUDE or EXCLUDE)
- Source URL verified for each entry
- Top-5-per-register elite usage proof from priority sources

**Format**: same column structure as v2 master table, plus an additional column `Audit status` with one of: `KEPT_FROM_V2`, `KEPT_VERIFIED`, `KEPT_DOWNGRADED`, `ADDED_GAP_FILL`, `ADDED_DIVERSIFICATION`, `ADDED_BORDERLINE`, `REMOVED_FILLER`.

# Quality bar — what we want, what we don't

**We want:**
- Defensive evidence (URLs, named projects, dated 2024-2026) for every contested point
- Concessions where evidence is absent ("REMOVE" or "WEAK_PROOF") rather than padding
- Diversification beyond Fontshare ITF and Google Fonts heritage popular
- Final pool count between 120 and 140 unique typefaces
- All 12 registers ≥10 unique (without inflating via cross-listings)

**We don't want:**
- Vague justifications ("growing adoption", "documented", "cited", "popular")
- Defensive complacency for the v2 output — concede when evidence is weak
- Padding to reach a target count by including weak entries
- Boutique paid typefaces (hard exclusion remains)
- Re-doing the v2 output from scratch — work on the delta

# Format

Return six output sections (one per weakness) followed by the final consolidated table. Clean Markdown, no exec summary, direct output.
