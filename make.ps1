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
            Write-Host "Rapport HTML introuvable"
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
    "dev" {
        Write-Host "Installation de l'environnement de développement..."
        
        if (-not (Test-Path "requirements.txt")) {
            Write-Host "Génération de requirements.txt..."
            pip-compile requirements.in
        }

        if (-not (Test-Path "requirements-dev.txt")) {
            Write-Host "Génération de requirements-dev.txt..."
            pip-compile requirements-dev.in
        }

        pip install -r requirements-dev.txt
    }
    "new" {
        if ($args.Count -eq 0) {
            Write-Host "❌ Veuillez fournir un nom de commande : make new <nom>"
            return
        }

        $commandName = $args[0]
        $sourcePath = "obsidian_cli\commands\template_command.py"
        $destPath = "obsidian_cli\commands\$commandName.py"

        if (-not (Test-Path $sourcePath)) {
            Write-Host "❌ Fichier modèle manquant : $sourcePath"
            return
        }

        Copy-Item $sourcePath $destPath
        (Get-Content $destPath) -replace "nom_de_la_commande", $commandName | Set-Content $destPath

        # Ajoute automatiquement l'import + register dans cli.py
        $cliPath = "obsidian_cli\cli.py"
        $importLine = "from obsidian_cli.commands import $commandName"
        $registerLine = "$commandName.register(app)"

        # Ajoute à la fin du bloc d'import s'il n'est pas déjà là
        if (-not (Get-Content $cliPath | Select-String $importLine)) {
            (Get-Content $cliPath) |
                ForEach-Object {
                    if ($_ -match "^from obsidian_cli.commands import") {
                        "$_`, $commandName"
                    } elseif ($_ -match "^$") {
                        "$_"
                    } else {
                        $_
                    }
                } | Set-Content $cliPath
        }

        # Ajoute le register à la fin si absent
        if (-not (Get-Content $cliPath | Select-String "$registerLine")) {
            Add-Content $cliPath "`n$registerLine"
        }

        Write-Host "✅ Commande '$commandName' créée avec succès dans $destPath"
    }
    "debug" {
        Write-Host "🧪 Lancement des tests de debug scan..."

        if ($args.Count -eq 0 -or $args[0] -eq "temp") {
            Write-Host "→ Debug avec TemporaryDirectory (test_debug_scan)"
            pytest -s tests/test_scan.py::test_debug_scan
        } elseif ($args[0] -eq "inspect") {
            Write-Host "→ Debug avec C:/Temp/debug-scan (test_debug_scan_inspectable)"
            pytest -s tests/test_scan.py::test_debug_scan_inspectable
        } else {
            Write-Host "❌ Usage : make debug [temp|inspect]"
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
        Write-Host "  dev         -> installe l'environnement de dev complet"
        Write-Host "  new <nom>   -> genere une nouvelle commande CLI"
        Write-Host "  debug       -> lance un test de debug sur la commande scan (temp ou inspect)"
    }
    default {
        Write-Host "Tache inconnue : $Task"
    }
}
