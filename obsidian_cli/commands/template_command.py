import typer

def register(app: typer.Typer):
    @app.command()
    def nom_de_la_commande(param: str = typer.Argument(..., help="Description de l'argument")):
        """Description de la commande"""
        typer.echo(f"Commande exécutée avec param = {param}")
