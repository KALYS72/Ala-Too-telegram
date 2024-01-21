ef next_or_current_lesson_today(group):
    now = datetime.strftime((datetime.now() + timedelta(hours=1)), '%H:%M')
    today_name = datetime.now().strftime("%A").lower()
    today_schedule = week["days"].get(today_name, {}).get(group, {})
    
    if not today_schedule:
        return None, None 
    
    current_lesson = None
    next_lesson = None
    next_lesson_time = None
    
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
