from yadisk import YaDisk
from mytools.setting import setting

class WorkingYandexDisk:
    # YANDEX_TOKEN = "y0_AgAAAAABJQnxAAkufQAAAADiFPV_TjOFwUIbR6KNgvJ5KSFpjefPkow"  #мой токен
    def __init__(self, yandex_token):
        try:
            self.yadisk = YaDisk(token=yandex_token)

            if self.yadisk.check_token():
                # print("Connection to YD")
                pass
            else:
                # print(f"Ошибка!\nНе удалось подключиться к яндекс-диску.")
                raise ConnectionError

        except Exception as ex:
            print(ex, f"Ошибка!\nНе удалось подключиться к яндекс-диску.")

    def download_to_yd(self)->bool:
        try:
            folder_name = setting.folder_sett
            filename = setting.models

            if folder_name:
                path = f'/{folder_name}/{filename}'
            else:
                path = f'/{filename}'

            self.yadisk.download(path, filename)
            return True
        except Exception as ex:
            print(ex)

    def upload_of_yd(self,
                     filename: str,
                     folder_name: str,
                     file_obj,
                     folder_path: str='STATISTIC',
                     )->bool:
        """
        Загрузка файла filename в подпапку folder_name папки folder_path_local на яндекс диске
        :param folder_name: str - имя подкаталога
        :param filename: str - имя загружаемого файла
        :param folder_path: str - название основной папки в корне диска
        :return:
        """
        try:
            # path_name = ""
            # создаем папку на яндекс-диске, если ее там нет
            if folder_path != "":
                if not self.yadisk.is_dir(f"{folder_path}"):
                    self.yadisk.mkdir(f"{folder_path}")
                else:
                    if not self.yadisk.is_dir(f"{folder_path}/{folder_name}/"):
                        self.yadisk.mkdir(f"{folder_path}/{folder_name}/")

                path_name = f"{folder_path}/{folder_name}/"
            else:
                if not self.yadisk.is_dir(f"{folder_name}/"):
                    self.yadisk.mkdir(f"{folder_name}/")
                path_name = f"{folder_name}/"

            if file_obj:
                if filename:
                    path_name = path_name + filename
                else:
                    path_name = path_name + 'test.txt'

                self.yadisk.upload(file_obj, path_name, overwrite=True)
            else:
                self.yadisk.upload(filename, path_name, overwrite=True)

        except Exception as ex:
            print(ex)

    def listdir(self, path: str, **kwargs):
        return self.yadisk.listdir(path, **kwargs)

    def remove(self, path: str, **kwargs):
        return self.yadisk.remove(path, **kwargs)