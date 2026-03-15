from datetime import datetime
import json
text = """
test 1 test 2 test 2
test 4 test 5 test 6

"""

from Functions.printer import Printer
from Functions.interface import Interface
from Functions.updater import Updater

class Config(object):
    version = 1.53 # Не редактируйте.
    autoupdate = True
    whp = Printer()
    wgp = Printer("#caffc0")
    wwp = Printer("#e9e9e9")
    wrp = Printer("#f8b9b9")
    wyp = Printer("#f4f763")
    exp = Printer("#63b4f7")
    ppp = Printer("#d58eff")
    rrp = Printer("#f13d3d")
    
    deviation = 0.02
    volume = 40

    effects = {
        "♪": ["1234567890", 3, 100, 0.1],
        "*": ["01", 8, 100, 0.03],
        "!": ["clear"]
    }

cfg = Config()

def run_write():
    data = []
    timing = datetime.now()


print(run_write()[1])