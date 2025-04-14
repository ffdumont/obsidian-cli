import tempfile
from pathlib import Path
from obsidian_cli.helpers.classifiers import Classifier

def test_classifier_loading():
    content = """1000\tAdministration & Maison
2000\tSavoirs
2100\tPhilosophie
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "classification.txt"
        path.write_text(content, encoding="utf-8")

        c = Classifier(path)

        assert c.get_label("1000") == "Administration & Maison"
        assert c.is_valid("2000")
        assert not c.is_valid("9999")
        all_codes = c.list_classifiers()
        assert len(all_codes) == 3
