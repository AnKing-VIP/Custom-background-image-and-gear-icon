import os

from aqt import mw


addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)


def gc(arg="", fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        if arg:
            return conf.get(arg, fail)
        else:
            return conf
    return fail


userOption = None

def _getUserOption(refresh):
    global userOption
    if userOption is None or refresh:
        userOption = mw.addonManager.getConfig(__name__)


def getUserOption(key=None, default=None, refresh=False):
    _getUserOption(refresh)
    if key is None:
        return userOption
    if key in userOption:
        return userOption[key]
    else:
        return default


def writeConfig(configToWrite=userOption):
    mw.addonManager.writeConfig(__name__, configToWrite)


def getDefaultConfig():
    addon = __name__.split(".")[0]
    return mw.addonManager.addonConfigDefaults(addon)
