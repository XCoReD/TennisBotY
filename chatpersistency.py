"""Data persistency support"""
import pickle
from competition import Competition
from chat import Chat

class ChatPersistency:
    """Data persistency support"""

    def __init__(self, competition, chat, ignore = False) -> None:
        self.competition = competition
        self.chat = chat
        self.ignore = ignore

    @classmethod
    def load_competition(cls) -> Competition:
        """Loading the competition info."""
        with open('competition.pickle', 'rb') as f:
            return pickle.load(f)

    @classmethod
    def load_chat(cls) -> Chat:
        """Loading the chat info."""
        with open('chat.pickle', 'rb') as f:
            return pickle.load(f)

    def save(self):
        """Saving all."""
        self.save_competition()
        self.save_chat()

    def save_competition(self):
        """Saving the competition info."""
        if not self.ignore:
            with open('competition.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(self.competition, f, pickle.HIGHEST_PROTOCOL)

    def save_chat(self):
        """Saving the chat info."""
        if not self.ignore:
            with open('chat.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(self.chat, f, pickle.HIGHEST_PROTOCOL)
