import typer

app = typer.Typer()

# Import des modules de commande
from obsidian_cli.commands import hello, version

# Enregistrement des commandes
hello.register(app)
version.register(app)
