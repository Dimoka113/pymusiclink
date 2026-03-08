from rich import print as rprint
import os


class Printer(object):
    color = str()

    def __init__(self, color: str = "#ffffff"):
        if color:
            self.color = color
        else:
            self.color = "#ffffff"

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self, *words, formatting: str ="", end="\n"):
        if formatting:
            rprint(f"[{formatting} {self.color}]{' '.join(str(x) for x in words)}[/{formatting} {self.color}]", end=end, flush=True)
        else:
            rprint(f"[{self.color}]{' '.join(str(x) for x in words)}[/{self.color}]", end=end, flush=True)

# pr = Printer("#4f37b9")
# pr.print("test", "еее", formatting="")
