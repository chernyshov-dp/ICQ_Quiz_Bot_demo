import json
from time import sleep

from bot.bot import Bot
from bot.filter import Filter
from bot.handler import UnknownCommandHandler, MessageHandler, CommandHandler, StartCommandHandler,\
     BotButtonCommandHandler, NewChatMembersHandler
from logic import start_cb, help_cb, image_cb, sticker_cb,  message_cb, buttons_answer_cb, team_cb, rules_cb, play_cb,\
     unknown_command_cb, new_chat_members_cb, show_leaderboard

from pprint import pprint

NAME = "FL test bot"
VERSION = "alpha"
TOKEN = "001.1884298346.2404420450:766302308"
OWNER = "@chaddydaddy"
TEST_CHAT = "XXXXX"
TEST_USER = "XXXXX"
API_URL = " "


def main():

    bot = Bot(token=TOKEN, name=NAME, version=VERSION)

    # Handler for start command
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))

    # Handler for simple text message without media content
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.text, callback=message_cb))

    # Handler for help command
    bot.dispatcher.add_handler(CommandHandler(command="help", callback=help_cb))

    # Any other user command handler
    bot.dispatcher.add_handler(CommandHandler(command="team", callback=team_cb))
    bot.dispatcher.add_handler(CommandHandler(command="rules", callback=rules_cb))
    bot.dispatcher.add_handler(CommandHandler(command="play", callback=play_cb))
    bot.dispatcher.add_handler(CommandHandler(command="top", callback=show_leaderboard))

    # Handler for unknown commands
    bot.dispatcher.add_handler(UnknownCommandHandler(callback=unknown_command_cb))

    # Handler for sticker
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.sticker, callback=sticker_cb))

    # Handlers for other file types
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.image, callback=image_cb))

    # Handler for bot buttons reply.
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

    # Handler for add user to chat
    bot.dispatcher.add_handler(NewChatMembersHandler(callback=new_chat_members_cb))

    bot.start_polling()

    bot.idle()


if __name__ == '__main__':
    main()

'''
    # Send bot buttons
    bot.send_text(chat_id=OWNER,
                  text="Hello with buttons.",
                  inline_keyboard_markup="[{}]".format(json.dumps([
                      {"text": "Action 1", "url": "http://mail.ru"},
                      {"text": "Action 2", "callbackData": "call_back_id_2"},
                      {"text": "Action 3", "callbackData": "call_back_id_3"}
                  ])))
'''