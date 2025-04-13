from typer.testing import CliRunner
from obsidian_cli.cli import app
import subprocess
import sys
import os

runner = CliRunner()

def test_hello():
    result = runner.invoke(app, ["hello", "Francois"])
    assert result.exit_code == 0
    assert "Bonjour, Francois!" in result.output

def test_hello_missing_argument():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code != 0
    assert "Usage: root hello" in result.output

def test_hello_help_text():
    result = runner.invoke(app, ["hello", "--help"])
    assert result.exit_code == 0
    assert "Nom de la personne à saluer" in result.output

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "obsidian-cli v0.1.0" in result.output

def test_main_entry_point():
    """Teste que le module obsidian_cli.main fonctionne comme point d'entrée CLI."""
    result = subprocess.run(
        [sys.executable, "-m", "obsidian_cli", "hello", "Francois"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Bonjour, Francois!" in result.stdout

