import os
import time
import logging

from telebot import TeleBot

from dromSearch import DromSearch
from settings import *


bot = TeleBot(API_TOKEN)
files_list = os.listdir('cars')
channel_ids = [1214900768, 455035418]

cars_list = []
for file in files_list:
    car = DromSearch(f'cars/{file}')
    cars_list.append(car)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/errors.txt")
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


while True:
    try:
        for car in cars_list:
            car.update_link()
            if car.sending:
                for channel_id in channel_ids:
                    bot.send_message(channel_id, car.message)
                    print(f'Отправлено\n{car.message}')
        time.sleep(5)
    except Exception as ex:
        logger.exception(ex)
        time.sleep(10)
