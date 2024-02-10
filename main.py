from datetime import datetime, timedelta
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
# def passed_or_not(type, day=None, group=None):
#     if type == "lesson":
#         current_time = time_to_minutes(datetime.strftime(((datetime.now() + timedelta(hours=1)) + timedelta(minutes=2)), '%H:%M'))
#         lesson_start = time_to_minutes(week['days']['monday']['COMSEP-23'][0]["time"].split('-')[0].strip())
#         lesson_end = time_to_minutes(week['days']['monday']['COMSEP-23'][0]["time"].split('-')[1].strip())
#         if current_time < lesson_start:
#             return "not_started"
#         elif current_time > lesson_end:
#             return "passed"
#         return "going on"
#     elif type == "day":
#         today_number = today_number(datetime.now().strftime("%A").lower())
#         day_number = 

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
    for day in today_list:
        result += day
    return result
    
def get_schedule_for_group(group, day):                                         # получить расписание
    if day == 'week':
        result = []
        for today, lessons in week["days"].items():
            if group in lessons and len(week['days'][today][group]) != 0:
                result.append(f"{today.capitalize()}:\n\n")
                for lesson in lessons[group]:
                    if lesson["lesson"] == "LUNCH-TIME":
                        result.append(f"&#x1F37D <b>Lunch at {lesson['time']}</b>\n\n")
                    elif lesson['lesson'] == "ELECTIVES":
                        electives = []
                        elective_string = ''
                        for elective in lesson['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F4DA;  Electives:{elective_string}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
                    elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
                        electives = []
                        elective_string = ''
                        for elective in lesson['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F1EC;&#x1F1E7;  Languages:{elective_string}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
                    elif lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                        electives = []
                        elective_string = ''
                        for elective in lesson['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F4DA;  Department Electives:{elective_string}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
                    else:
                        result.append(f"&#x1F4D6 {lesson['lesson']}\n&#x1F3E2 {lesson['audience']}\n&#x1F474;&#x1F3FB; {lesson['teacher']}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
            result.append('\n\n')
        return result                
    result = []
    if day == 'today':
        today = datetime.now().strftime('%A').lower()
        if today == 'sunday':
            return ['<b>Today is a sunday, you dont have any lessons</b>']
        elif "saturday" not in week['days'].keys() and today == "saturday":
            return ['<b>Today is a saturday, you dont have any lessons</b>']
        result.append(f"Today is {today.capitalize()}:\n\n")
    else:
        today = day
    if group not in week["days"][today] or len(week['days'][today][group]) == 0:
        return [f"<b>Your group doesn't have any lessons on {today}</b>\n"]
    for lesson in week['days'][today][group]:
        if lesson["lesson"] == "LUNCH-TIME":
            result.append(f"&#x1F37D <b>Lunch at {lesson['time']}</b>\n\n")
        elif lesson['lesson'] == "ELECTIVES":
            electives = []
            elective_string = ''
            for elective in lesson['electives']:
                electives.append(f"\n{elective}")
                elective_string += f"\n{elective}"
            result.append(f"&#x1F4DA;  Electives:{elective_string}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
        elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
            electives = []
            elective_string = ''
            for elective in lesson['electives']:
                electives.append(f"\n{elective}")
                elective_string += f"\n{elective}"
            result.append(f"&#x1F1EC;&#x1F1E7;  Languages:{elective_string}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
        elif lesson['lesson'] == "DEPARTMENT_ELECTIVE":
            electives = []
            elective_string = ''
            for elective in lesson['electives']:
                electives.append(f"\n{elective}")
                elective_string += f"\n{elective}"
            result.append(f"&#x1F4DA;  Department Electives:{elective_string}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
        else:
            result.append(f"&#x1F4D6 {lesson['lesson']}\n&#x1F3E2 {lesson['audience']}\n&#x1F474;&#x1F3FB; {lesson['teacher']}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
    return result

def get_lesson(group):                                                             
    today = datetime.now().strftime("%A").lower()
    if today == 'sunday':
            return ['<b>Today is a sunday, you dont have any lessons</b>']
    elif "saturday" not in week['days'].keys() and today == "saturday":
        return ['<b>Today is a saturday, you dont have any lessons</b>']
    elif len(week['days'][today][group]) != 0:
        current_lesson, next_lesson, today, group, id = next_or_current_lesson_today(group) 
        result = []
        if current_lesson:
            if current_lesson['lesson'] == "LUNCH-TIME":
                result.append(f"&#x1F37D  Your group is having a lunch! {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n&#x1F552  Lunch time: <b>{current_lesson['time']}</b>\n\n")
                if id + 1 < len(week['days'][today][group]):
                    next_lesson_after_lunch = week['days'][today][group][id+1]
                    if next_lesson_after_lunch['lesson'] == "ELECTIVES":
                        electives = []
                        elective_string = ''
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F4DA;  You have electives after the lunch:{elective_string}\n&#x1F552 {next_lesson_after_lunch['time']}\n")
                    elif next_lesson_after_lunch['lesson'] == "LANGUAGE_ELECTIVES":
                        electives = []
                        elective_string = ''
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F1EC;&#x1F1E7;  You have the language after the lunch:{elective_string}\n&#x1F552 {next_lesson_after_lunch['time']}\n")
                    elif next_lesson_after_lunch['lesson'] == "DEPARTMENT_ELECTIVE":
                        electives = []
                        elective_string = ''
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F4DA;  You have the department elective after the lunch:{elective_string}\n&#x1F552 {next_lesson_after_lunch['time']}\n")
                    else:
                        result.append(f"\n<code> Lesson after lunch: {next_lesson_after_lunch['lesson']}\n&#x1F3E2 {next_lesson_after_lunch['audience']}\n&#x1F474;&#x1F3FB; {next_lesson_after_lunch['teacher']}\n&#x1F552  <b>{next_lesson_after_lunch['time']}</b>\n")
            elif current_lesson['lesson'] == "ELECTIVES":
                electives = []
                elective_string = ''
                for elective in current_lesson['electives']:
                    electives.append(f"\n{elective}")
                    elective_string += f"\n{elective}"
                result.append(f"&#x1F4DA;  Your electives are going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}{elective_string}\n&#x1F552 Time: <b>{current_lesson['time']}</b>")
            elif current_lesson['lesson'] == "LANGUAGE_ELECTIVES":
                electives = []
                elective_string = ''
                for elective in current_lesson['electives']:
                    electives.append(f"\n{elective}")
                    elective_string += f"\n{elective}"
                result.append(f"&#x1F1EC;&#x1F1E7;  Your language is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}{elective_string}\n&#x1F552 Time: <b>{current_lesson['time']}</b>")
            elif current_lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                electives = []
                elective_string = ''
                for elective in current_lesson['electives']:
                    electives.append(f"\n{elective}")
                    elective_string += f"\n{elective}"
                result.append(f"&#x1F4DA;  Your department elective is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}{elective_string}\n&#x1F552 Time: <b>{current_lesson['time']}</b>")
            else:
                result.append(f"&#x1F4DA;  Your lesson is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n\n&#x1F4D6 {current_lesson['lesson']}\n&#x1F3E2 {current_lesson['audience']}\n&#x1F474;&#x1F3FB; {current_lesson['teacher']}\n&#x1F552  <b>{current_lesson['time']}</b>")
        elif next_lesson: 
            if next_lesson['lesson'] == "LUNCH-TIME": 
                result.append(f"&#x1F37D  You're gonna have a lunch! {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n&#x1F552 <b> Lunch: {next_lesson['time']}</b>")
                if id + 1 <= len(week['days'][today][group]):
                    next_lesson_after_lunch = week['days'][today][group][id+1]
                    if next_lesson_after_lunch['lesson'] == "ELECTIVES":
                        electives = []
                        elective_string = ''
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F4DA;  You have the electives after the lunch:{elective_string}\n&#x1F552 <b>{next_lesson_after_lunch['time']}</b>")
                    elif next_lesson_after_lunch['lesson'] == "LANGUAGE_ELECTIVES":
                        electives = []
                        elective_string = ''
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F1EC;&#x1F1E7;  You have the language after the lunch:{elective_string}\n&#x1F552 <b>{next_lesson_after_lunch['time']}</b>")
                    elif next_lesson_after_lunch['lesson'] == "DEPARTMENT_ELECTIVE":
                        electives = []
                        elective_string = ''
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(f"\n{elective}")
                            elective_string += f"\n{elective}"
                        result.append(f"&#x1F4DA;  You have the department elective after the lunch:{elective_string}\n&#x1F552 <b>{next_lesson_after_lunch['time']}</b>")
                    else:
                        result.append(f"\n&#x1F4DA;  Lesson after lunch: {next_lesson_after_lunch['lesson']}\n&#x1F3E2 {next_lesson_after_lunch['audience']}\n&#x1F474;&#x1F3FB; {next_lesson_after_lunch['teacher']}\n&#x1F552  <b>{next_lesson_after_lunch['time']}</b>")
                else:
                    result.append("<b>There's no lessons after lunch, you can go home</b>")
                    return result
            elif next_lesson['lesson'] == "ELECTIVES":
                electives = []
                elective_string = ''
                for elective in next_lesson['electives']:
                    electives.append(f"\n{elective}")
                    elective_string += f"\n{elective}"
                result.append(f"&#x1F4DA;  Your elective is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}{elective_string}\n&#x1F552 {next_lesson['time']}</b>")
            elif next_lesson['lesson'] == "LANGUAGE_ELECTIVES":
                result.append(f"&#x1F1EC;&#x1F1E7;  Your language is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}{elective_string}\n&#x1F552 {next_lesson['time']}</b>")
                electives = []
                elective_string = ''
                for elective in next_lesson['electives']:
                    electives.append(f"\n{elective}")
                    elective_string += f"\n{elective}"
            elif next_lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                electives = []
                elective_string = ''
                for elective in next_lesson['electives']:
                    electives.append(f"\n{elective}")
                    elective_string += f"\n{elective}"
                result.append(f"&#x1F4DA;  Your department elective is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}{elective_string}\n&#x1F552 {next_lesson['time']}</b>")
            else:
                result.append(f"&#x1F4DA;  Your next lesson is {next_lesson['lesson']}!:  {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n\n&#x1F3E2 {next_lesson['audience']}\n&#x1F474;&#x1F3FB; {next_lesson['teacher']}\n&#x1F552  <b>{next_lesson['time']}</b>")
        else:
            result.append("<b>Your group doesn't have any lessons for today or they already passed</b>")
        return result
    return ["<b>Your group doesn't have any lessons for today</b>"]

# print(get_lesson('COM-21a'))
# print(get_schedule_for_group('EEAIR-23', 'week')) 
# print(passed_or_not(week['days']['monday']['COMSEP-23'][0], 'lesson')