#!/usr/bin/env bash
#
# install.sh — Setup automatique pour BIG-portable
#
# Clone SPG-portable et nano-banana-edit-portable côte à côte avec BIG-portable,
# initialise le .env de nano-banana-edit avec le placeholder, ouvre les
# ressources nécessaires pour que tu n'aies plus qu'à coller ta clé Gemini
# le moment venu.
#
# Idempotent : tu peux le relancer autant de fois que tu veux, il skippe ce
# qui est déjà fait.
#
# Usage :
#   ./install.sh

set -euo pipefail

# Couleurs terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

# ─────────────────────────────────────────────────────────────────────────────
# DÉTECTION DES CHEMINS
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PARENT_DIR=$(dirname "$SCRIPT_DIR")

# Repos voisins à cloner
SPG_REPO="https://github.com/Drazeb/SPG-portable.git"
NB_REPO="https://github.com/Drazeb/nano-banana-edit-portable.git"

SPG_PATH="$PARENT_DIR/SPG-portable"
NB_PATH="$PARENT_DIR/nano-banana-edit-portable"
# Le SKILL nano-banana-edit cherche `.env` à la racine de son dossier de skill
# (cf. nb-api.py : SKILL_ROOT / ".env"). Donc on copie .env.example au bon
# endroit, pas à la racine du repo.
NB_SKILL_DIR="$NB_PATH/.claude/skills/nano-banana-edit"
NB_ENV_EXAMPLE="$NB_SKILL_DIR/.env.example"
NB_ENV="$NB_SKILL_DIR/.env"

# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────

echo
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  BIG-portable — Setup                                        ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "  BIG-portable : ${BLUE}$SCRIPT_DIR${NC}"
echo -e "  Dossier parent : ${BLUE}$PARENT_DIR${NC}"
echo -e "  → Je vais cloner SPG-portable et nano-banana-edit-portable dans ce dossier parent."
echo

# ─────────────────────────────────────────────────────────────────────────────
# CHECK PRÉALABLE : git installé ?
# ─────────────────────────────────────────────────────────────────────────────

if ! command -v git >/dev/null 2>&1; then
  echo -e "${YELLOW}❌ git n'est pas installé sur ta machine.${NC}"
  echo -e "   Installe-le d'abord : ${BLUE}brew install git${NC}"
  echo -e "   (Si tu n'as pas brew : https://brew.sh)"
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────────────
# 1. CLONE SPG-portable
# ─────────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}── 1. SPG-portable ──${NC}"
if [ -d "$SPG_PATH" ]; then
  echo -e "  ${GREEN}✓${NC} déjà présent dans $SPG_PATH (skip)"
else
  echo -e "  ${BLUE}→${NC} clone depuis $SPG_REPO..."
  git clone "$SPG_REPO" "$SPG_PATH"
  echo -e "  ${GREEN}✓${NC} cloné dans $SPG_PATH"
fi
echo

# ─────────────────────────────────────────────────────────────────────────────
# 2. CLONE nano-banana-edit-portable
# ─────────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}── 2. nano-banana-edit-portable ──${NC}"
if [ -d "$NB_PATH" ]; then
  echo -e "  ${GREEN}✓${NC} déjà présent dans $NB_PATH (skip)"
else
  echo -e "  ${BLUE}→${NC} clone depuis $NB_REPO..."
  git clone "$NB_REPO" "$NB_PATH"
  echo -e "  ${GREEN}✓${NC} cloné dans $NB_PATH"
fi
echo

# ─────────────────────────────────────────────────────────────────────────────
# 3. INITIALISER .env de nano-banana-edit
# ─────────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}── 3. .env de nano-banana-edit-portable ──${NC}"
if [ -f "$NB_ENV" ]; then
  echo -e "  ${GREEN}✓${NC} .env déjà présent (skip)"
elif [ -f "$NB_ENV_EXAMPLE" ]; then
  cp "$NB_ENV_EXAMPLE" "$NB_ENV"
  echo -e "  ${GREEN}✓${NC} .env créé depuis .env.example (clé Gemini = placeholder)"
else
  echo -e "  ${YELLOW}⚠${NC} .env.example introuvable dans $NB_PATH — le repo a probablement été cloné incomplètement"
fi
echo

# ─────────────────────────────────────────────────────────────────────────────
# RÉCAP FINAL
# ─────────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  Setup terminé ✓                                             ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "  Structure finale :"
echo -e "  ${BLUE}$PARENT_DIR/${NC}"
echo -e "  ├── ${GREEN}BIG-portable/${NC}                    ← tu es ici"
echo -e "  ├── ${GREEN}SPG-portable/${NC}                    ← pour le brand book final"
echo -e "  └── ${GREEN}nano-banana-edit-portable/${NC}       ← pour les corrections NB2 et variantes d'atmosphère"
echo
echo -e "${BOLD}── Prochaine étape ──${NC}"
echo -e "  1. Ouvre Claude Code dans ce dossier (BIG-portable)"
echo -e "  2. Tape ${BLUE}/brand-identity${NC}"
echo -e "  3. Le pipeline démarre. Tu peux explorer la Phase 1 à 5 sans"
echo -e "     configurer aucune clé API."
echo -e "  4. Au moment où tu auras besoin de générer un visuel hero, je"
echo -e "     te guiderai pour configurer ta clé Gemini (2 min, gratuit)."
echo
echo -e "${BOLD}── Pour mettre à jour plus tard ──${NC}"
echo -e "  ${BLUE}./update.sh${NC}    # tire les dernières maj des 3 repos"
echo
