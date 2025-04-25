import os
import re
import json
import frontmatter
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from tqdm import tqdm

def index_notes(vault_path: Path) -> set:
    """Retourne un set des noms de notes sans extension."""
    notes = set()
    for path in vault_path.rglob("*.md"):
        notes.add(path.stem)
    return notes

def find_internal_links(text: str) -> List[str]:
    """Trouve tous les liens internes Obsidian [[...]] dans un texte."""
    return re.findall(r"\[\[([^\]]+)\]\]", text)

def analyze_note(filepath: Path, notes_index: set) -> Dict:
    with filepath.open('r', encoding='utf-8') as f:
        raw = f.read()

    try:
        post = frontmatter.loads(raw)
    except Exception as e:
        raise ValueError(f"Erreur parsing frontmatter dans {filepath.relative_to(filepath.parents[2])}: {e}")

    frontmatter_links = []
    body_links = []

    def link_info(match, context, lineno=None, property=None, semantic_type=None):
        name_only = match.split('|')[0].strip()
        exists = name_only in notes_index
        print(".", end="", flush=True)  # 🔵 Afficher un point pour chaque lien trouvé
        return {
            "target": match,
            "context": context,
            "line": lineno,
            "property": property,
            "semantic_type": semantic_type,
            "exists": exists,
            "is_note": exists
        }

    # Analyse frontmatter
    for key, value in post.metadata.items():
        if isinstance(value, str) and '[[' in value:
            matches = find_internal_links(value)
            for match in matches:
                frontmatter_links.append(link_info(match, "frontmatter", property=key, semantic_type=key.lower() if key.lower() in ("parent", "child", "children", "siblings") else None))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and '[[' in item:
                    matches = find_internal_links(item)
                    for match in matches:
                        frontmatter_links.append(link_info(match, "frontmatter", property=key, semantic_type=key.lower() if key.lower() in ("parent", "child", "children", "siblings") else None))

    # Analyse corps
    inside_code_block = False
    for lineno, line in enumerate(post.content.splitlines(), start=1):
        if line.strip().startswith("```"):
            inside_code_block = not inside_code_block
            continue
        if inside_code_block:
            continue
        matches = find_internal_links(line)
        for match in matches:
            semantic_type = None
            excalibrain_match = re.match(r"^\s*(\w+)::\s*\[\[", line)
            if excalibrain_match:
                semantic_type = excalibrain_match.group(1).lower()
            body_links.append(link_info(match, "inline", lineno=lineno, semantic_type=semantic_type))

    return {
        "file": filepath.name,
        "frontmatter_links": frontmatter_links,
        "inline_links": body_links
    }


def analyze_links_vault(
    vault_path: Path,
    output_path: Path,
    filtered_path: Path,
    log_path: Optional[Path] = None
) -> Tuple[List[Dict], List[Dict]]:
    """Scanne tout le vault et génère les fichiers d'analyse."""

    notes_index = index_notes(vault_path)
    results = []
    log_lines = []

    # 🔥 Recherche fichiers .md avec affichage progressif
    md_files = []
    print("🔍 Recherche des fichiers .md :", end="", flush=True)
    for path in vault_path.rglob("*.md"):
        md_files.append(path)
        print(".", end="", flush=True)
    print("")  # retour ligne propre

    # 📂 Scanning avec tqdm
    print("📂 Lecture des fichiers...")
    for filepath in tqdm(md_files, desc="📂 Lecture fichiers"):
        try:
            filepath.read_text(encoding='utf-8')  # Juste lecture pour valider l'accès
        except Exception as e:
            log_lines.append(f"❌ {filepath.relative_to(vault_path)} ERROR: {e}")

    # 🔍 Analyse liens
    print("🔍 Analyse des liens :", end="", flush=True)
    for filepath in md_files:
        try:
            result = analyze_note(filepath, notes_index)
            if result["frontmatter_links"] or result["inline_links"]:
                results.append(result)
            print(".", end="", flush=True)
        except Exception as e:
            log_lines.append(f"❌ {filepath.relative_to(vault_path)} ERROR during analyze: {e}")
    print("")  # retour ligne

    # ✅ Sauvegarde des résultats
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    filtered_results = []
    for note in results:
        filtered_note = {
            "file": note["file"],
            "frontmatter_links": [link for link in note["frontmatter_links"] if link["exists"] and link["is_note"]],
            "inline_links": [link for link in note["inline_links"] if link["exists"] and link["is_note"]]
        }
        if filtered_note["frontmatter_links"] or filtered_note["inline_links"]:
            filtered_results.append(filtered_note)
    filtered_path.write_text(json.dumps(filtered_results, indent=2, ensure_ascii=False), encoding='utf-8')

    if log_path:
        log_path.write_text("\n".join(log_lines), encoding='utf-8')

    return results, filtered_results
