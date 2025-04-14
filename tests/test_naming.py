from pathlib import Path
from obsidian_cli.helpers.naming import generate_filename
from obsidian_cli.helpers.classifiers import Classifier


def test_generate_filename_with_classifier_and_date(tmp_path: Path):
    # Simule un fichier de classifieurs
    classifier_file = tmp_path / "classification.txt"
    classifier_file.write_text("1000\tAdministration & Maison\n4000\tAéronautique", encoding="utf-8")
    classifier = Classifier(classifier_file)

    pattern = "{classifier}-{date} {name}"
    result = generate_filename(
        note_type="project",
        title="Révision chauffage",
        classifier_code="1000",
        date_format="%y%m",
        pattern=pattern,
        classifier=classifier
    )

    assert result.startswith("1000-")
    assert "Révision chauffage" in result
    date_part = result.split("-")[1].split(" ")[0]
    assert len(date_part) == 4  # yyMM
