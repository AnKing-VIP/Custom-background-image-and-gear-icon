# Copyright: ijgnd
#            AnKingMed
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import random

from aqt.editor import pics
from aqt import gui_hooks

from .config import addon_path, addonfoldername, gc


def add_bg_img(filecontent, imgname, location, review=False):
    #add background image for normal and nightmode
    img_web_rel_path  = f"/_addons/{addonfoldername}/user_files/background/{imgname}"
    old = "/*AnKing edits*/"
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
    if review:
        opacity = gc("background opacity review", "1")
    else:
        opacity = gc("background opacity main", "1")      
    scale = gc("background scale", "1")

    bracket_start = "body::before {"
    bracket_close = "}"     
    if review and not gc("Reviewer image"):
        background = "background-image:none!important;"
    else:    
        background = f"""
    background-image: url("{img_web_rel_path}"); 
    background-size: {gc("background-size", "contain")};  
    background-attachment: {gc("background-attachment", "fixed")}!important; 
    background-repeat: no-repeat;
    background-position: {bg_position};
    background-color: {bg_color}!important; 
    opacity: {opacity};
    content: "";
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    position: fixed;
    z-index: -99;
    will-change: transform;
    transform: scale({scale});
    """

    new = f"""{bracket_start}\n{background}\n{bracket_close}"""   
    cont = filecontent.replace(old, new) 
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
def reset_image(new_state, old_state):
    global imgname
    if new_state == "deckBrowser":
        imgname = get_bg_img()
gui_hooks.state_did_change.append(reset_image)

def adjust_deckbrowser_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "body")
    #do not invert gears if using personal image
    if gc("Image name for gear") != "gears.svg":
        old_gears = "filter: invert(180);"
        new_gears = "/* filter: invert(180); */"
        cont = cont.replace(old_gears, new_gears)
    return cont

def adjust_toolbar_css22(filecontent):
    cont = add_bg_img(filecontent, imgname, "top")
    return cont

def adjust_bottomtoolbar_css22(filecontent):  
    cont = add_bg_img(filecontent, imgname, "bottom")
    return cont

def adjust_overview_css22(filecontent):  
    cont = add_bg_img(filecontent, imgname, "body")
    return cont

def adjust_reviewer_css22(filecontent): 
    cont = add_bg_img(filecontent, imgname, "body", True)
    return cont    

def adjust_reviewerbottom_css22(filecontent):  
    cont = add_bg_img(filecontent, imgname, "bottom", True)
    return cont       
