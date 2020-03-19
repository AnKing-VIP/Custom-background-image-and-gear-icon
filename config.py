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
