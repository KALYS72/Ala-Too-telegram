from datetime import datetime, timedelta
import json

#TODO сделать кнопки одноразовыми
# сделать систему элективов


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
            return data
    except FileNotFoundError:
        data = {}
        return data
    
def record_push(file, data):
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)    # indent for better readability

week = record_get("source.json")

def get_schedule_for_group(group, day):                                         # получить расписание
    if day == 'week':
        result = []
        for today, lessons in week["days"].items():
            if group in lessons and len(week['days'][today][group]) != 0:
                result.append(f"{today.capitalize()}:\n\n")
                for lesson in lessons[group]:
                    if lesson["lesson"] == "LUNCH-TIME":
                        result.append(f"Lunch at {lesson['time']}\n\n")
                    elif lesson['lesson'] == "ELECTIVES":
                        result.append(f"Electives:")
                        for elective in lesson['electives']:
                            result.append(f"\n{elective}")
                        result.append(f"\nTime: {lesson['time']}\n\n")
                    elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
                        result.append(f"Languages:")
                        for elective in lesson['electives']:
                            result.append(f"\n{elective}")
                        result.append(f"\nTime: {lesson['time']}\n\n")
                    elif lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                        result.append(f"Department electives:")
                        for elective in lesson['electives']:
                            result.append(f"\n{elective}")
                        result.append(f"\nTime: {lesson['time']}\n\n")
                    else:
                        result.append(f"Lesson: {lesson['lesson']}\nAudience: {lesson['audience']}\nTeacher: {lesson['teacher']}\nTime: {lesson['time']}\n\n")
            result.append('\n\n')
        return result                
    result = []
    if day == 'today':
        today = datetime.now().strftime('%A').lower()
        if today == 'sunday':
            result.append('Today is a sunday, you dont have any lessons')
            return result
        elif "saturday" not in week['days'].keys() and today == "saturday":
            result.append('Today is a saturday, you dont have any lessons')
            return result
        result.append(f"Today is {today}:\n\n")
    else:
        today = day
    if group not in week["days"][today] or len(week['days'][today][group]) == 0:
        return f"Your group doesn't any lessons on {today}\n"
    for lesson in week['days'][today][group]:
        if lesson["lesson"] == "LUNCH-TIME":
            result.append(f"Lunch at {lesson['time']}\n\n")
        elif lesson['lesson'] == "ELECTIVES":
            result.append(f"Electives:")
            for elective in lesson['electives']:
                result.append(f"\n{elective}")
            result.append(f"\nTime: {lesson['time']}\n\n")
        elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
            result.append(f"Languages:")
            for elective in lesson['electives']:
                result.append(f"\n{elective}")
            result.append(f"\nTime: {lesson['time']}\n\n")
        elif lesson['lesson'] == "DEPARTMENT_ELECTIVE":
            result.append(f"Department electives:")
            for elective in lesson['electives']:
                result.append(f"\n{elective}")
            result.append(f"\nTime: {lesson['time']}\n\n")
        else:
            result.append(f"Lesson: {lesson['lesson']}\nAudience: {lesson['audience']}\nTeacher: {lesson['teacher']}\nTime: {lesson['time']}\n\n")
    return result
    

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
    for lesson in today_schedule:
        lesson_start = time_to_minutes(lesson["time"].split('-')[0].strip())
        lesson_end = time_to_minutes(lesson["time"].split('-')[1].strip())
        if lesson_start <= now_minutes <= lesson_end:
            current_lesson = lesson
        elif now_minutes < lesson_start:
            if (current_lesson is None and next_lesson_time is None) or (next_lesson_time is not None and lesson_start < next_lesson_time):
                next_lesson = lesson
                next_lesson_time = lesson_start
    return current_lesson, next_lesson

def time_left(end_time, state):
    current_time = datetime.strftime(datetime.now(), '%H:%M')
    end_time_datetime = datetime.strptime(end_time, "%H:%M")
    end_time_hour = datetime.strftime(end_time_datetime, "%H:%M")
    time_difference = time_to_minutes(end_time_hour) - time_to_minutes(current_time)
    hours, minutes = time_difference // 60, time_difference % 60
    if state == 'going_on':
        if hours == 0:
            return f"Time left until the end: {minutes} minutes"
        return f"Time left until the end: {hours} hours and {minutes} minutes"
    else:
        if hours == 0:
            return f"Time left until the start: {minutes} minutes"
        return f"Time left until the start: {hours} hours and {minutes} minutes"

def get_lesson(group):                                                              # получить текущий или следующий урок
    current_lesson, next_lesson = next_or_current_lesson_today(group)
    today = datetime.now().strftime("%A").lower()
    result = []
    if today == 'sunday':
        result.append('Today is a sunday, you dont have any lessons')
    if current_lesson:
        if current_lesson['lesson'] == "LUNCH-TIME":
            result.append("Your group is having a lunch! {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\nTime of lunch:{current_lesson['time']}")
        elif current_lesson['lesson'] == "ELECTIVES":
            result.append(f"Your electives is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n\nTime: {current_lesson['time']}")
            for elective in current_lesson['electives']:
                result.append(f"\n{elective}")
        elif current_lesson['lesson'] == "LANGUAGE_ELECTIVES":
            result.append(f"Your language is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n\nTime: {current_lesson['time']}")
            for elective in current_lesson['electives']:
                result.append(f"\n{elective}")
        elif current_lesson['lesson'] == "DEPARTMENT_ELECTIVE":
            result.append(f"Your department elective is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n\nTime: {current_lesson['time']}")
            for elective in current_lesson['electives']:
                result.append(f"\n{elective}")
        else:
            result.append(f"Your lesson is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n\nLesson: {current_lesson['lesson']}\nAudience: {current_lesson['audience']}\nTeacher: {current_lesson['teacher']}\nTime: {current_lesson['time']}")
    elif next_lesson: 
        if next_lesson['lesson'] == "LUNCH-TIME": 
            result.append(f"You're gonna have a lunch! {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\nTime of lunch: {next_lesson['time']}")
        elif next_lesson['lesson'] == "ELECTIVES":
            result.append(f"Your electives is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n\nTime: {next_lesson['time']}")
            for elective in next_lesson['electives']:
                result.append(f"\n{elective}")
        elif next_lesson['lesson'] == "LANGUAGE_ELECTIVES":
            result.append(f"Your language is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n\nTime: {next_lesson['time']}")
            for elective in next_lesson['electives']:
                result.append(f"\n{elective}")
        elif next_lesson['lesson'] == "DEPARTMENT_ELECTIVE":
            result.append(f"Your department elective is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n\nTime: {next_lesson['time']}")
            for elective in next_lesson['electives']:
                result.append(f"\n{elective}")
        else:
            result.append(f"Your next lesson is {next_lesson['lesson']}!:  {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n\nAudience: {next_lesson['audience']}\nTeacher: {next_lesson['teacher']}\nTime: {next_lesson['time']}")
    else:
        result.append("Your group doesn't have any lessons for today or they already passed")
    return result

# print(get_lesson('EEAIR-23'))
# print(get_schedule_for_group('EEAIR-23', 'monday')) 
# print(passed_or_not(week['days']['monday']['COMSEP-23'][0], 'lesson')