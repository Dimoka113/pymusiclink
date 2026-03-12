import requests
import os
import hashlib
from Functions.printer import Printer


class Updater(object):
    local_version = str()
    r = None

    ignore = {".git", "data", "share", "music", "texts"}
    owner = "Dimoka113"
    repo = "pymusiclink"
    branch = "main"

    def __init__(self, printer: Printer, ignore: list = None, branch="main"):
        self.local_version = "0.0"
        self.branch = branch
        self.r = printer
        if ignore: self.ignore = ignore

    def run(self):
        if os.path.exists("version.txt"):
            with open("version.txt", "r", encoding="utf-8") as f:
                self.local_version = f.read().strip()

        remote_version = self.get_remote_version()
        if self.parse_version(remote_version) <= self.parse_version(self.local_version):
            return False

        tree = self.get_repo_tree()

        repo_files = {}
        for item in tree:
            if item["type"] != "blob": continue
            path = item["path"]
            if self.is_ignored(path): continue
            repo_files[path] = item["sha"]

        local_files = {}

        for root, _, files in os.walk("."):
            for file in files:
                path = os.path.join(root, file).replace("\\", "/")
                path = path.removeprefix("./")

                if path == "version.txt":
                    continue

                local_files[path] = self.sha1_file(path)

        for path, sha in repo_files.items():
            if path not in local_files:
                self.r.print("Добавлено:", path)
                self.download_file(path)
            elif local_files[path] != sha:
                self.r.print("Обновлено:", path)
                self.download_file(path)
        for path in local_files:
            if path not in repo_files and not self.is_ignored(path):
                self.r.print("Удалено:", path)
                os.remove(path)
        with open("version.txt", "w", encoding="utf-8") as f:
            f.write(remote_version)
        return True
    
    def done(self):
        self.r.print("Обновление завершено, перезапустите скрипт, чтобы оно вступило в силу.")
        exit()

    def is_ignored(self, path: str):
        parts = path.split("/")
        return any(p in self.ignore for p in parts)

    @staticmethod
    def parse_version(v):
        try: return float(v)
        except: return str(v)

    def sha1_file(self, path):
        h = hashlib.sha1()
        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    def get_remote_version(self):
        url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}/version.txt"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text.strip()

    def get_repo_tree(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{self.branch}?recursive=1"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()["tree"]

    def download_file(self, path):
        url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}/{path}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, "wb") as f:
            f.write(r.content)