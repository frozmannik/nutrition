from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
import os.path

def simple_get(url): # get a response
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):  # check if response is correct
    content_type = resp.headers['Content-type'].lower()
    return(resp.status_code == 200
           and content_type is not None
           and content_type.find('html') > -1)

def get_diets(url,name): #return date,calories, sugar_carb
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        data = []
        ## get calories
        calories = float((html.find_all('table', {'class' : 'table table-condensed'})[1].find('th', {'class' : 'align-right'}).text).split()[0])
        buf = (html.find('h2', {'class' : 'page-header'}).text.split())[3:]
        options = {
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9,
        'October' : 10,
        'November' : 11,
        'December' :12
        }
        # get date
        date = '{}.{}.{}'.format(buf[1][:-1],options[buf[0]],buf[2]) # check it with 1 digit day

        #get sugar
        total_carb = float((html.find('div', {'id' : 'content'})).find('table', {'class' : 'table table-condensed'}).find('tbody').find_all('tr')[2].find_all('td')[1].text.split()[0])
        total_perc = float((html.find('div', {'id' : 'content'})).find('table', {'class' : 'table table-condensed'}).find('tbody').find_all('tr')[2].find_all('td')[2].text.split()[0])
        sugar_carb = float((html.find('div', {'id' : 'content'})).find('table', {'class' : 'table table-condensed'}).find('tbody').find_all('tr')[3].find_all('td')[1].text.split()[0])
        daily_sugar = sugar_carb/total_carb * total_perc

        return (date,calories,round(daily_sugar,2),name)

def write_data(info):
    data = {}
    data[info[3]] = []  # name

    buf = {}
    buf[str(info[0])] = []
    buf[str(info[0])].append({'calories' : info[1],
                  'energy_from_sugar': info[2] })

    if os.path.isfile('data.json'): # check if file exist
        with open('data.json', 'r') as f:
            file = json.load(f)
            # check if name in file than check date
            if info[3] in file: # if name in a list overwrite (CHECK FOR DATE)
                if buf not in file[info[3]]: # if record already exist do nothing
                    file[info[3]].append(buf)
            else: # name not in a list
                new = {}
                new[str(info[0])] = []
                new[str(info[0])].append({'calories' : info[1],
                              'energy_from_sugar': info[2]})
                file[info[3]] = []
                file[info[3]].append(new)
                f.close()

        with open('data.json', 'w') as f:
            json.dump(file,f,indent = 4, sort_keys = True)

    else: # if file doesn't exist then create
        data[info[3]].append(buf)
        with open('data.json', 'w') as f:
            json.dump(data,f, indent = 4, sort_keys = True)

    f.close()
