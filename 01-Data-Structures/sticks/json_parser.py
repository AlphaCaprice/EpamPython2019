import pprint
from time import clock
import json


# encoding="unicode-escape"
def dump_json_file(file_path, wines):
    data = {}
    with open(file_path, "r") as json_file:
        all_wine = json_file.read()[3:-2]
        all_wine = all_wine.replace("\n", "").split("}, {")
        for wine in all_wine:
            wine = wine.split(', "')
            for field in wine:
                field = field.split(": ", 1)
                field[0] = field[0].lstrip('"')
                data[f'"{field[0]}'] = field[1]

            wine_key = (data['"variety"'], data['"description"'],
                        data['"price"'] if data['"price"'] != 'null' else -1)
            wines[wine_key] = data.copy()


def load_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write("[\n")
        for elem in data:
            out_f.write("{")
            for key, value in elem[1].items():
                out_f.write(f"{key}: {value}, ")
            out_f.seek(out_f.tell() - 2)
            out_f.write("},\n")
        out_f.seek(out_f.tell() - 3)
        out_f.write("]\n")


def update_variety_stat(wine, variety, wine_stat):
    price = wine[1]['"price"']
    score = wine[1]['"points"'].replace('"', '')
    country = wine[1]['"country"'].replace('"', '')
    regions = (wine[1]['"region_1"'], wine[1]['"region_2"'])

    if not (price == 'null'):
        price = int(price)
        wine_stat[variety]["amount_with_price"] += 1
        wine_stat[variety]["average_price"] += price
        wine_stat[variety]["min_price"] = \
            min(wine_stat[variety]["min_price"], price)
        wine_stat[variety]["max_price"] = \
            max(wine_stat[variety]["max_price"], price)

    if not (score == 'null'):
        wine_stat[variety]["average_score"] += int(score)
        wine_stat[variety]["amount_with_score"] += 1

    if not (country == 'null'):
        if country in wine_stat[variety]["most_common_country"]:
            wine_stat[variety]["most_common_country"][country] += 1
        else:
            wine_stat[variety]["most_common_country"][country] = 1

    for region in regions:
        if not (region == 'null'):
            region = region.replace('"', '')
            if region in wine_stat[variety]["most_common_region"]:
                wine_stat[variety]["most_common_region"][region] += 1
            else:
                wine_stat[variety]["most_common_region"][region] = 1


def update_another_stat(wine, stat):
    country = wine[1]['"country"'].replace('"', '')
    title = wine[1]['"title"'].replace('"', '')
    price = wine[1]['"price"']
    score = wine[1]['"points"'].replace('"', '')
    commentator = (wine[1]['"taster_name"'].replace('"', ''))

    # most active commentator
    if not (commentator == 'null'):
        if commentator in stat["most_active_commentator"]:
            stat["most_active_commentator"][commentator] += 1
        else:
            stat["most_active_commentator"][commentator] = 1

    if not (score == 'null'):
        score = int(score)

        #  most rated country
        if country != 'null':
            if country in stat["country_counter_with_score"]:
                stat["country_counter_with_score"][country] += 1
                stat["most_rated_country"][country] += score
            else:
                stat["country_counter_with_score"][country] = 1
                stat["most_rated_country"][country] = score

        #  highest_score
        if stat["highest_score"]:
            if score > stat["highest_score"]["score"]:
                stat["highest_score"]["score"] = score
                stat["highest_score"]["wines"] = [title]
            elif score == stat["highest_score"]["score"]:
                stat["highest_score"]["wines"].append(title)
        else:
            stat["highest_score"]["score"] = score
            stat["highest_score"]["wines"] = [title]

        #  lowest_score
        if stat["lowest_score"]:
            if score < stat["lowest_score"]["score"]:
                stat["lowest_score"]["score"] = score
                stat["lowest_score"]["wines"] = [title]
            elif score == stat["lowest_score"]["score"]:
                stat["lowest_score"]["wines"].append(title)
        else:
            stat["lowest_score"]["score"] = score
            stat["lowest_score"]["wines"] = [title]

    if not (price == 'null'):
        price = int(price)
        #  most cheap and expensive country
        if country != 'null':
            if country in stat["country_counter_with_price"]:
                stat["country_counter_with_price"][country] += 1
                stat["most_expensive_country"][country] += price
            else:
                stat["country_counter_with_price"][country] = 1
                stat["most_expensive_country"][country] = price

        # most expensive wine
        if stat["most_expensive_wine"]:
            if price > stat["most_expensive_wine"]["price"]:
                stat["most_expensive_wine"]["price"] = price
                stat["most_expensive_wine"]["wines"] = [title]
            elif price == stat["most_expensive_wine"]["price"]:
                stat["most_expensive_wine"]["wines"].append(title)
        else:
            stat["most_expensive_wine"]["price"] = price
            stat["most_expensive_wine"]["wines"] = [title]

        # most cheapest wine
        if stat["cheapest_wine"]:
            if price < stat["cheapest_wine"]["price"]:
                stat["cheapest_wine"]["price"] = price
                stat["cheapest_wine"]["wines"] = [title]
            elif price == stat["cheapest_wine"]["price"]:
                stat["cheapest_wine"]["wines"].append(title)
        else:
            stat["cheapest_wine"]["price"] = price
            stat["cheapest_wine"]["wines"] = [title]


