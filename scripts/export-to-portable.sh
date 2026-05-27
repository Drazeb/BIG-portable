#!/usr/bin/env bash
#
# export-to-portable.sh — Sync filtré du sandbox BIG vers ce repo portable.
#
# Stratégie : LISTE BLANCHE par dossier (plus robuste qu'une liste noire — un
# nouveau parasite futur dans le sandbox ne contamine pas le portable tant qu'il
# n'est pas dans un dossier whitelisté).
#
# Usage :
#   ./scripts/export-to-portable.sh             # dry-run par défaut (sûr)
#   ./scripts/export-to-portable.sh --apply     # exécute le sync pour de vrai
#   ./scripts/export-to-portable.sh --apply --verbose
#
# Après un --apply, faire :
#   git diff           # vérifier visuellement
#   git add -A && git commit -m "..."
#   git push

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SANDBOX="/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator"
PORTABLE="$HOME/repos/BIG-portable"

# Skills à inclure (liste blanche dure)
SKILLS_TO_PORT=(
  "brand-identity"
  "visual-brief"
  "test-big"
  "brand-book"
  "visual-prompt"
)

# Fichiers racine à porter (depuis le sandbox vers le portable)
ROOT_FILES_TO_PORT=(
  "ARCHITECTURE.md:docs/ARCHITECTURE.md"
  "DECISIONS.md:docs/internal/DECISIONS.md"
  "CHANGELOG.md:docs/internal/BUILD-LOG.md"
  "brief-guide.md:guides/brief-guide.md"
  "prompt-perplexity-logo-bible.md:guides/prompt-perplexity-logo-bible.md"
)
# Note : CLAUDE.md racine du sandbox N'EST PAS porté automatiquement — il sera
# adapté manuellement (références persos à Charles à retirer). Voir étape
# manuelle dans le plan.

# Exclusions dans tout dossier copié (parasites, sensibles, etc.)
RSYNC_EXCLUDES=(
  # macOS
  ".DS_Store"

  # Sessions outputs (jamais portées)
  "outputs/"

  # Briefs clients confidentiels (CRITIQUE — ne jamais exposer)
  "briefs/"

  # Backups internes du sandbox
  "*.bak"
  "*.bak-pre-*"
  "*.backup"

  # Fichiers temporaires
  ".tmp-*"
  "*.tmp"
  "*.swp"

  # Python
  "__pycache__/"
  "*.pyc"
  ".pytest_cache/"

  # Node
  "node_modules/"

  # Secrets
  ".env"
  ".env.*"
  "*.pem"
  "credentials.json"

  # Logs
  "*.log"
  ".progress-*.log"
)

# Couleurs terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# ─────────────────────────────────────────────────────────────────────────────
# PARSING DES ARGUMENTS
# ─────────────────────────────────────────────────────────────────────────────

APPLY=0
VERBOSE=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    --verbose) VERBOSE=1 ;;
    -h|--help)
      grep -E '^# ' "$0" | head -20
      exit 0
      ;;
    *)
      echo "Argument inconnu : $arg"
      exit 1
      ;;
  esac
done

# ─────────────────────────────────────────────────────────────────────────────
# CHECKS PRÉALABLES
# ─────────────────────────────────────────────────────────────────────────────

if [ ! -d "$SANDBOX" ]; then
  echo -e "${RED}❌ Sandbox introuvable :${NC} $SANDBOX"
  exit 1
fi

if [ ! -d "$PORTABLE" ]; then
  echo -e "${RED}❌ Portable introuvable :${NC} $PORTABLE"
  exit 1
fi

if [ ! -d "$PORTABLE/.git" ]; then
  echo -e "${RED}❌ Le portable n'est pas un repo git${NC}"
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUCTION DES OPTIONS RSYNC
# ─────────────────────────────────────────────────────────────────────────────

RSYNC_OPTS=(
  --archive          # préserve permissions/timestamps
  --delete           # supprime du portable ce qui n'est plus dans le sandbox
  --human-readable
)

if [ "$APPLY" -eq 0 ]; then
  RSYNC_OPTS+=(--dry-run)
fi

if [ "$VERBOSE" -eq 1 ]; then
  RSYNC_OPTS+=(--verbose)
else
  RSYNC_OPTS+=(--itemize-changes)
fi

for exclude in "${RSYNC_EXCLUDES[@]}"; do
  RSYNC_OPTS+=(--exclude="$exclude")
done

# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────

