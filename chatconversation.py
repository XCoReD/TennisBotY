"""Telegram Chat logic."""
from typing import Sequence
from datetime import datetime, time
import asyncio
import gettext
_ = gettext.gettext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ContextTypes,
    MessageHandler,
    filters,
    PicklePersistence,
    Updater
)

from nextgame import NextGame
from level import Level
from player import Player
from yearsexperience import YearsExperience
from yesno import YesNo
from chatuser import Chatuser
from chat import Chat
from competition import Competition
from chatpersistency import ChatPersistency

class ChatConversation:

    msg_bot_intro = _("Hi! I am a very kind and patient Tennis Chat bot, and hope I will help you somehow:) ")
    msg_help = _("Hi, and welcome to the Table Tennis Chat of the best city in the world. I could not find a pinned message, hope %s will help")
    msg_admins_any_of = _("any of ")
    msg_start_newcomer = _("First, Register. I mean tell me about your table tennis experience: on which level and for how many years have you been played, do you have own racket, and don't you mind to play with us? Then submit your answers, and welcome to our club!")
    msg_register_first = _("To join a game first you need to Register, to confirm your agreement with the rules.")
    msg_switching_to_private = _("Switching to private chat..")

    msg_start_trusted = _("Let's go!")
    msg_start_admin = _("Straight to our admin business!")

    msg_register_top_level = _("Level of play")
    msg_register_top_years = _("Years of experience")
    msg_register_top_racket = _("Own racket")
    msg_register_top_wannaplay = _("Wanna play")
    msg_register_top_moreinfo = _("More info...")
    msg_register_top_viewinfo = _("View your info")
    msg_register_top_submit = _("Submit info")
    msg_done = _("Exit")

    msg_select_level = _("Select your level of play. Don't be shy, but don't overestimate your skills too:). Watch Ma Long on Youtube to get 100%, and give a racket to your dog to get 0%.")
    msg_select_years = _("Select the number of years you have been played in table tennis. Try to get as much precise number as possible.")
    msg_select_racket = _("Do you own a table tennis racket?")
    msg_select_wannaplay = _("Are you planning to participate in table tennis trainings with us?")
    msg_confirm_membership = _("By clicking the Yes button below, I confirm that I am agree with the Rules of the Table Tennis club.")
    msg_view_info_finished = _("Thank you for reviewing your personal info.")

    msg_top_register = _("Register")
    msg_top_rules = _("See Rules")
    msg_trusted_top_join = _("Join the Game")
    msg_admin_top_manage = _("Manage")

    msg_admin_manage_view_players = _("View Players")
    msg_admin_manage_update_facility = _("Update Facility")
    msg_admin_manage_close_registration = _("Close Registration")
    msg_admin_manage_cancel_game = _("Cancel Game")

    msg_admin_manage_open_registration = _("Open Registration")
    msg_admin_manage_schedule = _("Schedule")
    msg_admin_confirm_cancel = _("Confirm Cancel")

    msg_game_register = _("Register to Game")
    msg_game_deregister = _("Unregister")


    msg_back = _("Back")
    msg_finished = _("All is set up.")
    msg_stopped = _("Okay, bye.")
    msg_submitted = _("Your responses are submitted. Now you are welcome to play!")

    # Different constants
    (
        END,
        BACK,
        GAME_JOIN,
        GAME_JOIN_REGISTER,
        GAME_JOIN_DEREGISTER,
        REGISTER,
        REGISTER_LEVEL,
        REGISTER_YEARS,
        REGISTER_RACKET,
        REGISTER_WANNAPLAY,
        REGISTER_CONFIRM_INFO,
        REGISTER_SUBMIT_INFO,
        RULES,
        GAME_MANAGE,
        GAME_MANAGE_VIEW_PARTICIPANTS,
        GAME_MANAGE_UPDATE_FACILITY,
        GAME_MANAGE_CANCEL,
        GAME_MANAGE_CANCEL_CONFIRM,
        GAME_MANAGE_CLOSE_REGISTRATION,
        GAME_MANAGE_SCHEDULE,
        GAME_MANAGE_SCHEDULE_NEXT_REGULAR_DATE,
        GAME_MANAGE_SCHEDULE_SKIP_NEXT_REGULAR_DATE,
        GAME_MANAGE_SCHEDULE_CUSTOM_DATE,
        GAME_MANAGE_SCHEDULE_GETDATE_REGISTRATION_OPEN,
        GAME_MANAGE_SET_PARTICIPANTS,
        GAME_MANAGE_SET_PARTICIPANTS_AS_BEFORE,
        GAME_MANAGE_SET_PARTICIPANTS_10,
        GAME_MANAGE_SET_PARTICIPANTS_12,
        GAME_MANAGE_SET_PARTICIPANTS_14,
        GAME_MANAGE_SET_PARTICIPANTS_16,
        GAME_MANAGE_SET_PARTICIPANTS_18,
        GAME_MANAGE_OPEN,
        START_OVER,
        FEATURES,
        CURRENT_FEATURE,
        CURRENT_LEVEL,
        USER_NAME,
        USER_FULLNAME,
        USER_STATUS,
        USER_TELEGRAM_ID,

    ) = map(chr, range(1, 41))

    user_menu_top_trusted = [
        [
            {'text': msg_trusted_top_join, 'callback_data' : str(GAME_JOIN)},
            {'text': msg_top_register, 'callback_data' : str(REGISTER)},
            {'text': msg_top_rules, 'callback_data' : str(RULES)},
            {'text': msg_done, 'callback_data' : str(END)}
        ]
    ]

    user_menu_top_new = [
        [
            {'text': msg_top_register, 'callback_data' : str(REGISTER)},
            {'text': msg_top_rules, 'callback_data' : str(RULES)},
            {'text': msg_done, 'callback_data' : str(END)}
        ]
    ]

    """
    user_menu_register_level = [
        [
            {'text': msg_register_top_level, 'callback_data' : str(REGISTER_LEVEL)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ]
    ]

    user_menu_register_years = [
        [
            {'text': msg_register_top_years, 'callback_data' : str(REGISTER_YEARS)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ]
    ]

    user_menu_register_racket = [
        [
            {'text': msg_register_top_racket, 'callback_data' : str(REGISTER_RACKET)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ]
    ]

    user_menu_register_wannaplay = [
        [
            {'text': msg_register_top_wannaplay, 'callback_data' : str(REGISTER_WANNAPLAY)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ]
    ]
    """
    
    user_menu_register_submit_info = [
        [
            {'text': msg_register_top_submit, 'callback_data' : str(REGISTER_SUBMIT_INFO)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ]
    ]

    admin_menu_top = [
        [
            {'text': msg_admin_top_manage, 'callback_data' : str(GAME_MANAGE)},
            {'text': msg_trusted_top_join, 'callback_data' : str(GAME_JOIN)},
            {'text': msg_done, 'callback_data' : str(END)}
        ]
    ]

    admin_menu_manage_competition_active = [
        [
            {'text': msg_admin_manage_update_facility, 'callback_data' : str(GAME_MANAGE_UPDATE_FACILITY)},
            {'text': msg_admin_manage_close_registration, 'callback_data' : str(GAME_MANAGE_CLOSE_REGISTRATION)},
            {'text': msg_admin_manage_cancel_game, 'callback_data' : str(GAME_MANAGE_CANCEL)}
        ],
        [
            {'text':msg_back, 'callback_data': str(BACK)}
        ],
    ]

    admin_menu_manage_competition_scheduled = [
        [
            {'text': msg_admin_manage_open_registration, 'callback_data' : str(GAME_MANAGE_OPEN)},
            {'text': msg_admin_manage_cancel_game, 'callback_data' : str(GAME_MANAGE_CANCEL)}
        ],
        [
            {'text':msg_back, 'callback_data': str(BACK)}
        ],
    ]

    admin_menu_manage_competition_not_scheduled = [
        [
            {'text': msg_admin_manage_schedule, 'callback_data' : str(GAME_MANAGE_SCHEDULE)},
        ],
        [
            {'text': msg_back, 'callback_data': str(BACK)}
        ],
    ]

    admin_menu_game_cancel = [
        [
            {'text': msg_admin_confirm_cancel, 'callback_data' : str(GAME_MANAGE_CANCEL_CONFIRM)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ],
    ]

    admin_menu_set_participants = [
        [
            {'text': str(10), 'callback_data' : str(GAME_MANAGE_SET_PARTICIPANTS_10)},
            {'text': str(12), 'callback_data' : str(GAME_MANAGE_SET_PARTICIPANTS_12)},
            {'text': str(14), 'callback_data' : str(GAME_MANAGE_SET_PARTICIPANTS_14)},
            {'text': str(16), 'callback_data' : str(GAME_MANAGE_SET_PARTICIPANTS_16)},
            {'text': str(18), 'callback_data' : str(GAME_MANAGE_SET_PARTICIPANTS_18)},
            {'text': _("As Before"), 'callback_data' : str(GAME_MANAGE_SET_PARTICIPANTS_AS_BEFORE)},
            {'text': msg_back, 'callback_data': str(BACK)}
        ]
    ]

    menu_back = [ 
        [
            {'text':msg_back, 'callback_data': str(BACK)}
        ],
    ]

    menu_join_register = [ 
        [
            {'text':msg_game_register, 'callback_data': str(GAME_JOIN_REGISTER)},
            {'text':msg_back, 'callback_data': str(BACK)}
        ],
    ]

    menu_join_deregister = [ 
        [
            {'text':msg_game_deregister, 'callback_data': str(GAME_JOIN_DEREGISTER)},
            {'text':msg_back, 'callback_data': str(BACK)}
        ],
    ]

    start_time = time(hour=19, minute=15)
    next_plays = [ NextGame(start_time), NextGame(start_time, 1), ]

    admin_menu_schedule = [ 
        [
            {'text':str(next_plays[0]), 'callback_data': str(GAME_MANAGE_SCHEDULE_NEXT_REGULAR_DATE)},
            {'text':str(next_plays[1]), 'callback_data': str(GAME_MANAGE_SCHEDULE_SKIP_NEXT_REGULAR_DATE)},
            {'text':msg_back, 'callback_data': str(BACK)}
        ],
    ]

    user_select_level = [
        [
            {'text': Level.LEVEL_NONE, 'callback_data' : str(Level.LEVEL_NONE)},
            {'text': Level.LEVEL_BEGINNER, 'callback_data' : str(Level.LEVEL_BEGINNER)},
            {'text': Level.LEVEL_MEDIUM, 'callback_data' : str(Level.LEVEL_MEDIUM)},
            {'text': Level.LEVEL_ADVANCED, 'callback_data' : str(Level.LEVEL_ADVANCED)},
            {'text': Level.LEVEL_CHAMPION, 'callback_data' : str(Level.LEVEL_CHAMPION)},
            {'text': msg_back, 'callback_data' : str(BACK)}
        ]
    ]

    user_select_years = [
        [
            {'text': YearsExperience.YEARS_0, 'callback_data' : str(YearsExperience.YEARS_0)},
            {'text': YearsExperience.YEARS_1, 'callback_data' : str(YearsExperience.YEARS_1)},
            {'text': YearsExperience.YEARS_3, 'callback_data' : str(YearsExperience.YEARS_3)},
            {'text': YearsExperience.YEARS_5, 'callback_data' : str(YearsExperience.YEARS_5)},
            {'text': YearsExperience.YEARS_10, 'callback_data' : str(YearsExperience.YEARS_10)},
            {'text': YearsExperience.YEARS_100, 'callback_data' : str(YearsExperience.YEARS_100)},
            {'text': msg_back, 'callback_data' : str(BACK)}
        ]
    ]

    user_yes_no = [
        [
            {'text': YesNo.YESNO_YES, 'callback_data' : str(YesNo.YESNO_YES)},
            {'text': YesNo.YESNO_NO, 'callback_data' : str(YesNo.YESNO_NO)},
            {'text': msg_back, 'callback_data' : str(BACK)}
        ]
    ]

    user_confirm_registration = [
        [
            {'text': YesNo.YESNO_YES, 'callback_data' : str(REGISTER_CONFIRM_INFO)},
            {'text': msg_back, 'callback_data' : str(BACK)}
        ]
    ]

    def reset_user_context(self, context: CallbackContext) -> None:
        """resets the user context variables"""
        context.user_data[ChatConversation.START_OVER] = False
        context.user_data[ChatConversation.CURRENT_FEATURE] = ''

    def load_user_context(self, context: CallbackContext, user: Chatuser, user_name: str, full_name: str) -> None:
        """sets the user context variables"""
        self.reset_user_context(context)
        if user:
            level = getattr(user, 'level', Level.LEVEL_UNKNOWN)
            years = getattr(user, 'years', YearsExperience.YEARS_UNKNOWN)
            racket = getattr(user, 'racket', YesNo.YESNO_UNKNOWN)
            wannaplay = getattr(user, 'wannaplay', YesNo.YESNO_UNKNOWN)
            status = getattr(user, 'status', Chatuser.NEW)
            user_id = getattr(user, 'user_id', 0)

        context.user_data[ChatConversation.FEATURES] = {
            ChatConversation.REGISTER_LEVEL:level,
            ChatConversation.REGISTER_YEARS:years,
            ChatConversation.REGISTER_RACKET:racket,
            ChatConversation.REGISTER_WANNAPLAY:wannaplay,
            ChatConversation.REGISTER:-1
        }
        context.user_data[ChatConversation.USER_NAME] = user_name
        context.user_data[ChatConversation.USER_FULLNAME] = full_name
        context.user_data[ChatConversation.USER_STATUS] = status
        context.user_data[ChatConversation.USER_TELEGRAM_ID] = user_id
        
    def save_user_context(self, context: CallbackContext, final_status = Chatuser.VALIDATING) -> None:
        """saves the user context variables"""
        user_name = context.user_data[ChatConversation.USER_NAME]
        full_name = context.user_data[ChatConversation.USER_FULLNAME]
        user_id = context.user_data[ChatConversation.USER_TELEGRAM_ID]
        user = self.chat.find_user(user_id)
        if not user:
            user = Chatuser(user_name, user_id, final_status)
            self.chat.users.append(user)
        user.full_name = full_name
        user.level = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_LEVEL]
        user.years = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_YEARS]
        user.racket = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_RACKET]
        user.wannaplay = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_WANNAPLAY]
        user.status = final_status

    # Top level conversation callbacks
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """starts the conversation"""
        reply_privately = context._chat_id != context._user_id

        if update.message:
            user = self.chat.find_or_add(update.message.from_user.id, update.message.from_user.username)
            self.load_user_context(context, user, update.message.from_user.username, update.message.from_user.full_name)

        status = context.user_data[ChatConversation.USER_STATUS]

        if status == Chatuser.ADMIN:
            text = ChatConversation.msg_start_admin
            buttons = self.admin_menu_top
        elif status == Chatuser.TRUSTED:
            text = ChatConversation.msg_start_trusted
            buttons = self.user_menu_top_trusted
        else:
            text = ChatConversation.msg_start_newcomer
            buttons = self.user_menu_top_new

        keyboard = InlineKeyboardMarkup(buttons)
        # If we're starting over we don't need to send a new message
        start_over = context.user_data.get(ChatConversation.START_OVER)
        if reply_privately:
            if update.message:
                await context.bot.delete_message(chat_id = context._chat_id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=context._user_id, text=text, reply_markup=keyboard)
        else:
            if start_over:
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
            else:
                await update.message.reply_text(text=ChatConversation.msg_bot_intro + '\n\n' + text, reply_markup=keyboard)
        context.user_data[ChatConversation.START_OVER] = False

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """End Conversation by command."""
        await update.message.reply_text(ChatConversation.msg_stopped)
        self.save_user_context(context)

    async def end(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """End conversation from InlineKeyboardButton."""
        await update.callback_query.answer()
        self.save_user_context(context)
        await update.callback_query.edit_message_text(text=ChatConversation.msg_finished)

    # Second level conversation callbacks
    async def register_entry(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """questionnary for new players, and to update existing info about players"""
        level = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_LEVEL] != Level.LEVEL_UNKNOWN
        years = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_YEARS] != YearsExperience.YEARS_UNKNOWN
        racket = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_RACKET] != YesNo.YESNO_UNKNOWN
        wannaplay = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_WANNAPLAY] != YesNo.YESNO_UNKNOWN
        current_page = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER]
        if current_page == -1:
            context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER] = current_page = 0
        if not level or current_page == 0:
            await self.select_level(update, context)
        elif not years or current_page == 1:
            await self.select_years(update, context)
        elif not racket or current_page == 2:
            await self.select_racket(update, context)
        elif not wannaplay or current_page == 3:
            await self.select_wannaplay(update, context)
        elif current_page == 4:
            await self.register_confirm_info(update, context)
        else:
            assert False
            #await self.register_submit_info(update, context)

    async def register_confirm_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """confirmation of the agreement with the Rules for new players"""
        trusted = context.user_data[ChatConversation.USER_STATUS] in (Chatuser.TRUSTED, Chatuser.ADMIN, Chatuser.SUPERADMIN)

        self.headline = ChatConversation.msg_confirm_membership if trusted else ChatConversation.msg_view_info_finished
        summary = _("The information you've reported: ") + "\n\n\t" + \
            _("Level of play: %s") % context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_LEVEL] + "\n\t" + \
            _("Years you are playing: %s") % context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_YEARS] + "\n\t" + \
            _("Owns a racket: %s") % context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_RACKET] + "\n\t" + \
            _("Want to play: %s") % context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_WANNAPLAY] + "\n"
            
        text = self.headline + summary
        buttons = self.menu_back if trusted else self.user_confirm_registration
        await self.reply(update, context, buttons, text, ChatConversation.REGISTER_CONFIRM_INFO)

    async def select_level(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """questionnary for new players - select the level"""
        self.headline = text = ChatConversation.msg_select_level
        value = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_LEVEL]
        if value and value != Level.LEVEL_UNKNOWN:
            text += "\n\n" + _("Level you've told earlier: %s") % value
        await self.reply(update, context, self.user_select_level, text, ChatConversation.REGISTER_LEVEL)

    async def select_years(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """questionnary for new players - select the number of years played"""
        self.headline = text = ChatConversation.msg_select_years
        value = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_YEARS]
        if value and value != YearsExperience.YEARS_UNKNOWN:
            text += "\n\n" + _("Value you've told earlier: %s") % value
        await self.reply(update, context, self.user_select_years, text, ChatConversation.REGISTER_YEARS)

    async def select_racket(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """questionnary for new players - select the racket availability"""
        self.headline = text = ChatConversation.msg_select_racket
        value = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_RACKET]
        if value and value != YesNo.YESNO_UNKNOWN:
            text += "\n\n" + _("Value you've told earlier: %s") % value
        await self.reply(update, context, self.user_yes_no, text, ChatConversation.REGISTER_RACKET)

    async def select_wannaplay(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """questionnary for new players - select if the user wants to play or just be a watcher"""
        self.headline = text = ChatConversation.msg_select_wannaplay
        value = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER_WANNAPLAY]
        if value and value != YesNo.YESNO_UNKNOWN:
            text += "\n\n" + _("Value you've told earlier: %s") % value
        await self.reply(update, context, self.user_yes_no, text, ChatConversation.REGISTER_WANNAPLAY)

    async def register_submit_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """finish entering the info and return to the top level conversation."""
        context.user_data[ChatConversation.START_OVER] = True
        self.keyboard = None
        self.headline = ""

        self.save_user_context(context, Chatuser.TRUSTED)

        text = ChatConversation.msg_submitted
        await update.callback_query.edit_message_text(text=text)

    async def game_manage(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """top level menu for administrator to manage the game"""
        if self.competition.is_open():
            buttons = self.admin_menu_manage_competition_active
            status = _("Next play is scheduled on %s, max capacity is %s\n\n%s") % \
            ( self.competition.get_date_str() , str(self.competition.capacity_max), self.competition.get_report())
        elif self.competition.is_scheduled():
            buttons = self.admin_menu_manage_competition_scheduled
            status = _("Next play is scheduled on %s, registration is not open yet, max capacity is %s") % (self.competition.get_date_str() , str(self.competition.capacity_max))
        else:
            buttons = self.admin_menu_manage_competition_not_scheduled
            status = _("Next play is not scheduled")

        self.headline = text = ChatConversation.msg_admin_top_manage + "\n\n" + status
        await self.reply(update, context, buttons, text, ChatConversation.GAME_MANAGE)

    async def game_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """top level menu for players or administrators to self-register in the game"""
        username = context.user_data[ChatConversation.USER_NAME]
        dt = self.competition.get_date()
        buttons = self.menu_back
        if dt and dt > datetime.now() and self.competition.capacity_max > 0:
            status = _("Next play is scheduled on %s, max capacity is %s\n\n%s") %\
                (self.competition.get_date_str() , str(self.competition.capacity_max), self.competition.get_report())
            if self.competition.is_open():
                if username in self.competition.players:
                    buttons = self.menu_join_deregister
                elif self.competition.status == Competition.OPEN_ACCEPTING:
                    buttons = self.menu_join_register
        else:
            status = _("Next play is not scheduled")

        self.headline = text = ChatConversation.msg_trusted_top_join + "\n\n" + status
        await self.reply(update, context, buttons, text, ChatConversation.GAME_JOIN)

    async def game_view_participants(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """view the participants registered to a game"""
        text=self.headline + "\n\n" + _("Participants list:") + "\n" + self.competition.get_report()
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=self.keyboard)

    async def game_register(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to self-register to the upcoming game"""
        userid = update.effective_user.id
        username = update.effective_user.username
        fullname = update.effective_user.full_name

        chatuser = self.chat.find_user(userid)
        if chatuser and chatuser.check_and_update(username, fullname):
            self.persistency.save_chat()

        registered, reply = self.competition.register(chatuser, 1)
        if reply:
            await self.send_user_message(context, chatuser, reply)
        if registered:
            self.persistency.save_competition()
            await context.bot.send_message(chat_id=self.chat_id,
                text=_("Participants list is updated:") + "\n\n" + self.competition.get_report())

    async def game_deregister(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to de-register from the game"""
        userid = update.effective_user.id
        chatuser = self.chat.find_user(userid)

        registered, reply = self.competition.deregister(chatuser)
        if reply:
            await self.send_user_message(context, chatuser, reply)
        if registered:
            self.persistency.save_competition()
            await context.bot.send_message(chat_id=self.chat_id,
                text=_("Participants list is updated:") + "\n\n" + self.competition.get_report())

    async def game_update_facility(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """update the game: increase max amount of participants, or reduce the number of participants with random exclusion
        or TODO add one more play time to the same day"""
        
        status = _("Next play is scheduled on %s, with max capacity of %s players. \nPress the button with the updated max number of participants, or type it from the keyboard\n\n%s") %\
              ( self.competition.get_date_str(), str(self.competition.capacity_max), self.competition.get_report())
        self.headline = text = ChatConversation.msg_admin_top_manage + "\n\n" + status
        await self.reply(update, context, self.admin_menu_set_participants, text, ChatConversation.GAME_MANAGE_SET_PARTICIPANTS)

    async def game_close_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to close the registration to the game"""
        self.competition.close()
        self.persistency.save_competition()
        text=_("Registration is closed. Date: ") + self.competition.get_date_str() + "\n\n" + self.competition.get_report()
        await context.bot.send_message(chat_id=self.chat_id, text=text)

    async def game_open_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to open the registration to the game"""
        if self.competition.get_date() < datetime.now():
            text=_("Next game is not scheduled yet")
            await update.message.reply_text(text)
            await self.game_schedule(update, context)
            return
        self.competition.open_pending = True
        await self.game_update_facility(update, context)
        
    async def game_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to cancel the next game"""
        status = _("Next play is scheduled on %s. Please confirm cancel game\n\n%s") % ( self.competition.get_date_str(), str(self.competition.get_report()))
        self.headline = text = ChatConversation.msg_admin_top_manage + "\n\n" + status
        await self.reply(update, context, self.admin_menu_game_cancel, text, ChatConversation.GAME_MANAGE_CANCEL)

    async def send_user_message(self, context: ContextTypes.DEFAULT_TYPE, user: Chatuser, text: str) -> None:
        try:
            await context.bot.send_message(chat_id=user.user_id, text=text)
        except ValueError:
            #it is normal when user have not talked with the bot yet
            pass

    async def game_cancel_confirm(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """confirmation of cancelling the game with private notifications of users"""
        for player in self.competition.players:
            text=_("Dear %s. I regret to say, but the next game scheduled at %s is cancelled. See the common chat for details") % (player.owner.get_name(), self.competition.get_date_str())
            await self.send_user_message(context, player.owner, text)
        self.competition.reset()
        self.persistency.save_competition()
        text=_("Dear friends. I regret to say, but the next game scheduled at %s is cancelled. I am really very sorry") % self.competition.get_date_str()
        await context.bot.send_message(chat_id=self.chat_id, text=text)
        await self.reply(update, context, None, self.msg_done, context)

    async def game_schedule(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """display menu to schedule the next game"""
        text = _("Select the date of the next game, or type in. \n" 
                 "The format of date: <day>.<month>.<year> <hour>:<min>, e.g. 15.05.2023 19:15\n\nCurrent set date: %s") \
            % self.competition.get_date_str()
        await self.reply(update, context, self.admin_menu_schedule, text, ChatConversation.GAME_MANAGE_SCHEDULE)

    async def reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE, buttons:Sequence[Sequence[InlineKeyboardButton]], text:str, feature:str = '') -> None:
        """send the reply message to the user's conversation"""
        context.user_data[ChatConversation.CURRENT_FEATURE] = feature
        self.keyboard = InlineKeyboardMarkup(buttons) if (buttons and len(buttons) != 0) else None
        if update.callback_query is not None:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text=text, reply_markup=self.keyboard)
        else:
            await context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=text,
                reply_markup=self.keyboard
            )

    async def game_schedule_next(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to schedule the next game"""
        self.competition.competition_date = ChatConversation.next_plays[0].start
        await self.game_schedule(update, context)

    async def game_schedule_skip_next(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to schedule the next after next game"""
        self.competition.competition_date = ChatConversation.next_plays[1].start
        await self.game_schedule(update, context)

    def parse_date(self, text: str) -> datetime:
        """parse the date in several possible formats"""
        for f in ('%d.%m.%Y %H:%M', '%d.%m.%Y %H.%M'):
            try:
                datetime_object = datetime.strptime(text, f)
                #dateparser.parse(text, date_formats=['%d.%m.%Y %H:%M', '%d.%m.%Y %H.%M']) 
                # -- mixes day and month sometimes, particularly, for 08.11.2023 21:45, en-US locale, even the date format was given!!
                return datetime_object
            except ValueError:
                pass
        return None

    async def game_schedule_date_enter(self, text:str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """callback to enter the date of the next game from the keyboard"""
        d = self.parse_date(text)
        if d is None:
            return False
        self.competition.competition_date = d
        print(_('Entered date: %s') % str(d))
        await self.game_schedule(update, context)

    async def truncate_participants(self, context: ContextTypes.DEFAULT_TYPE):
        """cut the amount of participants"""
        while self.competition.capacity > self.competition.capacity_max:
            #remove first guys who came with friends
            diff = self.competition.capacity - self.competition.capacity_max
            removed = False
            for p in reversed(self.competition.players):
                if p.participants == diff:
                    self.competition.capacity -= diff
                    self.competition.players.remove(p)
                    await self.notify_removed(context, p)
                    removed = True
                    break
            if not removed:
                p = self.competition.players.pop()
                await self.notify_removed(context, p)
                self.competition.capacity -= 1

    async def game_set_participants(self, update: Update, context: ContextTypes.DEFAULT_TYPE, participants:int) -> None:
        """callback to set the number of participants in the next game"""
        self.competition.capacity_max = participants
        if self.competition.capacity > participants:
            await self.truncate_participants(context)
        open_pending = getattr(self.competition, "open_pending", False)
        if open_pending:
            self.competition.open(self.competition.capacity_max)
            text=_("Good news, the registration for the game scheduled at %s is OPEN,\n"
                   "with %s as the maximum number of participants. \n\nJust write '+1' in this chat to join!") % \
                (self.competition.get_date_str(), str(self.competition.capacity_max))
            await context.bot.send_message(chat_id=self.chat_id, text=text)
            self.competition.open_pending = False
        self.persistency.save_competition()
        await self.game_update_facility(update, context)

    async def notify_removed(self, context: ContextTypes.DEFAULT_TYPE, p: Player):
        """notify the player privately that he/she has denied to play"""
        try:
            await self.send_user_message(context, p.owner, 
                _("Sorry, but there is no place for you in the next game at %s") % self.competition.get_date_str())
        except ValueError:
            pass #may be OK because of Telegram bot chatting rules

    async def game_set_participants_as_before(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to set the number of participants"""
        await self.game_set_participants(update, context, self.competition.capacity_max_past)

    async def game_set_participants_10(self,  update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to set the number of participants"""
        await self.game_set_participants(update, context, 10)

    async def game_set_participants_12(self,  update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to set the number of participants"""
        await self.game_set_participants(update, context, 12)

    async def game_set_participants_14(self,  update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to set the number of participants"""
        await self.game_set_participants(update, context, 14)

    async def game_set_participants_16(self,  update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to set the number of participants"""
        await self.game_set_participants(update, context, 16)

    async def game_set_participants_18(self,  update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """callback to set the number of participants"""
        await self.game_set_participants(update, context, 18)

    async def game_manage_participants_enter(self, text:str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """a callback to enter the number of participants"""
        try:
            number = int(text)
        except ValueError:
            return False
        print (_('Number of participants entered: %s') % text)
        await self.game_set_participants(update, context, number)
        return True

    async def end_second_level(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """return to top level conversation or register entry."""
        context.user_data[ChatConversation.START_OVER] = True
        self.keyboard = None
        self.headline = ""
        current_page = context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER]
        if current_page != -1 and current_page < 4:
            context.user_data[ChatConversation.FEATURES][ChatConversation.REGISTER] = current_page + 1
            await self.register_entry(update, context)
        else:
            await self.start(update, context)

    # Third level callbacks
    async def select_feature(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """a generic callback to enter the value"""
        value = update.callback_query.data
        index = context.user_data[ChatConversation.CURRENT_FEATURE]
        context.user_data[ChatConversation.FEATURES][index] = value

        text = self.headline + "\n\n" + _("Selected value: %s") % value
        await update.callback_query.edit_message_text(text=text, reply_markup=self.keyboard)

    def __init__(self, bot_token, chat_id, chat: Chat, competition: Competition, persistency: ChatPersistency):
        """constructor"""
        self.chat = chat
        self.chat_id = chat_id
        self.competition = competition
        self.persistency = persistency

        self.keyboard = None
        self.headline = ""
        self.que = None
        self.updater = None

        # Create the Application and pass it your bot's token.
        builder = Application.builder()
        telegram_persistence = PicklePersistence(filepath='telegram-bot.pickle')

        self.application = builder.token(bot_token).persistence(telegram_persistence).concurrent_updates(False).build()

        #generic command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        # on non command i.e message - register to the game if open, and receive text input if needed
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.user_message))
        #callback handlers - top level menu
        self.application.add_handler(CallbackQueryHandler(self.register_entry, pattern="^" + str(ChatConversation.REGISTER) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.select_level, pattern="^" + str(ChatConversation.REGISTER_LEVEL) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.select_years, pattern="^" + str(ChatConversation.REGISTER_YEARS) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.select_racket, pattern="^" + str(ChatConversation.REGISTER_RACKET) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.select_wannaplay, pattern="^" + str(ChatConversation.REGISTER_WANNAPLAY) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.register_submit_info, pattern="^" + str(ChatConversation.REGISTER_CONFIRM_INFO) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_manage, pattern="^" + str(ChatConversation.GAME_MANAGE) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_join, pattern="^" + str(ChatConversation.GAME_JOIN) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.end, pattern="^" + str(ChatConversation.END) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.help_command, pattern="^" + str(ChatConversation.RULES) + "$"))
        #and registration sub-menu
        self.application.add_handler(CallbackQueryHandler(self.end_second_level, pattern="^" + str(ChatConversation.BACK) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.select_feature, pattern=
                "^" + str(Level.LEVEL_NONE) 
                + "$|^" + str(Level.LEVEL_BEGINNER)
                + "$|^" + str(Level.LEVEL_MEDIUM)
                + "$|^" + str(Level.LEVEL_ADVANCED)
                + "$|^" + str(Level.LEVEL_CHAMPION)
                + "$|^" + str(YearsExperience.YEARS_0) 
                + "$|^" + str(YearsExperience.YEARS_1)
                + "$|^" + str(YearsExperience.YEARS_3)
                + "$|^" + str(YearsExperience.YEARS_5)
                + "$|^" + str(YearsExperience.YEARS_10)
                + "$|^" + str(YearsExperience.YEARS_100)
                + "$|^" + str(YesNo.YESNO_YES) 
                + "$|^" + str(YesNo.YESNO_NO)
                + "$"
        ))
        #and game management sub-menus
        self.application.add_handler(CallbackQueryHandler(self.game_view_participants, pattern="^" + str(ChatConversation.GAME_MANAGE_VIEW_PARTICIPANTS) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_update_facility, pattern="^" + str(ChatConversation.GAME_MANAGE_UPDATE_FACILITY) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_cancel, pattern="^" + str(ChatConversation.GAME_MANAGE_CANCEL) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_cancel_confirm, pattern="^" + str(ChatConversation.GAME_MANAGE_CANCEL_CONFIRM) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_close_registration, pattern="^" + str(ChatConversation.GAME_MANAGE_CLOSE_REGISTRATION) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_schedule, pattern="^" + str(ChatConversation.GAME_MANAGE_SCHEDULE) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_schedule_next, pattern="^" + str(ChatConversation.GAME_MANAGE_SCHEDULE_NEXT_REGULAR_DATE) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_schedule_skip_next, pattern="^" + str(ChatConversation.GAME_MANAGE_SCHEDULE_SKIP_NEXT_REGULAR_DATE) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_open_registration, pattern="^" + str(ChatConversation.GAME_MANAGE_OPEN) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_register, pattern="^" + str(ChatConversation.GAME_JOIN_REGISTER) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_deregister, pattern="^" + str(ChatConversation.GAME_JOIN_DEREGISTER) + "$"))

        self.application.add_handler(CallbackQueryHandler(self.game_set_participants_as_before, pattern="^" + str(ChatConversation.GAME_MANAGE_SET_PARTICIPANTS_AS_BEFORE) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_set_participants_10, pattern="^" + str(ChatConversation.GAME_MANAGE_SET_PARTICIPANTS_10) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_set_participants_12, pattern="^" + str(ChatConversation.GAME_MANAGE_SET_PARTICIPANTS_12) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_set_participants_14, pattern="^" + str(ChatConversation.GAME_MANAGE_SET_PARTICIPANTS_14) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_set_participants_16, pattern="^" + str(ChatConversation.GAME_MANAGE_SET_PARTICIPANTS_16) + "$"))
        self.application.add_handler(CallbackQueryHandler(self.game_set_participants_18, pattern="^" + str(ChatConversation.GAME_MANAGE_SET_PARTICIPANTS_18) + "$"))

        #diagnostic
        self.application.add_handler(CallbackQueryHandler(self.generic_callback))

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handles the /help command"""
        reply_privately = context._chat_id != context._user_id
        chat = await update.get_bot().get_chat(self.chat_id)
        text = chat.pinned_message.text if chat.pinned_message else ChatConversation.msg_help % self.chat.get_admins(ChatConversation.msg_admins_any_of)
        if reply_privately:
            if update.message:
                await context.bot.delete_message(chat_id = context._chat_id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=context._user_id, text=text)
        else:
            await self.reply(update, context, None, text)

    async def generic_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """A generic callback, useful for debugging not handled messages. In the normal life, it SHALL NOT FIRE"""
        if str(context._chat_id) != self.chat_id and context._chat_id != context._user_id:
            return

        await update.callback_query.edit_message_text(text="Unprocessed!")

    async def user_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """handles the incoming text message from a user, typed either directly to a chatbot, or in the chat"""
        if str(context._chat_id) != self.chat_id and context._chat_id != context._user_id:
            return
        if not update.message:
            return
        text_lc = update.message.text.lower().strip()
        if len(text_lc) == 0:
            return
       
        reply = ""
        registered = False

        userid = update.message.from_user.id
        username = update.message.from_user.username
        fullname = update.message.from_user.full_name

        chatuser = self.chat.find_user(userid)
        if chatuser and chatuser.check_and_update(username, fullname):
            self.persistency.save_chat()

        admin = chatuser.status in {Chatuser.ADMIN} if chatuser else False
        if admin:
            if context.user_data[ChatConversation.CURRENT_FEATURE] == ChatConversation.GAME_MANAGE_SCHEDULE:
                if await self.game_schedule_date_enter(text_lc, update, context):
                    return
            if context.user_data[ChatConversation.CURRENT_FEATURE] == ChatConversation.GAME_MANAGE_SET_PARTICIPANTS:
                if await self.game_manage_participants_enter(text_lc, update, context):
                    return

        trusted = chatuser.status in {Chatuser.TRUSTED, Chatuser.ADMIN} if chatuser else False
        if trusted:
            if text_lc and text_lc[0] == "+" and (len(text_lc) == 1 or text_lc[1:].isnumeric()):
                num = 1 if len(text_lc) == 1 else int(text_lc[1:])
                registered, reply = self.competition.register(chatuser, num)
            elif text_lc and text_lc[0] == "-" and (len(text_lc) == 1 or text_lc[1:].isnumeric()):
                num = 1 if len(text_lc) == 1 else int(text_lc[1:])
                registered, reply = self.competition.deregister(chatuser, num)
        else:
             registered, reply = False, ChatConversation.msg_register_first
        if reply:
            if trusted:
                await self.send_user_message(context, chatuser, reply)
            else:
                await update.message.reply_text(reply + "\n\n" + ChatConversation.msg_switching_to_private)
                await self.start(update, context)
        
        if registered:
            self.persistency.save_competition()
            await update.message.reply_text(self.competition.get_report())

    def run(self):
        """run message loop pooling"""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def process_events(self, min_events = 0):
        """pooling procedure to handle incoming events in the unit test mode"""
        if getattr(self, "que", None) is None:
            self.que = asyncio.Queue()
            await self.application.initialize()
            self.updater = Updater(self.application.bot, update_queue=self.que)
            await self.updater.initialize()
            await self.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        processed = 0
        proceed = True
        while proceed:
            if processed < min_events:
                update = await self.que.get()
                await self.application.process_update(update)
                processed = processed + 1
            else:
                proceed = not self.que.empty()
                if proceed:
                    update = self.que.get_nowait()
                    await self.application.process_update(update)
                    processed = processed + 1
