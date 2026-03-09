import os
import zipfile
from pathlib import Path


def zip_files(json_dir: str, track_dir: str, all: bool = False):

    json_dir = Path(json_dir)
    track_dir = Path(track_dir)

    name = json_dir.stem

    allowed = {".json", ".mp3", ".wav"}

    with zipfile.ZipFile(f"share/{name}.zip", "w", compression=zipfile.ZIP_DEFLATED) as z:
        for base in [json_dir, track_dir]:
            for root, dirs, files in os.walk(base):
                root = Path(root)
                for file in files:
                    path = root / file
                    if not all and path.suffix.lower() not in allowed:
                        continue
                    arcname = path.relative_to(base)
                    z.write(path, arcname=arcname)


def give_any_zip(udir: str = "share"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(udir) if i.endswith(".zip")]

def give_any_mp3(udir: str = "music"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(f"{udir}")]

def give_any_json(udir: str = "data"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(udir) if i not in {"data.json.schema"}]

def check_exists(dirs: list):
    def init_temp_dirs(dirs):
        [os.makedirs(i, exist_ok=True) for i in dirs]
        
    if not all([os.path.exists(i) for i in dirs]):
        init_temp_dirs(dirs)
        return False
    return True