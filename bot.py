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
The Telegram bot "Bot Name" is a convenient tool for students, providing instant access to class schedules. 

Commands:
<b>Days</b> - Displays the days of the week
<b>Week</b> - Displays the schedule for the whole week
<b>Next/Current lesson</b> - Shows the remaining time until the end of the lesson
<b>Today</b> - Schedule for current day
<b>Change the group</b> - Change the group
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
    bot.send_message(message.chat.id, f"{define_text}\n\nSchedule information:\n\nUniversity: {week['university']}\nSemester: {week['semester']}", reply_markup=keyboard, parse_mode="HTML")

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
    text='Your group has been deleted. Choose another one:\n'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)

def schedule_menu(message, user=None, back=None): 
    users = record_get("users.json")
    if not user:
        user = str(message.from_user.id)
    group = users[user]
    keyboard = types.InlineKeyboardMarkup()
    button_days = types.InlineKeyboardButton(text="Days", callback_data='days')
    button_today = types.InlineKeyboardButton(text="Today", callback_data='today')
    button_week = types.InlineKeyboardButton(text="Week", callback_data='week')
    button_lesson = types.InlineKeyboardButton(text="Next/Current lesson", callback_data='lesson')
    button_change_group = types.InlineKeyboardButton(text="Change the group", callback_data='change_group')
    keyboard.add(button_days, button_week)
    keyboard.add(button_today, button_lesson)
    keyboard.add(button_change_group)
    text = f'Your group is {group}!\nPlease choose an option:'
    if back:
        bot.edit_message_text(chat_id=back[0], message_id=back[1], text=text, reply_markup=keyboard)
    else :
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard, parse_mode="HTML")
    
@bot.message_handler(commands=['schedule'])
def schedule(message):
    users = record_get("users.json")
    user = str(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    if not user_exists(user, users):
        bot.send_message(message.chat.id, 'Looks like you haven\'t chosen your group yet. Let\'s choose one:\n', reply_markup=keyboard)
        get_group_with_elective(message)
    else:
        schedule_menu(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('back'))
def choose_group(call):
    schedule_menu(call.message, user=str(call.from_user.id), back=(call.message.chat.id, call.message.message_id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('group'))
def choose_group_callback(call):
    users = record_get("users.json")
    user = call.from_user.id
    group = call.data.split('_')[1]
    users[user] = group
    record_push("users.json", users)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('days'))
def choose_days_callback(call):
    keyboard = types.InlineKeyboardMarkup()  
    for day in week['days'].keys():
        button = types.InlineKeyboardButton(text=day.capitalize(), callback_data=f"day_{day}")
        keyboard.add(button)
    button_back = types.InlineKeyboardButton(text="<< Back to schedule", callback_data='back')
    keyboard.add(button_back)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Choose a day:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
def choose_day_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.message.message_id-1:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    day = call.data.split('_')[1]
    day_list = get_schedule_for_group(group, day)
    result = ''
    for day in day_list:
        result += day
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('today'))
def choose_group(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.message.message_id-1:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    today_list = get_schedule_for_group(group, 'today')
    result = ''
    for day in today_list:
        result += day
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('week'))
def choose_group(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.message.message_id-1:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    week_list = get_schedule_for_group(group, "week")
    result = ''
    for day in week_list:
        result += day
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('lesson'))
def choose_group(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.message.message_id-1:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]
    lesson_list = get_lesson(group)
    result = ''
    for day in lesson_list:
        result += day
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_group'))
def change_group(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    users = record_get("users.json")
    user = str(call.from_user.id)
    if user in users:
        del users[user]
        record_push('users.json', users)
        get_group_with_elective(call.message)
    else:
        bot.send_message(call.message.chat.id, 'You don\'t have a group to delete. Choose one:\n')
        get_group_with_elective(call.message)
    
if __name__ == '__main__':
    bot.infinity_polling()