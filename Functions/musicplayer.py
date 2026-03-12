from ctypes import c_buffer, windll
from random import random
from time import sleep
from sys import getfilesystemencoding
import ffmpeg, os


class PlaysoundException(Exception):
    pass

class PlaySound(object):
    file = str()
    volume = int()

    def __init__(self, file: str, volume: int = 100):
        self.file = file
        self.volume = volume
        self.alias = 'playsound_' + str(random())

    def windowscmd(self, *command):
                buf = c_buffer(255)
                command = ' '.join(command).encode(getfilesystemencoding())
                errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
                if errorCode:
                    errorBuffer = c_buffer(255)
                    windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
                    exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                        '\n        ' + command.decode() +
                                        '\n    ' + errorBuffer.value.decode('mbcs'))
                    raise PlaysoundException(exceptionMessage)
                return buf.value

    def convert(self, filename: str):
        os.rename(filename, f"{filename}.tmp")

        (
            ffmpeg
            .input(f"{filename}.tmp")
            .output(
                filename,
                map_metadata='-1',
                map='0:a',
                c='copy'
            )
            .run()
        )
        os.remove(f"{filename}.tmp")

    def get_time_left(self):
        duration = self.windowscmd('status', self.alias, 'length')
        position = self.windowscmd('status', self.alias, 'position')
        remaining = int(duration) - int(position)
        return float(remaining / 1000.0)

    def stop(self): self.windowscmd('stop', self.alias)

    def run(self, block=True):
        try:
            self.windowscmd('open "' + self.file + '" alias', self.alias)
            self.windowscmd('setaudio', self.alias, 'volume to', str(self.volume * 10))

            self.windowscmd('set', self.alias, 'time format milliseconds')
            durationInMS = self.windowscmd('status', self.alias, 'length')
            self.windowscmd('play', self.alias, 'from 0 to', durationInMS.decode('mbcs'))
        except:
            self.convert(self.file)
            self.windowscmd('open "' + self.file + '" alias', self.alias)
            self.windowscmd('setaudio', self.alias, 'volume to', str(self.volume * 10))

            self.windowscmd('set', self.alias, 'time format milliseconds')
            durationInMS = self.windowscmd('status', self.alias, 'length')
            self.windowscmd('play', self.alias, 'from 0 to', durationInMS.decode('mbcs'))

        if block:
            sleep(float(durationInMS) / 1000.0)
        else:
            return float(durationInMS.decode()) / 1000.0

# p = PlaySound(file="music/Karma.mp3", volume=100)
# p.run()