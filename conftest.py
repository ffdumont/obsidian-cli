# conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil

CUSTOM_TMP_BASE = Path("G:/Mon Drive/!2-Projects/0240-2504 Obsidian CLI/.pytest-tmp")

@pytest.fixture(scope="session")
def tmp_path_base():
    CUSTOM_TMP_BASE.mkdir(parents=True, exist_ok=True)
    # Utilise tempfile.mkdtemp() pour créer un dossier unique dans ce répertoire
    path = Path(tempfile.mkdtemp(dir=CUSTOM_TMP_BASE))
    yield path
    # Nettoyage après tous les tests si tu veux
    # shutil.rmtree(path, ignore_errors=True)

@pytest.fixture
def tmp_path(tmp_path_base):
    sub = Path(tempfile.mkdtemp(dir=tmp_path_base))
    yield sub
    shutil.rmtree(sub, ignore_errors=True)
