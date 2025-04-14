# obsidian_cli/scan.py
from pathlib import Path
import frontmatter
from typing import Dict

def scan_vault(base_path: Path) -> Dict[str, dict]:
    index = {}
    counter = 1

    for path in sorted(base_path.rglob("*.md")):
        with path.open(encoding="utf-8") as f:
            post = frontmatter.load(f)

        metadata = post.metadata
        if not metadata.get("uuid") or not metadata.get("type") or not metadata.get("title"):
            continue

        key = f"{counter:05d}"
        entry = {
            "uuid": metadata["uuid"],
            "type": metadata["type"],
            "title": metadata["title"],
            "path": str(path.relative_to(base_path)).replace("\\", "/"),
            "links": []  # ✅ Initialisation des liens ici
        }

        # ✅ Ajout du lien parent si existant
        if "parent" in metadata:
            entry["links"].append({
                "type": "parent",
                "target": metadata["parent"]
            })

        index[key] = entry
        counter += 1

    return index
