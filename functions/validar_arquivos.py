import os
from dotenv import load_dotenv
load_dotenv()

def validar_arquivos_pasta(downloads_path, default_extension: str = os.getenv('DEFAULT_EXTENSION', '.sswweb')):
    files = set([os.path.join(downloads_path, f) for f in os.listdir(downloads_path) if f.endswith(default_extension)])
    return files