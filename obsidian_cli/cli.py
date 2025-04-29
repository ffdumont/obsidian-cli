# obsidian_cli/cli.py

import typer

app = typer.Typer()

# Import des modules de commande
from obsidian_cli.commands import hello, version, scan, create, analyze, rebuild

# Enregistrement des commandes
hello.register(app)
version.register(app)
create.register(app)
scan.register(app)
analyze.register(app)
rebuild.register(app)  # ✅ Ajout du register pour rebuild

if __name__ == "__main__":
    app()
