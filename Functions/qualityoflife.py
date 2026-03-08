import os


def give_any_mp3(udir: str = "music"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(f"{udir}")]

def give_any_json(udir: str = "data"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(udir) if i not in {"data.json.schema"}]

def check_exists(dirs=["music", "texts"]):
    def init_temp_dirs(dirs):
        [os.makedirs(i, exist_ok=True) for i in dirs]
        
    if not all([os.path.exists(i) for i in dirs]):
        init_temp_dirs(dirs)