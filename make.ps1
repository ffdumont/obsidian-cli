param (
    [string]$Task = "help"
)

switch ($Task) {
    "test" {
        Write-Host "Lancement des tests avec couverture..."
        pytest --cov=obsidian_cli tests/ --cov-report=term --cov-report=html
        if (Test-Path "htmlcov\index.html") {
            Write-Host "Ouverture du rapport de couverture HTML..."
            Start-Process "htmlcov\index.html"
        } else {
            Write-Host "Rapport HTML introuvable"
        }
    }

    "clean" {
        Write-Host "🧹 Nettoyage complet..."

        $patterns = @(
            ".venv",
            "__pycache__",
            "*.pyc",
            "htmlcov",
            ".coverage",
            "requirements.txt",
            "*.egg-info",
            "dist",
            "build",
            ".pytest_cache"
        )

        foreach ($pattern in $patterns) {
            Get-ChildItem -Path . -Include $pattern -Recurse -Force -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        }

        $testArtifacts = "G:\Mon Drive\!2-Projects\0240-2504 Obsidian CLI\.pytest-tmp"
        if (Test-Path $testArtifacts) {
            Remove-Item -Recurse -Force $testArtifacts -ErrorAction SilentlyContinue
            Write-Host "✅ Artefacts supprimés : $testArtifacts"
        }

        Write-Host "✅ Environnement et fichiers nettoyés"
    }

    "dev" {
        Write-Host "🔧 Création de l'environnement de développement..."

        python -m venv .venv
        . .\.venv\Scripts\Activate.ps1

        Write-Host "📦 Installation de pip-tools (si besoin)..."
        pip install pip-tools

        if (Test-Path "requirements.in") {
            Write-Host "📦 Compilation requirements.txt..."
            pip-compile requirements.in
        }

        if (Test-Path "requirements-dev.in") {
            Write-Host "📦 Compilation requirements-dev.txt..."
            pip-compile requirements-dev.in
        }

        pip install -r requirements.txt
        pip install -r requirements-dev.txt

        Write-Host "✅ Installation terminée. Tu peux utiliser obsidian-cli si tout est bien configuré."
    }

    "completion" {
        Write-Host "Génération du script de complétion PowerShell..."
        try {
            obsidian-cli --show-completion powershell
        } catch {
            Write-Host "Erreur : obsidian-cli non trouvé ou non installable"
        }
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

        $cliPath = "obsidian_cli\cli.py"
        $importLine = "from obsidian_cli.commands import $commandName"
        $registerLine = "$commandName.register(app)"

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

        if (-not (Get-Content $cliPath | Select-String "$registerLine")) {
            Add-Content $cliPath "`n$registerLine"
        }

        Write-Host "✅ Commande '$commandName' créée avec succès dans $destPath"
    }

    "help" {
        Write-Host "Tâches disponibles :"
        Write-Host "  test        -> Tests unitaires avec coverage"
        Write-Host "  clean       -> Nettoyage complet du projet"
        Write-Host "  dev         -> Crée et installe l'env de dev complet"
        Write-Host "  completion  -> Génère l'autocomplétion PowerShell"
        Write-Host "  new <nom>   -> Génère une nouvelle commande CLI"
    }

    default {
        Write-Host "Tâche inconnue : $Task"
    }
}
