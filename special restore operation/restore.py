from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path
import io
import os
from googleapiclient.http import MediaIoBaseDownload

# --- CONFIGURATION ---
VAULT_PATH = Path("G:/Mon Drive")  # 📂 Ton chemin local du vault
CREDENTIALS_FILE = "credentials.json"  # 📜 Ton fichier téléchargé
DRY_RUN = False  # 🛡️ True = simulation, False = écrasement réel

# 📄 Liste des chemins des fichiers détériorés (COMPLÈTE)
DAMAGED_FILES_LIST = [
    r"G:\Mon Drive\!3-Areas\1200 Appartement Villenave d'Ornon\Impôts\Déclaration H1\Déclaration H1.md",
    r"G:\Mon Drive\!6-Archives\0000 Daily Notes\23-12\23-12-20\DA40-D-AFM-complete.pdf.md",
    r"G:\Mon Drive\!6-Archives\0000 Daily Notes\24-03\24-03-17\Da40.md"
]
# --- AUTHENTIFICATION GOOGLE DRIVE ---
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# --- UTILITAIRES ---
def find_file_id_by_name(name):
    """Cherche un fichier sur Google Drive par son nom."""
    results = service.files().list(
        q=f"name='{name}' and trashed=false",
        spaces='drive',
        fields="files(id, name)",
        pageSize=1
    ).execute()
    files = results.get('files', [])
    if not files:
        return None
    return files[0]['id']

def download_revision(file_id, revision_id):
    """Télécharge une révision spécifique d'un fichier."""
    request = service.revisions().get_media(fileId=file_id, revisionId=revision_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return fh.getvalue()

# --- RESTAURATION ---
for damaged_file_path in DAMAGED_FILES_LIST:
    local_path = Path(damaged_file_path)
    file_name = local_path.name
    print(f"🔎 Traitement de : {file_name}")

    file_id = find_file_id_by_name(file_name)
    if not file_id:
        print(f"❌ Fichier {file_name} non trouvé sur Google Drive.")
        continue

    revisions = service.revisions().list(fileId=file_id).execute()
    revisions_list = revisions.get('revisions', [])
    
    if len(revisions_list) >= 3:
        revision_to_restore = revisions_list[-3]
    elif len(revisions_list) > 0:
        revision_to_restore = revisions_list[-2]
        print(f"⚠️ Moins de 3 révisions pour {file_name}, on utilise la plus récente.")
    else:
        print(f"❌ Aucune révision disponible pour {file_name}, impossible de restaurer.")
        continue

    revision_id = revision_to_restore['id']

    try:
        file_content = download_revision(file_id, revision_id)

        if DRY_RUN:
            print(f"✅ [Dry Run] Fichier {file_name} prêt à être restauré depuis la révision {revision_id}")
        else:
            with open(local_path, 'wb') as f:
                f.write(file_content)
            print(f"✅ Fichier {file_name} restauré depuis la révision {revision_id}")
    except Exception as e:
        print(f"❌ Erreur restauration {file_name}: {e}")

print("\n🎯 Processus de restauration terminé (mode dry run = {})".format(DRY_RUN))
