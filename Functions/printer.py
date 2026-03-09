from rich import print as rprint
import os, random

class Printer(object):
    color = str()
    effects = None
    def __init__(self, color: str = "#ffffff"):
        if color:
            self.color = color
        else:
            self.color = "#ffffff"
        self.effects = Effects(self)

    def clear(self): os.system('cls' if os.name == 'nt' else 'clear')

    def print(self, *words, formatting: str ="", end="\n"):
        if formatting:
            rprint(f"[{formatting} {self.color}]{' '.join(str(x) for x in words)}[/{formatting} {self.color}]", end=end)
        else:
            rprint(f"[{self.color}]{' '.join(str(x) for x in words)}[/{self.color}]", end=end)

class Effects(object):
    r: Printer = None

    def __init__(self, printer: Printer):
        self.r = printer

    def random_words(self, words, lines, limit, clear=True):
        if clear:
            self.r.clear()

        block = "\n".join(
            "".join(random.choices(words, k=limit))
            for _ in range(lines)
        )

        self.r.print(block)

# pr = Printer("#4f37b9")
# pr.print("test", "еее", formatting="")