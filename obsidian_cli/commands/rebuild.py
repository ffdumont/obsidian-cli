import typer
import frontmatter
import yaml  # ✅ utilisé pour reparser proprement si besoin
from pathlib import Path
import os

from obsidian_cli.scan import scan_vault
from obsidian_cli.settings import Settings
from obsidian_cli.helpers.file_ops import safe_frontmatter_write

rebuild_app = typer.Typer(help="Reconstruire complètement l'index UUID du vault.")

@rebuild_app.command("index")
def rebuild_index(
    config: str = typer.Option(None, "--config", "-c", help="Chemin de config spécifique (optionnel)"),
    vault: Path = typer.Option(None, "--vault", help="Chemin vers le vault Obsidian (optionnel)")
):
    """Commande CLI pour reconstruire l'index du vault."""

    typer.secho("🚧 Reconstruction complète de l'index...", fg=typer.colors.YELLOW)

    settings = Settings(Path(config) if config else None)
    vault_path = vault if vault else settings.vault_path
    uuid_index_path = vault_path / "uuid_index.json"

    # Suppression de l'ancien index si présent
    if uuid_index_path.exists():
        uuid_index_path.unlink()
        typer.secho("🗑️ uuid_index.json supprimé.", fg=typer.colors.RED)

    # Suppression de l'ancien log détaillé si présent
    detailed_log_path = vault_path / "index_log.json"
    if detailed_log_path.exists():
        detailed_log_path.unlink()
        typer.secho("🗑️ index_log.json supprimé.", fg=typer.colors.RED)

    # Nettoyage des fichiers existants (on retire les uuid et key pour forcer recréation propre)
    for path in vault_path.rglob("*.md"):
        if "Modèles" in path.parts or path.name.endswith("template.md"):
            continue
        try:
            post = frontmatter.load(path)
        except Exception as e:
            typer.secho(f"❌ Erreur lecture {path}: {e}", fg=typer.colors.RED)
            continue

        modified = False
        for field in ["uuid", "key", "parent", "child"]:
            if field in post.metadata:
                del post.metadata[field]
                modified = True

        if modified:
            safe_frontmatter_write(post, path)

    # Relancer un scan complet pour réécrire les UUID et produire les index + logs
    scan_vault(
        base_path=vault_path,
        write=True,  # ✅ IMPORTANT : on écrit réellement les UUID et keys
        dry_run=False,
        force=True,
        config_path=config
    )

    typer.secho("✅ Reconstruction de l'index terminée !", fg=typer.colors.GREEN)

def register(app: typer.Typer):
    app.add_typer(rebuild_app, name="rebuild")
