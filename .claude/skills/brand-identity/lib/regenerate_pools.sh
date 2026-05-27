#!/bin/bash
# Regenerate the 6 BIG font pools (Display A1/A2/A3 + Body A1/A2/A3)
# Source : ref/pool-allocation-axes-audace-2026-04-28.md
# Outputs : ref/font-pools/font-pool-{display,body}-A{1,2,3}-mapping.json + planches PNG
# Last update : 2026-04-28

set -e
cd "$(dirname "$0")/.."

OUT_DIR="ref/font-pools"
SAMPLE_TEXT="Ag Stratégie & Vision 2026"

# Helper: write config + invoke tooling
generate_pool() {
  local pool_name="$1"
  local fonts_json="$2"
  echo ""
  echo "════════════════════════════════════════════════════════"
  echo "Pool: $pool_name"
  echo "════════════════════════════════════════════════════════"
  cat > "$OUT_DIR/.tmp-pool-config.json" <<EOF
{
  "fonts": $fonts_json,
  "sampleText": "$SAMPLE_TEXT"
}
EOF
  node lib/font-pool-contact-sheet.mjs "$OUT_DIR" "$pool_name"
}

# ═══ Display A1 (43 fontes) — sober conservative display ═══
generate_pool "display-A1" '[
  "Young Serif","Newsreader","Gambetta","Noto Serif Display","Bespoke Serif","Libre Baskerville",
  "Source Serif 4","Erode","Alegreya","Labrada","Eczar","Piazzolla",
  "Geist","Schibsted Grotesk","Outfit","Switzer","Onest","Recursive","Hubot Sans","Rethink Sans",
  "Cabinet Grotesk","Clash Grotesk","Author","Supreme","Excon","Funnel Sans","Hanken Grotesk","General Sans","Mona Sans","Albert Sans",
  "Atkinson Hyperlegible Next","Reddit Sans","Wix Madefor Display","Figtree","Inclusive Sans","Instrument Sans","Sora","Bespoke Sans","Manrope","Hedvig Letters Sans","Comico",
  "Vollkorn",
  "JetBrains Mono"
]'

# ═══ Body A1 (50 fontes) — sober conservative body ═══
generate_pool "body-A1" '[
  "Young Serif","Newsreader","Gambetta","Bespoke Serif","Libre Baskerville",
  "Source Serif 4","Spectral","Literata","Erode","Crimson Pro","Lora","Alegreya","Labrada","Eczar",
  "Geist","Geist Mono","Schibsted Grotesk","Outfit","Switzer","Onest","Recursive","Hubot Sans","Rethink Sans",
  "Cabinet Grotesk","Clash Grotesk","Author","Supreme","Excon","Funnel Sans","Hanken Grotesk","General Sans","Mona Sans","Albert Sans",
  "Atkinson Hyperlegible Next","Reddit Sans","Wix Madefor Text","Figtree","Inclusive Sans","Instrument Sans","Sora","Bespoke Sans","Manrope","Hedvig Letters Sans",
  "Bitter","Aleo","Petrona","Faustina","Vollkorn",
  "JetBrains Mono","Reddit Mono"
]'

# ═══ Display A2 (73 fontes) — contemporary distinctive display ═══
generate_pool "display-A2" '[
  "Young Serif","Newsreader","Gambetta","Noto Serif Display","Bespoke Serif","Libre Baskerville","Bodoni Moda","Instrument Serif","Zodiak","Hedvig Letters Serif",
  "Source Serif 4","Erode","Recia","Alegreya","Labrada","Eczar","Piazzolla",
  "Geist","Schibsted Grotesk","Familjen Grotesk","Outfit","Switzer","Onest","Rethink Sans","Recursive","Mona Sans",
  "Cabinet Grotesk","Clash Grotesk","Author","Supreme","Excon","Funnel Sans","Hanken Grotesk","Ranade",
  "Atkinson Hyperlegible Next","Instrument Sans","Reddit Sans","Wix Madefor Display","Bespoke Sans","Manrope","Sora","Figtree","Inclusive Sans","Hedvig Letters Sans","Comico",
  "Syne","Calistoga","Sansita",
  "Clash Display","Big Shoulders Display","Funnel Display","Melodrama","Technor","Oswald",
  "Zilla Slab","Vollkorn","Trench Slab","Chubbo",
  "Anybody","Stardom","Bevellier","New Title","Bricolage Grotesque","Sporting Grotesque",
  "JetBrains Mono","Martian Mono","Azeret Mono","Space Mono","Fragment Mono","Spline Sans Mono","Sono",
  "Epilogue",
  "Array"
]'

