from enum import StrEnum
import gettext
_ = gettext.gettext

class YesNo(StrEnum):
    YESNO_UNKNOWN =     _("Unknown"),
    YESNO_YES =         _("Yes"),
    YESNO_NO =          _("No"),
