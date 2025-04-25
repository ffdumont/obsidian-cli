import typer
from pathlib import Path
from obsidian_cli.analyze import analyze_links_vault

analyze_app = typer.Typer()

@analyze_app.command("links")
def links(
    vault: str = typer.Option(..., help="Chemin vers le dossier du vault"),
    output: str = typer.Option(None, help="Chemin du fichier de sortie brut"),
    filtered_output: str = typer.Option(None, help="Chemin du fichier de sortie filtré")
):
    """Analyse les liens internes du vault et génère des fichiers JSON + un fichier de log."""
    vault_path = Path(vault)
    if not vault_path.exists():
        typer.echo(f"❌ Vault non trouvé : {vault}")
        raise typer.Exit(code=1)

    output_path = Path(output) if output else vault_path / "analyze_links_output.json"
    filtered_path = Path(filtered_output) if filtered_output else vault_path / "analyze_links_filtered.json"
    log_path = vault_path / "analyze_links.log"

    typer.echo(f"🔍 Analyse des liens du vault : {vault_path}")
    results, filtered_results = analyze_links_vault(vault_path, output_path, filtered_path, log_path=log_path)

    total_links = sum(len(note["frontmatter_links"]) + len(note["inline_links"]) for note in results)
    total_valid_links = sum(len(note["frontmatter_links"]) + len(note["inline_links"]) for note in filtered_results)

    typer.echo("\n📊 Rapport d'analyse :")
    typer.echo(f"- 📄 Fichiers analysés                         : {len(results)}")
    typer.echo(f"- 🔗 Total de liens détectés                   : {total_links}")
    typer.echo(f"- ✅ Liens valides vers des notes .md          : {total_valid_links}")
    typer.echo(f"- 🧩 Fichiers contenant au moins 1 lien valide : {len(filtered_results)}")

def register(app: typer.Typer):
    app.add_typer(analyze_app, name="analyze")
