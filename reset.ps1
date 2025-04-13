Write-Host "Suppression de l'environnement virtuel existant..."
deactivate 2>$null
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

Write-Host "Creation du nouvel environnement virtuel..."
python -m venv .venv

Write-Host "Activation de l'environnement virtuel..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Installation du package en mode developpement..."
pip install -e .

Write-Host "Verification de la disponibilite de la commande obsidian-cli..."
$cli = Get-Command obsidian-cli -ErrorAction SilentlyContinue

if ($cli) {
    Write-Host "obsidian-cli est bien installe : $($cli.Source)"
} else {
    Write-Host "obsidian-cli est introuvable. Verifie ton setup.py ou ton environnement."
}
