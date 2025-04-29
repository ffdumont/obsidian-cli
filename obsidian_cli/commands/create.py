# obsidian_cli/commands/create.py

import typer
from obsidian_cli.create import create_note
from obsidian_cli.settings import Settings
from obsidian_cli.ontology import Ontology
from obsidian_cli.helpers.key_prefixes import load_key_prefixes

create_app = typer.Typer(help="Créer une nouvelle note.")

@create_app.command("note")
def create(
    note_type: str = typer.Argument(..., help="Type de la note"),
    title: str = typer.Argument(..., help="Titre de la note"),
    classifier_code: str = typer.Option(None, help="Classifieur optionnel"),
    parent_uuid: str = typer.Option(None, help="UUID du parent optionnel"),
    config: str = typer.Option(None, "--config", "-c", help="Chemin de config spécifique (optionnel)"),
):
    """Commande CLI pour créer une note."""
    settings = Settings()
    ontology = Ontology(settings.config.get("relationships", {}))
    file_path, key = create_note(note_type, title, settings, ontology, classifier_code, parent_uuid)
    typer.secho("✅ Note créée :", fg=typer.colors.GREEN, nl=False)
    typer.secho(f" {key}", fg=typer.colors.BLUE, nl=False)
    typer.secho(f" {file_path}", fg=typer.colors.GREEN)


def register(app: typer.Typer):
    app.add_typer(create_app, name="create")
