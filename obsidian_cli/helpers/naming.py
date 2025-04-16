from typing import List
from datetime import datetime
from obsidian_cli.helpers.classifiers import Classifier

def generate_key(note_type: str, existing_keys: List[str], prefix_map=None) -> str:
    if prefix_map is None:
        prefix_map = {}

    prefix = prefix_map.get(note_type, note_type[:3].upper())
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
    classifier_code: str,
    date_format: str,
    pattern: str,
    classifier: Classifier
) -> str:
    """
    Génère un nom de fichier formaté à partir du type de note, du titre,
    d'un code classifieur et d'une date.
    """
    now = datetime.now()
    date_str = now.strftime(date_format)
    classifier_label = classifier.get_label(classifier_code)

    filename = pattern.format(
        name=title,
        classifier=classifier_code,
        label=classifier_label,
        date=date_str
    )

    return filename
