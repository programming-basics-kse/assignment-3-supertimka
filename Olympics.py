with open("data.csv", "rt") as file:
    next(file)
    contents = file.readlines()
    for line in contents:
        line = line[:-1]
        split = line.split('\t')
        medal = split[-1]
        names = split[1]
        countrys_split = split[6]
        years = split[9]
        sports = split[12]

country = input(f"olympics.py data.csv -medals")
year = input(f"olympics.py data.csv -medals {country}")

country_list = []
if country in countrys_split:
    country_list[country].append((names, sports, medal))
year_list = []
if year in countrys_split:
    year_list[year].append((names, sports, medal))

medals={
    "Gold": 0,
    "Silver": 0,
    "Bronze": 0
}
for medal in year_list:
    if year_list[medal] in medals:
        medals[year_list[medal]] += 1

