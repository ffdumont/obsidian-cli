from pathlib import Path
from typing import Dict

class Classifier:
    def __init__(self, file_path: Path):
        self.classifiers: Dict[str, str] = {}
        self._load(file_path)

    def _load(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier classification introuvable: {file_path}")

        with file_path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        code, label = line.strip().split("\t", 1)
                        self.classifiers[code] = label
                    except ValueError:
                        continue

    def get_label(self, code: str) -> str:
        return self.classifiers.get(code, "")

    def is_valid(self, code: str) -> bool:
        return code in self.classifiers

    def list_classifiers(self) -> Dict[str, str]:
        return self.classifiers.copy()

__all__ = ["Classifier"]
