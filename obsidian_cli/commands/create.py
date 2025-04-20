from obsidian_cli.create import create_note
from obsidian_cli.settings import Settings
from obsidian_cli.ontology import Ontology

def create(note_type, title):
    settings = Settings()  # Assuming Settings is properly initialized
    ontology = Ontology()  # Assuming Ontology is properly initialized
    file_path = create_note(note_type, title, settings, ontology)
    print(f"Note created at {file_path}")
