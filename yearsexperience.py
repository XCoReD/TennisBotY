from enum import StrEnum
import gettext
_ = gettext.gettext

class YearsExperience(StrEnum):
    YEARS_UNKNOWN = _("Unknown"),
    YEARS_0 =       _("Not played at all")
    YEARS_1 =       _("Up to 1 year")
    YEARS_3 =       _("1-3 years")
    YEARS_5 =       _("3-5 years")
    YEARS_10 =      _("5-10 years")
    YEARS_100 =     _("More than 10 years")
