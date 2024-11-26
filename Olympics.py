import csv
import argparse

# argparse є подиви, воно працює
parser = argparse.ArgumentParser(description="Підрахунок медалей для заданої країни, року, або загального результату.")
parser.add_argument("file", help="Шлях до файлу athlete_events.csv!!! НЕ ЗАБУДЬ ПРАВИЛЬНУ НАЗВУ")
parser.add_argument("-c", "--country", help="Код країни (наприклад, 'UKR')")
parser.add_argument("-y", "--year", help="Рік (наприклад, '2016')")
# Завдання 2
parser.add_argument("-total", "--total", help="Вивести медалі всіх країн за рік.", action="store_true")
# Завдання 3
parser.add_argument("-overall", "--overall", nargs="+", help="Список країн найуспішніші роки.")
args = parser.parse_args()

# Це перевірка моя
print("Отримані аргументи:")
print(f"Файл: {args.file}")
if args.country:
    print(f"Країна: {args.country}")
if args.year:
    print(f"Рік: {args.year}")
if args.total:
    print("Режим -total активовано")
if args.overall:
    print(f"Режим -overall для країн: {', '.join(args.overall)}")

# Читаємо файл без коментарів
medal_data = []
try:
    with open(args.file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            medal_data.append(row)
except FileNotFoundError:
    print(f"Файл {args.file} не знайдено. Перевірте шлях до файлу.")
    exit()

# логіка для -total: вивести всі країни, медалі по 1 року
if args.total and args.year:
    countries_medals = {}

    # Фільтруємо дані
    filtered_data = [row for row in medal_data if row["Year"] == args.year and row["Medal"] in ["Gold", "Silver", "Bronze"]]

    # Рахуємо медалі по країнах
    for row in filtered_data:
        country = row["NOC"]
        medal = row["Medal"]
        if country not in countries_medals:
            countries_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
        countries_medals[country][medal] += 1

    # результат
    print(f"Медалі за {args.year} рік:")
    for country, counts in sorted(countries_medals.items()):
        print(f"{country} - Золото: {counts['Gold']}, Срібло: {counts['Silver']}, Бронза: {counts['Bronze']}")

# логіка для -c та -y: медалі для конкретної країни та року
elif args.country and args.year:
    filtered_data = [
        row for row in medal_data
        if row["NOC"] == args.country and row["Year"] == args.year and row["Medal"] in ["Gold", "Silver", "Bronze"]
    ]

    # Рахунок медалей
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for row in filtered_data:
        medals[row["Medal"]] += 1

    # Результат
    print(f"Медалі для країни {args.country} у {args.year} році:")
    print(f"Золото: {medals['Gold']}")
    print(f"Срібло: {medals['Silver']}")
    print(f"Бронза: {medals['Bronze']}")

# Логіка для -overall: найуспішніші роки для країн
elif args.overall:
    overall_results = {}

    for country in args.overall:
        country_data = [row for row in medal_data if row["NOC"] == country and row["Medal"] in ["Gold", "Silver", "Bronze"]]
        yearly_counts = {}

        # рахуємо медалі роки
        for row in country_data:
            year = row["Year"]
            if year not in yearly_counts:
                yearly_counts[year] = 0
            yearly_counts[year] += 1

        # найуспішніший рік
        if yearly_counts:
            best_year = max(yearly_counts, key=yearly_counts.get)
            overall_results[country] = (best_year, yearly_counts[best_year])

    # Результат
    print("Найуспішніші роки для заданих країн:")
    for country, result in overall_results.items():
        print(f"{country}: {result[0]} рік, {result[1]} медалей")

# якщо нічого не вибрано
else:
    print("Необхідно вказати правильні аргументи: -c/--country та -y/--year, або -total/-overall.")
