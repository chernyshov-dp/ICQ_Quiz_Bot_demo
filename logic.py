import os
import sys
import pickle
import random
import threading
from time import sleep

# Проверка на наличие существующих данных о чатах
if os.path.exists('settings.pkl'):
    with open('settings.pkl', 'rb') as f:
        chats = pickle.load(f)
else:
    chats = {}

question1 = ['Шахматный скакун', 'Свадебный клич', 'Самая важная для человека жидкость']
question3 = ['Чему равен факториал нуля', 'Солнце это', '"В подворотне нас ждёт ...,  хочет нас посадить на крючок" ('
                                                        'песня)']

answers = {'q1': ['конь', 'горько', 'вода'], 'q2': ['японского', 'чёрный', 'черный', 'африка'],
           'q3': ['1', 'звезда', 'маньяк']}


class Sender(threading.Thread):
    """ Отправляет сообщение пользователю с задержкой """

    def __init__(self, bot, chat_id, message, delay, seed):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.message = message
        self.delay = delay
        self.seed = seed

    def run(self):
        """ Класс потока, который вызывается вместе со start() """
        if self.seed == 'pause':
            sleep(self.delay)
            self.bot.send_text(chat_id=self.chat_id, text=self.message)

        else:
            sleep(self.delay - 30)
            if chats[f'{self.chat_id}'][0] == 'q3' and self.seed == chats[f'{self.chat_id}'][4]:
                chats[f'{self.chat_id}'][3] -= 50
                self.bot.send_text(chat_id=self.chat_id, text="Осталось 30 секунд ⏱")
                sleep(self.delay - 40)

                if chats[f'{self.chat_id}'][0] == 'q3' and self.seed == chats[f'{self.chat_id}'][4]:
                    chats[f'{self.chat_id}'][3] -= 25
                    self.bot.send_text(chat_id=self.chat_id, text="Осталось 10 секунд ⏱")
                    sleep(self.delay - 50)

                    if chats[f'{self.chat_id}'][0] == 'q3' and self.seed == chats[f'{self.chat_id}'][4]:
                        self.bot.send_text(chat_id=self.chat_id, text=self.message)
                        self.bot.send_text(chat_id=self.chat_id, text=get_leaderboard(self.chat_id))
                        chats[f'{self.chat_id}'][0] = 'added'
                        chats[f'{self.chat_id}'][2] = None
                        chats[f'{self.chat_id}'][3] = None
                        chats[f'{self.chat_id}'][4] = random.randint(100000, 999999)


def start_cb(bot, event):
    """ Вызов команды /start """
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Всем привет, меня зовут Квиз-бот! 🤖\n  "
                                                             "\nЯ создан "
                                                             "специально "
                                                             "для того, чтобы проводить интеллектуальные соревнования "
                                                             "между различными командами, находящимися на "
                                                             "просторах ICQ.\n\n"
                                                             "Для того чтобы узнать о моих возможностях более "
                                                             "подробно\n"
                                                             "воспользуйтесь командой /help")
    chat_id = event.data['chat']['chatId']  # УБРАТЬ (ТЕСТ)
    chats[f'{chat_id}'] = ['added', None, None, None, random.randint(100000, 999999)]  # УБРАТЬ (ТЕСТ)


def help_cb(bot, event):
    """ Вызов команды /help """
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Список доступных команд 🎲\n\n"
                                                             "/play - начать игру\n"
                                                             "/rules - узнать правила игры\n"
                                                             "/team - изменить название команды\n"
                                                             "/stop - закончить игру\n")


def team_cb(bot, event):
    """ Вызов команды /team """
    (useless, team_name) = event.data["text"].partition(" ")[::2]
    this_chat = event.data['chat']['chatId']
    team_status = chats[f'{this_chat}'][1]

    if team_status is None:

        # Если название для команды не задано 
        if team_name == "":
            bot.send_text(chat_id=this_chat, text='Эй, так не пойдёт, я хочу чтобы вы придумали '
                                                  'название для вашей команды! 😛\n\n'
                                                  '/team "Название команды"')
        else:
            bot.send_text(chat_id=this_chat, text=f'"{team_name}" - звучит круто! 😎')
            chats[f'{this_chat}'][1] = team_name
            bot.send_text(chat_id=this_chat, text='🔥 Ну что, вы готовы? 🔥')
            bot.send_text(chat_id=this_chat, text='/play - начать игру')
    else:
        (useless, team_name) = event.data["text"].partition(" ")[::2]
        if team_name == "":
            bot.send_text(chat_id=this_chat, text='Недопустимое название 😛\n\n'
                                                  '/team "Название команды"')

        else:
            chats[f'{this_chat}'][1] = team_name
            bot.send_text(chat_id=this_chat, text='Вы успешно изменили название своей команды! 🤠')
            bot.send_text(chat_id=this_chat, text=f'Текущее название - "{team_name}"')


