from decouple import config
from telebot import types
import telebot
from main import record_get, record_push, get_schedule_for_group, get_lesson, user_exists

week = record_get("source.json")
token = config("TOKEN")
bot =  telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 
        'Hello, I am a bot that will help you to know where you are supposed to be at a particular time!\n\nCommands:\n\n/info - information about bot and Ala-too\n/schedule - begin to work with a bot!\n'
    )

@bot.message_handler(commands=["info"])
def info(message):
    define_text = """
The Telegram bot "Bot Name" is a convenient tool for students, providing instant access to class schedules. The bot is developed with the needs of the student community in mind, offering a fast and easy way to check current and upcoming classes.

The main features of the bot include:

- The ability to view schedules by day, week, or specific subjects.
- Students can also receive notifications about upcoming classes, deadlines, or changes in the schedule.
- The bot has an intuitively understandable interface, making it easy to use even for less experienced users.

"Bot Name" - this Telegram bot will be a reliable assistant in organizing the educational process and day-to-day tasks for students.
    """
    keyboard = types.InlineKeyboardMarkup()
    ala_too_website = types.InlineKeyboardButton(
        text="Info about Ala-Too", 
        url='http://alatoo.edu.kg/#gsc.tab=0'
    )
    schedule = types.InlineKeyboardButton(
        text="Original Schedule (access required)", 
        url=week['schedule']
    )
    keyboard.add(ala_too_website)
    keyboard.add(schedule)
    bot.send_message(message.chat.id, f"{define_text}\n\nSchedule information:\n\nUniversity: {week['university']}\nSemester: {week['semester']}", reply_markup=keyboard)

def get_group_with_elective(message):
    keyboard = types.InlineKeyboardMarkup()
    count = []
    for group in week['groups']:
        button = types.InlineKeyboardButton(text=group, callback_data=f"group_{group}")
        count.append(button)
        if len(count) == 2:
            keyboard.add(count[0], count[1])
            count = []
    if len(count) == 1:
        keyboard.add(count[0])
    bot.send_message(message.chat.id, 'Choose your group:\n', reply_markup=keyboard)


@bot.message_handler(commands=['schedule'])
def schedule(message):
    users = record_get("users.json")
    user = str(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    if not user_exists(user, users):
        bot.send_message(message.chat.id, 'Looks like you haven\'t chosen your group yet. Let\'s choose one:\n', reply_markup=keyboard)
        get_group_with_elective(message)
    else:
        group = users[user]
        button_days = types.InlineKeyboardButton(text="Days", callback_data=f"days")
        button_today = types.InlineKeyboardButton(text="Today", callback_data=f"today")
        button_week = types.InlineKeyboardButton(text="Week", callback_data=f"week")
        button_lesson = types.InlineKeyboardButton(text="Next/Current lesson", callback_data=f"lesson")
        button_change_group = types.InlineKeyboardButton(text="Change the group", callback_data=f"change_group")
        keyboard.add(button_days, button_week)
        keyboard.add(button_today, button_lesson)
        keyboard.add(button_change_group)
        text = f'Your group is {group}!\nPlease choose an option:'
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('group'))
def choose_group_callback(call):
    users = record_get("users.json")
    user = call.from_user.id
    group = call.data.split('_')[1]
    bot.send_message(call.message.chat.id, f'Great! Your group is {group}!\nPress /schedule to begin to use our bot.')
    users[user] = group
    record_push("users.json", users)

@bot.callback_query_handler(func=lambda call: call.data == 'days')
def choose_days_callback(call):
    keyboard = types.InlineKeyboardMarkup()
    for day in week['days'].keys():
        button_day = types.InlineKeyboardButton(text=day.capitalize(), callback_data=f"day_{day}")
        keyboard.add(button_day)
    bot.send_message(call.message.chat.id, 'Choose a day:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
def choose_day_callback(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    day = call.data.split('_')[1]
    day_list = get_schedule_for_group(group, day)
    result = ''
    for day in day_list:
        result += day
    bot.send_message(call.message.chat.id, f'{result}')
    bot.send_message(call.message.chat.id, 'Press /schedule to use bot again.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('today'))
def choose_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    today_list = get_schedule_for_group(group, 'today')
    result = ''
    for day in today_list:
        result += day
    bot.send_message(call.message.chat.id, f'{result}')
    bot.send_message(call.message.chat.id, 'Press /schedule to use bot again.')
    

@bot.callback_query_handler(func=lambda call: call.data.startswith('week'))
def choose_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    week_list = get_schedule_for_group(group, "week")
    result = ''
    for day in week_list:
        result += day
    bot.send_message(call.message.chat.id, result)
    bot.send_message(call.message.chat.id, 'Press /schedule to use bot again.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('lesson'))
def choose_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    lesson_list = get_lesson(group)
    result = ''
    for day in lesson_list:
        result += day
    bot.send_message(call.message.chat.id, result)
    bot.send_message(call.message.chat.id,'Press /schedule to use bot again.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_group'))
def change_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    if user in users:
        del users[user]
        record_push('users.json', users)
        bot.send_message(call.message.chat.id, 'Your group has been deleted. Choose another one:\n')
        get_group_with_elective(call.message)
    else:
        bot.send_message(call.message.chat.id, 'You don\'t have a group to delete. Choose one:\n')
        get_group_with_elective(call.message)
    
if __name__ == '__main__':
    bot.infinity_polling()