from Functions.printer import Printer
from Functions.qualityoflife import *
from Functions.interface import Interface


class Config(object):
    whp = Printer()
    wgp = Printer("#caffc0")
    wwp = Printer("#e9e9e9")
    wrp = Printer("#f8b9b9")
    wyp = Printer("#f4f763")
    deviation = 0.02
    volume = 40

cfg = Config()
"#ffffff" # Вы можете использовать эту строчку для получения нужных цветов (если вы в vs (просто нажмите на квадратик))

if __name__ == "__main__":
    interface = Interface(cfg)

    tracks = give_any_mp3()
    if len(tracks) == 0:
        cfg.whp.clear()
        cfg.wrp.print("В папке с треками нет треков!\nВыход...")
        exit()
    else:
        while True:
            cfg.whp.print("Выберите, что вы хотите сделать (1/2):", formatting="bold")
            cfg.wrp.print("0. Выход")
            cfg.wgp.print("1. Записать текст и тайминги нового трека")
            cfg.wwp.print("2. Воспроизвести уже существующий трек")
            
            _ = str(input())
            if _ == "1":
                cfg.whp.clear()
                interface.white_text()
            elif _ == "2":
                cfg.whp.clear()
                interface.play()
            elif _ == "0":
                cfg.whp.clear()
                exit()
            else:
                cfg.whp.clear()
                cfg.wrp.print("Что вы хотите сделать?")
                continue