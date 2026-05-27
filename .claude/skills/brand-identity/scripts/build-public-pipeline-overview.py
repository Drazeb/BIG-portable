#!/usr/bin/env python3
"""
Génère la version publique de pipeline-overview.md depuis la version interne.

Source  : ref/pipeline-overview.md (interne, garde tout)
Cible   : ref/pipeline-overview-public.md (publique, sans "sous le capot")

Stratégie de strip :
- Supprime les blocs `*Sous le capot ...*` (mono ou multi-paragraphes italiques)
  jusqu'à la prochaine ligne `→ ...` (input section) ou `---` (séparateur).
- Supprime la `*Note technique...` finale.
- Garde tout le reste : titres, paragraphes principaux, listes user-facing,
  sections "→ Tes inputs", écosystème de skills, récap, Mode D.

Le script est idempotent — peut être relancé sans risque.
"""
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SOURCE = SKILL_DIR / "ref" / "pipeline-overview.md"
TARGET = SKILL_DIR / "ref" / "pipeline-overview-public.md"

BANNER = """<!--
  AUTO-GÉNÉRÉ — ne pas modifier ce fichier manuellement.
  Source de vérité : ref/pipeline-overview.md (version interne avec "sous le capot")
  Script de build : scripts/build-public-pipeline-overview.py
  Régénération auto au pre-commit (.githooks/pre-commit).
-->

"""


def strip_internals(text: str) -> str:
    lines = text.splitlines()
    result = []
    in_sous_le_capot = False

    for line in lines:
        stripped = line.lstrip()

        # Start of "Sous le capot" block
        if not in_sous_le_capot and stripped.startswith("*Sous le capot"):
            in_sous_le_capot = True
            continue

        # Inside block — skip until → or ---
        if in_sous_le_capot:
            if line.startswith("→") or line.strip() == "---":
                in_sous_le_capot = False
                result.append(line)
            # else: drop the line silently
            continue

        # End-of-file technical note
        if stripped.startswith("*Note technique"):
            # Also pop the trailing --- separators / blank lines
            while result and (result[-1].strip() == "---" or result[-1].strip() == ""):
                result.pop()
            break

        result.append(line)

    # Trim trailing blank lines
    while result and result[-1].strip() == "":
        result.pop()
    result.append("")  # final newline

    return "\n".join(result)


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Source introuvable : {SOURCE}")

    source_text = SOURCE.read_text(encoding="utf-8")
    public_body = strip_internals(source_text)
    final_text = BANNER + public_body

    # Idempotence : ne pas réécrire si rien n'a changé
    if TARGET.exists() and TARGET.read_text(encoding="utf-8") == final_text:
        print(f"= {TARGET.name} déjà à jour")
        return

    TARGET.write_text(final_text, encoding="utf-8")
    print(f"✓ Généré : {TARGET.name} ({len(final_text.splitlines())} lignes)")


if __name__ == "__main__":
    main()
