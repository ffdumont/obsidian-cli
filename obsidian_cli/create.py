# obsidian_cli/create.py

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import yaml

from obsidian_cli.helpers.naming import generate_filename
from obsidian_cli.helpers.classifiers import Classifier
from obsidian_cli.settings import Settings
from obsidian_cli.ontology import Ontology


def create_note(
    note_type: str,
    title: str,
    settings: Settings,
    ontology: Ontology,
    classifier_code: str = None,
    parent_uuid: str = None,
) -> Path:
    """
    Crée une nouvelle note dans le vault avec le nommage dynamique et le template approprié.
    """

    vault_path = settings.vault_path
    templates_path = settings.templates_path
    naming_patterns = settings.config.get("namingPattern", {})
    pattern = naming_patterns.get(note_type, "{name}")
    date_format = settings.config.get("dateFormat", "%y%m")

    # Charger les classifieurs si nécessaires
    classifier_file = Path(settings.config.get("classificationPath", ""))
    classifier = None
    if classifier_file.exists():
        classifier = Classifier(classifier_file)

    # Génère le nom de fichier
    filename = generate_filename(
        note_type=note_type,
        title=title,
        classifier_code=classifier_code,
        date_format=date_format,
        pattern=pattern,
        classifier=classifier,
    )

    folder = vault_path / note_type
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"{filename}.md"

    # Lecture du template
    template_file = templates_path / f"{note_type}.md"
    if template_file.exists():
        content = template_file.read_text(encoding="utf-8")
    else:
        content = "# Nouvelle note\n"

    # YAML frontmatter enrichi
    metadata = {
        "uuid": str(uuid4()),
        "type": note_type,
        "title": title,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    if parent_uuid:
        metadata["parent"] = parent_uuid
    if classifier_code:
        metadata["classifier"] = classifier_code

    # Écriture finale
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(metadata, f, sort_keys=False, allow_unicode=True)
        f.write("---\n\n")
        f.write(content)

    return file_path
