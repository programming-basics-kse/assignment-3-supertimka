import csv
import argparse
#argparse є подиви, воно працює
parser = argparse.ArgumentParser(description="Підрахунок медалей для заданої країни та року.")
parser.add_argument("file", help="Шлях до файлу athlete_events.csv!!!!!! <<<<<------ його назва, його юзай, не свое обезличенне")
parser.add_argument("-c", "--country", required=True, help="Код країни (наприклад, 'UKR')")
parser.add_argument("-y", "--year", required=True, help="Рік наприклад '2016'")
args = parser.parse_args()

#це перевірка моя
print("Отримані аргументи:")
print(f"Файл: {args.file}")
print(f"Країна: {args.country}")
print(f"Рік: {args.year}")

# Зчитування аргументів, див argparse
file_path = args.file
country = args.country
year = args.year

# Зчитування файлу, без коментарів
medal = []
try:
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            medal.append(row)
except FileNotFoundError:
    print(f"Файл {file_path} не знайдено. Перевірте шлях до файлу.")
    exit()

# Фільтрація за країною та роком, не питай
filtered_data = [
    row for row in medal
    if row["NOC"] == country and row["Year"] == year and row["Medal"] in ["Gold", "Silver", "Bronze"]
]

# Підрахунок медалей, не i in range чи щось таке просте с присобаченим a, бо в мене комп матюкається на цикли останнім часом, тому я ускладнила, бо грішила на них, а виявилося проблема в версії пайтона
medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
for row in filtered_data:
    medals[row["Medal"]] += 1
# перевір свою версію пайтона!!!!! напиши в терміналі python --version

# Виведення результатів
print(f"Медалі для країни {country} у {year} році:")
print(f"Золото: {medals['Gold']}")
print(f"Срібло: {medals['Silver']}")
print(f"Бронза: {medals['Bronze']}")
# перевірка через термінал там пишешь python3 Olympics.py athlete_events.csv -c UKR -y 2016
