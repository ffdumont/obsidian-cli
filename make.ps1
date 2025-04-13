param (
    [string]$Task = "help"
)

switch ($Task) {
    "install" {
        Write-Host "Installation des dependances..."
        pip install -r requirements.txt
    }
    "test" {
        Write-Host "Lancement des tests avec couverture..."
        pytest --cov=obsidian_cli --cov-report=term --cov-report=html
        if (Test-Path "htmlcov\index.html") {
            Write-Host "Ouverture du rapport de couverture HTML..."
            Start-Process "htmlcov\index.html"
        } else {
            Write-Host "⚠️ Rapport HTML introuvable"
        }
    }
    "freeze" {
        Write-Host "Generation de requirements.txt depuis requirements.in..."
        pip-compile requirements.in
    }
    "clean" {
        Write-Host "Nettoyage des fichiers temporaires..."
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue `
            __pycache__, *.pyc, .coverage, htmlcov
    }
    "reset" {
        Write-Host "Reinitialisation de l'environnement virtuel..."
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .venv
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1
        pip install -r requirements.txt
    }
    "completion" {
        Write-Host "Generation du script de completion PowerShell..."
        try {
            obsidian-cli --show-completion powershell
        } catch {
            Write-Host "Erreur : obsidian-cli non trouve ou non installable"
        }
    }
    "help" {
        Write-Host "Taches disponibles :"
        Write-Host "  install     -> pip install -r requirements.txt"
        Write-Host "  test        -> pytest avec coverage"
        Write-Host "  freeze      -> pip-compile requirements.in"
        Write-Host "  clean       -> suppression des fichiers temporaires"
        Write-Host "  reset       -> supprime et recree l'environnement virtuel"
        Write-Host "  completion  -> affiche le script de completion PowerShell"
    }
    default {
        Write-Host "Tache inconnue : $Task"
    }
}
