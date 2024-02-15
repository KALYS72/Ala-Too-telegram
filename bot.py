from decouple import config
from telebot import types
import telebot
from functions import record_get, record_push, user_exists, sort_today
from main import get_schedule_for_group, get_lesson

week = record_get("source.json")
reviews = record_get('reviews.json')
token = config("TOKEN")
bot =  telebot.TeleBot(token)
user_electives={}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 
        'Hello, I am a bot that will help you to know where you are supposed to be at a particular time!\n\nCommands:\n\n/info - information about bot and Ala-too\n/schedule - begin to work with a bot!'
    )
    review_message = bot.send_message(message.chat.id, '/review - Please leave your review if:\n-Something goes wrong\n-You have some idea to improve this bot')
    bot.pin_chat_message(message.chat.id, review_message.id)

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


@bot.message_handler(commands=['review'])
def start_review(message):
    bot.send_message(message.chat.id, "Please leave your review: ")
    bot.register_next_step_handler(message, process_review)

def process_review(message):
    review_text = message.text
    user_id = str(message.from_user.id)
    reviews = record_get('reviews.json')
    if user_id in reviews:
        reviews[user_id].append(review_text)
    else:
        reviews[user_id] = [review_text]
    record_push('reviews.json', reviews)
    bot.send_message(message.chat.id, "Thank you for your review!\n\nCommands:\n\n/start - get back to menu\n/info - information about bot and Ala-too\n/schedule - begin to work with a bot!")

def get_groups(message, back=None):
    week = record_get("source.json")
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
    if back:
        bot.edit_message_text(chat_id=back[0], message_id=back[1], text=text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)

