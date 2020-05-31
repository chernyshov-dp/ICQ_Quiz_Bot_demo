import json
import random
from time import sleep


def start_cb(bot, event):
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=["typing"])
    sleep(1)
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=[])
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Всем привет, меня зовут Квиз-бот!\n\n  Я создан "
                                                             "специально "
                                                             "для того, чтобы проводить интеллектуальные соревнования "
                                                             "между различными командами, находящимися на "
                                                             "просторах ICQ.\n\n"
                                                             "Для того чтобы узнать о моих возможностях более подробно"
                                                             "воспользуйтесь командой /help")


def help_cb(bot, event):
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=["typing"])
    sleep(1)
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=[])
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Список доступных команд:\n"
                                                             "/play - начать игру\n"
                                                             "/rules - узнать правила игры\n"
                                                             "/team - выбрать название команды\n")


def team_cb(bot, event):
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=["typing"])
    sleep(1)
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=[])
    bot.send_text(chat_id=event.data['chat']['chatId'], text='Ну что, придумали название для вашей команды?\n'
                                                             '/name "Название команды" - для того чтобы выбрать '
                                                             'название')
    sleep(0.5)
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Кстати, совсем забыл сказать, я могу помочь вам в "
                                                             "выборе классного названия",
                  inline_keyboard_markup="[{}]".format(json.dumps([
                      {"text": "Случайное название", "callbackData": "get_team_name", "style": "primary"}
                  ])))


def rules_cb(bot, event):
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=["typing"])
    sleep(1)
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=[])
    bot.send_text(chat_id=event.data['chat']['chatId'], text='Как устроена игра?\n\n'
                                                             'Квиз - соревнование, в ходе которого один или несколько '
                                                             'участников отвечают на поставленные им вопросы.\n '
                                                             'Наша игра будет состоять из трёх вопросов:\n'
                                                             '- Самый первый и простой этап, количество ответов и '
                                                             'время неограниченно\n '
                                                             '- На втором этапе вам предоставляется 3 варианта и '
                                                             'всего 2 попытки для того, чтобы ответиь правильно\n '
                                                             '- Наиболее сложный и интересный этап - 1 вопрос и 1 '
                                                             'минута на верный ответ\n\n '
                                                             'Удачи!')


def not_ready_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text='Эй, а как же выбрать название для своей команды - это '
                                                             'очень важно!\n\n'
                                                             'Воспользуйтесь командой /team')


def team_status():
    pass


def play_cb(bot, event):
    status = 0
    questions = {'2 + 2': '4', '3 + 3': '6', '5 + 5': '10'}

    if not status:
        phrases = ["На старт!", "Внимание!", "Время напрячь мозги!"]
        bot.send_text(chat_id=event.data['chat']['chatId'], text="Начинаю отсчёт...")
        sleep(2)
        for go in phrases:
            bot.send_text(chat_id=event.data['chat']['chatId'], text=go)
            sleep(1)

        firs_q = random.choice(list(questions.keys()))
        bot.send_text(chat_id=event.data['chat']['chatId'],
                      text=firs_q)


        if (event.dataх['text'])[6:] == questions[firs_q]:
            bot.send_text(chat_id=event.data['chat']['chatId'],
                          text='Совершенно верно!')
        else:
            bot.send_text(chat_id=event.data['chat']['chatId'],
                          text='Не-а')




def answer_cb(bot, event):
    if (event.dataх['text'])[6:] == questions[firs_q]:
        bot.send_text(chat_id=event.data['chat']['chatId'],
                      text='Совершенно верно!')



def get_leaderboard():
    top = []

    fake_teams = {'team1': str(random.randrange(0, 300, 50)), 'team2': str(random.randrange(0, 300, 50)),
                  'team3': str(random.randrange(0, 300, 50)), 'team4': str(random.randrange(0, 300, 50)),
                  'team5': str(random.randrange(0, 300, 50))}

    for team in reversed(sorted(fake_teams.items(), key=lambda duo: duo[1])):
        top.append(team[0] + ' - ' + team[1])

    return ('Результаты игры 🏆 \n\n'
            f'1. {top[0]}\n'
            f'2. {top[1]}\n'
            f'3. {top[2]}\n'
            f'4. {top[3]}\n'
            f'5. {top[4]}'
            )


def show_leaderboard(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text=get_leaderboard())


def image_cb(bot, event):
    bot.send_text(
        chat_id=event.data['chat']['chatId'],
        text="Images with {filed} fileId was received".format(
            filed=", ".join([p['payload']['fileId'] for p in event.data['parts']])
        )
    )


def sticker_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Your sticker is so funny!")


def message_cb(bot, event):
    if event.data:
        bot.send_text(chat_id=event.data['chat']['chatId'], text="Message was received")


def buttons_answer_cb(bot, event):
    default_teams = ['team1', 'team2', 'team3', 'team4', 'team5']
    if event.data['callbackData'] == "get_team_name":
        team_name = random.choice(default_teams)
        sleep(2)
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=f'Придумал, "{team_name}", звучит классно!',
            show_alert=True
        )


def unknown_command_cb(bot, event):
    user = event.data['chat']['chatId']
    (command, command_body) = event.data["text"].partition(" ")[::2]
    bot.send_text(
        chat_id=user,
        text="Unknown command '{message}' with body '{command_body}' received from '{source}'.".format(
            source=user, message=command[1:], command_body=command_body
        )
    )


def new_chat_members_cb(bot, event):
    if bot.event.data['newMembers']['userId'] == '766302308' or bot.event.data['newMembers'][
        'firstName'] == 'fl_test_bot':
        bot.send_text(
            chat_id=event.data['chat']['chatId'],
            text="Hi, everyone!"
        )
