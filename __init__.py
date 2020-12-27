# Copyright: ijgnd
#            The AnKing
# Code License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 
# Background images  were obtained from Pexels.com under this license https://www.pexels.com/photo-license/
# Gear icons were obtained from Wikimedia Commons https://commons.wikimedia.org/wiki/Category:Noto_Color_Emoji_Pie (license listed in link)

import os
import random

from anki.utils import pointVersion
from aqt import mw
from aqt import gui_hooks
from aqt.editor import pics

#for the toolbar buttons
from aqt.qt import *
from aqt.addons import *
from aqt.utils import openFolder, showInfo


from .config import addon_path, addonfoldername, gc



css_folder_for_anki_version = {
    "22": "22",
    "23": "22",  # example: for Anki version 23 use the contents of the folder 22 
}


v = pointVersion()
if v in css_folder_for_anki_version:
    version_folder = css_folder_for_anki_version[v]
else:  # for newer Anki versions try the latest version and hope for the best
    version_folder = css_folder_for_anki_version[max(css_folder_for_anki_version, key=int)]


source_absolute = os.path.join(addon_path, "sources", "css", version_folder)
web_absolute = os.path.join(addon_path, "web", "css")

regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)


# on startup: combine template files with config and write into webexports folder
change_copy = [os.path.basename(f) for f in os.listdir(source_absolute) if f.endswith(".css")]
for f in change_copy:
    with open(os.path.join(source_absolute, f)) as FO:
        filecontent = FO.read()

    if v == 22:
        from .adjust_css_files22 import *
        if f == "deckbrowser.css":
            filecontent = adjust_deckbrowser_css22(filecontent)
        if f == "toolbar.css" and gc("Toolbar image"):
            filecontent = adjust_toolbar_css22(filecontent)
        if f == "overview.css":
            filecontent = adjust_overview_css22(filecontent)
        if f == "toolbar-bottom.css" and gc("Toolbar image"):
            filecontent = adjust_bottomtoolbar_css22(filecontent)
        if f == "reviewer.css" and gc("Reviewer image"):
            filecontent = adjust_reviewer_css22(filecontent)
        if f == "reviewer-bottom.css" and gc("Reviewer image") and gc("Toolbar image"):
            filecontent = adjust_reviewerbottom_css22(filecontent)                        

    # for later versions: try the latest
    # this code will likely change when new Anki versions are released which might require 
    # updates of this add-on.
    else: 
        from .adjust_css_files22 import *
        if f == "deckbrowser.css":
            filecontent = adjust_deckbrowser_css22(filecontent)
        if f == "toolbar.css" and gc("Toolbar image"):
            filecontent = adjust_toolbar_css22(filecontent)
        if f == "overview.css":
            filecontent = adjust_overview_css22(filecontent)
        if f == "toolbar-bottom.css" and gc("Toolbar image"):
            filecontent = adjust_bottomtoolbar_css22(filecontent)
        if f == "reviewer.css" and gc("Reviewer image"):
            filecontent = adjust_reviewer_css22(filecontent)
        if f == "reviewer-bottom.css" and gc("Reviewer image"):
            filecontent = adjust_reviewerbottom_css22(filecontent)                           

    with open(os.path.join(web_absolute, f), "w") as FO:
        FO.write(filecontent)


css_files_to_replace = [os.path.basename(f) for f in os.listdir(web_absolute) if f.endswith(".css")]

from anki.utils import pointVersion 
def maybe_adjust_filename_for_2136(filename): 
    if pointVersion() >= 36: 
        filename = filename.lstrip("css/") 
    return filename

def replace_css(web_content, context):
    for idx, filename in enumerate(web_content.css):
        filename = maybe_adjust_filename_for_2136(filename)
        if filename in css_files_to_replace:
            web_content.css[idx] = f"/_addons/{addonfoldername}/web/css/{filename}"
            web_content.css.append(f"/_addons/{addonfoldername}/user_files/css/custom_{filename}")
gui_hooks.webview_will_set_content.append(replace_css)


def get_gearfile():
    gear_abs = os.path.join(addon_path, "user_files", "gear")
    gear_list = [os.path.basename(f) for f in os.listdir(gear_abs) if f.endswith(pics)]
    val = gc("Image name for gear")
    if val and val.lower() == "random":
        return random.choice(gear_list)
    if val in gear_list:
        return val
    else:
        # if empty or illegal value try to use 'AnKing.png' to signal that an illegal values was
        # used AnKing's gears folder doesn't contain a file named "gears.svg"
        if "AnKing.png" in gear_list:
            return "AnKing.png"
        else:
            return ""


def replace_gears(deck_browser, content):
    old = """<img src='/_anki/imgs/gears.svg'"""
    new = f"""<img src='/_addons/{addonfoldername}/user_files/gear/{get_gearfile()}'"""
    if gc("Image name for gear") != "gears.svg":
        content.tree = content.tree.replace(old, new)
    else:
        content.tree = content.tree.replace(old, old)
gui_hooks.deck_browser_will_render_content.append(replace_gears)


menu = QMenu(('Custom Background & Gear Icon'), mw)
mw.form.menuTools.addMenu(menu)

#add config button
def on_advanced_settings():
	addonDlg = AddonsDialog(mw.addonManager)
	addonDlg.accept() #closes addon dialog
	ConfigEditor(addonDlg,__name__,mw.addonManager.getConfig(__name__))

#menu.addSeparator()
advanced_settings = QAction('Set up Background/Gear (Config)', mw)
menu.addAction(advanced_settings)
advanced_settings.triggered.connect(on_advanced_settings)

shortcut = gc("Keyboard Shortcut", "Ctrl+shift+b")
#add folder button
imgfolder = os.path.join(addon_path, "user_files") 
action = QAction(mw) 
action.setText("Background/gear image folder") 
action.setShortcut(QKeySequence(shortcut))
menu.addAction(action) 
action.triggered.connect(lambda: openFolder(imgfolder))

def wc(arg, val):
    config = mw.addonManager.getConfig(__name__)
    config[arg] = val
    mw.addonManager.writeConfig(__name__, config)

def notify():
    if pointVersion() >=36:
        if gc("notify", True):
            message = """The <i>Custom Background and Gear Icon addon</i> you have updated or downloaded
            has not been fully tested for Anki 2.1.36+. 
            <br><br>
            We are currently testing a version with multiple other updates on our 
            <a href="https://www.patreon.com/ankingmed">Patreon</a>.
            <br><br>
            Thanks,
            <br>
                 -The AnKing
            """
            showInfo(message, textFormat="rich")
            wc("notify", False)
notify()
