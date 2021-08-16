# -*- coding: utf-8 -*-
# Copyright: Lovac42 (much of this card heavily borrowed from the Dancing Baloney Add-on)
# Copyright: The AnKing 
# Also thanks to ijgnord who helped on this
# Support: 
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt.qt import *
from aqt import mw
from aqt.utils import getFile, openFolder
from anki import version as anki_version

import webbrowser

from .settings import Ui_Dialog
from .config import getUserOption, writeConfig, addon_path, getDefaultConfig
conf = getUserOption()

imgfolder = os.path.join(addon_path, "user_files") 
RE_BG_IMG_EXT = "*.gif *.png *.apng *.jpg *.jpeg *.svg *.ico *.bmp"


def getMenu(parent, menuName):
    menu = None
    for a in parent.form.menubar.actions():
        if menuName == a.text():
            menu = a.menu()
            break
    if not menu:
        menu = parent.form.menubar.addMenu(menuName)
    return menu

class SettingsDialog(QDialog):
    timer = None

    def __init__(self, parent):
        QDialog.__init__(self, mw, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.parent = parent
        self.setupDialog()
        self.loadConfigData()
        self.setupConnections()
        
        self.exec_()


    def reject(self):
        self.accept()
        self.close()

    def accept(self):
        QDialog.accept(self)
        self.close()

    def setupDialog(self):
        self.form = Ui_Dialog()
        self.form.setupUi(self)

    def setupConnections(self):
        f = self.form
        
        # PushButtons -------------
        f.OkButton.clicked.connect(self.accept)
        f.RestoreButton.clicked.connect(self.resetConfig)

        f.pushButton_randomize.clicked.connect(self.random)
        f.pushButton_imageFolder.clicked.connect(lambda: openFolder(imgfolder))
        f.pushButton_videoTutorial.clicked.connect(lambda _:self.openWeb("video"))

        f.toolButton_website.clicked.connect(lambda _:self.openWeb("anking")) 
        f.toolButton_youtube.clicked.connect(lambda _:self.openWeb("youtube"))
        f.toolButton_patreon.clicked.connect(lambda _:self.openWeb("patreon"))
        f.toolButton_instagram.clicked.connect(lambda _:self.openWeb("instagram"))
        f.toolButton_facebook.clicked.connect(lambda _:self.openWeb("facebook"))

        # Color Pickers -------------
        controller = {
            f.toolButton_color_main : (f.lineEdit_color_main,),
            f.toolButton_color_top : (f.lineEdit_color_top,),
            f.toolButton_color_bottom : (f.lineEdit_color_bottom,),
        }
        for btn,args in controller.items():
            btn.clicked.connect(
                lambda a="a",args=args:self.getColors(a,*args)
            )

        # File Buttons -----------------------
        controller = {
          # Image Buttons -----------------------
            f.toolButton_background : (f.lineEdit_background,),
        }
        for btn,args in controller.items():
            # 'a' is used to get around an issue
            # with pything binding
            btn.clicked.connect(
                lambda a="a",args=args:self._getFile(a,*args)
            )
        # File Buttons -----------------------
        controller = {
          # Image Buttons -----------------------
            f.toolButton_gear : (f.lineEdit_gear,),
        }
        for btn,args in controller.items():
            # 'a' is used to get around an issue
            # with pything binding
            btn.clicked.connect(
                lambda a="a",args=args:self._getGearFile(a,*args)
            )

        # Checkboxes ----------------
        controller = {
            f.checkBox_reviewer: ("Reviewer image",),
            f.checkBox_toolbar: ("Toolbar image",),
            f.checkBox_topbottom: ("Toolbar top/bottom",),
        }
        for cb,args in controller.items():
            cb.stateChanged.connect(
                lambda cb=cb,args=args:self._updateCheckbox(cb, *args)
            )  

        # Comboboxes ---------------
        controller = {
            f.comboBox_attachment: ("background-attachment",),
            f.comboBox_position: ("background-position",),
            f.comboBox_size: ("background-size",),
        }
        for cb,args in controller.items():
            t = cb.currentText()
            cb.currentTextChanged.connect(
                lambda t=t,args=args:self._updateComboBox(t, *args)
            )           

        # Sliders --------------             
        controller = {
            f.Slider_main : ("background opacity main",),
            f.Slider_review : ("background opacity review",),
        }
        for slider,args in controller.items():
            s = slider.value()
            slider.valueChanged.connect(
                lambda s=s,args=args:self._updateSliderLabel(s, *args)
            )

        # QDoubleSpinBox ------------
        f.scaleBox.valueChanged.connect(self._updateSpinBox)

        # LineEdits -------------
        a = f.lineEdit_background
        t = a.text()
        a.textChanged.connect(lambda t=a.text():self._updateLineEdit(t,"Image name for background")) 

        a = f.lineEdit_gear
        t = a.text()
        a.textChanged.connect(lambda t=a.text():self._updateLineEdit(t,"Image name for gear")) 

        a = f.lineEdit_color_main
        t = a.text()
        a.textChanged.connect(lambda t=a.text():self._updateLineEdit(t,"background-color main")) 

        a = f.lineEdit_color_top
        t = a.text()
        a.textChanged.connect(lambda t=a.text():self._updateLineEdit(t,"background-color top")) 

        a = f.lineEdit_color_bottom
        t = a.text()
        a.textChanged.connect(lambda t=a.text():self._updateLineEdit(t,"background-color bottom")) 


    def loadConfigData(self):
        f = self.form

        # Checkboxes -------------
        c = conf["Reviewer image"]
        if f.checkBox_reviewer.isChecked() != c:
            f.checkBox_reviewer.click()

        c = conf["Toolbar image"]
        if f.checkBox_toolbar.isChecked() != c:
            f.checkBox_toolbar.click()

        c = conf["Toolbar top/bottom"]
        if f.checkBox_topbottom.isChecked() != c:
            f.checkBox_topbottom.click()

        # Comboboxes -------------
        c = conf["background-attachment"]
        f.comboBox_attachment.setCurrentText(c)

        c = conf["background-position"]
        f.comboBox_position.setCurrentText(c)

        c = conf["background-size"]
        f.comboBox_size.setCurrentText(c)

        # Sliders --------------
        c = float(conf["background opacity main"])
        f.Slider_main.setValue(c*100)

        c = float(conf["background opacity review"])
        f.Slider_review.setValue(c*100)

        # QDoubleSpinBox ------------------
        c = float(conf["background scale"])
        f.scaleBox.setValue(c)

        # LineEdits -------------
        t = conf["Image name for background"]
        f.lineEdit_background.setText(t)

        t = conf["Image name for gear"]
        f.lineEdit_gear.setText(t)

        t = conf["background-color main"]
        f.lineEdit_color_main.setText(t)

        t = conf["background-color top"]
        f.lineEdit_color_top.setText(t)

        t = conf["background-color bottom"]
        f.lineEdit_color_bottom.setText(t)        


    def _getFile(self, pad, lineEditor, ext=RE_BG_IMG_EXT):
        def setWallpaper(path):
            f = path.split("user_files/background/")[-1]
            lineEditor.setText(f)

        f = getFile(mw, "Wallpaper",
            cb=setWallpaper,
            filter=ext,
            dir=f"{addon_path}/user_files/background"
        )

    def _getGearFile(self, pad, lineEditor, ext=RE_BG_IMG_EXT):
        def setWallpaper(path):
            f = path.split("user_files/gear/")[-1]
            lineEditor.setText(f)

        f = getFile(mw, "Gear icon",
            cb=setWallpaper,
            filter=ext,
            dir=f"{addon_path}/user_files/gear"
        )

    def _updateCheckbox(self, cb, key):
        n = -1 if cb==2 else 1
        v = True if n ==-1 else False
        conf[key] = v
        writeConfig(conf)
        self._refresh()

    def _updateComboBox(self, text, key):
        conf[key] = text
        writeConfig(conf)
        self._refresh()

    def _updateSliderLabel(self, val, key):
        conf[key] = str(round(val/100,2))
        writeConfig(conf)
        self._refresh()

    def _updateSpinBox(self):
        f = self.form
        n = round(f.scaleBox.value(),2)
        conf["background scale"] = str(n)
        writeConfig(conf)
        self._refresh()

    def _updateLineEdit(self, text, key):
        conf[key] = text
        writeConfig(conf)
        self._refresh()

    def getColors(self, pad, lineEditor):
        qcolor = QColorDialog.getColor()
        if not qcolor.isValid():
            return
        color = qcolor.name()
        lineEditor.setText(color)
   
    def openWeb(self, site):
        if site == "anking":
            webbrowser.open('https://www.ankingmed.com')
        elif site == "youtube":        
            webbrowser.open('https://www.youtube.com/theanking')
        elif site == "patreon":        
            webbrowser.open('https://www.patreon.com/ankingmed')
        elif site == "instagram":        
            webbrowser.open('https://instagram.com/ankingmed')
        elif site == "facebook":        
            webbrowser.open('https://facebook.com/ankingmed')
        elif site == "video":        
            webbrowser.open('https://youtu.be/5XAq0KpU3Jc')

    def random(self):
        f = self.form
        f.lineEdit_background.setText("random")
        f.lineEdit_gear.setText("random")
    
    def resetConfig(self):
        global conf
        conf = getDefaultConfig()
        writeConfig(conf)
        self._refresh()
        self.close()
        SettingsDialogExecute()

    def _refresh(self, ms=100):
        if self.timer:
            self.timer.stop()
        old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 27)

        if old_anki:        
            self.timer = mw.progress.timer(
                ms, lambda:mw.reset(True), False)  
        else:
            self.timer = mw.progress.timer(
                ms, self._resetMainWindow, False)

    def _resetMainWindow(self):
        mw.reset(True)
        # Anki 2.1.28 and up no longer fully redraw the toolbar on mw reset,
        # so trigger the redraw manually:
        mw.toolbar.draw()
        # NOTE (Glutanimate):
        # This is not an ideal solution as forcing a full redraw might
        # interfere with the background sync indicator and potentially other
        # add-ons in the future. For a definitive fix please consider refactoring
        # the add-on so that the web content is updated dynamically without
        # having to reload the web view.




