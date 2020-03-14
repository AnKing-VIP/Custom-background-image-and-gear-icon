# Copyright: ijgnd
# Modified by: The AnKing 
### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)
#
#            Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 

import os

from anki.utils import pointVersion

from aqt import mw
from aqt import gui_hooks
from anki import version as anki_version
from .config import gc 


my_css_folder = "web"

addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
my_css_folder_absolute = os.path.join(addon_path, my_css_folder)

mycssfiles = [os.path.basename(f) for f in os.listdir(my_css_folder_absolute) if f.endswith(".css")]

regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)

def replace_css(web_content, context):
    for idx, filename in enumerate(web_content.css):
        if gc("Toolbar image") == True:   
            if filename in mycssfiles:
                web_content.css[idx] = f"/_addons/{addonfoldername}/{my_css_folder}/{filename}"
        else:
            if filename == "deckbrowser.css":
                web_content.css[idx] = f"/_addons/{addonfoldername}/{my_css_folder}/{filename}"        


old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 21)

if not old_anki:                    
    gui_hooks.webview_will_set_content.append(replace_css)
