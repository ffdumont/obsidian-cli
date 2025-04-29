import frontmatter
from pathlib import Path
from obsidian_cli.helpers.file_ops import safe_frontmatter_write

def clean_vault(vault_path: Path):
    count = 0
    for path in vault_path.rglob("*.md"):
        try:
            post = frontmatter.load(path)
        except Exception as e:
            print(f"❌ Erreur de lecture de {path}: {e}")
            continue

        modified = False

        # Suppression des propriétés inutiles
        for field in ["uuid", "key"]:
            if field in post.metadata:
                del post.metadata[field]
                modified = True

        # Suppression des parent/child vides ou nuls
        for field in ["parent", "child"]:
            if field in post.metadata:
                value = post.metadata[field]
                if value in ("", None, [], {}):
                    del post.metadata[field]
                    modified = True

        if modified:
            safe_frontmatter_write(post, path)
            print(f"✅ Nettoyé : {path}")
            count += 1

    print(f"\n🎉 Terminé. {count} fichiers modifiés.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python clean_uuid_key.py <chemin_vers_vault>")
    else:
        vault = Path(sys.argv[1])
        if not vault.exists():
            print(f"❌ Dossier introuvable : {vault}")
        else:
            clean_vault(vault)
