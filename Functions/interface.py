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