import typer

app = typer.Typer()

@app.command()
def hello(name: str = typer.Argument(..., help="Nom de la personne à saluer")):
    """Dis bonjour à quelqu'un"""
    typer.echo(f"Bonjour, {name}!")

@app.command()
def version():
    """Affiche la version de l'application"""
    typer.echo("obsidian-cli v0.1.0")