def get_final_variety_stat(wine_stat):
    for wine, stat in wine_stat.items():
        amount_with_price = stat.pop("amount_with_price")
        amount_with_score = stat.pop("amount_with_score")

        # Окончательная средняя оценка и цена для сорта
        stat["average_price"] = round(stat["average_price"] / amount_with_price, 2) if amount_with_price else 'None'
        stat["average_score"] = round(stat["average_score"] / amount_with_score, 2) if amount_with_score != 0 else 'None'

        # Сортируем по количеству встреченных стран и берём первую
        if stat["most_common_country"]:
            stat["most_common_country"] = \
                sorted(stat["most_common_country"].items(), key=lambda k: k[1] ,reverse=True)[0][0]
        else:
            stat["most_common_country"] = "None"

        # Сортируем по количеству встреченных регионов и берём первый
        if stat["most_common_region"]:
            stat["most_common_region"] = \
                sorted(stat["most_common_region"].items(), key=lambda k: k[1], reverse=True)[0][0]
        else:
            stat["most_common_region"] = "None"

        if stat["min_price"] == 99999:
            stat["min_price"] = "None"

        if stat["max_price"] == 0:
            stat["max_price"] = "None"


def get_final_another_stat(stat):
    country_with_score = stat.pop("country_counter_with_score")
    country_with_price = stat.pop("country_counter_with_price")

    stat['most_active_commentator'] = \
        dict([sorted(stat['most_active_commentator'].items(), key=lambda k: k[1], reverse=True)[0]])

    for country, amount in country_with_score.items():
        stat['most_rated_country'][country] = \
            round(stat['most_rated_country'][country] / amount, 2)
    stat['most_rated_country'] = \
        sorted(stat['most_rated_country'].items(), key=lambda k: k[1], reverse=True)

    for country, amount in country_with_price.items():
        stat['most_expensive_country'][country] = \
            round(stat['most_expensive_country'][country] / amount, 2)
    stat['most_expensive_country'] = \
        sorted(stat['most_expensive_country'].items(), key=lambda k: k[1], reverse=True)

    stat['cheapest_country'] = dict([stat['most_expensive_country'][-1]])
    stat['underrated_country'] = dict([stat['most_rated_country'][-1]])
    stat['most_expensive_country'] = dict([ stat['most_expensive_country'][0]])
    stat['most_rated_country'] = dict([stat['most_rated_country'][0]])


