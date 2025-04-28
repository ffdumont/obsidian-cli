# obsidian_cli/create.py

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import yaml
import typer
import re

from obsidian_cli.helpers.naming import generate_filename
from obsidian_cli.helpers.classifiers import Classifier
from obsidian_cli.settings import Settings
from obsidian_cli.ontology import Ontology
from obsidian_cli.helpers.obsidian import find_daily_notes_folder

import frontmatter
import re
from pathlib import Path

def generate_next_key(vault_path: Path, note_type: str, structure_map: dict) -> str:
    """
    Génère la prochaine clé unique pour un type de note donné (ex : P-001, A-002).
    """
    note_type = note_type.lower()

    prefix = None
    if note_type in structure_map and "prefix" in structure_map[note_type]:
        prefix = structure_map[note_type]["prefix"]
    else:
        raise ValueError(f"❌ Aucun préfixe défini pour le type '{note_type}' dans structure.")

    existing_numbers = []

    for path in vault_path.rglob("*.md"):
        try:
            post = frontmatter.load(path)
            key = post.metadata.get("key")
            if key and isinstance(key, str) and key.startswith(prefix):
                suffix = key[len(prefix):].lstrip("-")
                if suffix.isdigit():
                    existing_numbers.append(int(suffix))
        except Exception:
            continue

    next_num = max(existing_numbers, default=0) + 1
    return f"{prefix}-{next_num:03}"

def create_note(
    note_type: str,
    title: str,
    settings: Settings,
    ontology: Ontology,
    classifier_code: str = None,
    parent_uuid: str = None,
) -> Path:
    """
    Crée une nouvelle note dans le vault avec clé, nommage dynamique et le template approprié.
    """

    vault_path = settings.vault_path
    templates_path = settings.templates_path
    naming_patterns = settings.config.get("namingPattern", {})
    pattern = naming_patterns.get(note_type, "{name}")
    date_format = settings.config.get("dateFormat", "%y%m")
    key_prefixes = settings.config.get("keyPrefixes", {})  # ✅ On lit ici

    # Charger les classifieurs
    classifier_file = Path(settings.config.get("classificationPath", ""))
    classifier = None
    if classifier_file.is_file():
        classifier = Classifier(classifier_file)
    elif classifier_file.exists():
        typer.echo(f"⚠️  Attention: {classifier_file} existe mais n'est pas un fichier.")
    else:
        typer.echo("⚠️  Aucun fichier de classification trouvé, les classifieurs ne seront pas utilisés.")

    # Gestion du classifier si nécessaire
    if note_type in ("area", "project") and not classifier_code:
        if not classifier:
            raise ValueError(f"Le type '{note_type}' nécessite un classifier, mais aucun fichier de classification n'est disponible.")

        typer.echo(f"\n👉 Le type '{note_type}' nécessite un classifier.")
        typer.echo("Veuillez choisir un classifieur parmi la liste suivante :")
        for code, label in classifier.classifiers.items():
            typer.echo(f"  {code} - {label}")
        classifier_code = typer.prompt("Entrez le code du classifieur souhaité")

        if classifier_code not in classifier.classifiers:
            raise ValueError(f"❌ Classifieur '{classifier_code}' inconnu. Abandon.")

    # Générer la clé
    key = generate_next_key(vault_path, note_type, key_prefixes)

    # Générer le nom de fichier
    filename = generate_filename(
        note_type=note_type,
        title=title,
        classifier_code=classifier_code,
        date_format=date_format,
        pattern=pattern,
        classifier=classifier,
    )

    # Déterminer le bon dossier
    if note_type in ("project", "task"):
        folder = find_daily_notes_folder(vault_path)
    else:
        folder = vault_path / note_type

    folder.mkdir(parents=True, exist_ok=True)

    note_folder = folder / filename
    note_folder.mkdir(parents=True, exist_ok=True)

    file_path = note_folder / f"{filename}.md"

    # Lecture du template
    template_file = templates_path / f"{note_type}.md"
    if template_file.exists():
        content = template_file.read_text(encoding="utf-8")
    else:
        content = "# Nouvelle note\n"

    # YAML frontmatter enrichi
    metadata = {
        "uuid": str(uuid4()),
        "key": key,
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
