import time

import requests
import json
import os
import multiprocessing
import threading

from yadisk import YaDisk
from datetime import datetime
from mytools.tool_class import ColorPrint, StatisticCollection

printer = ColorPrint().print_error
printinf = ColorPrint().print_info
printw = ColorPrint().print_warning
printy = ColorPrint().print_yellow
statistic = StatisticCollection()

def upload_to_yadick(content: dict)->None:
    """
    Загружает на яндекс диск в папку folder_name(ip-адрес пользователя)
    статистику по работе программы:
    :param folder_name: IP-адрес пользователя
    :return:
    """
    # загрузка параметров: FOLDER_PATH - папка, в которую сохранится folder_name на яддекс_диске
    # YANDEX_TOKEN - токен яндекс REST API
    while True:
        try:
            FOLDER_PATH = 'STATISTIC'
            YANDEX_TOKEN = 'y0_AgAAAAABJQnxAAkufQAAAADiFPV_TjOFwUIbR6KNgvJ5KSFpjefPkow'

            if YANDEX_TOKEN == "":
                raise ValueError
            break

        except Exception as ex:
            print(ex)

    try:
        folder_name = content['IP']
        yadisk = YaDisk(token=YANDEX_TOKEN)

        # if not yadisk.check_token():
        #     print("Неверный токен доступа")
        #     exit()

        if yadisk.check_token():
            # print("Connection to YD")
            pass
        else:
            # print(f"Ошибка!\nНе удалось подключиться к яндекс-диску.")
            return

        path_name = ""
        # создаем папку на яндекс-диске, если ее там нет
        if FOLDER_PATH != "":
            if not yadisk.is_dir(f"{FOLDER_PATH}"):
                yadisk.mkdir(f"{FOLDER_PATH}")
            else:
                if not yadisk.is_dir(f"{FOLDER_PATH}/{folder_name}/"):
                    yadisk.mkdir(f"{FOLDER_PATH}/{folder_name}/")

            path_name = f"{FOLDER_PATH}/{folder_name}/"
        else:
            if not yadisk.is_dir(f"{folder_name}/"):
                yadisk.mkdir(f"{folder_name}/")
                path_name = f"{folder_name}/"

    except Exception as ex:
        printer(ex)
        return

    try:
        # имя файла, равно текущему времени на ПК
        now = datetime.now()
        content['time_start'] = f'{now.strftime("%Y.%m.%d_%H:%M:%S")}'
        filename = f'{now.strftime("%Y.%m.%d_%H.%M.%S")}.json'
        destination_path = f"{path_name + filename}"

        # Открытие файла для записи
        with open(filename, "w", encoding="utf-8", newline="") as json_file:
            # Сохранение словаря в JSON файл
            json.dump(content, json_file, indent=4)

        yadisk.upload(filename, destination_path, overwrite=True)
        os.remove(filename)

    except Exception as ex:
        printer(ex)

def main_func()->None:
    content = statistic.get_full_info
    upload_to_yadick(content)

def main_multiprocessing():
    printw("version 1.2 (02.09.2023)")
    printw("Программа для сбора информации об интернет соединении")
    printinf('Благодарю за использование программы!')

    # Создаем пул процессов с двумя процессами
    pool = multiprocessing.Pool(processes=2)

    # Запускаем функции upload_to_yd() и calculate() в пуле процессов
    pool.apply_async(main_func,())
    pool.apply_async(statistic.draw,())

    # Закрываем пул процессов и ждем завершения выполнения всех процессов
    pool.close()
    pool.join()

if __name__ == '__main__':
    main_multiprocessing()
    printw('Каждый запуск помогает мне в обучении')
    statistic.print_smile()
    time.sleep(3)