def SettingsDialogExecute():
    SettingsDialog(mw)
    

'''
m = getMenu(mw, "&View")
a = QAction("Custom Background and Gear Icon", mw)
a.triggered.connect(SettingsDialogExecute)
m.addAction(a)
'''
mw.addonManager.setConfigAction(__name__, SettingsDialogExecute)

'''
def add_menu(Name, Button, exe, *sc):
	action = QAction(Button, mw)
	action.triggered.connect(exe)
	if not hasattr(mw, 'menu'):
		mw.menu = {}
	if Name not in mw.menu:
		add = QMenu(Name, mw)
		mw.menu[Name] = add
		mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(), add)
	mw.menu[Name].addAction(action)
	for i in sc:
		action.setShortcut(QKeySequence(i))

add_menu('&AnKing',"Custom BackGround and Gear Icon", SettingsDialogExecute, 'Shift+X')
'''


def getMenu(parent, menuName):
    menubar = parent.form.menubar
    for a in menubar.actions():
        if menuName == a.text():
            return a.menu()
    else:
        return menubar.addMenu(menuName)


def getSubMenu(menu, subMenuName):
    for a in menu.actions():
        if subMenuName == a.text():
            return a.menu()
    else:
        subMenu = QMenu(subMenuName, menu)
        menu.addMenu(subMenu)
        return subMenu

def openWeb1():
    webbrowser.open('https://courses.ankipalace.com/?utm_source=anking_bg_add-on&utm_medium=anki_add-on&utm_campaign=mastery_course')

def openWeb2():
    webbrowser.open('https://www.ankipalace.com/memberships')

def openWeb3():
    webbrowser.open('https://www.ankipalace.com/tutoring')

def setupMenu():
    MENU_OPTIONS=( # CONF_KEY, TITLE, CALLBACK
        ("", "Online Mastery Course", openWeb1),
        ("", "Daily Q and A Support", openWeb2),
        ("", "1-on-1 Tutoring", openWeb3)
    )
    menu_name = "&AnKing"
    menu = getMenu(mw, menu_name)
    submenu = getSubMenu(menu, "Get Anki Help")
    for k, title, cb in MENU_OPTIONS:
        if title in [x.text() for x in submenu.actions()]:
            continue

        hk=QKeySequence()
        act=QAction(title,mw)
        act.setShortcut(QKeySequence(hk))
        act.triggered.connect(cb)
        submenu.addAction(act)
        #menuItem[k]=act
    a = QAction("Custom Background and Gear Icon", mw)
    a.triggered.connect(SettingsDialogExecute)
    menu.addAction(a)

setupMenu()
