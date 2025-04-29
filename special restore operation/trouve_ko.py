from pathlib import Path

vault_path = Path("G:/Mon Drive")  # ➔ adapte ici ton chemin exact
deteriorated_files = []

for path in vault_path.rglob("*.md"):
    try:
        content = path.read_text(encoding="utf-8").strip()
        # Détecter les fichiers avec uniquement un frontmatter vide
        if content == "---" or content == "---\n---" or content.replace("-", "").strip() == "":
            deteriorated_files.append(path)
    except Exception as e:
        print(f"Erreur lecture {path}: {e}")

# Construction de la liste Python proprement formatée
print("\nDAMAGED_FILES_LIST = [")
for file in deteriorated_files:
    # on convertit le chemin en chaîne Windows avec r"" pour que les backslashes soient échappés
    print(f'    r"{file}",')
print("]")

print(f"\n✅ Total : {len(deteriorated_files)} fichiers détériorés trouvés.")
