"""Chat storage."""
import gettext
_ = gettext.gettext
from chatuser import Chatuser

class Chat:

    def __init__(self):
        self.users = []

    def find_user(self, userid: int) -> Chatuser:
        return next((x for x in self.users if x.user_id == userid), None)
    
    def trusted(self, userid: int):
        user_object = self.find_user(userid)
        return user_object.status in {Chatuser.TRUSTED, Chatuser.ADMIN} if user_object else False
    
    def find_or_add(self, userid, username, status = None) -> Chatuser:
        if not status:
            status = Chatuser.NEW
        user = next((x for x in self.users if x.user_id == userid), None)
        if not user:
            user = Chatuser(username, userid, status)
            self.users.append(user)
        return user

    def get_admins(self, prefix_if_multiple = None):
        admins = list(filter(lambda u: u.status is Chatuser.ADMIN, self.users))
        return prefix_if_multiple + ','.join(map(lambda user: '@' + user.name, admins)) if len(admins) > 1 else ( ('@' + admins[0].name) if len(admins) == 1 else '(not found)')
