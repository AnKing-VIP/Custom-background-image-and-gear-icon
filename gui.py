# -*- coding: utf-8 -*-
# Copyright: 
# Support: 
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt.qt import *
from aqt import mw
from aqt.utils import getFile

from .settings import *
from .config import getUserOption, writeConfig
conf = getUserOption()


class Manager:
    shown = False

    def __init__(self):
        #self.conf = conf
        self.setupMenu()

    def setupMenu(self):
        a = QAction("Custom Background Image and Gear Icon", mw)
        a.triggered.connect(self.show)
        mw.form.menuTools.addAction(a)

    def show(self):
        if not self.shown:
            self.shown = True
            s = SettingsDialog(self.reset)
            s.show()

    def reset(self):
        self.shown = False

 

class SettingsDialog(QDialog):
    timer = None

    def __init__(self, callback):
        QDialog.__init__(self, mw, Qt.Window)
        mw.setupDialogGC(self)
        #self.conf = conf
        self.mw = aqt.mw
        self.cleanup = callback
        #TODO I don't get what this is or how it's used?
        self.setupDialog()
        self.loadConfigData()
        self.setupConnections()
        
        self.exec_()


    def setupDialog(self):
        #window title for entire thing
        self.setWindowTitle("Custom Wallpaper Settings")
        #setting up tab widget  TODO how to add more tabs?
        #self.tabWidget = QTabWidget(self)
        #TODO what does this do? 
        #self.tabWidget.setFocusPolicy(Qt.StrongFocus)
        #self.tabWidget.setObjectName("tabWidget")
        self.form = Ui_Dialog()
        #TODO why do you need to setupUI with the tabwidget?
        self.form.setupUi(self)

    def setupConnections(self):
        f = self.form
        
        # LineEdits -------------
        a = f.lineEdit_background
        t = a.text()
        a.textChanged.connect(_updateLineEdit(t,"Image name for background"))  
        

    def loadConfigData(self):
        f = self.form

        #LineEdits

    def _updateLineEdit(self, text, key):
        #self.conf.set(key, text)
        conf[key] = text
        writeConfig(conf)
        self._refresh()

    def _refresh(self, ms=100):
        if self.timer:
            self.timer.stop()
        self.timer = mw.progress.timer(
            ms, lambda:mw.reset(True), False)    




def SettingsDialogExecute():
    SettingsDialog(mw)


mw.addonManager.setConfigAction(__name__, SettingsDialogExecute)


''' DANCING BALONEY STUFF
    #TODO why?
    def reject(self):
        self.accept()

    def accept(self):
        self.conf.save()
        #why do you need to accept with the qdialog?
        QDialog.accept(self)
        self.cleanup()




    def _updateComboBox(self):
        self.conf.set("theme",
            self.form.theme_combobox.currentText())
        self._refresh(150)

    def _updateSliderLabel(self, num, label, key, format="% 5d%%"):
        label.setText(format%num)
        self.conf.set(key, num)
        self._refresh()

    def _getThemes(self):
        d = f"{ADDON_PATH}/theme"
        return [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]

    def _getFile(self, pad, lineEditor, ext=RE_BG_IMG_EXT):
        def setWallpaper(path):
            f = path.split("user_files/")[-1]
            lineEditor.setText(f)

        f = getFile(mw, "Wallpaper",
            cb=setWallpaper,
            filter=ext,
            dir=f"{ADDON_PATH}/user_files"
        )

    def _chooseColor(self, pad, lineEditor):
        def liveColor(qcolor):
            if qcolor.isValid():
                self.lastColor=qcolor
                lineEditor.setText(qcolor.name())

        diag=QDialog(self)
        form=getcolor.Ui_Dialog()
        form.setupUi(diag)
        cor = lineEditor.text()
        if QColor.isValidColor(cor):
            form.color.setCurrentColor(QColor(cor))
        else:
            form.color.setCurrentColor(self.lastColor)
        form.color.currentColorChanged.connect(liveColor)
        diag.show()

    def _updateCheckbox(self, cb, key):
        n = -1 if cb==2 else 1
        self.conf.set(key, n)
        self._refresh()


'''