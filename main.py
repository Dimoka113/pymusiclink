from Functions.qualityoflife import *

try:
    from Functions.printer import Printer
    from Functions.interface import Interface
    from Functions.updater import Updater
except:
    install_requirements()
    from Functions.printer import Printer
    from Functions.interface import Interface
    from Functions.updater import Updater

class Config(object):
    version = 1.57 # Не редактируйте.
    autoupdate = True
    whp = Printer()
    wgp = Printer("#caffc0")
    wwp = Printer("#e9e9e9")
    wrp = Printer("#f8b9b9")
    wyp = Printer("#f4f763")
    exp = Printer("#63b4f7")
    ppp = Printer("#d58eff")
    rrp = Printer("#f13d3d")
    grp = Printer("#858585")

    deviation = 0.02

    deviation_in_word = 0.0
    animation_in_word = 0.05
    volume = 40

    effects = {
        "♪": ["1234567890", 3, 100, 0.1],
        "*": ["01", 8, 100, 0.03],
        "!": ["clear"]
    }

cfg = Config()
"#ffffff" # Вы можете использовать эту строчку для получения нужных цветов (если вы в vs (просто нажмите на квадратик))


def main():
    if cfg.autoupdate:
        try:
            u = Updater(printer=cfg.exp, branch="main")
            if u.run(): install_requirements(); u.done(); 
        except:
            cfg.rrp.print("Не удалось проверить наличие обновлений. Проверьте подключение к интернету!")
            cfg.whp.print("Нажмите на любую клавишу, чтобы открыть скрипт, или нажмите 0, для выхода")
            if input() == "0": exit()


    interface = Interface(cfg)
    interface.main()

if __name__ == "__main__": main()