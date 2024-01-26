# Copyright: ijgnd
#            The AnKing
# Code License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 
# Background images  were obtained from Pexels.com under this license https://www.pexels.com/photo-license/
# Gear icons were obtained from Wikimedia Commons https://commons.wikimedia.org/wiki/Category:Noto_Color_Emoji_Pie (license listed in link)

import os
import random
from pathlib import Path
import json

from anki.utils import pointVersion
from aqt import mw
from aqt import gui_hooks
from aqt.editor import pics

#for the toolbar buttons
from aqt.qt import *
from aqt.addons import *
from aqt.utils import openFolder 
from .adjust_css import *

QDir.addSearchPath("CustomBackground", str(Path(__file__).parent / "AnKing"))



from .config import addon_path, addonfoldername, gc, getUserOption

#from .gui import Manager
#a = Manager()
from . import gui_updatemanager

css_folder_for_anki_version = {
    "22": "22", "23": "22", "24": "22",
    "25": "25","26": "25","27": "25","28": "25","29": "25",
    "30": "25","31": "31","32": "31","33": "31","34": "31",
    "35": "31","36": "36","37": "36","38": "36","39": "36",
    "40": "36","41": "36","42": "36","43": "36","44": "36",
    "45": "36","46": "36","47": "36","48": "36","49": "36",
    "50": "36","51": "36","52": "36","53": "36","54": "36",
    "55": "55",
}
v = str(pointVersion())

if v in css_folder_for_anki_version:
    version_folder = css_folder_for_anki_version[v]
else:  # for newer Anki versions try the latest version and hope for the best
    version_folder = css_folder_for_anki_version[max(css_folder_for_anki_version, key=int)]


regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)

#reset background when refreshing page (for use with "random" setting)
def reset_background(new_state, old_state):
    if new_state == "deckBrowser":
        from anki import version as anki_version
        old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 27)
        mw.deckBrowser.show()
        if not old_anki:        
            #mw.reset(True)
            # Anki 2.1.28 and up no longer fully redraw the toolbar on mw reset,
            # so trigger the redraw manually:
            mw.toolbar.draw()

gui_hooks.state_did_change.append(reset_background)

#reset background when changing config
def apply_config_changes(config):
    mw.moveToState("deckBrowser") 
    #mw.toolbar.draw()
mw.addonManager.setConfigUpdatedAction(__name__, apply_config_changes)


css_files_to_modify = [
    "webview.css", "deckbrowser.css", "overview.css", "reviewer-bottom.css",
    "toolbar-bottom.css", "reviewer.css", "toolbar.css",
]

from anki.utils import pointVersion 
def maybe_adjust_filename_for_2136(filename): 
    if pointVersion() >= 36: 
        filename = filename.lstrip("css/") 
    return filename

def inject_css(web_content, context):
    for filename in web_content.css.copy():
        filename = maybe_adjust_filename_for_2136(filename)
        if filename in css_files_to_modify:
            web_content.css.append(f"/_addons/{addonfoldername}/web/css/{version_folder}/{filename}")
            web_content.css.append(f"/_addons/{addonfoldername}/user_files/css/custom_{filename}")

        f = filename
        css = ''
        if f == "deckbrowser.css":
            css = adjust_deckbrowser_css()
        if f == "toolbar.css" and gc("Toolbar image"):
            css = adjust_toolbar_css()
        if f == "overview.css":
            css = adjust_overview_css()
        if f == "toolbar-bottom.css" and gc("Toolbar image"):
            css = adjust_bottomtoolbar_css()
        if f == "reviewer.css" and gc("Reviewer image"):
            css = adjust_reviewer_css()
        if f == "reviewer-bottom.css":
            if v == 22:
                if gc("Reviewer image") and gc("Toolbar image"):
                    css = adjust_reviewerbottom_css()
            else:
                css = adjust_reviewerbottom_css()
        if css:
            web_content.head += f"<style>{css}</style>"

def inject_css_into_ts_page(web):
    page = os.path.basename(web.page().url().path())
    if page != "congrats.html":
        return
    css = adjust_congrats_css()
    web.eval(
        """
(() => {
    const style = document.createElement("style");
    style.textContent= %s;
    document.head.appendChild(style);
})();
""" % json.dumps(css)
    )

gui_hooks.webview_will_set_content.append(inject_css)
gui_hooks.webview_did_inject_style_into_page.append(inject_css_into_ts_page)

def get_gearfile():
    gear_abs = os.path.join(addon_path, "user_files", "gear")
    os.makedirs(gear_abs, exist_ok=True)
    if not os.listdir(gear_abs):
        shutil.copytree(src=os.path.join(addon_path, "user_files", "default_gear"), dst=gear_abs, dirs_exist_ok=True)

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


#No longer needed
'''
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
'''
