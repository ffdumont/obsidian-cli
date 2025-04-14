import yaml
from pathlib import Path

def scan_vault(vault_path: Path) -> dict:
    index = {}
    current_id = 1

    for md_file in vault_path.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")

        # Frontmatter YAML attendu entre ---
        if content.startswith("---"):
            try:
                _, frontmatter, _ = content.split("---", 2)
                meta = yaml.safe_load(frontmatter)
            except Exception:
                continue  # Frontmatter mal formé, on ignore

            # Clés obligatoires
            if not all(k in meta for k in ("uuid", "type", "title")):
                continue

            key = str(current_id).zfill(5)
            index[key] = {
                "uuid": meta["uuid"],
                "type": meta["type"],
                "title": meta["title"],
                "path": str(md_file.relative_to(vault_path)).replace("\\", "/")
            }
            current_id += 1

    return index
