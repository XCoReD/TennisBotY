"""competition info"""
from datetime import datetime
import gettext
_ = gettext.gettext
from player import Player
from chatuser import Chatuser
from yesno import YesNo
from nextgame import NextGame
from myexception import LogicException

class Competition:
    """competition class, to keep info about competition status, date, and players registered"""
    CLOSED, OPEN_ACCEPTING, OPEN_FULL = range(3)

    #the attributes must be declared for serializaton
    status : range
    competition_date : datetime

    def __init__(self):
        self.status = Competition.CLOSED
        self.capacity_max = 0
        self.capacity = 0
        self.players = []

    def open(self, capacity_max = -1):
        #self.reset()
        #TODO what if the competition is already open?
        if capacity_max == -1:
            capacity_max = self.capacity_max_past
        if self.status != Competition.CLOSED:
            raise LogicException("Cannot open the competition, it is already open")
        self.capacity_max = capacity_max
        self.status = Competition.OPEN_ACCEPTING if self.capacity < self.capacity_max else Competition.OPEN_FULL
        return True

    def close(self):
        self.status = Competition.CLOSED
        if self.capacity_max > 0:
            self.capacity_max_past = self.capacity_max

    def reset(self):
        self.close()
        self.players.clear()
        self.capacity = 0
        self.competition_date = None

    def get_status(self):
        match self.status:
            case Competition.CLOSED:
                return _("Registration to an upcoming game is not open yet or cancelled")
            case Competition.OPEN_ACCEPTING:
                return _("Registration is open, you can join")
            case Competition.OPEN_FULL:
                return _("Registration is complete, the maximum number of players is reached")

    def is_open(self) -> bool:
        return getattr(self, 'status', Competition.CLOSED) != Competition.CLOSED
    
    def is_scheduled(self) -> bool:
        d = self.get_date()
        return d is not None and d > datetime.now()
    
    def get_date(self) -> datetime:
        return self.competition_date if getattr(self, 'competition_date', None) else None

    def get_date_str(self):
        d = self.get_date()
        return datetime.strftime(d, '%A, %d.%m.%Y %H:%M') if d is not None else _("Not scheduled")
    
    def get_report(self):
        result = _("Registered %s players") % str(self.capacity)
        i = 1
        for player in self.players:
            result += f"\n\t{i}: {str(player)}"
            i = i + 1
        return result

    def find_player(self, userid: int) -> Player:
        return next((x for x in self.players if x.owner.user_id == userid), None)

    def register(self, user: Chatuser, participants = 1) -> (bool, str):
        if self.status != Competition.OPEN_ACCEPTING:
            return False, _("Registration is not open")
        player = self.find_player(user.user_id)
        if player:
            return False, _("You have already registered for the play, all is OK")
        if self.capacity + participants > self.capacity_max:
            return False, _("Number of participants is more than capacity of the facility")
        self.capacity += participants
        self.players.append(Player(user, participants))
        if self.capacity >= self.capacity_max:
            self.status = Competition.OPEN_FULL
        return True, _("You have registered, congratulations!")

    def deregister(self, user: Chatuser, participants = -1)-> (bool, str):
        if self.status == Competition.CLOSED:
            return False, _("Registration is not open")
        player = self.find_player(user.user_id)
        if not player:
            return False, _("You haven't registered for the play")
        if participants == -1:
            participants = player.participants
        if participants > player.participants:
            return False, _("You cannot deregister more players that you have registered earlier")
        self.capacity -= participants
        result_message = ""
        if participants == player.participants:
            self.players.remove(player)
            result_message = _("You have deregistered")
        else:
            player.participants -= participants
            result_message = _("You have decreased number of your guests, remaining %s") % str(player.participants) if player.participants > 1 else _("only you")
        if self.capacity < self.capacity_max:
            self.status = Competition.OPEN_ACCEPTING
        return True, result_message

