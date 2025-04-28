import typer
import json
from pathlib import Path
from obsidian_cli.scan import scan_vault

def scan_command(
    vault: str = typer.Option(None, help="Chemin vers le dossier du vault"),
    config: str = typer.Option(None, help="Chemin vers le fichier de configuration JSON"),
    index_path: str = typer.Option(None, help="Chemin de sortie pour l'index JSON"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Affiche les changements sans écrire."),
    write: bool = typer.Option(False, "--write", "-w", help="Écrit dans les fichiers et dans l'index."),
    force: bool = typer.Option(False, "--force", help="Force la mise à jour des clés existantes."),
):
    """
    Commande CLI pour scanner un vault Obsidian et construire/corriger l'index UUID.
    """
    if config:
        config_path = Path(config)
        if not config_path.exists():
            typer.echo(f"❌ Fichier de configuration introuvable : {config}")
            raise typer.Exit(code=1)
        with config_path.open("r", encoding="utf-8") as f:
            config_data = json.load(f)
        vault_path = Path(config_data["vault_path"])
    elif vault:
        vault_path = Path(vault)
        config_path = None
    else:
        typer.echo("❌ Vous devez spécifier --vault ou --config avec 'vault_path'.")
        raise typer.Exit(code=1)

    typer.echo(f"🔍 Scanning vault: {vault_path}")
    scan_vault(
        base_path=vault_path,
        index_path=index_path,
        write=write,
        dry_run=dry_run,
        force=force,
        config_path=config  # <-- Passe le chemin de config à scan_vault
    )

def register(app: typer.Typer):
    app.command(name="scan")(scan_command)
