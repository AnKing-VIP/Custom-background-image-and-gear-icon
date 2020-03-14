# Copyright: 2020- ijgnd
# Modified by: The AnKing 
### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)
#
#            Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 

from aqt import mw


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail