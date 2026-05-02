import os
import shutil


class FileHandler:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def get_file_info(self, filename):
        path = os.path.join(self.upload_folder, filename)
        if not os.path.exists(path):
            return None
        return {
            'name': filename,
            'path': path,
            'size': os.path.getsize(path),
            'extension': filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        }

    def delete_file(self, filename):
        path = os.path.join(self.upload_folder, filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def cleanup_old_files(self, max_age_seconds=3600):
        import time
        now = time.time()
        cleaned = 0
        for fname in os.listdir(self.upload_folder):
            fpath = os.path.join(self.upload_folder, fname)
            if os.path.isfile(fpath):
                age = now - os.path.getmtime(fpath)
                if age > max_age_seconds:
                    os.remove(fpath)
                    cleaned += 1
        return cleaned
