from Functions.qualityoflife import *
from Functions.typing import Config
from Functions.printer import Printer
from datetime import datetime
import os, json
from Functions.musicplayer import PlaySound
from time import sleep, perf_counter

class Interface(object):
    cfg = None
    def __init__(self, config: Config):
        self.cfg = config
        if not check_exists(["data", "music", "texts", "share"]):
            self.cfg.ppp.print("Были созданы нужные папки")
            self.help(is_only=True)

    def main(self):
        self.cfg.whp.clear()
        tracks = give_any_mp3()
        if len(tracks) == 0:
            self.cfg.whp.clear()
            self.cfg.wrp.print("В папке с треками нет треков!")
            self.cfg.wrp.print("0. Выход.")
            self.cfg.wyp.print("1. Вызвать меню помощи.")
            self.cfg.ppp.print("2. Обновить содержимое папок.")
            self.cfg.exp.print("3. Экспорт/Импорт ваших \"сведениями\".")
            _ = input()

            if   _ == "1": self.cfg.whp.clear(); self.help()
            elif _ == "2": self.cfg.whp.clear(); self.main()
            elif _ == "3": self.cfg.whp.clear(); self.share()
            elif _ == "0": self.cfg.whp.clear(); exit()
        else:
            while True:
                self.cfg.whp.print("Выберите, что вы хотите сделать:", formatting="bold")
                self.cfg.wrp.print("0. Выход")
                self.cfg.wgp.print("1. Записать текст и тайминги нового трека.")
                self.cfg.wwp.print("2. Воспроизвести уже существующий трек.")
                self.cfg.exp.print("3. Экспорт/Импорт ваших \"сведениями\".")
                self.cfg.wyp.print("4. Вызвать меню помощи.")
                self.cfg.rrp.print("5. Очистить ваши сохранения...")

                _ = str(input())
                if   _ == "1": self.cfg.whp.clear(); self.white_text()
                elif _ == "4": self.cfg.whp.clear(); self.help()
                elif _ == "2": self.cfg.whp.clear(); self.play()
                elif _ == "3": self.cfg.whp.clear(); self.share()
                elif _ == "5": self.cfg.rrp.clear(); self.data_delete()
                elif _ == "0": self.cfg.whp.clear(); exit()
                else: self.cfg.whp.clear(); self.cfg.wrp.print("Что вы хотите сделать?"); continue


    def _export(self):
        js = give_any_json()
        self.cfg.wrp.print("0. Для выхода в меню", end="\n"); 
        self.cfg.exp.print("-1. Если вы хотите экспортировать всё", end="\n"); 
        for track in js: self.cfg.wwp.print(f"{1+js.index(track)}. {track[0]}")
        self.cfg.wgp.print("Выберите какой файл таймингов вы хотите сохранить:", end=""); 
        number = str(input())
        if number == "0": self.cfg.whp.clear(); self.share()
        elif number == "-1":
            zip_files(
                        json_files=[json[1] for json in give_any_json()], 
                        track_files=[mp3[1] for mp3 in give_any_mp3()], 
                        txt_files=[txt[1] for txt in give_any_txt()]
                     )
            
            self.cfg.wgp.print("Эксорт завершён!"); 
            self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
            input(); self.cfg.whp.clear()
        else:
            try:
                file = js[int(number)-1]
            except:
                self.cfg.whp.clear()
                self.cfg.wrp.print("Что вы хотите сделать?"); 
                self._export()
            else:
                with open(file[1], "r", encoding="utf-8") as fe:
                    je = json.load(fe)
                    zip_files(json_files=[file[1]], track_files=[je["file"]], txt_files=[f"texts/{'.'.join(file[0].split('.')[:-1])}.txt"])
                self.cfg.wgp.print("Эксорт завершён!"); 
                self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
                input(); self.cfg.whp.clear()

    def _import(self):
        zips = give_any_zip()
        if len(zips) == 0:
            self.cfg.wrp.print("Нет архивов для импорта!")
            self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
            input(); self.cfg.whp.clear(); self.share()

        self.cfg.wrp.print("0. Для выхода в меню", end="\n"); 

        for track in zips:
            self.cfg.wwp.print(f"{1+zips.index(track)}. {track[0]}")
        self.cfg.wgp.print("Выберите какой архив вы хотите импортировать:", end=""); 
        
        number = str(input())
        if number == "0": self.cfg.whp.clear(); self.share()

        try:
            file = zips[int(number)-1][1]
        except:
            self.cfg.whp.clear()
            self.cfg.wrp.print("Что вы хотите сделать?"); 
            self._import()
        else:
            unzip_files(file)
            self.cfg.wgp.print("Импорт завершён!"); 
            self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
            input(); self.cfg.whp.clear(); self.main()

    def share(self):
        js = give_any_json()
        zip = give_any_zip()
        if len(js) != 0 or len(zip) != 0:
            self.cfg.whp.print("Выберите, что вы хотите сделать:", formatting="bold")
            self.cfg.wrp.print("0. Выход")
            self.cfg.wgp.print("1. Экспортировать (сохранить) уже существующие свидения.")
            self.cfg.wwp.print("2. Импортировать (загрузить) чьё-то сведение.")
            
            _ = str(input())
            
            if   _ == "0": self.cfg.whp.clear(); self.main()
            elif _ == "1": self.cfg.whp.clear(); self._export()
            elif _ == "2": self.cfg.whp.clear(); self._import()
        else:
            self.cfg.wrp.print("Нет таймингов/архивов для экспорта/импорта!")
            self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
            input()
            
    def help(self, is_only=False):
        self.cfg.wgp.print("Чтобы использовать этот скрипт для начала вам нужно поместить в папку \"music\" те самые треки, которые вы хотите свести.")
        self.cfg.wgp.print("В папке texts в будующем будум появляться файлы, куда вы должны будете положить текст ваших песен.")
        self.cfg.wgp.print("Дальше просто следуйте по номерам, там всё интуетивно понятно. Удачи)")
        
        if is_only: self.cfg.wyp.print("Это сообщение появиться только один раз. Вы сможете его выздать повторно, в меню скрипта.")
        self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
        input()

    def data_delete(self):
        self.cfg.rrp.print("Вы уверены, что хотите очистить ваши сохранения?")
        self.cfg.wwp.print("Напишите \"Да\" или \"Yes\" или напишите 0, чтобы открыть меню... ")
        
        text = input().lower()

        if text in ["да", "yes", "y", "yea", "yep"]:
            js   = [os.remove(js[1]) for js in  give_any_json()]
            mp3  = [os.remove(mp[1]) for mp in   give_any_mp3()]
            txts = [os.remove(txt[1]) for txt in give_any_txt()]

            self.cfg.wgp.print("Было удалено файлов: {files}.".format(files=len(mp3 + js + txts)), end="\n")
            self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
            input()
            self.cfg.whp.clear()
            self.main()
        else:
            self.cfg.whp.clear()
            self.main()

    def white_text(self):
        tracks = give_any_mp3()

        self.cfg.wrp.print("В любой момент вы можете написать 0, чтобы отменить создание.")
        self.cfg.wgp.print("Введите название сохранения: ", end=""); 
        
        def check_name():
            while True:
                name = input()
                if name == "0": return False
                elif name == "": 
                    self.cfg.wrp.clear()
                    self.cfg.wrp.print("Название не может быть пустым!", end="\n\n")
                    self.cfg.wrp.print("В любой момент вы можете написать 0, чтобы отменить создание.")
                    self.cfg.wgp.print("Введите название сохранения: ", end=""); 
                    continue


                else: return name

        name = check_name()
        if not name: return False


        self.cfg.wgp.print("Введите цвет сохранения в hex формате (#ffffff): ", end="\n"); 
        self.cfg.wyp.print("(Или просто нажмите Enter, чтобы пропустить)", formatting="italic")
        
        def check_color_exist():
            while True:
                color = input(); 
                if color == "0": return False
                elif color == "":
                    return color
                elif not contains_hex_color(color):
                    self.cfg.wrp.print("Вы уверены, что это hex цвет?", end="\n")
                    self.cfg.wgp.print("Введите цвет сохранения в hex формате (#ffffff): ", end="\n"); 
                    self.cfg.wyp.print("(Или просто нажмите Enter, чтобы пропустить)", formatting="italic")
                    input()
                    self.cfg.ppp.clear()
                else:
                    return color
                
        color = check_color_exist()

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

        def check_type_write():
            self.cfg.whp.print("Введите тип записи:", end="\n")
            self.cfg.wwp.print("1. По строчно", end="\n")
            self.cfg.wgp.print("2. По словам (новое)", end="\n")

            _type = input()
            if _type in ["1", ""]: return "line"
            elif _type in ["2"]: return "word"

        _type = check_type_write()

        def check_text_exist():
            while True:
                with open(f"texts/{name}.txt", "r", encoding="utf-8") as file:
                    text = file.read() 

                if text != "":
                    self.cfg.wgp.print("Отлично! Как будете готовы, нажмите Enter, чтобы начать запись таймингов трека!", end="\n")
                    # cfg.wyp.print("Если во время записи вы сделали ошибку, вы можете написать 1, чтобы отмотать трек до предыдущего тайминга!", end="\n")
                    self.cfg.wrp.print("Если-же, вы захотите начать сначала, напишите 2.")
                    return text
                else:
                    self.cfg.wrp.print("Текст файла пустой!\nВозможно вы забыли сохранить файл?", end="\n")
                    input()
                    self.cfg.ppp.clear()

        text = check_text_exist()
        userin = input()
        if userin == "0": return False 

        def run_write(sound: PlaySound, _type: int):
            sound.run(False)
            
            tpr = Printer(color)
            timing = datetime.now()
            data = []
            if _type == "line":
                for line in text.split("\n"):
                    if line != "":
                        self.cfg.wgp.clear()
                        temp = []
                        temp.append(line)

                        tpr.print(line, end="")
                        self.cfg.wrp.print(" <- Enter, когда начнётся эта строчка")
                        userin = input()
                        if userin == "0": return [False, 0]
                        elif userin == "2": return [False, 2]
                        temp.append(((datetime.now() - timing).total_seconds()) - self.cfg.deviation)
                        self.cfg.wgp.clear()
                        timing = datetime.now()

                        self.cfg.wgp.print(line, end="")
                        self.cfg.wrp.print(" <- Enter, когда закончится эта строчка")
                        if input() == "0":  return [False, 0]
                        elif userin == "2": return [False, 2]

                        temp.append(((datetime.now() - timing).total_seconds()) - self.cfg.deviation)
                        self.cfg.wgp.clear()

                        timing = datetime.now()

                        data.append(temp)
            elif _type == "word":
                lines_words = [line.split() for line in text.split("\n") if line.strip()]
                data = [[] for _ in lines_words]

                line_i = 0
                word_i = 0

                prev_line = None
                prev_word = None

                while line_i < len(lines_words):
                    words = lines_words[line_i]

                    self.cfg.wgp.clear()

                    # текущая строка
                    for i, w in enumerate(words):
                        if i < word_i:
                            tpr.print(w, end=" ")
                        elif i == word_i:
                            self.cfg.wgp.print(w, end=" ")
                        else:
                            self.cfg.grp.print(w, end=" ")

                    self.cfg.wrp.print("<- Enter когда начинается это слово", end="")
                    print()

                    # следующая строка (серым)
                    if line_i + 1 < len(lines_words):
                        for w in lines_words[line_i + 1]:
                            self.cfg.grp.print(w, end=" ")
                        print()


                    userin = input()
                    if userin == "0": return [False, 0]
                    elif userin == "2": return [False, 2]

                    now = ((datetime.now() - timing).total_seconds()) - self.cfg.deviation_in_word
                    timing = datetime.now()

                    # закрываем предыдущее слово
                    if prev_line is not None:
                        data[prev_line][prev_word].append(now)

                    # старт текущего слова
                    word = lines_words[line_i][word_i]
                    data[line_i].append([word, now])

                    prev_line = line_i
                    prev_word = word_i

                    word_i += 1

                    if word_i >= len(words):
                        line_i += 1
                        word_i = 0

                # закрываем последнее слово
                self.cfg.wgp.clear()
                self.cfg.wrp.print("Нажмите Enter когда закончится последнее слово")

                userin = input()
                self.cfg.wgp.clear()
                if userin == "0": return [False, 0]
                elif userin == "2": return [False, 2]

                end = ((datetime.now() - timing).total_seconds()) - self.cfg.deviation_in_word

                data[prev_line][prev_word].append(end)

            with open(f"data/{name}.json", "w+", encoding="utf-8") as file:
                json.dump(
                    {
                        "version": self.cfg.version, 
                        "file": tracks[number-1][1], 
                        "color": color, 
                        "lines": data, 
                        "_type": _type
                    }, 
                    file, indent=3, ensure_ascii=False
                )

            return [True, sound.get_time_left()]


        while True:
            playread = PlaySound(tracks[number-1][1], volume=self.cfg.volume)
            status, data = run_write(playread, _type)
            if status:
                sleep(data)
                self.cfg.wgp.clear()
                return True
            else:
                if data == 0: self.cfg.wgp.clear(); playread.stop(); return False
                elif data == 2: 
                    playread.stop(); self.cfg.wgp.clear(); continue


    def play(self):
        tracks = give_any_json()

        if len(tracks) == 0:
            self.cfg.wrp.print("У вас нет сохранённых таймингов. Создайте или импортируйте!", end="\n"); 
            self.cfg.whp.print("Нажмите Enter, чтобы открыть меню.")
            input(); self.main()

        def let_check():
            self.cfg.wrp.print("0. Для выхода в меню", end="\n"); 
            for track in tracks:
                self.cfg.wwp.print(f"{1+tracks.index(track)}. {track[0]}")
            self.cfg.wgp.print("Выберите какой трек вы хотите воспоизвести: ", end=""); 

        while True:
            let_check()
            try:
                number = int(input())
            except:
                self.cfg.whp.clear()
                self.cfg.wrp.print("Что вы хотите сделать?")
                self.play()
            if number == 0: self.cfg.whp.clear(); self.main()
            elif number <= len(tracks):
                with open(tracks[int(number)-1][1], "r", encoding="utf-8") as jsn:
                    data = json.load(jsn)
                    data["volume"] = self.cfg.volume
                    self.play_sound(**data)
            else:
                self.cfg.whp.clear()
                self.cfg.wrp.print("Такого номера не существует!")
                self.play()


    def play_sound(self, file: str, color: str, lines: list, volume: int, version: int, _type: str):
        print(self.cfg.version, version)
        if self.cfg.version > version:
            self.cfg.wrp.print(f"Версия таймингов ({version}) старее версии скрипта ({self.cfg.version}), вы уверены, что хотите воспроизвести этот трек? (y/n)")
            if not (input().lower() in ["", "y", "yes", "да", "д"]): return False
        elif self.cfg.version < version:
            self.cfg.wrp.print(f"Версия таймингов ({version}) новее версии скрипта ({self.cfg.version}), вы уверены, что хотите воспроизвести этот трек? (y/n)")
            if not (input().lower() in ["", "y", "yes", "да", "д"]): return False

        r = Printer(color)
        r.clear()

        p = PlaySound(file, volume=volume)
        timer = p.run(False)

        bonus = 0.0
        if _type == "line":
            for line, words_delay, timing in lines:
                if bonus > 0:
                    words_delay = words_delay - bonus
                    bonus = 0

                sleep(words_delay)
                timer -= words_delay

                if line in self.cfg.effects:
                    eff = self.cfg.effects[line]
                    if eff[0] == "clear": r.clear(); continue; bonus += 0.10

                    remaining = timing
                    while remaining > 0:
                        start = perf_counter()
                        r.effects.random_words(eff[0], lines=eff[1], limit=eff[2])
                        elapsed = perf_counter() - start
                        delay = eff[3] - elapsed

                        if delay > 0:
                            sleep(delay)
                            elapsed += delay

                        remaining -= elapsed
                        timer -= elapsed

                    r.clear()
                    bonus += 0.10

                else:
                    if len(line) > 0:
                        char_delay = timing / len(line)
                        for ch in line:
                            sleep(char_delay)
                            timer -= char_delay
                            r.print(ch, end='')

                    r.print("\t")

            sleep(timer)
            r.clear()

        elif _type == "word":
            bonus = 0.0
            tmp = 0.0
            tmp_w = 0.0
            for line in lines:
                for word, words_delay, timing in line:
                    if bonus > 0:
                        words_delay -= bonus
                        bonus = 0.0
                    if words_delay > 0:
                        if words_delay - tmp - tmp_w > 0:
                            sleep(words_delay - tmp - tmp_w)
                            timer -= words_delay - timing
                    tmp = 0.0
                    for w in word:
                        r.print(w, end="")
                        tt = timing / len(word)
                        sleep(tt)
                        timer -= tt
                        tmp += tt
                    r.print(" ", end="")
                r.print("", end="\n")
        sleep(timer)
        r.clear()