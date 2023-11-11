"""next game date helper"""
from datetime import datetime, time, timedelta
import gettext
_ = gettext.gettext

class NextGame:
    """next game date helper class"""
    def __init__(self, start = time(hour=19, minute=15), skip: int = 0, game_days: int = { 1, 4 }):
        if type(start) is datetime:
            self.start = start
        elif type(start) is time:
            found = 0
            now = datetime.now()
            start = datetime(year = now.year, month=now.month, day = now.day, hour = start.hour, minute = start.minute, second = 0)
            if start < now:
                start = start + timedelta(days=1)
            for days_shift in range(30):
                next_day = (start + timedelta(days=days_shift)) if days_shift > 0 else start
                if next_day.weekday() in game_days:
                    if found == skip:
                        self.start = next_day
                        return
                    found += 1
        else:
            self.start = None

    def __str__(self):
        return datetime.strftime(self.start, '%d.%m.%Y %H:%M') if self.start is not None else _("Not scheduled")
