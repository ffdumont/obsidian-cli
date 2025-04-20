import typer
from pathlib import Path
from obsidian_cli.scan import scan_vault

import typer
import json
from pathlib import Path
from obsidian_cli.scan import scan_vault

def scan(
    vault: str = typer.Option(None, help="Chemin vers le dossier du vault"),
    config: str = typer.Option(None, help="Chemin vers le fichier de configuration JSON"),
    index_path: str = typer.Option(None, help="Chemin de sortie pour l'index JSON")
):
    """
    Scanne un vault Obsidian et construit l'index UUID.
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
    else:
        typer.echo("❌ Vous devez spécifier --vault ou --config avec 'vault_path'.")
        raise typer.Exit(code=1)
    typer.echo(f"🔍 Scanning vault: {vault_path}")
    scan_vault(base_path=vault_path, index_path=index_path, write=True)

def register(app: typer.Typer):
    app.command(name="scan")(scan)
