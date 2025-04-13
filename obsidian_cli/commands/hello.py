import typer

def register(app: typer.Typer):
    @app.command()
    def hello(name: str = typer.Argument(..., help="Nom de la personne à saluer")):
        """Dis bonjour à quelqu'un"""
        typer.echo(f"Bonjour, {name}!")
