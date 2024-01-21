from datetime import datetime, timedelta
import json

def split_time(time_range):
    start_time, end_time = time_range.split('-')
    return start_time.strip(), end_time.strip()

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
        result = ""
        for day, lessons in week["days"].items():
            if group in lessons:
                result += f"{day.capitalize()}:\n\n"
                for lesson in lessons[group]:
                    if lesson["lesson"] == "LUNCH-TIME":
                        result += f"Lunch at {lesson['time']}\n\n"
                    elif lesson['lesson'] == "ELECTIVES":
                        result += f"Electives:"
                        for elective in lesson['electives']:
                            result += f"\n{elective}"
                        result += f"\nTime: {lesson['time']}\n\n"
                    elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
                        result += f"Languages:"
                        for elective in lesson['electives']:
                            result += f"\n{elective}"
                        result += f"\nTime: {lesson['time']}\n\n"
                    else:
                        result += f"Lesson: {lesson['lesson']}\nAudience: {lesson['audience']}\nTeacher: {lesson['teacher']}\nTime: {lesson['time']}\n\n"
            result += '\n'
        return result                
    if day == 'today':
        today = datetime.now().strftime('%A').lower()
        if today == 'sunday':
            return 'Today is a sunday, you dont have any lessons'
    else:
        today = day
    if group not in week["days"][today]:
        return "Your group doesn't any lessons on this day"
    result = ''
    for lesson in week['days'][today][group]:
        if lesson["lesson"] == "LUNCH-TIME":
            result += f"Lunch at {lesson['time']}\n\n"
        elif lesson['lesson'] == "ELECTIVES":
            result += f"Electives:"
            for elective in lesson['electives']:
                result += f"\n{elective}"
            result += f"\nTime: {lesson['time']}\n\n"
        elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
            result += f"Languages:"
            for elective in lesson['electives']:
                result += f"\n{elective}"
            result += f"\nTime: {lesson['time']}\n\n"
        else:
            result += f"Lesson: {lesson['lesson']}\nAudience: {lesson['audience']}\nTeacher: {lesson['teacher']}\nTime: {lesson['time']}\n\n"
    return result
    

def time_to_minutes(time):
    hours = time.split(":")[0]
    minutes = time.split(':')[1]
    result = int(hours) * 60 + int(minutes)
    return result

def next_or_current_lesson_today(group):                    
    current_lesson = None
    next_lesson = None
    next_lesson_time = None
    now = datetime.strftime((datetime.now() + timedelta(hours=1)), '%H:%M')
    today_name = datetime.now().strftime("%A").lower()
    today_schedule = week["days"].get(today_name, {}).get(group, {})
    if not today_schedule:
        return None, None 
    
    for lesson in today_schedule:
        lesson_start = time_to_minutes(lesson["time"].split('-')[0].strip())
        lesson_end = time_to_minutes(lesson["time"].split('-')[1].strip())
        now_minutes = time_to_minutes(now)
        
        if lesson_start <= now_minutes <= lesson_end:
            current_lesson = lesson
        elif now_minutes <= lesson_start:
            if current_lesson is None or lesson_start < next_lesson_time or next_lesson_time is None:
                next_lesson = lesson
                next_lesson_time = lesson_start
    
    return current_lesson, next_lesson

def time_left(end_time, state):
    current_time = datetime.strftime(((datetime.now() + timedelta(hours=1)) + timedelta(minutes=2)), '%H:%M')
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
    if today == 'sunday':
        return 'Today is a sunday, you dont have any lessons'
    if current_lesson:
        if current_lesson['lesson'] == "LUNCH-TIME":
            return f"Your group is having a lunch! {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\nTime of lunch:{current_lesson['time']}"
        elif current_lesson['lesson'] == "ELECTIVES":
            result = f"Your electives is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\nTime: {current_lesson['time']}"
            for elective in current_lesson['electives']:
                result += f"\n{elective}"
            return result
        elif current_lesson['lesson'] == "LANGUAGE_ELECTIVES":
            result = f"Your language is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\nTime: {current_lesson['time']}"
            for elective in current_lesson['electives']:
                result += f"\n{elective}"
            return result
        else:
            return f"Your lesson is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\nLesson: {current_lesson['lesson']}\nAudience: {current_lesson['audience']}\nTeacher: {current_lesson['teacher']}\nTime: {current_lesson['time']}"
    elif next_lesson: 
        if next_lesson['lesson'] == "LUNCH-TIME": 
            return f"You're gonna have a lunch! {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\nTime of lunch: {next_lesson['time']}"
        elif next_lesson['lesson'] == "ELECTIVES":
            result = f"Your electives is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\nTime: {next_lesson['time']}"
            for elective in next_lesson['electives']:
                result += f"\n{elective}"
            return result
        elif next_lesson['lesson'] == "LANGUAGE_ELECTIVES":
            result = f"Your language is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\nTime: {next_lesson['time']}"
            for elective in next_lesson['electives']:
                result += f"\n{elective}"
            return result
        else:
            return f"Your next lesson is {next_lesson['lesson']}!:  {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\nAudience: {next_lesson['audience']}\nTeacher: {next_lesson['teacher']}\nTime: {next_lesson['time']}"
    else:
        return "Your group doesn't have any lessons for today or they already passed"

# print(get_lesson('COMSEP-23'))
# print(get_schedule_for_group('EEAIR-23', 'monday')) 

for lesson in week['groups']:
    print(lesson + '\n')