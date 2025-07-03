# utils/backup_utils.py

import shutil
import os
from datetime import datetime

def backup_database(db_path="neurosim_memory.db", backup_dir="backups"):
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")

    try:
        shutil.copy2(db_path, backup_path)
        print(f"Backup successful: {backup_path}")
    except Exception as e:
        print(f"Backup failed: {e}")
