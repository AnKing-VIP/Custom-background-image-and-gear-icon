# Copyright: ijgnd
#            AnKingMed
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import random

from aqt.editor import pics

from .config import addon_path, addonfoldername, gc


def add_bg_img(filecontent, imgname, bodynightreplace=True, overview=False):
    #add background image for normal and nightmode
    img_web_rel_path  = f"/_addons/{addonfoldername}/user_files/background/{imgname}"
    old = "body {"
    night_old = "body.nightMode {"
    overview_old = "/*AnKing edits*/"
    background = f"""
    background-image: url("{img_web_rel_path}"); 
    background-size: {gc("background-size", "contain")};  
    background-position: {gc("background-position", "center")};
    background-attachment: {gc("background-attachment", "fixed")}; 
    background-repeat: {gc("background-repeat", "no-repeat")};"""
    new = f"""{old}\n{background}"""
    night_new = f"""{night_old}\n{background}"""
    bracketclose = "}"    
    overview_new = f"""{new}\n{bracketclose}\n{night_new}\n{bracketclose}"""
    if bodynightreplace:
        cont = filecontent.replace(old, new).replace(night_old, night_new)
    elif overview:  # for overview: added text so I could replace it because body isn't in the file normally
        cont = filecontent.replace(overview_old, overview_new)     
    else:  # for toolbar bottom: prepend missing class body.nightMode
        newboth = f"""{night_new}}}\n{new}"""
        cont = filecontent.replace(old, newboth) 
    return cont


def get_bg_img():
    bg_abs_path = os.path.join(addon_path, "user_files", "background")
    bgimg_list = [os.path.basename(f) for f in os.listdir(bg_abs_path) if f.endswith(pics)]
    val = gc("Image name for background")
    if val and val.lower() == "random":
        return random.choice(bgimg_list)
    if val in bgimg_list:
        return val
    else:
        # if empty or illegal value try to use 'AnKing.png' to signal that an illegal values was used
        if "AnKing.png" in bgimg_list:
            return "AnKing.png"
        else:
            return ""
 
imgname = get_bg_img()

def adjust_deckbrowser_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, True)
    #do not invert gears if using personal image
    if gc("Image name for gear") != "gears.svg":
        old_gears = "filter: invert(180);"
        new_gears = "/* filter: invert(180); */"
        cont = cont.replace(old_gears, new_gears)
    return cont


def adjust_toolbar_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, False)
    return cont

def adjust_overview_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, False, True)
    return cont
