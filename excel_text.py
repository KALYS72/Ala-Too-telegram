import pandas as pd

# Загрузка данных из Excel-таблицы
excel_file_path = ''
df = pd.read_excel(excel_file_path)

# Создание структуры данных для JSON
schedule_data = {
    "university": "ALATOO INTERNATIONAL UNIVERSITY - DEPARTMENT OF COMPUTER SCIENCE",
    "semester": "2023-2024 SPRING SEMESTER",
    "schedule": "https://docs.google.com/spreadsheets/d/1jlJ6kG4FXChjH3a01dOmEX6BQ3i-QHeQzFgyjDup35o/edit#gid=1118793443",
    "groups": df['Group'].tolist(),
    "days": {}
}

# Заполнение расписания для каждой группы
for group in schedule_data["groups"]:
    group_schedule = df[df['Group'] == group]
    schedule_data["days"][group] = {}
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
        schedule_data["days"][group][day] = []

        # Добавление уроков для каждого дня
        for index, row in group_schedule.iterrows():
            lessons = row[day]
            if pd.notna(lessons):
                schedule_data["days"][group][day].append({
                    "lesson": lessons,
                    "time": row['Time'],
                    "audience": row['Audience'],
                    "teacher": row['Teacher']
                })

# Вывод в JSON-файл
output_json_file_path = 'расписание.json'
with open(output_json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(schedule_data, json_file, ensure_ascii=False, indent=2)

print(f"Расписание успешно преобразовано в JSON и сохранено в {output_json_file_path}")