def get_electives(message, user, group, back=None, electives=[], again=False):
    week = record_get("source.json")
    keyboard = types.InlineKeyboardMarkup()
    count = []
    for elective in week['electives']:
        if elective not in electives:
            button = types.InlineKeyboardButton(text=elective, callback_data=f"elective_{elective}")
            count.append(button)
        if len(count) == 2:
            keyboard.add(count[0], count[1])
            count = []
    if len(count) == 1:
        keyboard.add(count[0])
    text='Choose electives from your programm:\n'
    if back:
        bot.edit_message_text(chat_id=back[0], message_id=back[1], text=text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)
    new_keyboard = types.InlineKeyboardMarkup()
    elective_list = []
    try:
        elective_list = user_electives[user]
    except KeyError:
        user_electives[user] = elective_list
    text = f"Chosen group: {group}\nChosen electives:\n"
    for elective in elective_list:
        text += f'{elective}\n' 
    back_button = types.InlineKeyboardButton(text="Reset", callback_data=f"change_group_{user}")
    submit_button = types.InlineKeyboardButton(text="Submit", callback_data="confirm")
    new_keyboard.add(back_button, submit_button)
    if again:
        bot.edit_message_text(chat_id=back[0], message_id=back[1]+1, text=text, reply_markup=new_keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=new_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
def choose_group_callback(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = call.data.split('_')[1]
    if user not in users:
        users[user] = {'electives':[]}
    users[user]['group'] = group
    record_push("users.json", users)
    get_electives(call.message, back=(call.message.chat.id, call.message.message_id), user=user, group=group)

@bot.callback_query_handler(func=lambda call: call.data.startswith('elective_'))
def choose_elective_callback(call):
    user = str(call.from_user.id)
    elective = call.data.split('_')[1]
    if user in user_electives:
        user_electives[user].append(elective)
    else:
        user_electives[user] = [elective]
    users = record_get("users.json")
    group = users[user]['group']
    get_electives(call.message, user=user, group=group, back=(call.message.chat.id, call.message.message_id), electives=user_electives[user], again=True)

@bot.message_handler(commands=['schedule'])
def schedule(message):
    users = record_get("users.json")
    user = str(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    if not user_exists(user, users):
        bot.send_message(message.chat.id, 'Looks like you haven\'t chosen your group yet. Let\'s choose one:\n', reply_markup=keyboard)
        get_groups(message)
    else:
        schedule_menu(message)

def schedule_menu(message, user=None, back=None): 
    users = record_get("users.json")
    if not user:
        user = str(message.from_user.id)
    group = users[user]['group']
    keyboard = types.InlineKeyboardMarkup()
    button_days = types.InlineKeyboardButton(text="Days", callback_data='days')
    button_today = types.InlineKeyboardButton(text="Today", callback_data='today')
    button_week = types.InlineKeyboardButton(text="Week", callback_data='week')
    button_lesson = types.InlineKeyboardButton(text="Next/Current lesson", callback_data='lesson')
    button_change_group = types.InlineKeyboardButton(text="Change a group with electives", callback_data='change_group')
    keyboard.add(button_days, button_week)
    keyboard.add(button_today, button_lesson)
    keyboard.add(button_change_group)
    electives = ''
    for elective in users[user]['electives']:
        if elective != users[user]['electives'][-1]:
            electives += f'{elective}, '
        else:
            electives += f'{elective}'
    text = f'Your group is {group}!\nYour Electives: {electives}\n\nPlease choose an option:'
    if back:
        bot.edit_message_text(chat_id=back[0], message_id=back[1], text=text, reply_markup=keyboard, parse_mode="HTML")
    else :
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith('back'))
def back(call):
    schedule_menu(call.message, user=str(call.from_user.id), back=(call.message.chat.id, call.message.message_id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm'))
def confirm(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    elective_list = user_electives[user]
    users[user]['electives'] = elective_list
    record_push("users.json", users)
    del user_electives[user]
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    except:
        print('confirm')
    schedule_menu(call.message, user=str(call.from_user.id), back=(call.message.chat.id, call.message.message_id))


@bot.callback_query_handler(func=lambda call: call.data.startswith('days'))
def choose_days(call):
    week = record_get("source.json")
    keyboard = types.InlineKeyboardMarkup()  
    for day in week['days'].keys():
        button = types.InlineKeyboardButton(text=day.capitalize(), callback_data=f"day_{day}")
        keyboard.add(button)
    button_back = types.InlineKeyboardButton(text="<< Back to schedule", callback_data='back')
    keyboard.add(button_back)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Choose a day:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
def choose_day_callback(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]['group']
    day = call.data.split('_')[1]
    user_electives = users[user]['electives']
    day_list = get_schedule_for_group(group, day, user_electives)
    result = ''
    if not day_list[0].startswith("Your group doesn't have any lessons on"):
        result += f'{day.capitalize()}:\n\n' 
    for lesson in day_list:    
        if 'Lunch' in lesson:
            if lesson != day_list[-1]:
                result += lesson
        else:
            result += lesson
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    except:
        print('day')
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('today'))
def today(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]['group']
    user_electives = users[user]['electives']
    today_list = get_schedule_for_group(group, 'today', user_electives)
    result = sort_today(today_list=today_list)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    except:
        print('today')
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('week'))
def week(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]['group']
    user_electives = users[user]['electives']
    week_list = get_schedule_for_group(group, "week", user_electives)
    result = '' 
    for day in week_list:
        for lesson in day:    
            if 'Lunch' in lesson:
                if lesson != day[-2]:
                    result += lesson
            else:
                result += lesson
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    except:
        print('week')
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('lesson'))
def lesson(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    group = users[user]['group']
    user_electives = users[user]['electives']
    lesson_list = get_lesson(group, user_electives)
    result = '' 
    for day in lesson_list:
        result += day
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    except:
        print('lesson')
    bot.send_message(chat_id=call.message.chat.id, text=result, parse_mode="HTML")
    schedule_menu(call.message, str(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_group'))
def change_group(call):
    users = record_get("users.json")
    user = str(call.from_user.id)
    if len(call.data.split('_')) > 2:
        check_user = call.data.split('_')[2]
        del user_electives[check_user]
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    except:
        print('change')
    if user in users:
        del users[user]
        record_push('users.json', users)
        get_groups(call.message, back=(call.message.chat.id, call.message.message_id))
    else:
        get_groups(call.message, back=(call.message.chat.id, call.message.message_id))
    
if __name__ == '__main__':
    bot.infinity_polling()