import tempfile
import shutil
from pathlib import Path
import frontmatter

def safe_frontmatter_write(post, path: Path):
    """Écrit un fichier Markdown de manière sécurisée en préservant son contenu."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp_file:
        tmp_file.write(frontmatter.dumps(post))
        temp_path = Path(tmp_file.name)

    shutil.move(str(temp_path), path)
