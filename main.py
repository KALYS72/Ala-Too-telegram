from datetime import datetime
from functions import record_get, next_or_current_lesson_today, time_left

week = record_get("source.json")
    
def get_schedule_for_group(group, day, user_electives):                                         # получить расписание
    if day == 'week':
        result = []
        for today, lessons in week["days"].items():
            day = []
            if group in lessons and len(week['days'][today][group]) != 0:
                day.append(f"{today.capitalize()}:\n\n")
                for lesson in lessons[group]:
                    if lesson["lesson"] == "LUNCH-TIME":
                        day.append(f"&#x1F37D <b>Lunch at {lesson['time']}</b>\n\n")
                    elif lesson['lesson'] == "ELECTIVES":
                        electives = []
                        user_elective_final = None
                        for elective in lesson['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')    
                            day.append(f"&#x1F4DA; Your elective:\n&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
                    elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
                        electives = []
                        user_elective_final = None
                        for elective in lesson['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')    
                            day.append(f"&#x1F1EC;&#x1F1E7; Your language:\n&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
                    elif lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                        electives = []
                        user_elective_final = None
                        for elective in lesson['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')    
                            day.append(f"&#x1F4DA; Your department elective:\n&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
                    else:
                        day.append(f"&#x1F4D6 {lesson['lesson']}\n&#x1F3E2 {lesson['audience']}\n&#x1F474;&#x1F3FB; {lesson['teacher']}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
            day.append('\n\n')
            result.append(day)
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
            user_elective_final = None
            for elective in lesson['electives']:
                electives.append(elective)
            for user_elective in user_electives:
                for elective in electives:
                    if user_elective in elective:
                        user_elective_final = elective
                        break
            if user_elective_final:
                elective_name, teacher, room = user_elective_final.split('/')    
                result.append(f"&#x1F4DA; Your elective:\n&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
        elif lesson['lesson'] == "LANGUAGE_ELECTIVES":
            electives = []
            user_elective_final = None
            for elective in lesson['electives']:
                electives.append(elective)
            for user_elective in user_electives:
                for elective in electives:
                    if user_elective in elective:
                        user_elective_final = elective
                        break
            if user_elective_final:
                elective_name, teacher, room = user_elective_final.split('/') 
                result.append(f"&#x1F1EC;&#x1F1E7; Your language:\n&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
        elif lesson['lesson'] == "DEPARTMENT_ELECTIVE":
            electives = []
            user_elective_final = None
            for elective in lesson['electives']:
                electives.append(elective)
            for user_elective in user_electives:
                for elective in electives:
                    if user_elective in elective:
                        user_elective_final = elective
                        break
            if user_elective_final:
                elective_name, teacher, room = user_elective_final.split('/') 
                result.append(f"&#x1F4DA; Your Department Elective:\n&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
        else:
            result.append(f"&#x1F4D6 {lesson['lesson']}\n&#x1F3E2 {lesson['audience']}\n&#x1F474;&#x1F3FB; {lesson['teacher']}\n&#x1F552 <b>{lesson['time']}</b>\n\n")
    return result


def get_lesson(group, user_electives):                                                             
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
                        user_elective_final = None
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')
                            result.append(f"&#x1F4DA; You have an elective after the lunch:&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 {next_lesson_after_lunch['time']}\n")
                        else:
                            result.append(f'<b>There are electives going on, but none of them are yours!</b>') 
                    elif next_lesson_after_lunch['lesson'] == "LANGUAGE_ELECTIVES":
                        electives = []
                        user_elective_final = None
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')
                            result.append(f"&#x1F1EC;&#x1F1E7; You have the language after the lunch:&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 {next_lesson_after_lunch['time']}\n")
                        else:
                            result.append(f"<b>There are electives going on, but none of them are yours!</b>") 
                    elif next_lesson_after_lunch['lesson'] == "DEPARTMENT_ELECTIVE":
                        electives = []
                        user_elective_final = None
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')
                            result.append(f"&#x1F4DA; You have the department elective after the lunch:&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 {next_lesson_after_lunch['time']}\n")
                        else:
                            result.append(f"<b>There are electives going on, but none of them are yours!</b>") 
                    else:
                        result.append(f"\nLesson after lunch: {next_lesson_after_lunch['lesson']}\n&#x1F3E2 {next_lesson_after_lunch['audience']}\n&#x1F474;&#x1F3FB; {next_lesson_after_lunch['teacher']}\n&#x1F552  <b>{next_lesson_after_lunch['time']}</b>\n")
            elif current_lesson['lesson'] == "ELECTIVES":
                electives = []
                user_elective_final = None
                for elective in current_lesson['electives']:
                    electives.append(elective)
                for user_elective in user_electives:
                    for elective in electives:
                        if user_elective in elective:
                            user_elective_final = elective
                            break
                if user_elective_final:
                    elective_name, teacher, room = user_elective_final.split('/')
                    result.append(f"&#x1F4DA; Your electives are going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 Time: <b>{current_lesson['time']}</b>")
                else:
                    result.append(f"<b>There are electives going on, but none of them are yours!</b>")
            elif current_lesson['lesson'] == "LANGUAGE_ELECTIVES":
                electives = []
                user_elective_final = None
                for elective in current_lesson['electives']:
                    electives.append(elective)
                for user_elective in user_electives:
                    for elective in electives:
                        if user_elective in elective:
                            user_elective_final = elective
                            break
                if user_elective_final:
                    elective_name, teacher, room = user_elective_final.split('/')
                    result.append(f"&#x1F1EC;&#x1F1E7; Your language is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 Time: <b>{current_lesson['time']}</b>")
                else:
                    result.append('<b>There are electives going on, but none of them are yours!</b>')
            elif current_lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                electives = []
                user_elective_final = None
                for elective in current_lesson['electives']:
                    electives.append(elective)
                for user_elective in user_electives:
                    for elective in electives:
                        if user_elective in elective:
                            user_elective_final = elective
                            break
                if user_elective_final:
                    elective_name, teacher, room = user_elective_final.split('/')
                    result.append(f"&#x1F4DA; Your department elective is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 Time: <b>{current_lesson['time']}</b>")
                else:
                    result.append(f"<b>There are electives going on, but none of them are yours!</b>")
            else:
                result.append(f"&#x1F4DA; Your lesson is going on!: {time_left(current_lesson['time'].split('-')[1].strip(), 'going_on')}\n\n&#x1F4D6 {current_lesson['lesson']}\n&#x1F3E2 {current_lesson['audience']}\n&#x1F474;&#x1F3FB; {current_lesson['teacher']}\n&#x1F552 <b>{current_lesson['time']}</b>")
        elif next_lesson: 
            if next_lesson['lesson'] == "LUNCH-TIME": 
                result.append(f"&#x1F37D  You're gonna have a lunch! {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n&#x1F552 <b> Lunch: {next_lesson['time']}</b>")
                if id + 1 <= len(week['days'][today][group]):
                    next_lesson_after_lunch = week['days'][today][group][id+1]
                    if next_lesson_after_lunch['lesson'] == "ELECTIVES":
                        electives = []
                        user_elective_final = None
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')
                            result.append(f"&#x1F4DA; You have an elective after the lunch:&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{next_lesson_after_lunch['time']}</b>")
                        else:
                            result.append(f'<b>There are electives going on, but none of them are yours!</b>')
                    elif next_lesson_after_lunch['lesson'] == "LANGUAGE_ELECTIVES":
                        electives = []
                        user_elective_final = None
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')
                            result.append(f"&#x1F1EC;&#x1F1E7; You have the language after the lunch:&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{next_lesson_after_lunch['time']}</b>")
                        else:
                            result.append(f'<b>There are electives going on, but none of them are yours!</b>')
                    elif next_lesson_after_lunch['lesson'] == "DEPARTMENT_ELECTIVE":
                        electives = []
                        user_elective_final = None
                        for elective in next_lesson_after_lunch['electives']:
                            electives.append(elective)
                        for user_elective in user_electives:
                            for elective in electives:
                                if user_elective in elective:
                                    user_elective_final = elective
                                    break
                        if user_elective_final:
                            elective_name, teacher, room = user_elective_final.split('/')
                            result.append(f"&#x1F4DA; You have the department elective after the lunch:&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 <b>{next_lesson_after_lunch['time']}</b>")
                        else:
                            result.append(f"<b>There are electives going on, but none of them are yours!</b>")
                    else:
                        result.append(f"\n&#x1F4DA; Lesson after lunch: {next_lesson_after_lunch['lesson']}\n&#x1F3E2 {next_lesson_after_lunch['audience']}\n&#x1F474;&#x1F3FB; {next_lesson_after_lunch['teacher']}\n&#x1F552  <b>{next_lesson_after_lunch['time']}</b>")
                else:
                    result.append("<b>There's no lessons after lunch, you can go home</b>")
                    return result
            elif next_lesson['lesson'] == "ELECTIVES":
                electives = []
                user_elective_final = None
                for elective in next_lesson['electives']:
                    electives.append(elective)
                for user_elective in user_electives:
                    for elective in electives:
                        if user_elective in elective:
                            user_elective_final = elective
                            break
                if user_elective_final:
                    elective_name, teacher, room = user_elective_final.split('/')
                    result.append(f"&#x1F4DA; Your elective is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 {next_lesson['time']}</b>")
                else:
                    result.append(f"<b>There are electives going on, but none of them are yours!</b>")
            elif next_lesson['lesson'] == "LANGUAGE_ELECTIVES":
                electives = []
                user_elective_final = None
                for elective in next_lesson['electives']:
                    electives.append(elective)
                for user_elective in user_electives:
                    for elective in electives:
                        if user_elective in elective:
                            user_elective_final = elective
                            break
                if user_elective_final:
                    elective_name, teacher, room = user_elective_final.split('/')
                    result.append(f"&#x1F1EC;&#x1F1E7; Your language is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 {next_lesson['time']}</b>")
                else:
                    result.append(f"<b>There are electives going on, but none of them are yours!</b>")
            elif next_lesson['lesson'] == "DEPARTMENT_ELECTIVE":
                electives = []
                user_elective_final = None
                for elective in next_lesson['electives']:
                    electives.append(elective)
                for user_elective in user_electives:
                    for elective in electives:
                        if user_elective in elective:
                            user_elective_final = elective
                            break
                if user_elective_final:
                    elective_name, teacher, room = user_elective_final.split('/')
                    result.append(f"&#x1F4DA; Your department elective is gonna start!: {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}&#x1F4D6 {elective_name}\n&#x1F3E2{room}\n&#x1F474;&#x1F3FB;{teacher}\n&#x1F552 {next_lesson['time']}</b>")
                else:
                    result.append(f"<b>There are electives going on, but none of them are yours!</b>")
            else:
                result.append(f"&#x1F4DA; Your next lesson is {next_lesson['lesson']}!:  {time_left(next_lesson['time'].split('-')[0].strip(), 'next')}\n\n&#x1F3E2 {next_lesson['audience']}\n&#x1F474;&#x1F3FB; {next_lesson['teacher']}\n&#x1F552 <b>{next_lesson['time']}</b>")
        else:
            result.append("<b>Your group doesn't have any lessons for today or they already passed</b>")
        return result
    return ["<b>Your group doesn't have any lessons for today</b>"]

# print(get_lesson('EEAIR-23', ['English']))
# get_schedule_for_group('EEAIR-23', 'week', ['Philosophy'])
# print(passed_or_not(week['days']['monday']['COMSEP-23'][0], 'lesson')