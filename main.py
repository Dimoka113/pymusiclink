from Functions.printer import Printer
from Functions.qualityoflife import *
from Functions.interface import Interface


class Config(object):
    version = 1.3 # Не редактируйте.
    whp = Printer()
    wgp = Printer("#caffc0")
    wwp = Printer("#e9e9e9")
    wrp = Printer("#f8b9b9")
    wyp = Printer("#f4f763")
    exp = Printer("#63b4f7")
    ppp = Printer("#d58eff")
    deviation = 0.02
    volume = 40

    effects = {
        "♪": ["1234567890", 3, 100, 0.1],
        "*": ["01", 8, 100, 0.03],
        "!": ["clear"]
    }

cfg = Config()
"#ffffff" # Вы можете использовать эту строчку для получения нужных цветов (если вы в vs (просто нажмите на квадратик))


def main():
    interface = Interface(cfg)
    interface.main()

if __name__ == "__main__": main()