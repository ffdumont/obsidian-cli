from typing import List, Optional
import typer
from datetime import datetime
from obsidian_cli.helpers.classifiers import Classifier

def generate_key(note_type: str, existing_keys: List[str], structure_map: dict) -> str:
    """
    Génère une clé unique pour une note :
    - Utilise structure_map[note_type]["prefix"]
    - Sinon, fallback sur la 1ère lettre sans afficher de warning.
    """
    note_type = note_type.lower()

    if note_type in structure_map and "prefix" in structure_map[note_type]:
        prefix = structure_map[note_type]["prefix"]
    else:
        prefix = note_type[:1].upper()
        # Ne rien afficher ici pour ne pas perturber tqdm

    counter = 1
    existing_keys_set = set(existing_keys)

    while True:
        key = f"{prefix}-{counter:03}"
        if key not in existing_keys_set:
            return key
        counter += 1

def generate_filename(
    note_type: str,
    title: str,
    classifier_code: Optional[str] = None,
    date_format: str = "%y%m",
    pattern: str = "{name}",
    classifier: Optional[Classifier] = None,
) -> str:
    """
    Génère un nom de fichier basé sur le modèle de nommage et le classifieur si nécessaire.
    """
    now = datetime.now()
    date_str = now.strftime(date_format)

    # Ici : on protège l'accès à classifier
    classifier_label = ""
    if classifier and classifier_code:
        classifier_label = classifier_code

    filename = pattern.format(
        name=title,
        date=date_str,
        classifier=classifier_label,
    )

    return filename

