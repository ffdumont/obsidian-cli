import typer

def register(app: typer.Typer):
    @app.command()
    def version():
        """Affiche la version de l'application"""
        typer.echo("obsidian-cli v0.1.0")
