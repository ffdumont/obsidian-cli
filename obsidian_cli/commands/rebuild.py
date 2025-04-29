import typer
import frontmatter
import yaml  # ✅ Ajout nécessaire
from pathlib import Path
import os

from obsidian_cli.scan import scan_vault
from obsidian_cli.settings import Settings

rebuild_app = typer.Typer(help="Reconstruire complètement l'index UUID du vault.")

@rebuild_app.command("index")
def rebuild_index(
    config: str = typer.Option(None, "--config", "-c", help="Chemin de config spécifique (optionnel)")
):
    """Commande CLI pour reconstruire l'index du vault."""

    typer.secho("🚧 Reconstruction complète de l'index...", fg=typer.colors.YELLOW)

    settings = Settings()
    vault_path = settings.vault_path
    uuid_index_path = vault_path / "uuid_index.json"

    # 1. Nettoyer tous les fichiers
    for path in vault_path.rglob("*.md"):
        try:
            post = frontmatter.load(path)
            changed = False

            if "uuid" in post.metadata:
                del post.metadata["uuid"]
                changed = True
            if "key" in post.metadata:
                del post.metadata["key"]
                changed = True

            if changed:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    yaml.dump(post.metadata, f, sort_keys=False, allow_unicode=True)
                    f.write("---\n\n")
                    f.write(post.content)
        except Exception as e:
            typer.secho(f"⚠️ Erreur sur {path}: {e}", fg=typer.colors.RED)

    # 2. Supprimer l'index existant
    if uuid_index_path.exists():
        os.remove(uuid_index_path)
        typer.secho("🗑️ uuid_index.json supprimé.", fg=typer.colors.MAGENTA)

    # 3. Relancer un scan complet
    scan_vault(settings.vault_path)  # ✅ Correction ici

    typer.secho("✅ Reconstruction de l'index terminée !", fg=typer.colors.GREEN)

def register(app: typer.Typer):
    app.add_typer(rebuild_app, name="rebuild")
