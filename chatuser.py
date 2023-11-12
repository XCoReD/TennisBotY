from level import Level
from yearsexperience import YearsExperience
from yesno import YesNo

class Chatuser:

    NEW, VALIDATING, TRUSTED, ADMIN, SUPERADMIN, BOT = range(6)

    #the attributes must be declared for serializaton
    status : range
    level : Level
    years : YearsExperience
    racket : YesNo
    wannaplay : YesNo
    name : str
    full_name : str
    user_id: int

    def __init__(self, name:str, user_id:int, status: range):
        self.name = name
        self.user_id = user_id
        self.status = status

    def check_and_update(self, name: str, full_name:str) -> bool:
        if self.name == name and hasattr(self, "full_name") and self.full_name == full_name:
            return False
        self.name = name
        self.full_name = full_name
        return True

    def get_name(self):
        return self.full_name if hasattr(self, "full_name") else self.name

    def get_fqn_name(self):
        return f"{self.name} ({self.full_name})" if hasattr(self, "full_name") else self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Chatuser):
            return self.name == other.name
    
    def __str__(self):
        return f"{self.get_fqn_name()} [{str(self.status)}]"
        