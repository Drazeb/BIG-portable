#!/usr/bin/env bash
#
# update.sh — Met à jour BIG-portable et ses 2 repos voisins.
#
# Lance `git pull --ff-only` dans BIG-portable + SPG-portable + nano-banana-edit-portable
# (s'ils sont présents). Affiche un récap.
#
# Usage :
#   ./update.sh

set -uo pipefail

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PARENT_DIR=$(dirname "$SCRIPT_DIR")

REPOS=(
  "$SCRIPT_DIR:BIG-portable"
  "$PARENT_DIR/SPG-portable:SPG-portable"
  "$PARENT_DIR/nano-banana-edit-portable:nano-banana-edit-portable"
)

echo
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  Mise à jour des repos                                       ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo

for entry in "${REPOS[@]}"; do
  REPO_PATH="${entry%%:*}"
  REPO_NAME="${entry##*:}"

  echo -e "${BOLD}── $REPO_NAME ──${NC}"

  if [ ! -d "$REPO_PATH" ]; then
    echo -e "  ${YELLOW}⚠ absent — skip${NC} (lance ./install.sh pour le cloner)"
    echo
    continue
  fi

  if [ ! -d "$REPO_PATH/.git" ]; then
    echo -e "  ${YELLOW}⚠ pas un repo git — skip${NC}"
    echo
    continue
  fi

  # Fetch + pull --ff-only
  cd "$REPO_PATH"
  BEFORE=$(git rev-parse HEAD 2>/dev/null || echo "")
  PULL_OUTPUT=$(git pull --ff-only 2>&1 || true)
  AFTER=$(git rev-parse HEAD 2>/dev/null || echo "")

  if [ "$BEFORE" = "$AFTER" ]; then
    echo -e "  ${GREEN}✓${NC} déjà à jour"
  else
    COMMITS=$(git rev-list --count "$BEFORE..$AFTER" 2>/dev/null || echo "?")
    echo -e "  ${GREEN}✓${NC} $COMMITS nouveau(x) commit(s) récupéré(s)"

    # Si SPG-portable et package.json a changé, suggérer npm install
    if [ "$REPO_NAME" = "SPG-portable" ]; then
      if git diff "$BEFORE..$AFTER" --name-only | grep -q "^package.json$"; then
        echo -e "  ${YELLOW}💡 package.json a changé — pense à relancer : npm install${NC}"
      fi
    fi
  fi

  # Erreur de pull (ex: conflit, divergence)
  if echo "$PULL_OUTPUT" | grep -q -i "error\|conflict\|cannot fast-forward\|aborting"; then
    echo -e "  ${RED}⚠ git pull a échoué :${NC}"
    echo "$PULL_OUTPUT" | sed 's/^/      /'
    echo -e "  ${RED}→ Résous le conflit à la main puis relance ./update.sh${NC}"
  fi

  echo
done

echo -e "${BOLD}── Terminé ──${NC}"
echo -e "  Tu peux maintenant relancer Claude Code et utiliser /brand-identity"
echo -e "  avec les dernières améliorations."
echo
