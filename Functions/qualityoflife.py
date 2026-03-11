import os, zipfile
from pathlib import Path
from datetime import datetime
import subprocess
import sys
from pathlib import Path

def install_requirements(requirements_path="requirements.txt"):
    req_file = Path(requirements_path)
    if not req_file.exists():
        raise FileNotFoundError(f"{requirements_path} не найден")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
    except subprocess.CalledProcessError as e:
        print("Ошибка установки зависимостей.")
        raise e

def zip_files(json_files: list, track_files: list, txt_files: list):
    json_files  = [Path(p) for p in  json_files]
    track_files = [Path(p) for p in track_files]
    txt_files   = [Path(p) for p in   txt_files]
    
    if len(json_files) == 1: name = json_files[0].stem if json_files else "archive"
    else: name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    with zipfile.ZipFile(f"share/{name}.zip", "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in json_files:
            if path.suffix.lower() == ".json" and path.exists():
                z.write(path, arcname=f"data/{path.name}")
        
        for path in txt_files:
            if path.suffix.lower() == ".txt" and path.exists():
                z.write(path, arcname=f"texts/{path.name}")
        
        for path in track_files:
            if path.suffix.lower() in {".mp3", ".wav"} and path.exists():
                z.write(path, arcname=f"music/{path.name}")

def unzip_files(zip_path: str, out_dir: str = "."):
    zip_path = Path(zip_path)
    out_dir = Path(out_dir)
    json_files = []
    track_files = []
    txt_files = []

    with zipfile.ZipFile(zip_path, "r") as z:
        for member in z.infolist():
            name = Path(member.filename)
            if name.suffix.lower() == ".json":
                target = out_dir / "data" / name.name
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())
                json_files.append(target)
            elif name.suffix.lower() in {".mp3", ".wav"}:
                target = out_dir / "music" / name.name
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())
                track_files.append(target)
            elif name.suffix.lower() in {".txt"}:
                target = out_dir / "texts" / name.name
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())
                track_files.append(target)

    return json_files, track_files, txt_files


def give_any_zip(udir: str = "share"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(udir) if i.endswith(".zip")]

def give_any_mp3(udir: str = "music"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(f"{udir}")]

def give_any_txt(udir: str = "texts"):
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