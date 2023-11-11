from datetime import datetime, timedelta
import asyncio
from telethon import TelegramClient, events, errors
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, ACCOUNT_PHONE, ACCOUNT_USER_ID, ACCOUNT_USER, ANOTHER_USER, ANOTHER_USER_ID, BOT_ID
from competition import Competition
from chat import Chat
from chatuser import Chatuser
from chatpersistency import ChatPersistency
from chatconversation import ChatConversation
from nextgame import NextGame

class TestChatConversation:
    def __init__(self, chat: Chat, competition: Competition, persistency: ChatPersistency):
        self.chat = chat
        self.competition = competition
        self.persistency = persistency
        
        self.client = TelegramClient(self.get_session(), API_ID, API_HASH, )

        self.chat_id = int(CHAT_ID)
        self.user_id = int(ACCOUNT_USER_ID)
        self.bot_id = int(BOT_ID)

        self.bot_entity = None
        self.chat_entity = None
        self.conversation = None

    def get_session(self) -> str:
        return f"testchat-{datetime.strftime(datetime.now(), '%d-%m-%Y')}"
        #''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    async def test_main(self):
        @self.client.on(events.NewMessage(chats = [self.chat_id]))
        async def handler_1(event):
            self.on_new_chat_message(event)

        @self.client.on(events.MessageEdited(chats = [self.chat_id]))
        async def handler_2(event):
            self.on_new_chat_message(event)

        @self.client.on(events.NewMessage(chats = [self.bot_id]))
        async def handler_3(event):
            self.on_new_private_message(event)

        @self.client.on(events.MessageEdited(chats = [self.bot_id]))
        async def handler_4(event):
            self.on_new_private_message(event)

        """@self.client.on(events.CallbackQuery)
        async def callback(event):
            await event.edit('Thank you for clicking {}!'.format(event.data))
        """

        self.chat.users.clear()
        self.conversation = ChatConversation(BOT_TOKEN, CHAT_ID, self.chat, self.competition, self.persistency)

        #client.start(phone=your_phone_callback,password=your_password_callback,code_callback=your_code_callback)
        
        await self.client.start(phone=self.your_phone_callback)
        # This part is IMPORTANT, because it fills the entity cache.
        dialogs = await self.client.get_dialogs()

        self.chat_entity = await self.client.get_entity(self.chat_id)
        self.bot_entity = await self.client.get_entity(self.bot_id)

        asyncio.create_task(self.test()) 
        await self.client.run_until_disconnected()

    async def test(self):
        #await self.test_admin_access()
        await self.test_user_access()

    async def test_user_access(self):
        print("Testing new user access..")

        self.competition.reset()
        self.competition.open(1)
        n = NextGame()
        self.competition.competition_date = n.start
        self.competition.capacity_max_past = 9

        self.chat.users.clear()
        user = self.chat.find_user(self.user_id)
        assert not user

        msg = "/start"
        await self.send_chat_message(msg)
        self.check_menu(ChatConversation.user_menu_top_new)
        user = self.chat.find_user(self.user_id)
        assert user.status == Chatuser.NEW

        #register to the chat
        msg = self.get_command_text(ChatConversation.user_menu_top_new[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.user_select_level)
        await self.click(self.buttons[0][2])    #medium
        self.check_menu(ChatConversation.user_select_level)
        await self.click(self.buttons[0][5])    #back
        self.check_menu(ChatConversation.user_select_years)
        await self.click(self.buttons[0][3])    #up to 5 years
        self.check_menu(ChatConversation.user_select_years)
        await self.click(self.buttons[0][6])    #back
        self.check_menu(ChatConversation.user_yes_no)
        await self.click(self.buttons[0][0])    #yes - possesses the racket
        self.check_menu(ChatConversation.user_yes_no)
        await self.click(self.buttons[0][2])    #back
        self.check_menu(ChatConversation.user_yes_no)
        await self.click(self.buttons[0][0])    #yes - wants to play
        self.check_menu(ChatConversation.user_yes_no)
        await self.click(self.buttons[0][2])    #back
        self.check_menu(ChatConversation.user_confirm_registration)
        await self.click(self.buttons[0][0])    #yes - confirms
        user = self.chat.find_user(self.user_id)
        assert user.status == Chatuser.TRUSTED

        msg = "/start"
        await self.send_chat_message(msg)
        self.check_menu(ChatConversation.user_menu_top_trusted)
        await self.click(self.buttons[0][0])    #join
        self.check_menu(ChatConversation.menu_join_register)
        await self.click(self.buttons[0][0])    #register
        player = self.competition.find_player(self.user_id)
        assert player.participants == 1

        msg = "/start"
        await self.send_chat_message(msg)
        self.check_menu(ChatConversation.user_menu_top_trusted)
        await self.click(self.buttons[0][0])    #join
        self.check_menu(ChatConversation.menu_join_deregister)
        await self.click(self.buttons[0][0])    #deregister
        player = self.competition.find_player(self.user_id)
        assert not player
        assert self.competition.capacity == 0

        fake_user = Chatuser("Dummy", 1, Chatuser.TRUSTED)
        self.competition.register(fake_user)
        msg = "/start"
        await self.send_chat_message(msg)
        self.check_menu(ChatConversation.user_menu_top_trusted)
        await self.click(self.buttons[0][0])    #join
        assert self.button_count == 1   #no register button!
        await self.click(self.buttons[0][0])    #back
        self.check_menu(ChatConversation.user_menu_top_trusted)
        await self.click(self.buttons[0][3])    #rules

        player = self.competition.find_player(self.user_id)
        assert not player

        print('passed registering of new user and next joining the game')

    async def test_admin_access(self):
        print("Testing Admin features..")

        self.chat.find_or_add(self.user_id, ACCOUNT_USER, Chatuser.ADMIN)

        #await self.test_admin_manage()

        await self.test_admin_register()

    async def test_admin_manage(self):

        self.competition.reset()
        self.competition.open(20)
        n = NextGame()
        self.competition.competition_date = n.start
        self.competition.capacity_max_past = 9

        u1 = Chatuser(name = ANOTHER_USER, user_id=int(ANOTHER_USER_ID), status = Chatuser.TRUSTED)
        u2 = Chatuser(name = ACCOUNT_USER, user_id=int(ACCOUNT_USER_ID), status = Chatuser.TRUSTED)
        self.competition.register(u1, 3)
        self.competition.register(u2)
        assert self.competition.capacity == 4

        #test parcing dates from the keyboard
        dt = "14.11.2023 19:15"
        dt1 = datetime.strptime(dt, "%d.%m.%Y %H:%M")
        dt2 = self.conversation.parse_date(dt)
        assert self.datetime_match(dt1, dt2)

        msg = "/start"
        await self.send_chat_message(msg)
        self.check_menu(ChatConversation.admin_menu_top)
        print('passed ' + msg)

        msg = "/start"
        await self.send_bot_message(msg)
        self.check_menu(ChatConversation.admin_menu_top)
        print('passed ' + msg)

        #go to manage, view players too!
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_manage_competition_active)
        print('passed ' + msg)

        #go to update facility
        msg = self.get_command_text(ChatConversation.admin_menu_manage_competition_active[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_set_participants)
        print('passed ' + msg)

        #update facility max participants to 10
        msg = self.get_command_text(ChatConversation.admin_menu_set_participants[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_set_participants)
        assert self.competition.capacity_max == 10
        print('passed ' + msg)

        #update facility max participants to 12
        msg = self.get_command_text(ChatConversation.admin_menu_set_participants[0][1])
        await self.click(self.buttons[0][1])
        self.check_menu(ChatConversation.admin_menu_set_participants)
        assert self.competition.capacity_max == 12
        print('passed ' + msg)

        #update facility max participants to 1
        msg = "Leave 1 player, truncate 3"
        await self.send_bot_message("1")
        assert self.competition.capacity_max == 1
        assert self.competition.capacity == 1
        print('passed ' + msg)

        #update facility max participants to past value
        msg = self.get_command_text(ChatConversation.admin_menu_set_participants[0][5])
        await self.click(self.buttons[0][5])
        self.check_menu(ChatConversation.admin_menu_set_participants)
        assert self.competition.capacity_max == self.competition.capacity_max_past
        print('passed ' + msg)

        #back
        msg = self.get_command_text(ChatConversation.admin_menu_set_participants[0][6])
        await self.click(self.buttons[0][6])
        self.check_menu(ChatConversation.admin_menu_top)
        print('passed ' + msg)

        #close registration
        #first, open manage menu
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_manage_competition_active)
        #then close the registration
        msg = self.get_command_text(ChatConversation.admin_menu_manage_competition_active[0][1])
        await self.click(self.buttons[0][1])
        assert self.competition.is_scheduled() is True
        assert self.competition.is_open() is False
        #no menu
        # self.check_menu(ChatConversation.admin_menu_manage_competition_scheduled)
        print('passed ' + msg)

        #reopen registration
        msg = "/start"
        await self.send_bot_message(msg)
        self.check_menu(ChatConversation.admin_menu_top)
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_manage_competition_scheduled)
        msg = self.get_command_text(ChatConversation.admin_menu_manage_competition_scheduled[0][0])
        await self.click(self.buttons[0][0])
        await self.send_bot_message("10")
        assert self.competition.is_open() is True
        #the bot menu is closed
        print('passed ' + msg)

        #check force close from the program code
        self.competition.close()
        assert self.competition.is_open() is False

        #cancel the game; the menu is not redrawn, but it will work
        msg = "/start"
        await self.send_bot_message(msg)
        self.check_menu(ChatConversation.admin_menu_top)
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_manage_competition_scheduled)
        msg = self.get_command_text(ChatConversation.admin_menu_manage_competition_scheduled[0][1])
        await self.click(self.buttons[0][1])
        self.check_menu(ChatConversation.admin_menu_game_cancel)
        msg = self.get_command_text(ChatConversation.admin_menu_game_cancel[0][0])
        await self.click(self.buttons[0][0])

        assert self.competition.is_open() is False
        print('passed ' + msg)

        #schedule the game
        msg = "/start"
        await self.send_bot_message(msg)
        self.check_menu(ChatConversation.admin_menu_top)
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_manage_competition_not_scheduled)
        msg = self.get_command_text(ChatConversation.admin_menu_manage_competition_not_scheduled[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_schedule)
        assert self.competition.is_scheduled() is False
        #schedule the game to the first next date
        msg = self.get_command_text(ChatConversation.admin_menu_schedule[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_schedule)
        assert self.competition.is_scheduled() is True
        assert self.datetime_match(self.competition.get_date(), ChatConversation.next_plays[0].start)
        print('passed ' + msg)

        #schedule the game to the next next date
        msg = self.get_command_text(ChatConversation.admin_menu_schedule[0][1])
        await self.click(self.buttons[0][1])
        self.check_menu(ChatConversation.admin_menu_schedule)
        assert self.datetime_match(self.competition.get_date(), ChatConversation.next_plays[1].start)
        print('passed ' + msg)

        #schedule the game to the custom date
        custom_date = datetime.now() +  timedelta(days=1)
        msg = "Schedule the next play to " + str(custom_date)
        await self.send_bot_message(custom_date.strftime('%d.%m.%Y %H:%M'))
        assert self.datetime_match(self.competition.get_date(), custom_date)
        custom_date = datetime.now() +  timedelta(days=2)
        await self.send_bot_message(custom_date.strftime('%d.%m.%Y %H:%M'))
        assert self.datetime_match(self.competition.get_date(), custom_date)
        custom_date = datetime.now() +  timedelta(days=3)
        await self.send_bot_message(custom_date.strftime('%d.%m.%Y %H.%M'))
        assert self.datetime_match(self.competition.get_date(), custom_date)

        #go back, and see now the main scheduled menu
        self.check_menu(ChatConversation.admin_menu_schedule)
        await self.click(self.buttons[0][2])
        self.check_menu(ChatConversation.admin_menu_top)
        print('passed ' + msg)

        #open the registration to the game
        assert self.competition.is_open() is False
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_manage_competition_scheduled)
        msg = self.get_command_text(ChatConversation.admin_menu_manage_competition_scheduled[0][0])
        await self.click(self.buttons[0][0])
        self.check_menu(ChatConversation.admin_menu_set_participants)
        assert self.competition.capacity_max == 10
        #and select 16 participants
        await self.click(self.buttons[0][3])
        self.check_menu(ChatConversation.admin_menu_set_participants)
        assert self.competition.capacity_max == 16
        assert self.competition.is_open() is True
        assert self.datetime_match(self.competition.get_date(), custom_date)
        #TODO check the text notification in the chat
        print('passed registration open')

        #back
        msg = self.get_command_text(ChatConversation.admin_menu_set_participants[0][6])
        await self.click(self.buttons[0][6])
        self.check_menu(ChatConversation.admin_menu_top)
        await self.click(self.buttons[0][2])
        
    async def test_admin_register(self):

        self.competition.reset()
        self.competition.open(20)
        n = NextGame()
        self.competition.competition_date = n.start
        self.competition.capacity_max_past = 9

        msg = "/start"
        await self.send_bot_message(msg)
        self.check_menu(ChatConversation.admin_menu_top)

        #register to the game
        msg = self.get_command_text(ChatConversation.admin_menu_top[0][1])
        await self.click(self.buttons[0][1])
        self.check_menu(ChatConversation.menu_join_register)
        await self.click(self.buttons[0][0])
        assert self.button_count == 0
        assert self.competition.find_player(self.user_id) != None
        print('passed registering via button')

        self.competition.reset()
        self.competition.open()
        assert self.competition.find_player(self.user_id) == None
        await self.send_chat_message("+1")
        assert self.competition.find_player(self.user_id) != None
        assert self.competition.capacity == 1

        self.competition.reset()
        self.competition.open()
        await self.send_chat_message("+")
        assert self.competition.find_player(self.user_id) != None
        assert self.competition.capacity == 1

        self.competition.reset()
        self.competition.open()
        await self.send_chat_message("+4")
        player = self.competition.find_player(self.user_id)
        assert player != None
        assert player.participants == 4
        assert self.competition.capacity == 4
        print('passed registering via chat text')

        self.competition.reset()
        self.competition.open()
        assert self.competition.find_player(self.user_id) == None
        await self.send_bot_message("+1")
        assert self.competition.find_player(self.user_id) != None
        assert self.competition.capacity == 1

        self.competition.reset()
        self.competition.open()
        await self.send_bot_message("+")
        assert self.competition.find_player(self.user_id) != None
        assert self.competition.capacity == 1

        self.competition.reset()
        self.competition.open()
        await self.send_bot_message("+4")
        player = self.competition.find_player(self.user_id)
        assert player != None
        assert player.participants == 4
        assert self.competition.capacity == 4
        print('passed registering via bot text')


    def datetime_match(self, dt1:datetime, dt2: datetime):
        return datetime.strftime(dt1, "%d.%m.%Y %H:%M") == datetime.strftime(dt2, "%d.%m.%Y %H:%M")
    
    def get_command(self, menu):
        return menu['callback_data']
    
    def get_command_text(self, menu):
        return menu['text']

    async def send_chat_message(self, text):
        await self.send_message(entity=self.chat_entity,message=text)
        await self.wait_catch_up()

    async def send_bot_message(self, text):
        await self.send_message(entity=self.bot_entity,message=text)
        await self.wait_catch_up()

    async def send_message(self, entity, message):
        #https://stackoverflow.com/questions/57529546/how-to-handle-flood-wait-errors-when-using-telethon-sync
        for i in (0,1):
            try:
                await self.client.send_message(entity=entity,message=message)
                return
            except errors.FloodWaitError as e:
                if i == 1:
                    assert False
                    return
                await asyncio.sleep(e.seconds + 1)

    async def click(self, button):
        asyncio.create_task(button.click())
        await self.wait_catch_up()

    def check_menu(self, menu):
        count = len(menu[0])
        if len(menu) == 2:
            count += len(menu[1])
        assert self.button_count == count
        for i in (0, len(menu[0]) - 1):
            actual = self.buttons[0][i].data.decode('utf-8') 
            expected = self.get_command(menu[0][i])
            assert actual == expected
        if len(menu) == 2:
            for i in (0, len(menu[1]) - 1):
                actual = self.buttons[1][i].data.decode('utf-8') 
                expected = self.get_command(menu[1][i])
                assert actual == expected

    async def wait_catch_up(self):
        await asyncio.sleep(0.1)
        await self.conversation.process_events(1)
        await asyncio.sleep(0.5)
        #await self.client.catch_up()
        """while self.client._updates_queue:
            await asyncio.wait(self.client._updates_queue, return_when=asyncio.FIRST_COMPLETED)"""

    def on_new_chat_message(self, event) -> None:
        message = event.message
        text = getattr(message, "raw_text", None)
        print("new chat message: " + text)
        self.record_message(event.message)

    def on_new_private_message(self, event) -> None:
        message = event.message
        text = getattr(message, "raw_text", None)
        print("new private message: " + text)
        self.record_message(event.message)

    def record_message(self, message) -> None:
        self.button_count = message.button_count
        self.buttons = message.buttons
        self.raw_text = message.raw_text
        self.message = message

    def your_phone_callback(self) -> str:
        return ACCOUNT_PHONE

