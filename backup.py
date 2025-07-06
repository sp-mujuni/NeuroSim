# backup_daily.py
import os
from datetime import datetime
from utils.csv_export import export_memories_to_csv
from utils.pdf_export import export_memories_to_pdf
from engine.memory_engine import MemoryEngine
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Initialize the memory engine
memory_engine = MemoryEngine()

# Generate filename with current date
date_str = datetime.now().strftime("%Y-%m-%d")
csv_file = f"backup_records_{date_str}.csv"
pdf_file = f"backup_records_{date_str}.pdf"

# Get all patient records
memories = memory_engine.get_memories()

# Export to CSV and PDF
export_memories_to_csv(memories, csv_file)
export_memories_to_pdf(memories, pdf_file)

print(f"Backups saved as {csv_file} and {pdf_file}")

# --- Google Drive Upload ---
# Authenticate Google Drive
gauth = GoogleAuth()
if not os.path.exists('settings.yaml'):
    gauth.LocalWebserverAuth()
else:
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

# Find or create the "Namulundu" folder in Google Drive
folder_name = "Namulundu"
file_list = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
if file_list:
    folder_id = file_list[0]['id']
else:
    folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    folder_id = folder['id']

# Upload CSV
csv_drive_file = drive.CreateFile({"title": csv_file, "parents": [{"id": folder_id}]})
csv_drive_file.SetContentFile(csv_file)
csv_drive_file.Upload()
print(f"Uploaded {csv_file} to Google Drive folder '{folder_name}'")

# Upload PDF
pdf_drive_file = drive.CreateFile({"title": pdf_file, "parents": [{"id": folder_id}]})
pdf_drive_file.SetContentFile(pdf_file)
pdf_drive_file.Upload()
print(f"Uploaded {pdf_file} to Google Drive folder '{folder_name}'")
