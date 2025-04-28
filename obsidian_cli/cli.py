import typer

app = typer.Typer()


# Import des modules de commande
from obsidian_cli.commands import hello, version, scan, create, analyze

# Enregistrement des commandes
hello.register(app)
version.register(app)
create.register(app)
scan.register(app)
analyze.register(app)


if __name__ == "__main__":
    app()
