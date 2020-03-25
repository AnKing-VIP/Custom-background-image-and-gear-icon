# Copyright: ijgnd
#            AnKingMed
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import random

from aqt.editor import pics

from .config import addon_path, addonfoldername, gc


def add_bg_img(filecontent, imgname, location, bodynightreplace=True, overview=False):
    #add background image for normal and nightmode
    img_web_rel_path  = f"/_addons/{addonfoldername}/user_files/background/{imgname}"
    old = "body {"
    night_old = "body.nightMode {"
    overview_old = "/*AnKing edits*/"
    if location == "body":
        bg_position = gc("background-position", "center")
        bg_color = gc("background-color main", "")
    elif location == "top" and gc("Toolbar top/bottom"):
        bg_position = "top"
    elif location == "bottom" and gc("Toolbar top/bottom"):
        bg_position = "bottom;"
    else:
        bg_position = f"""background-position: {gc("background-position", "center")};""" 
    if location == "top":
        bg_color = gc("background-color top", "")
    elif location == "bottom":
        bg_color = gc("background-color bottom", "")        

           
    background = f"""
    background-image: url("{img_web_rel_path}"); 
    background-size: {gc("background-size", "contain")};  
    background-attachment: {gc("background-attachment", "fixed")}; 
    background-repeat: {gc("background-repeat", "no-repeat")};
    background-position: {bg_position};
    background-color: {bg_color}!important; """

    new = f"""{old}\n{background}"""
    night_new = f"""{night_old}\n{background}"""
    bracketclose = "}"    
    overview_new = f"""{new}\n{bracketclose}\n{night_new}\n{bracketclose}"""
    if bodynightreplace:
        cont = filecontent.replace(old, new).replace(night_old, night_new)
    elif overview:  # for overview and toolbar bottom: added text so I could replace it because body isn't in the file normally
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
        # if empty or illegal value show no background to signal that an illegal values was used
        return ""
 
imgname = get_bg_img()

def adjust_deckbrowser_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "body", True)
    #do not invert gears if using personal image
    if gc("Image name for gear") != "gears.svg":
        old_gears = "filter: invert(180);"
        new_gears = "/* filter: invert(180); */"
        cont = cont.replace(old_gears, new_gears)
    return cont


def adjust_toolbar_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "top", False)
    return cont

def adjust_bottomtoolbar_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "bottom", False, True)
    return cont

def adjust_overview_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "body", False, True)
    return cont

def adjust_reviewer_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "body", True, False)
    return cont    

def adjust_reviewerbottom_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "bottom", False, False)
    return cont       
