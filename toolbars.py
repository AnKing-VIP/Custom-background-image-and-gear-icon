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
from anki.utils import pointVersion
from anki.hooks import wrap
import aqt
from aqt import mw
from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from anki import version as anki_version
from .background import imgname as backgroundimg
from .config import gc 


addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)


fileversions_for_anki_version2 = {
    "20": "css_files/20_toolbar.css",
    "21": "css_files/20_toolbar.css",  # version for 20 and 21 are identical
}


v = pointVersion()
if v in fileversions_for_anki_version2:
    tbcss = fileversions_for_anki_version2[v]
else:  # for newer Anki versions try the latest version and hope for the best
    tbcss = fileversions_for_anki_version2[max(fileversions_for_anki_version2, key=int)]

tbcss_abs = os.path.join(addon_path, tbcss)

if gc("Image name for background") == "Random" or "random":
    imgname = backgroundimg
else:
    imgname = gc("Image name for background", "")

img_web_rel_path  = f"/_addons/{addonfoldername}/user_files/background/{imgname}"
merged = "web/toolbar.css"
merged_abs = os.path.join(addon_path, merged)
merged_web_rel_path  = f"/_addons/{addonfoldername}/{merged}"

#alter the css
with open(tbcss_abs) as f:
    cont = f.read()
#define config values
background_size = gc("background-size", "contain")
background_position = gc("background-position", "center")
background_attachment = gc("background-attachment", "fixed")
background_repeat = gc("background-repeat", "no-repeat")
#add background image for normal and nightmode
old = "body {"
night = "body.nightMode {"
bracket = "}"
background = f"""background-image: url("{img_web_rel_path}"); 
background-size: {background_size};  
background-position: {background_position};
background-attachment: {background_attachment}; 
background-repeat: {background_repeat};"""
new = f"""{night}\n{background}\n{bracket}\n{old}\n{background}"""
cont = cont.replace(old, new)

with open(merged_abs, "w") as f:
    f.write(cont)