# ═══ Body A2 (69 fontes) — contemporary distinctive body ═══
generate_pool "body-A2" '[
  "Young Serif","Newsreader","Gambetta","Bespoke Serif","Libre Baskerville","Zodiak","Hedvig Letters Serif",
  "Source Serif 4","Spectral","Literata","Erode","Crimson Pro","Lora","Alegreya","Labrada","Eczar","Piazzolla",
  "Geist","Geist Mono","Schibsted Grotesk","Familjen Grotesk","Outfit","Switzer","Onest","Rethink Sans","Recursive","Mona Sans",
  "Cabinet Grotesk","Clash Grotesk","Author","Supreme","Excon","Funnel Sans","Hanken Grotesk","Ranade",
  "Atkinson Hyperlegible Next","Instrument Sans","Reddit Sans","Wix Madefor Text","Bespoke Sans","Manrope","Sora","Figtree","Inclusive Sans","Hedvig Letters Sans","Fira Sans Condensed",
  "Syne","Sansita",
  "Technor",
  "Zilla Slab","Bitter","Aleo","Petrona","Faustina","Vollkorn","Chubbo",
  "Bricolage Grotesque","Sporting Grotesque",
  "JetBrains Mono","Martian Mono","Victor Mono","Azeret Mono","Space Mono","Fragment Mono","Reddit Mono","Spline Sans Mono","Kode Mono","Sono",
  "Epilogue",
  "Array"
]'

# ═══ Display A3 (48 fontes) — bold audacious display ═══
generate_pool "display-A3" '[
  "Gloock","Bodoni Moda","Instrument Serif","Zodiak","Gambarino","Hedvig Letters Serif","Recia",
  "Piazzolla",
  "Familjen Grotesk","Recursive","Onest",
  "Ranade",
  "Chillax","Syne","Calistoga",
  "Tanker","Clash Display","Panchang","Nippo","Big Shoulders Display","Funnel Display","Melodrama","Anton","Oswald","Pramukh Rounded","Bungee",
  "Hoover","Trench Slab",
  "Anybody","Stardom","Bevellier","New Title","Bricolage Grotesque","Noto Serif Display",
  "Martian Mono",
  "Epilogue","Figtree","Funnel Sans",
  "Kola",
  "Big Shoulders Inline Display","Big Shoulders Stencil","Sporting Grotesque","Aktura","Boxing","Segment","Zina","Styro","Kihim","Array"
]'

# ═══ Body A3 (30 fontes) — bold readable body (limit structurel marché free) ═══
generate_pool "body-A3" '[
  "Zodiak","Hedvig Letters Serif",
  "Spectral","Piazzolla",
  "Familjen Grotesk","Recursive","Onest",
  "Ranade",
  "Syne",
  "Funnel Sans","Bungee",
  "Bitter","Zilla Slab","Aleo",
  "Bricolage Grotesque","Figtree",
  "Martian Mono","Kode Mono","Sono","JetBrains Mono","Azeret Mono","Victor Mono","Fragment Mono","Spline Sans Mono","Geist Mono","Departure Mono",
  "Epilogue",
  "Array","Sporting Grotesque","Newsreader"
]'

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ 6 pools régénérés avec succès"
echo "════════════════════════════════════════════════════════"
ls -la "$OUT_DIR"/font-pool-{display,body}-A{1,2,3}*.{json,png} 2>/dev/null | head -30
