from time import sleep
from rich import print as rprint
from Functions.musicplayer import PlaySound
from Functions.printer import Printer

def play_sound(file: str, color: str, lines: list):
    r = Printer(color)
    r.clear()

    p = PlaySound(file, volume=40) 
    timer = p.run(False)

    
    r = Printer(color)
    for line, words_delay, timing in lines:
        sleep(words_delay)
        timer = timer - words_delay

        for words in line:
            timimg = timing / len(line) 
            sleep(timimg)
            timer = timer - timimg

            r.print(f"{words}", end='')
        r.print("\t")

    
    sleep(timer)