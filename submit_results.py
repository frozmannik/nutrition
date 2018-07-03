import facebook
import requests
import json
from diets import get_diets, write_data

def analyze():
    with open('data.json', 'r') as f :
        file = json.load(f)
    data = {}  # name: [(avg) total_carb, total_carb, total days, good_days    ]

    for user in file:
        data[user] = []
        carb = 0   # total amount of carb
        good_days = 0 # number of days where sugar < 10 %
        days = len(file[user]) # total number of days
        days_in_a_row = 0

        for dates in file[user]:
            list = dates.keys()
            for x in list:
                carb += dates[x][0]['calories']
                if dates[x][0]['energy_from_sugar'] < 10:
                    good_days += 1

        data[user].append(round(carb/days, 2))
        data[user].append(carb)
        data[user].append(days)
        data[user].append(good_days)

    max_days = 0
    low_car = 0
    lowest_avg_carb = 0

    # statistic for low sugar for all users
    print("SUGAR STATISTIC:")
    for user in data:
        print("{} has {} out of {} days with good sugar intake".format(user, data[user][3], data[user][2]))
        lowest_avg_carb = [user,data[user]]

    print("##################### \n Personal achivements")
    # lowest  avg carb  data[user][1]

    for user in data:
        if lowest_avg_carb[1][0] > data[user][0]:
            lowest_avg_carb = [user,data[user]]

    print('{} has lowest average Calories intake for all time ({})'.format(lowest_avg_carb[0], lowest_avg_carb[1][0]))

    print("##################### \n CALORIES STATISTIC:")

    with open('bmi.json', 'r') as f: # read bmi data
        bmi = json.load(f)

    for user in file:
        recomended_calories = round(calculate_recomended_calories(bmi[user][0]),2)
        cal_day = 0
        for dates in file[user]:
            list = dates.keys()
            for x  in list:
            #    print('calories : {} \n recomended : {} '.format(dates[x][0]['calories'], recomended_calories))
                if dates[x][0]['calories'] < recomended_calories * 1.1 and dates[x][0]['calories'] > recomended_calories * 0.9:
                    print('{} consumed recomended amount of calories '.format(user))
                    cal_day += 1
                elif dates[x][0]['calories'] > recomended_calories:
                    print('{} consumed on {} {}% more than recomended calories daily intake'.format(user, x, round((dates[x][0]['calories'] - recomended_calories)/recomended_calories * 100 ,1)))
                else:
                    print('{} consumed on {} {} less than recomended calories daily intake '.format(user, x, round((recomended_calories - dates[x][0]['calories'])/recomended_calories * 100 ,1 )))

        print("{} got recomended amout of calories in {} out of {} \n".format(user, cal_day, data[user][2]))

def calculate_recomended_calories(data):
    if data['gender']: #
        return 66.47 + (13.75 * data['weight']) + (5 * data['height']) - (6.76 * data['age'])
    else:
        return 65.51 + (9.56 * data['weight']) + (1.85 * data['height']) - (4.67 * data['age'])

analyze()
