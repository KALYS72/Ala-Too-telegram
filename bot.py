from decouple import config
from telebot import types
import telebot
from main import record_get, record_push, get_schedule_for_group, get_lesson, user_exists

week = record_get("source.json")
token = config("TOKEN")
bot =  telebot.TeleBot(token)
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''Hello, I am a bot that will help you to know where you are supposed to be at a particular time!\n\nCommands:\n\n/info - information about bot and Ala-too\n/schedule - begin to work with a bot!\n''')

@bot.message_handler(commands=["info"])
def info(message):
    keyboard = types.InlineKeyboardMarkup()
    ala_too_website = types.InlineKeyboardButton(text="Info about Ala-Too", url='http://alatoo.edu.kg/#gsc.tab=0')
    schedule = types.InlineKeyboardButton(text="Original Schedule (access required)", url=week['schedule'])
    keyboard.add(ala_too_website)
    keyboard.add(schedule)
    bot.send_message(message.chat.id, f"Schedule information:\n\nUniversity: {week['university']}\nSemester: {week['semester']}", reply_markup=keyboard)

def get_group(message):
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
        get_group(message)
    else:
        group = users[user]
        button_days = types.InlineKeyboardButton(text="Days", callback_data=f"days")
        button_week = types.InlineKeyboardButton(text="Week", callback_data=f"week")
        keyboard.add(button_days, button_week)
        button_lesson = types.InlineKeyboardButton(text="Next/Current lesson", callback_data=f"lesson")
        button_change_group = types.InlineKeyboardButton(text="Change the group", callback_data=f"change_group")
        keyboard.add(button_lesson, button_change_group)
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
    # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'days')
def choose_days_callback(call):
    keyboard = types.InlineKeyboardMarkup()
    for day in days:
        button_day = types.InlineKeyboardButton(text=day.capitalize(), callback_data=f"day_{day}")
        keyboard.add(button_day)
    bot.send_message(call.message.chat.id, 'Choose a day:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
def choose_day_callback(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    day = call.data.split('_')[1]
    result = get_schedule_for_group(group, day)
    bot.send_message(call.message.chat.id, f'{result}')
    bot.send_message(call.message.chat.id, 'Press /schedule to use bot again.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('week'))
def choose_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    result = get_schedule_for_group(group, "week")
    bot.send_message(call.message.chat.id, f'{result}')
    bot.send_message(call.message.chat.id,'Press /schedule to use bot again.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('lesson'))
def choose_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    result = get_lesson(group)
    bot.send_message(call.message.chat.id, f'{result}')
    bot.send_message(call.message.chat.id,'Press /schedule to use bot again.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_group'))
def change_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    if user in users:
        del users[user]
        record_push('users.json', users)
        bot.send_message(call.message.chat.id, 'Your group has been deleted. Choose another one:\n')
        get_group(call.message)
    else:
        bot.send_message(call.message.chat.id, 'You don\'t have a group to delete. Choose one:\n')
        get_group(call.message)
    
if __name__ == '__main__':
    bot.infinity_polling()
