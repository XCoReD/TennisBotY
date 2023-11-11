"""main entry point"""
import logging
import asyncio

from config import BOT_TOKEN, CHAT_ID
from competition import Competition
from chat import Chat
from chatpersistency import ChatPersistency
from chatconversation import ChatConversation
from testchatconversation import TestChatConversation

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def normal_run() -> None:

    competition = Competition()
    chat = Chat()

    try:
        competition = ChatPersistency.load_competition()
    except:
        pass

    try:
        chat = ChatPersistency.load_chat()
    except:
        pass

    persistency = ChatPersistency(competition, chat)

    conversation = ChatConversation(BOT_TOKEN, CHAT_ID, chat, competition, persistency)
    # Run the bot until the user presses Ctrl-C
    conversation.run()

async def test_run() -> None:

    competition = Competition()
    chat = Chat()

    persistency = ChatPersistency(competition, chat, True)

    test = TestChatConversation(chat, competition, persistency)
    await test.test_main()

def test_run_entry():
    asyncio.run(test_run())

def main():

    normal_run()
    #test_run_entry()
    
if __name__ == "__main__":
    main()

