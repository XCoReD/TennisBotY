from chatuser import Chatuser
import gettext
_ = gettext.gettext

class Player:

    owner: Chatuser
    participants: int

    def __init__(self, owner: Chatuser, participants = 1 ):
        self.owner = owner
        self.participants = participants

    def __eq__(self, other):
        if isinstance(other, str):
            return self.owner.name == other
        elif isinstance(other, Player):
            return self.owner.user_id == other.owner.user_id        
    
    def __name__(self):
        result = f'@{self.owner.name}'
        if hasattr(self.owner, 'full_name'):
            result += f' [{self.owner.full_name}]'
        return result
    
    def __str__(self):
        if self.participants != 1:
            return self.__name__() + " +" + _("%s guest(s)") % str(self.participants-1)
        return self.__name__()
        