def stop_playing_cb(bot, event):
    """ Вызов команды /stop """
    user = event.data['chat']['chatId']
    if chats[f'{user}'][0] == 'q1' or chats[f'{user}'][0] == 'q2' or chats[f'{user}'][0] == 'q3':
        chats[f'{user}'][0] = 'added'
        chats[f'{user}'][2] = None
        chats[f'{user}'][3] = None
        chats[f'{user}'][4] = random.randint(100000, 999999)
        bot.send_text(chat_id=user, text='Вы завершили игру 😐')

    else:
        bot.send_text(chat_id=user, text='🚫 Вы ещё не начали игру 🚫')


def rules_cb(bot, event):
    """ Вызов команды /rules"""
    bot.send_text(chat_id=event.data['chat']['chatId'], text='Как устроена игра? 🧠\n\n'
                                                             'Квиз - соревнование, в ходе которого один или несколько '
                                                             'участников отвечают на поставленные им вопросы.\n'
                                                             'Наша игра будет состоять из трёх вопросов:\n\n'
                                                             '1⃣ Самый первый и простой этап, количество ответов и '
                                                             'время неограниченно\n'
                                                             '2⃣ На втором этапе вам предоставляется 3 варианта и '
                                                             'всего 2 попытки для того, чтобы ответить правильно\n'
                                                             '3⃣ Наиболее сложный и интересный этап - 1 вопрос и  '
                                                             'лишь 1 минута на верный ответ\n\n'
                                                             'После того как я задам вашей команде вопрос вы должны '
                                                             'ответить на него в заданном формате - "!ВашОтвет"\n\n'
                                                             'Удачи! 🍀')


def play_cb(bot, event):
    """ Вызов команды /play """
    user = event.data['chat']['chatId']  # Id чата, из которого приходит сообщение
    # Проверка "регистрации" команды
    if chats[f'{user}'][1] is None:
        bot.send_text(chat_id=user, text='Для того чтобы начать игру придумайте название для вашей команды\n\n'
                                         'Воспользуйтесь /team  "Название команды"')
    else:

        if chats[f'{user}'][0] == 'added':

            first = random.choice(question1)
            bot.send_text(chat_id=event.data['chat']['chatId'], text="Начинаем игру! 💥")
            chats[f'{user}'][0] = 'q1'
            with open('pictures/q1.jpg', 'rb') as file:
                bot.send_file(chat_id=event.data['chat']['chatId'], file=file, caption="Вопрос 1 💬\n\n"
                                                                                       f"{first}")

        elif chats[f'{user}'][0] == 'q1' or chats[f'{user}'][0] == 'q2' or chats[f'{user}'][0] == 'q3':
            bot.send_text(chat_id=event.data['chat']['chatId'], text="Игра уже идёт! 💣")


def get_leaderboard(user):
    """ Формирование турнирной таблицы"""
    this_team = chats[f'{user}'][1]
    top = []
    fake_teams = {f'{this_team}': chats[f'{user}'][3],
                  'Розовые пантеры': random.randrange(0, 300, 50),
                  'Акулы вегетарианцы': random.randrange(0, 300, 50),
                  'Бодрые ленивцы': random.randrange(0, 300, 50),
                  'Утренние совы': random.randrange(0, 300, 50)}

    for team in reversed(sorted(fake_teams.items(), key=lambda duo: duo[1])):
        top.append(team[0] + ' - ' + str(team[1]))

    return ('Результаты игры 🏆 \n\n'
            f'1. {top[0]} 💡\n'
            f'2. {top[1]} 💡\n'
            f'3. {top[2]} 💡\n'
            f'4. {top[3]} 💡\n'
            f'5. {top[4]} 💡'
            )


