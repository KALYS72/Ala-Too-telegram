from datetime import datetime
import json, os

def user_exists(user, file):
    if user in file.keys():
        return True
    return False

def day_number(day):
    day_mapping = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5
    }
    day_value = day_mapping.get(day)
    return day_value

def time_to_minutes(time):
    hours = time.split(":")[0]
    minutes = time.split(':')[1]
    result = int(hours) * 60 + int(minutes)
    return result
"""
    to identify wether lesson/day passed or not
"""

def record_get(file):
    try:
        with open(file, 'r') as json_file:
            data = json.load(json_file)
    except:
        with open(file, 'w') as json_file:
            data = {}
    return data
    
def record_push(file_path, data):
    if os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # indent for better readability
    else:
        print(f"Error: File '{file_path}' not found.")

week = record_get("source.json")

def next_or_current_lesson_today(group):
    current_lesson = None
    next_lesson = None
    next_lesson_time = None
    now = datetime.strftime(datetime.now(), '%H:%M')
    today_name = datetime.now().strftime("%A").lower()
    today_schedule = week["days"].get(today_name, {}).get(group, {})
    now_minutes = time_to_minutes(now)

    if not today_schedule:
        return None, None 
    lesson_key = 0
    lesson_id = 0
    for lesson in today_schedule:
        lesson_start = time_to_minutes(lesson["time"].split('-')[0].strip())
        lesson_end = time_to_minutes(lesson["time"].split('-')[1].strip())
        if lesson_start <= now_minutes <= lesson_end:
            current_lesson = lesson
            lesson_id = lesson_key
        elif now_minutes < lesson_start:
            if (current_lesson is None and next_lesson_time is None) or (next_lesson_time is not None and lesson_start < next_lesson_time):
                next_lesson = lesson
                next_lesson_time = lesson_start
                lesson_id = lesson_key
        lesson_key += 1
    return current_lesson, next_lesson, today_name, group, lesson_id

def time_left(end_time, state):
    current_time = datetime.strftime(datetime.now(), '%H:%M')
    end_time_datetime = datetime.strptime(end_time, "%H:%M")
    end_time_hour = datetime.strftime(end_time_datetime, "%H:%M")
    time_difference = time_to_minutes(end_time_hour) - time_to_minutes(current_time)
    hours, minutes = time_difference // 60, time_difference % 60
    if state == 'going_on':
        if hours == 0:
            return f"Time left until the end:  <b>{minutes} minutes</b>"
        return f"Time left until the end:  <b>{hours} hours and {minutes} minutes</b>"
    else:
        if hours == 0:
            return f"Time left until the start:  <b>{minutes} minutes</b>"
        return f"Time left until the start: <b>{hours} hours and {minutes} minutes</b>"
    
def sort_today(today_list):
    result = '' 
    for lesson in today_list:    
        if 'Lunch' in lesson:
            if lesson != today_list[-1]:
                result += lesson
        else:
            result += lesson
    return result