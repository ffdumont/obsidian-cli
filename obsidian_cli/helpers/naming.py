from datetime import datetime
from obsidian_cli.helpers.classifiers import Classifier


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
