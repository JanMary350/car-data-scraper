import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_data(producer, model = None, pages = 100):
    dfData = []
    '''downloads data of choosen car brand (and model if chosen) from otomoto.pl'''
    if model is None:
        r = requests.get('https://www.otomoto.pl/osobowe/'+ str(producer)).text
        print('https://www.otomoto.pl/osobowe/'+ str(producer))
        i = 2
        while requests.get('https://www.otomoto.pl/osobowe/'+ str(producer) + '?page=' + str(i)).status_code == 200 and i < pages:
            print('https://www.otomoto.pl/osobowe/'+ str(producer) + '?page=' + str(i))
            r += requests.get('https://www.otomoto.pl/osobowe/'+ str(producer) + '?page=' + str(i)).text
            i+=1
    else:
        r = requests.get('https://www.otomoto.pl/osobowe/'+ str(producer) + '/' + str(model)).text
        print('https://www.otomoto.pl/osobowe/'+ str(producer) + '/' + str(model))
        i = 2
        while requests.get('https://www.otomoto.pl/osobowe/'+ str(producer) + '?page=' + str(i)).status_code == 200 and i < pages:
            print('https://www.otomoto.pl/osobowe/'+ str(producer) + '?page=' + str(i))
            r += requests.get('https://www.otomoto.pl/osobowe/'+ str(producer) + '?page=' + str(i)).text
            i+=1
    soup = BeautifulSoup(r, 'html.parser')
    arts = soup.find_all('article')
    # print(arts)
    for i in arts:
        isCar = re.search(r'https://www.otomoto.pl/oferta/', str(i))
        if isCar:
            try:
                dfData.append(separate_offert(i))
            except:
                pass
    df = pd.DataFrame.from_dict(dfData)
    df.to_csv('data_'+str(producer)+'_'+str(model)+'_'+str(pages)+'.csv', index = False)
    pass
def separate_price(offert):
    '''separates price from offert'''
    car_data = {}
    # print('price')
    price = re.search(r'>(\s|[0-9])*PLN', str(offert)).group().replace('>', '').replace('PLN', '').replace(' ', '')
    # print(price)
    # print('price')
    car_data['price'] = price
    return car_data

def separate_data(offert):
    '''separates data except of price from offert'''
    car_data = {}
    list_items = offert.find_all('li')
    for i in list_items:
        print(i)
        if re.search(r'\b\d{4}\b', str(i)):
            '''year'''
            car_data['year'] = re.search(r'\b\d{4}\b', str(i)).group()
            print(car_data['year'])
        elif re.search(r'\>*km', str(i)):
            '''kilometers'''
            kilometers = re.search(r'>(\s|[0-9])*km', str(i)).group().replace('>', '').replace('km', '').replace(' ', '')
            car_data['kilometers'] = kilometers
            print(car_data['kilometers'])
        elif re.search(r'Diesel|Benzyna|Hybryda', str(i)):
            '''type of fuel'''
            car_data['fuel'] = re.search(r'Diesel|Benzyna|Hybryda', str(i)).group()
            print(car_data['fuel'])
        elif re.search(r'\>*cm3', str(i)):
            '''engine size'''
            size = re.search(r'>(\s|[0-9])*cm3', str(i)).group().replace('>', '').replace('cm3', '').replace(' ', '')
            car_data['engine_size'] = size
            print(car_data['engine_size'])
    return car_data
def separate_offert(offert):
    '''separates data from offert'''
    print('next offert')
    print(offert)
    car_data = {
        'price': None,
        'year': None,
        'kilometers': None,
        'fuel': None,
        'engine_size': None,
    }
    try:
        car_data.update(separate_data(offert))
        car_data.update(separate_price(offert))
    except:
        pass
    return car_data


if __name__ == '__main__':
    get_data('volkswagen', model = 'golf', pages = 10)


