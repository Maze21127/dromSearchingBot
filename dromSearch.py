import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import json
from config import get_user_config


class DromSearch:
    def __init__(self, filename, config=get_user_config()):
        with open(f'{filename}', 'r', encoding='utf-8') as js_car:
            self.params = json.load(js_car)
            self.basic_params = self.params['basic']
            self.advanced_params = self.params['advanced']
        self.filename = filename
        self.not_404_page = True
        self.config = config
        self.region_type = self.config['region_type']
        self.city = self.config['city']
        self.region_number = self.config['region_number']
        self.additional_radius = self.config['addition_radius']
        self.html = None
        self.car = None
        self.last_car_link = None
        self.url_params = None
        self.final_url = None
        self.new_car_link = None
        self.car_name = None
        self.car_price = None
        self.car_disc = None
        self.car_spec = None
        self.no_car = None
        self.no_car_text_base = 'К сожалению, по заданным условиям не найдено ни одного объявления. ' \
                                'Попробуйте изменить условия поиска.'
        self.no_car_text = None
        self.message = ""
        self.params_list = []
        self.brand = self.basic_params['brand']
        self.model = self.basic_params['model']
        self.generation = self.basic_params['generation']
        if self.generation != "":
            self.generation = f'generation{self.generation}'
        self.restyling = self.basic_params['restyling']
        if self.restyling != "":
            self.restyling = f'restyling{self.restyling}'
        self.body_type = self.advanced_params['body_type']
        if self.advanced_params['bez-probega'] == "1":
            self.no_mileage = 'bez-probega'
        else:
            self.no_mileage = ""
        self.params_list.append(self.brand)
        self.params_list.append(self.model)
        self.params_list.append(self.generation)
        self.params_list.append(self.restyling)
        self.params_list.append(self.no_mileage)
        self.params_list.append(self.body_type)
        self.max_price = self.basic_params['maxprice']
        self.min_price = self.basic_params['minprice']
        self.unsold = self.basic_params['unsold']
        self.transmission = self.basic_params['transmission']
        self.min_year = self.basic_params['minyear']
        self.max_year = self.basic_params['maxyear']
        self.fuel_type = self.basic_params['fueltype']
        self.min_volume = self.basic_params['mv']
        self.max_volume = self.basic_params['xv']
        self.photo = self.basic_params['ph']
        self.docs = self.advanced_params['pts']
        self.damage = self.advanced_params['damaged']
        self.gear = self.basic_params['privod']
        self.min_power = self.advanced_params['minpower']
        self.max_power = self.advanced_params['maxpower']
        self.min_mileage = self.advanced_params['minprobeg']
        self.max_mileage = self.advanced_params['maxprobeg']
        self.url_params = {
            'unsold': self.unsold,
            'minprice': self.min_price,
            'maxprice': self.max_price,
            'transmission': self.transmission,
            'minyear': self.min_year,
            'maxyear': self.max_year,
            'fueltype': self.fuel_type,
            'mv': self.min_volume,
            'xv': self.max_volume,
            'ph': self.photo,
            'pts': self.docs,
            'damaged': self.damage,
            'privod': self.gear,
            'minpower': self.min_power,
            'maxpower': self.max_power,
            'minprobeg': self.min_mileage,
            'maxprobeg': self.max_mileage
        }
        self.url = None
        self.get_link()
        print(f"Бот запущен для {self.filename}")
        self.get_content()
        self.get_last_car_info()
        self.last_link = self.get_last_car_link()
        self.new_link = None
        self.sending = False
        self.cars = None

    def get_link(self):
        if self.region_type == 'city':
            self.url = f'https://{self.city}.drom.ru/'
            if self.additional_radius != "":
                self.url_params['distance'] = self.additional_radius
        elif self.region_type == 'area':
            self.url = f'https://auto.drom.ru/region{self.region_number}/'
        elif self.region_type == 'all':
            self.url = f'https://auto.drom.ru/'
        for param in self.params_list:
            if param != "":
                self.url += param
                self.url += '/'
        return self.url

    def get_content(self):
        headers = {'user-agent': UserAgent().Chrome,
                   'accept': '*/*'}
        self.html = requests.get(self.url, headers=headers, params=self.url_params)
        self.final_url = self.html.url
        if self.html.status_code == 200:
            return self.html
        elif self.html.status_code == 404:
            print(f"Запрошенная страница для {self.filename} не существует")
            self.not_404_page = False

    def get_last_car_info(self):
        if self.html.status_code == 200:
            soup = BeautifulSoup(self.html.text, 'lxml')
            self.no_car = soup.find(class_="css-1aqy7qq e1lm3vns0")
            if self.no_car is None:
                self.no_car_text = ""
                self.car = soup.find(class_="css-1psewqh ewrty961")
                self.cars = soup.find_all(class_="css-1psewqh ewrty961")
                for ind, sss in enumerate(self.cars):
                    t = sss.find('div', class_="css-1svsmzw e1vivdbi2").find('div')
                    try:
                        title = t.get('title')
                        if title != 'Прикреплено' or title is None:
                            self.car = self.cars[ind]
                            break
                    except AttributeError:
                        continue

                self.car_name = self.car.find("div", class_="css-1svsmzw e1vivdbi2").text
                self.car_spec = self.car.find("span", class_="css-1yg7m3u e1vivdbi0")
                if self.car_spec is not None:
                    self.car_spec = self.car_spec.text
                    if self.car_spec[0] != " ":
                        self.car_spec = " " + self.car_spec
                    self.car_name += self.car_spec
                self.car_price = self.car.find("span", class_="css-bhd4b0 e162wx9x0").text
                self.car_disc = self.car.find("div", class_="css-3xai0o e162wx9x0").text
            else:
                self.no_car_text = self.no_car_text_base

    def get_last_car_link(self):
        if self.html.status_code == 200 and self.no_car_text != self.no_car_text_base:
            return self.car.get('href')
        else:
            return None

    def create_message(self):
        if self.html.status_code == 200 and self.no_car_text != self.no_car_text_base:
            self.message = ""
            self.message += self.car_name + '\n'
            self.message += self.car_price + '\n'
            self.message += self.car_disc

    def send_message(self):
        if self.html.status_code == 200 and self.no_car_text != self.no_car_text_base:
            pass

    def update_link(self):
        self.sending = False
        self.get_link()
        self.get_content()
        self.get_last_car_info()
        self.new_link = self.get_last_car_link()
        if self.new_link != self.last_link:
            print(f"Новый ссылка для {self.filename}")
            self.last_link = self.new_link
            self.create_message()
            self.sending = True

