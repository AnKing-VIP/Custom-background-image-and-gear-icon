# Copyright: 2020- ijgnd
# Modified by: The AnKing 
### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)
#
#            Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 

"""
classic approach with wrap doesn't work: in main.py deckbrowser is instantiated 
before add-ons are loaded. Arthur's "Deck name in title" used a custom wrapping
function for bound methods to work around this. He plans to abandon this approach
by adding a new style hook "deck_browser_did_render" to Anki, see below.


new hooks don't help in 2020-03-01:
- gui_hooks.deck_browser_did_render is only called if the containing method is called
  with a non-default argument reuse=True which rarely happens
  this hooks was added by Arthur for the add-on "Deck name in title"
- gui_hooks.deck_browser_will_render_content(self, content): content is useless for me
  since it is:
          content = DeckBrowserContent(
            tree=self._renderDeckTree(self._dueTree),
            stats=self._renderStats(),
            countwarn=self._countWarn(),
        )
- gui_hooks.deck_browser_will_show_options_menu: useless
"""

import os
from anki.utils import pointVersion
from anki.hooks import wrap
import aqt
from aqt import mw
from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from anki import version as anki_version


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail


addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)


fileversions_for_anki_version = {
    "20": "css_files/20_deckbrowser.css",
    "21": "css_files/20_deckbrowser.css",  # version for 20 and 21 are identical
}


v = pointVersion()
if v in fileversions_for_anki_version:
    dbcss = fileversions_for_anki_version[v]
else:  # for newer Anki versions try the latest version and hope for the best
    dbcss = fileversions_for_anki_version[max(fileversions_for_anki_version, key=int)]

dbcss_abs = os.path.join(addon_path, dbcss)
imgname = gc("Image name for file in user_files subfolder", "")
img_web_rel_path  = f"/_addons/{addonfoldername}/user_files/background/{imgname}"
merged = "web/deckbrowser.css"
merged_abs = os.path.join(addon_path, merged)
merged_web_rel_path  = f"/_addons/{addonfoldername}/{merged}"

#alter the css
with open(dbcss_abs) as f:
    cont = f.read()
#define config values
background_size = gc("background-size", "contain")
background_position = gc("background-position", "center")
background_attachment = gc("background-attachment", "fixed")
background_repeat = gc("background-repeat", "no-repeat")
#add background image for normal and nightmode
old = "body {"
night_old = "body.nightMode {"
background = f"""background-image: url("{img_web_rel_path}"); 
background-size: {background_size};  
background-position: {background_position};
background-attachment: {background_attachment}; 
background-repeat: {background_repeat};"""
new = f"""{old}\n{background}"""
night_new = f"""{night_old}\n{background}"""
cont = cont.replace(old, new)
cont = cont.replace(night_old, night_new)
#do not invert gears if using personal image
if gc("Image name for gear") != "gears.svg":
    old_gears = "filter: invert(180);"
    new_gears = "/* filter: invert(180); */"
    cont = cont.replace(old_gears, new_gears)


with open(merged_abs, "w") as f:
    f.write(cont)


def replace_css(web_content, context):
    if isinstance(context, aqt.deckbrowser.DeckBrowser):
        for idx, filename in enumerate(web_content.css):
            if filename == "deckbrowser.css":
                web_content.css[idx] = merged_web_rel_path

#don't use this addon on versions earlier than 2.1.21 because it won't work
old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 21)

if not old_anki:           
    gui_hooks.webview_will_set_content.append(replace_css)

gearname = gc("Image name for gear", "gears.svg")
def replace_gears(deck_browser, content):
    print(f"in replace_gears and type of content.tree is {type(content.tree)}")  # that's a string
    old = """<img src='/_anki/imgs/gears.svg'"""
    new = f"""<img src='/_addons/{addonfoldername}/user_files/gear/{gearname}'"""
    content.tree = content.tree.replace(old, new)

if not old_anki:
    gui_hooks.deck_browser_will_render_content.append(replace_gears)    