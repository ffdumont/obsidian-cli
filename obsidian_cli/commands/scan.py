import typer
from pathlib import Path
from obsidian_cli.scan import scan_vault

def scan(
    vault: str = typer.Option(..., help="Chemin vers le dossier du vault"),
    config: str = typer.Option(None, help="Chemin vers le fichier de configuration JSON"),
    index_path: str = typer.Option(None, help="Chemin de sortie pour l'index JSON")
):
    """
    Scanne un vault Obsidian et construit l'index UUID.
    """
    vault_path = Path(vault)
    scan_vault(base_path=vault_path, index_path=index_path, write=True)



# Ici, on définit la commande comme une fonction, pas un groupe
def register(app: typer.Typer):
    app.command(name="scan")(scan)