def load_wine_stat_as_json(variety_data, all_stat_data, fp):
    with open(fp, "w") as out_f:
        out_f.write('{"statistics": { "wine": {')
        out_f.write(str(variety_data).replace('"', '').replace("'", '"')[1:-1])
        out_f.write("}, ")
        for stat, dict_data in all_stat_data.items():
            out_f.write(f'"{stat}": ')
            if len(dict_data) == 1:
                 out_f.write(str(dict_data).replace("'", '"') + ', ')
            else:
                out_f.write("{")
                for key, value in dict_data.items():
                    out_f.write(f'"{key}": ')
                    if not (type(value) == list):
                        out_f.write(f'"{value}", ')
                    else:
                        out_f.write("[")
                        for wine in value:
                            out_f.write(f'"{wine}", ')
                        out_f.seek(out_f.tell() - 2)
                        out_f.write("]")
                out_f.write("}, ")

        out_f.seek(out_f.tell() - 2)
        out_f.write("}}")

# unicode-escape
def load_wine_stat_as_markdown(variety_data, all_stat_data, fp):
    with open(fp, "w", encoding="utf-8") as out_f:
        for stat, dict_data in variety_data.items():
            out_f.write(f"{stat.encode('utf-8').decode('unicode-escape')}: \n")
            for key, value in dict_data.items():
                out_f.write(f"* `{key}`: {value} \n")
            out_f.write("\n")

        for stat, dict_data in all_stat_data.items():
            out_f.write(f'{stat} \n')
            for key, value in dict_data.items():
                out_f.write(f'* `{key}`: ')
                if not (type(value) == list):
                    out_f.write(f' {value} \n')
                else:
                    out_f.write('\n')
                    for wine in value:
                        out_f.write(f"  * {wine.encode('utf-8').decode('unicode-escape')} \n")
            out_f.write('\n')
        out_f.write('\n')

def get_stat(wine_data):
    varieties = ['"Gew\\u00fcrztraminer"', '"Riesling"', '"Merlot"',
                 '"Madera"', '"Tempranillo"', '"Red Blend"']

    varieties_stats = ["average_price", "min_price", "max_price",
                       "most_common_region", "most_common_country",
                       "average_score", "amount_with_price", "amount_with_score"]

    values = [0, 99999, 0, {}, {}, 0, 0, 0]
    # Создаём словарь со статистикой по указанным сортам с ключами из сортов
    # и значениями в виде словарей с парами искомая статистика-начальное знчачение из values
    wine_stat = {variety: {stat: value.copy() if type(value) == dict else value
                           for stat, value in zip(varieties_stats, values)} for variety in varieties}

    # Словарь с общей остальной статистикой по всем винам
    # cheapest_country и underrated_country не заполняются так как это та же
    # информация что и most_expensive_wine и most_rated_country
    another_values = ["most_expensive_wine", "cheapest_wine", "highest_score",
                      "lowest_score", "most_expensive_country",
                      "cheapest_country",
                      "most_rated_country", "underrated_country",
                      "most_active_commentator",
                      "country_counter_with_price", "country_counter_with_score"]
    another_stat = {value: {} for value in another_values}

    # Собираем сразу всю статистику за один проход по отсортированным данным,
    # полученными при загрузке .json файлов
    for wine in wine_data:
        variety = wine[0][0]
        if variety in varieties:
            update_variety_stat(wine=wine, variety=variety,
                                wine_stat=wine_stat)

        update_another_stat(wine=wine, stat=another_stat)

    get_final_variety_stat(wine_stat)
    get_final_another_stat(another_stat)

    # load_wine_stat_as_json(wine_stat, another_stat, "stats.json")
    load_wine_stat_as_markdown(wine_stat, another_stat, "stats.md")
    pprint.pprint(wine_stat)
    pprint.pprint(another_stat)


if __name__ == '__main__':
    start = clock()
    all_wines = {}
    file_paths = ("winedata_1.json", "winedata_2.json")
    for path in file_paths:
      dump_json_file(path, all_wines)
    # dump_json_file("winedata_2.json", all_wines)
    all_wines = sorted(all_wines.items(),
                       key=lambda k: (int(k[0][2]), k[0][0]), reverse=True)
    load_json(all_wines, "winedata_full.json")
    get_stat(all_wines)
    print(clock()-start)

    # Проверка на валидность
    with open("winedata_full.json", "r") as f:
        new_data = json.load(f)
        new_data.clear()
