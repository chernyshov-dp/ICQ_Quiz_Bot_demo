import signal

from bot.bot import Bot
from bot.filter import Filter
from bot.handler import UnknownCommandHandler, MessageHandler, CommandHandler, StartCommandHandler, \
     NewChatMembersHandler

from logic import start_cb, help_cb, message_cb, team_cb, rules_cb, play_cb, unknown_command_cb, \
     im_new_chat_member_cb, my_handler, stop_playing_cb

NAME = "Demo_Quiz_Bot"
VERSION = "alpha"
# Токен бота
TOKEN = "001.3745442009.2489702902:753354310"
# Модератор бота, может использоваться в дальнейшем,
# В данном проекте роли не играет
# Пример заполнения - @chaddydaddy
OWNER = "@chaddydaddy"
TEST_CHAT = None
TEST_USER = None
API_URL = None


def main():
    """ Основная функция """
    bot = Bot(token=TOKEN, name=NAME, version=VERSION)

    # Обработчик команды /start
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))

    # Обработчик основного потока текстовых сообщений
    bot.dispatcher.add_handler(MessageHandler(filters=Filter.text, callback=message_cb))

    # Обработчик команды /help
    bot.dispatcher.add_handler(CommandHandler(command="help", callback=help_cb))

    # Обработчики команд /team, /rules, /play, /stop
    bot.dispatcher.add_handler(CommandHandler(command="team", callback=team_cb))
    bot.dispatcher.add_handler(CommandHandler(command="rules", callback=rules_cb))
    bot.dispatcher.add_handler(CommandHandler(command="play", callback=play_cb))
    bot.dispatcher.add_handler(CommandHandler(command="stop", callback=stop_playing_cb))

    # Обработчик неизвестных команд
    bot.dispatcher.add_handler(UnknownCommandHandler(callback=unknown_command_cb))

    # Обработчик добавления бота в чат
    bot.dispatcher.add_handler(NewChatMembersHandler(callback=im_new_chat_member_cb))

    # Запуск чат-бота
    bot.start_polling()

    # Обеспечивает непреривную работу чат-бота
    bot.idle()

    # Перехват закрытия программы
    signal.signal(signal.SIGTERM, my_handler())


if __name__ == '__main__':
    main()
