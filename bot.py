from decouple import config
from telebot import types
import telebot, json

from main import get_schedule

week = get_schedule()
token = config("TOKEN")
bot =  telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''Hello, I am a bot that will help you to know where you are supposed to be at a particular time!\n\nCommands:\n\n/info - information about bot and Ala-too\n/schedule - begin to work with a bot!\n''')

@bot.message_handler(commands=["info"])
def info(message):
    keyboard = types.InlineKeyboardMarkup()
    ala_too_website = types.InlineKeyboardButton(text="Info about Ala-Too", url='http://alatoo.edu.kg/#gsc.tab=0')
    schedule = types.InlineKeyboardButton(text="Original Schedule (access required)", url='https://docs.google.com/spreadsheets/d/1jlJ6kG4FXChjH3a01dOmEX6BQ3i-QHeQzFgyjDup35o/edit#gid=1118793443')
    keyboard.add(ala_too_website)
    keyboard.add(schedule)
    bot.send_message(message.chat.id, f"Schedule information:\n\nUniversity: {week['university']}\nSemester: {week['semester']}", reply_markup=keyboard)

@bot.message_handler(commands=['schedule'])
def main(message):
    keyboard = types.InlineKeyboardMarkup()
    for group in week['groups']:
        button = types.InlineKeyboardButton(text=group, callback_data=f'group_{group}')
        keyboard.add(button)

    bot.send_message(message.chat.id, 'Choose your group:\n', reply_markup=keyboard)

if __name__ == '__main__':
    bot.infinity_polling()