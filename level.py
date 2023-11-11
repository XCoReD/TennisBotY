from enum import StrEnum
import gettext
_ = gettext.gettext

class Level(StrEnum):
    LEVEL_UNKNOWN =     _("Unknown"),
    LEVEL_NONE =        _("Not played"), 
    LEVEL_BEGINNER =    _("Beginner"), 
    LEVEL_MEDIUM =      _("Medium"), 
    LEVEL_ADVANCED =    _("Advanced"), 
    LEVEL_CHAMPION =    _("Top")
