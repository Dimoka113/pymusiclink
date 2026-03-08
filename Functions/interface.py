from Functions.qualityoflife import *
from Functions.typing import Config
from Functions.printer import Printer
from datetime import datetime
import os, json
from Functions.musicplayer import PlaySound
from Functions.musiclink import play_sound
from time import sleep

class Interface(object):
    cfg = None
    def __init__(self, config: Config):
        self.cfg = config
        if not check_exists(["music", "texts"]):
            self.cfg.ppp.print("Были созданы папки: \"music\" и \"texts\"")
            self.help(is_only=True)

    def main(self):
        self.cfg.whp.clear()
        tracks = give_any_mp3()
        if len(tracks) == 0:
            self.cfg.whp.clear()
            self.cfg.wrp.print("В папке с треками нет треков!")
            self.cfg.wyp.print("1. Вызвать меню помощи.")
            self.cfg.ppp.print("2. Обновить содержимое папок.")
            self.cfg.wrp.print("0. Выход.")
            input()
            if   _ == "1": self.cfg.whp.clear(); self.help()
            elif _ == "3": self.cfg.whp.clear(); self.help()
            elif _ == "2": self.cfg.whp.clear(); self.main()
            elif _ == "0": self.cfg.whp.clear(); exit()
        else:
            while True:
                self.cfg.whp.print("Выберите, что вы хотите сделать:", formatting="bold")
                self.cfg.wrp.print("0. Выход")
                self.cfg.wgp.print("1. Записать текст и тайминги нового трека")
                self.cfg.wwp.print("2. Воспроизвести уже существующий трек")
                self.cfg.wyp.print("3. Вызвать меню помощи.")
                _ = str(input())
                if   _ == "1": self.cfg.whp.clear(); self.white_text()
                elif _ == "3": self.cfg.whp.clear(); self.help()
                elif _ == "2": self.cfg.whp.clear(); self.play()
                elif _ == "0": self.cfg.whp.clear(); exit()
                else: self.cfg.whp.clear(); self.cfg.wrp.print("Что вы хотите сделать?"); continue


    def help(self, is_only=False):
        self.cfg.wgp.print("Чтобы использовать этот скрипт для начала вам нужно поместить в папку \"music\" те самые треки, которые вы хотите свести.")
        self.cfg.wgp.print("В папке texts в будующем будум появляться файлы, куда вы должны будете положить текст ваших песен.")
        self.cfg.wgp.print("Дальше просто следуйте по номерам, там всё интуетивно понятно. Удачи)")
        
        if is_only: self.cfg.wyp.print("Это сообщение появиться только один раз. Вы сможете его выздать повторно, в меню скрипта.")
        self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")

        input()

    def white_text(self):
        tracks = give_any_mp3()

        self.cfg.wrp.print("В любой момент вы можете написать 0, чтобы отменить создание.")
        self.cfg.wgp.print("Введите название сохранения:", end=" "); 
        
        name = input()
        if name == "0": return False

        self.cfg.wgp.print("Введите цвет сохранения в формате #ffffff:", end="\n"); 
        self.cfg.wyp.print("(Или просто нажмите Enter, чтобы пропустить)", formatting="italic")
        color = input(); 
        if color == "0": return False

        def let_check():
            for track in tracks:
                self.cfg.wwp.print(f"{1+tracks.index(track)}. {track[0]}")

            self.cfg.wgp.print("Выберите какой трек вы хотите привязать:", end=""); 

        while True:
            let_check()
            try:
                number = int(input())
                if number == "0": return False
            except:
                self.cfg.whp.clear()
            else:
                break


        if not os.path.exists(f"texts/{name}.txt"):
            with open(f"texts/{name}.txt", "w+", encoding="utf-8") as file: pass

        self.cfg.whp.print(f"Теперь полностью вставьте текст вашей песни в файл: texts/{name}.txt", end="\n")
        self.cfg.wgp.print(f"Как только текст будет вставлен, нажмите Enter", end="")

        if input() == "0": return False

        with open(f"texts/{name}.txt", "r", encoding="utf-8") as file:
            text = file.read()

        self.cfg.wgp.print("Отлично! Как будете готовы, нажмите Enter, чтобы начать запись таймингов трека!", end="\n")
        # cfg.wyp.print("Если во время записи вы сделали ошибку, вы можете написать 1, чтобы отмотать трек до предыдущего тайминга!", end="\n")
        self.cfg.wrp.print("Если-же, вы захотите начать сначала, напишите 2.")

        userin = input()
        if userin == "0": return False 

        def run_write():
            playread = PlaySound(tracks[number-1][1], volume=self.cfg.volume)
            playread.run(False)
            
            tpr = Printer(color)
            timing = datetime.now()
            data = []
            for i in text.split("\n"):
                self.cfg.wgp.clear()
                temp = []
                temp.append(i)

                tpr.print(i, end="")
                self.cfg.wrp.print(" <- Нажмите Enter, когда исполнитель начнёт петь эту строчку")
                userin = input()
                if userin == "0": return [False, 0]
                elif userin == "2": return [False, 2]

                print(datetime.now(), timing, (datetime.now() - timing).total_seconds())
                temp.append(((datetime.now() - timing).total_seconds()) - self.cfg.deviation)
                self.cfg.wgp.clear()
                timing = datetime.now()

                self.cfg.wgp.print(i, end="")
                self.cfg.wrp.print(" <- Нажмите Enter, когда исполнитель закончит петь эту строчку")
                if input() == "0": return False
                elif userin == "2": return [False, 2]

                print(datetime.now(), timing, (datetime.now() - timing).total_seconds())
                temp.append(((datetime.now() - timing).total_seconds()) - self.cfg.deviation)
                self.cfg.wgp.clear()

                timing = datetime.now()

                data.append(temp)

            with open(f"data/{name}.json", "w+", encoding="utf-8") as file:
                json.dump({"file": tracks[number-1][1], "color": color, "lines": data}, file, indent=3, ensure_ascii=False)

            print(playread.get_time_left())
            return [True, playread.get_time_left()]
            
        status, data = run_write()
        if status:
            self.cfg.wgp.clear()
            sleep(data)
        else:
            if data == 0: return False
            elif data == 2: run_write()


    def play(self):
        tracks = give_any_json()

        def let_check():
            self.cfg.wrp.print("0. Для выхода в меню", end="\n"); 
            for track in tracks:
                self.cfg.wwp.print(f"{1+tracks.index(track)}. {track[0]}")

            self.cfg.wgp.print("Выберите какой трек вы хотите воспоизвести:", end=""); 

        while True:
            let_check()
            try:
                number = int(input())
            except:
                self.cfg.whp.clear()
                self.cfg.wrp.print("Что вы хотите сделать?")
                self.play()
                return False
            
            if number == 0: self.cfg.whp.clear(); return False

            else:
                with open(tracks[int(number)-1][1], "r", encoding="utf-8") as jsn:
                    data = json.load(jsn)
                    data["volume"] = self.cfg.volume
                    play_sound(**data)