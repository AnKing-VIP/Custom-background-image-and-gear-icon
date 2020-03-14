# Copyright: 2020- ijgnd
# Modified by: The AnKing 
### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)
#
#            Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 

import os
import random
from aqt import mw
from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from anki import version as anki_version
from .config import gc


addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)

default_gears_list = ['AnKing.png', 'Cowboy.png', 'Crown.png', 'Cyclone.png', 'Fire.png', 'Firecracker.png', 'Globe.png', 
'HeartEyes.png', 'Nerd.png', 'Poop.png', 'Skull.png', 'Soccer.png', 'Star.png', 'Sunglasses.png']

if gc("Image name for gear") == "Random":
    gearname = random.choice(default_gears_list)
else:
    gearname = gc("Image name for gear", "gears.svg")

def replace_gears(deck_browser, content):
    old = """<img src='/_anki/imgs/gears.svg'"""
    new = f"""<img src='/_addons/{addonfoldername}/user_files/gear/{gearname}'"""
    content.tree = content.tree.replace(old, new)


old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 21)

if not old_anki:
    gui_hooks.deck_browser_will_render_content.append(replace_gears)    