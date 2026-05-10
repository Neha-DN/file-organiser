import os
import shutil
from datetime import datetime

# ─────────────────────────────────────────────
# FILE ORGANISER — Auto-sorts Downloads + logs every move
# Upgrade: now saves a history.txt file
# ─────────────────────────────────────────────

# STEP 1: Set the folder you want to organise
DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

# STEP 2: Log file will be saved inside your project folder
LOG_FILE = "history.txt"

# STEP 3: Define categories and file types
CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos":     [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"],
    "Audio":      [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "ZipFiles":   [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs":   [".exe", ".msi", ".apk"],
    "Code":       [".py", ".js", ".html", ".css", ".java", ".cpp", ".json", ".xml"],
    "Others":     []
}

# STEP 4: This function writes one line into history.txt
def write_log(message):
    with open(LOG_FILE, "a") as log:   # "a" means append — adds to existing file, never overwrites
        log.write(message + "\n")       # write the message and go to next line

# STEP 5: The main organiser function
def organise():
    print("\n🗂  File Organiser Starting...")
    print(f"📁 Folder: {DOWNLOADS}\n")

    # Write a session header into the log file
    # Every time you run the script, a new session block is added
    session_time = datetime.now().strftime("%d-%m-%Y  %I:%M %p")  # e.g. 09-05-2026  03:45 PM
    write_log("=" * 50)
    write_log(f"  SESSION: {session_time}")
    write_log("=" * 50)

    files_moved  = 0  # count files successfully moved
    files_skipped = 0  # count files skipped (open/busy)

    # Go through every item in Downloads
    for filename in os.listdir(DOWNLOADS):

        file_path = os.path.join(DOWNLOADS, filename)

        # Skip subfolders — only move files
        if os.path.isdir(file_path):
            continue

        # Get file extension
        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        # Find the right category
        destination_folder = "Others"
        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                destination_folder = category
                break

        # Build destination path
        dest_path = os.path.join(DOWNLOADS, destination_folder)
        os.makedirs(dest_path, exist_ok=True)

        # Try to move the file — skip it if it's open in another program
        try:
            shutil.move(file_path, os.path.join(dest_path, filename))

            # ✅ File moved successfully — print and log it
            message = f"  ✅  {filename}  →  {destination_folder}/"
            print(message)
            write_log(message)
            files_moved += 1

        except PermissionError:
            # ⚠ File is open — skip it and log the skip
            message = f"  ⚠   SKIPPED (file is open): {filename}"
            print(message)
            write_log(message)
            files_skipped += 1

    # Write the summary at the end of this session
    summary = f"\n  Total moved: {files_moved}  |  Skipped: {files_skipped}\n"
    print(summary)
    write_log(summary)

    print(f"📄 Log saved to → {LOG_FILE}\n")
    print("🎉 Done!\n")

# STEP 6: Run
if __name__ == "__main__":
    organise()