echo
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  BIG sandbox → portable repo                                 ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "  Sandbox  : ${BLUE}$SANDBOX${NC}"
echo -e "  Portable : ${BLUE}$PORTABLE${NC}"
echo

if [ "$APPLY" -eq 0 ]; then
  echo -e "${YELLOW}  ⚠ Mode DRY-RUN (aucun fichier modifié)${NC}"
  echo -e "${YELLOW}    Pour exécuter pour de vrai : ./scripts/export-to-portable.sh --apply${NC}"
else
  echo -e "${GREEN}  ✓ Mode APPLY (les fichiers vont être copiés)${NC}"
fi
echo

# ─────────────────────────────────────────────────────────────────────────────
# SYNC DES SKILLS
# ─────────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}── Sync des skills ──${NC}"
for skill in "${SKILLS_TO_PORT[@]}"; do
  SRC="$SANDBOX/.claude/skills/$skill/"
  DST="$PORTABLE/.claude/skills/$skill/"

  if [ ! -d "$SRC" ]; then
    echo -e "  ${YELLOW}⚠ $skill — absent du sandbox, skip${NC}"
    continue
  fi

  echo -e "  ${BLUE}→${NC} $skill"
  mkdir -p "$DST"
  rsync "${RSYNC_OPTS[@]}" "$SRC" "$DST" | sed 's/^/      /'
done
echo

# ─────────────────────────────────────────────────────────────────────────────
# SYNC DES FICHIERS RACINE
# ─────────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}── Sync des fichiers racine ──${NC}"
for mapping in "${ROOT_FILES_TO_PORT[@]}"; do
  SRC_REL="${mapping%%:*}"
  DST_REL="${mapping##*:}"
  SRC="$SANDBOX/$SRC_REL"
  DST="$PORTABLE/$DST_REL"

  if [ ! -f "$SRC" ]; then
    echo -e "  ${YELLOW}⚠ $SRC_REL — absent du sandbox, skip${NC}"
    continue
  fi

  echo -e "  ${BLUE}→${NC} $SRC_REL ${NC}→${NC} $DST_REL"
  mkdir -p "$(dirname "$DST")"

  if [ "$APPLY" -eq 1 ]; then
    cp "$SRC" "$DST"
  else
    if [ ! -f "$DST" ] || ! cmp -s "$SRC" "$DST"; then
      echo -e "      ${YELLOW}(would copy)${NC}"
    else
      echo -e "      (identique, no-op)"
    fi
  fi
done
echo

# ─────────────────────────────────────────────────────────────────────────────
# CHECKS POST-SYNC (uniquement en mode apply)
# ─────────────────────────────────────────────────────────────────────────────

if [ "$APPLY" -eq 1 ]; then
  echo -e "${BOLD}── Vérifications post-sync ──${NC}"

  # 1. Aucun brief client n'a fui
  echo -ne "  Aucun brief confidentiel exposé... "
  LEAKS=$(grep -rl "Jacques Brief\|Les Alchimistes" "$PORTABLE" 2>/dev/null | grep -v "/docs/internal/" || true)
  if [ -z "$LEAKS" ]; then
    echo -e "${GREEN}✓${NC}"
  else
    echo -e "${RED}✗${NC}"
    echo -e "  ${RED}Fichiers compromettants détectés :${NC}"
    echo "$LEAKS" | sed 's/^/    /'
  fi

  # 2. Aucun .bak parasite
  echo -ne "  Aucun fichier *.bak-pre-*... "
  BAKS=$(find "$PORTABLE" -name "*.bak-pre-*" 2>/dev/null || true)
  if [ -z "$BAKS" ]; then
    echo -e "${GREEN}✓${NC}"
  else
    echo -e "${RED}✗${NC}"
    echo "$BAKS" | sed 's/^/    /'
  fi

  # 3. Taille raisonnable
  echo -ne "  Taille du repo... "
  SIZE=$(du -sh "$PORTABLE" | cut -f1)
  echo -e "${BLUE}$SIZE${NC}"

  echo
  echo -e "${BOLD}── Prochaines étapes ──${NC}"
  echo -e "  ${BLUE}cd $PORTABLE${NC}"
  echo -e "  ${BLUE}git status${NC}             # voir les changements"
  echo -e "  ${BLUE}git diff${NC}               # détail des modifs"
  echo -e "  ${BLUE}git add -A${NC}             # stager"
  echo -e "  ${BLUE}git commit -m \"...\"${NC}    # committer"
  echo -e "  ${BLUE}git push${NC}               # publier sur GitHub"
  echo
fi
