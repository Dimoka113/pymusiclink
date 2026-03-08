from Functions.printer import Printer
import os, json
from time import sleep
from Functions.musicplayer import PlaySound
from datetime import datetime
from Functions.musiclink import play_sound

whp = Printer()
wgp = Printer("#caffc0")
wwp = Printer("#e9e9e9")
wrp = Printer("#f8b9b9")
wyp = Printer("#f4f763")

def give_any_mp3(udir: str = "music"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(f"{udir}")]

def give_any_json(udir: str = "data"):
    return [[i, f"{udir}/{i}"] for i in os.listdir(udir) if i not in {"data.json.schema"}]


def white_text():
    tracks = give_any_mp3()

    wrp.print("В любой момент вы можете написать 0, чтобы отменить создание.")
    wgp.print("Введите название сохранения:", end=" "); 
    
    name = input()
    if name == "0": return False

    wgp.print("Введите цвет сохранения в формате #ffffff:", end="\n"); 
    wyp.print("(Или просто нажмите Enter, чтобы пропустить)", formatting="italic")
    color = input(); 
    if color == "0": return False



    def let_check():
        for track in tracks:
            wwp.print(f"{1+tracks.index(track)}. {track[0]}")

        wgp.print("Выберите какой трек вы хотите привязать:", end=""); 

    while True:
        let_check()
        try:
            number = int(input())
            if number == "0": return False
        except:
            whp.clear()
        else:
            break


    if not os.path.exists(f"texts/{name}.txt"):
        with open(f"texts/{name}.txt", "w+", encoding="utf-8") as file: pass


    whp.print(f"Теперь полностью вставьте текст вашей песни в файл: texts/{name}.txt", end="\n")
    wgp.print(f"Как только текст будет вставлен, нажмите Enter", end="")

    if input() == "0": return False

    with open(f"texts/{name}.txt", "r", encoding="utf-8") as file:
        text = file.read()

    wgp.print("Отлично! Как будете готовы, нажмите Enter, чтобы начать запись таймингов трека!", end="\n")
    wyp.print("Если во время записи вы сделали ошибку, вы можете написать 1, чтобы отмотать трек до предыдущего тайминга!", end="\n")
    wrp.print("Если-же, вы захотите начать сначала, нажмите 2.")

    if input() == "0": return False

    print(tracks[number-1][1])
    PlaySound(tracks[number-1][1], volume=40).run(False)


    tpr = Printer(color)
    timing = datetime.now()

    data = []

    for i in text.split("\n"):
        wgp.clear()
        temp = []
        temp.append(i)

        tpr.print(i, end="")
        wrp.print(" <- Нажмите Enter, когда исполнитель начнёт петь эту строчку")
        if input() == "0": return False
        print(datetime.now(), timing, (datetime.now() - timing).total_seconds())
        temp.append(((datetime.now() - timing).total_seconds()) - 0.05)
        wgp.clear()
        timing = datetime.now()

        wgp.print(i, end="")
        wrp.print(" <- Нажмите Enter, когда исполнитель закончит петь эту строчку")
        if input() == "0": return False
        print(datetime.now(), timing, (datetime.now() - timing).total_seconds())
        temp.append(((datetime.now() - timing).total_seconds()) - 0.05)
        wgp.clear()

        timing = datetime.now()

        data.append(temp)

    wgp.clear()
    with open(f"data/{name}.json", "w+", encoding="utf-8") as file:
        json.dump({"file": tracks[number-1][1], "color": color, "lines": data}, file, indent=3, ensure_ascii=False)


def play():
    tracks = give_any_json()

    def let_check():
        for track in tracks:
            wwp.print(f"{1+tracks.index(track)}. {track[0]}")

        wgp.print("Выберите какой трек вы хотите воспоизвести:", end=""); 

    while True:
        let_check()
        try:
            number = int(input())
            if number == "0": return False
        except:
            whp.clear()
        else:
            with open(tracks[number-1][1], "r", encoding="utf-8") as jsn:
                data = json.load(jsn)
                play_sound(**data)

"#b922ff" # Вы можете использовать эту строчку для получения нужных цветов (если вы в vs (просто нажмите на квадратик))

if __name__ == "__main__":
    tracks = give_any_mp3()
    if len(tracks) == 0:
        whp.clear()
        wrp.print("В папке с треками нет треков!\nВыход...")
        exit()
    else:
        while True:
            whp.print("Выберите, что вы хотите сделать (1/2):", formatting="bold")
            wgp.print("1. Записать текст и тайминги нового трека")
            wwp.print("2. Воспроизвести уже существующий трек")
            wrp.print("3. Выход")

            
            _ = str(input())
            if _ == "1":
                whp.clear()
                white_text()
            elif _ == "2":
                whp.clear()
                play()
            elif _ == "3":
                whp.clear()
                exit()
            else:
                whp.clear()
                wrp.print("Что вы хотите сделать?")
                continue