def message_cb(bot, event):
    user = event.data['chat']['chatId']  # Id чата, из которого приходит сообщение

    if event.data["text"][0] == '!':

        if chats[f'{user}'][0] == 'q1':
            if event.data["text"][1:].lower() in answers['q1']:
                bot.send_text(chat_id=user, text="Совершенно верно! 🤩")
                chats[f'{user}'][0] = 'q2'
                chats[f'{user}'][2] = 2
                chats[f'{user}'][3] = 200

                #  Генерация случайного вопроса
                file_url = None
                question2 = random.randint(1, 3)
                if question2 == 1:
                    file_url = 'pictures/q2p1.jpg'
                elif question2 == 2:
                    file_url = 'pictures/q2p2.jpg'
                elif question2 == 3:
                    file_url = 'pictures/q2p3.jpg'

                with open(file_url, 'rb') as file:
                    bot.send_file(chat_id=event.data['chat']['chatId'], file=file, caption="Вопрос 2 💬\n\n"
                                                                                           "Не забывайте - у вас "
                                                                                           "только 2 попытки!")

            else:
                bot.send_text(chat_id=user, text="Не совсем, попробуйте ещё раз 😦")

        # БЛОК ВТОРОГО ЭТАПА
        elif chats[f'{user}'][0] == 'q2':
            if chats[f'{user}'][2] > 0:

                if event.data["text"][1:].lower() in answers['q2']:
                    bot.send_text(chat_id=user, text="Да вы сегодня в ударе! 🤩")
                    third = random.choice(question3)
                    bot.send_text(chat_id=user, text="Приготовьтесь, у вас есть только 1 минута для ответа на "
                                                     "следующий вопрос")
                    Sender(bot, user, f"Вопрос 3 💬\n\n{third}",
                           3, 'pause').start()

                    chats[f'{user}'][0] = 'q3'

                    Sender(bot, user, "🔔 ИГРА ОКОНЧЕНА 🔔", 60, chats[f'{user}'][4]).start()

                else:
                    if chats[f'{user}'][2] == 2:
                        chats[f'{user}'][3] = 150
                        bot.send_text(chat_id=user, text="Неправильно! 😦\n\n"
                                                         "🆘 У вас осталась 1 попытка 🆘")
                    chats[f'{user}'][2] -= 1

            if chats[f'{user}'][2] == 0:
                chats[f'{user}'][3] = 100
                bot.send_text(chat_id=user, text="К сожалению, количество попыток исчерпано 😒\n\n"
                                                 "Переходим к следующему вопросу...")
                third = random.choice(question3)
                bot.send_text(chat_id=user, text="Приготовьтесь, у вас есть только 1 минута для ответа на "
                                                 "следующий вопрос")
                Sender(bot, user, f"Вопрос 3 💬\n\n{third}",
                       3, 'pause').start()

                chats[f'{user}'][0] = 'q3'

                Sender(bot, user, "🔔 ИГРА ОКОНЧЕНА 🔔", 60, chats[f'{user}'][4]).start()
                chats[f'{user}'][0] = 'q3'

        #  БЛОК ТРЕТЬЕГО ЭТАПА
        elif chats[f'{user}'][0] == 'q3':

            if event.data["text"][1:].lower() in answers['q3']:
                bot.send_text(chat_id=user, text="Правильный ответ! 🤩")
                bot.send_text(chat_id=user, text="🔔 ИГРА ОКОНЧЕНА 🔔")
                bot.send_text(chat_id=user, text=get_leaderboard(user))
                chats[f'{user}'][0] = 'added'
                chats[f'{user}'][2] = None
                chats[f'{user}'][3] = None
                chats[f'{user}'][4] = random.randint(100000, 999999)

            else:
                bot.send_text(chat_id=user, text="Не совсем, попробуйте ещё раз 😦")


def unknown_command_cb(bot, event):
    """ Вызов неизвестной команды """
    user = event.data['chat']['chatId']
    bot.send_text(
        chat_id=user,
        text="Извини, я не совсем понимаю о чём ты 😅\n"
             "Воспользуйся /help для того, чтобы узнать о моих возможностях")


def im_new_chat_member_cb(bot, event):
    """ Возврат приветственного сообщения при добавлении в новый чат """
    try:
        # Пробное значение в 30 человек
        for i in range(31):
            chat_id = event.data['chat']['chatId']

            # Проверка на наличие id бота в списке добавленных участников
            if event.data['newMembers'][i]['userId'] == '753354310':
                # {"chat_id}:['этап игры', 'название команды', количество попыток, количество очков, сид сессии]
                chats[f'{chat_id}'] = ['added', None, None, None, random.randint(100000, 999999)]
                bot.send_text(
                    chat_id=event.data['chat']['chatId'],
                    text="Всем привет, меня зовут Квиз-бот! 🤖\n  "
                         "\nЯ создан "
                         "специально "
                         "для того, чтобы проводить интеллектуальные соревнования "
                         "между различными командами, находящимися на "
                         "просторах ICQ.\n\n"
                         "Для того чтобы узнать о моих возможностях более "
                         "подробно\n"
                         "воспользуйтесь командой /help"

                )

    except IndexError:
        pass


def my_handler(**args):
    """ Записать данных словаря chats """
    print("Данные о чатах успешно сохранены!")
    with open('settings.pkl', 'wb') as f:
        pickle.dump(chats, f)
    sys.exit(0)
