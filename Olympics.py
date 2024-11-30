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
# Завдання 4
parser.add_argument("-interactive","--interactive", help="Статистика для країни", action="store_true")
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
if args.interactive:
    print(f"Статистика для {args.country}:")

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
       result_overall = print(f"{country}: {result[0]} рік, {result[1]} медалей")

# Логіка для -interactive
elif args.interactive:
    while True:
        country_question = input("Введіть країну або код для виведення її статистики:")
        country_data = [row for row["NOC"] in medal_data if row["NOC"] == country_question]

        # перша олімпіада
        first_game = min(country_data, key=lambda x: int(x["Year"]))
        first_game_year = first_game["Year"]
        first_game_place = first_game["City"]

        # найуспішніший і найневдаліший рік( з overall)
        bestyear_results = {}
        worstyear_results = {}
        for country_question in args.overall:
            country_data = [row for row in medal_data if row["NOC"] == country_question and row["Medal"] in ["Gold", "Silver", "Bronze"]]
            yearly_counts = {}
            # рахуємо медалі роки
            for row in country_data:
                year = row["Year"]
                if year not in yearly_counts:
                    yearly_counts[year] = 0
                yearly_counts[year] += 1
            # найуспішніший рік і найневдаліший рік
            if yearly_counts:
                best_year = max(yearly_counts, key=yearly_counts.get)
                bestyear_results[country_question] = (best_year, yearly_counts[best_year])
                worst_year = min(yearly_counts, key=yearly_counts.get)
                worstyear_results[country_question] = (worst_year, yearly_counts[worst_year])
            # середня кількість медалей
            year_medals = {}
            filtered_data = [row for row in medal_data if
                             row["Year"] == args.year and row["Medal"] in ["Gold", "Silver", "Bronze"]]

            for row in filtered_data:
                city = row["City"]
                medal = row["Medal"]
                if city not in year_medals:
                    year_medals[city] = {"Gold": 0, "Silver": 0, "Bronze": 0}
                year_medals[city][medal] += 1
            total_medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
            for city, counts in year_medals.items():
                for medal in total_medals:
                    total_medals[medal] += counts[medal]
            number_years = len(year_medals)
            if number_years > 0:
                average_medals = {medal: total / number_years for medal, total in total_medals.items()}

        # результат
        print(f"Перша олімпіада в якій брала участь {country_question}: {first_game_year} рік, місто {first_game_place}.")
        print(f"Найуспісніша олімпіада:{bestyear_results}")
        print(f"Найневдаліша олімпіада:{worstyear_results}")
        print(f"Середня кількість медалей кожну олімпіаду:{average_medals}")
# якщо нічого не вибрано
else:
    print("Необхідно вказати правильні аргументи: -c/--country та -y/--year, або -total/-overall.")



