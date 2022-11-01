# encoding: utf-8
import json
import datetime
from pyowm import OWM
from tqdm import tqdm
from math import ceil
from tkinter import *
from time import sleep
from warnings import *
from requests import get
from pprint import pprint
from shutup import please
import requests.exceptions
from geocoder import location
from PIL import ImageTk, Image
from datetime import timedelta
from astral import LocationInfo
from webbrowser import open_new
from pyowm.utils import timestamps
from pyowm.commons import exceptions
from astral.sun import sunset, sunrise
from tkintermapview import TkinterMapView
from urllib3.exceptions import MaxRetryError
from urllib3.connection import HTTPSConnection
from pyowm.utils.config import get_default_config
from requests.exceptions import ConnectTimeout, ConnectionError
from pyowm.utils.config import get_default_config_for_subscription_type



try:  # Получение индивидуального токена
    from OWMTOKENs import token

except ModuleNotFoundError:

    pprint(f'Sing up in https://openweathermap.org and getting API key!')


def main():
    please()

    tk = Tk()

    for i in tqdm(range(100)):

        sleep(0.1)

        i += 0

        while not False:

            def tomorrows_weather_in_yourself_region():
                with open(file='weather.json', mode='w', encoding='utf-8') as del_file:
                    del_file.truncate()
                # Погода на завтра в родном городе,
                # данные о регионе мы получаем запарсив json | http://ip-api.com/json/

                if inputs['text']:

                    inputs['text'] = str(inputs.delete(0, END))

                else:

                    pass

                inputs['text'] += str(inputs.insert(0, jsons['city']))

                filterwarnings('ignore')
                filterwarnings('ignore', category=DeprecationWarning)

                filterwarnings('ignore', category=FutureWarning)
                filterwarnings('ignore', category=Warning)  # Обрабатываем ошибки и сразу заканчиваем код при ошибках.

                config_dict = get_default_config()
                config_dict['connection']['use_ssl'] = False
                config_dict['connection']["verify_ssl_certs"] = False

                if jsons['city']:  # Если значение не равно ничему-то начинаем запросы.

                    try:
                        config_dicts = get_default_config()
                        config_dicts['language'] = 'RU'

                        conf = get_default_config_for_subscription_type(name='professional')
                        owm = OWM(api_key=token, config=config_dicts and conf)

                        mgr = owm.weather_manager()
                        daily_forecaster = mgr.forecast_at_place(name=jsons["city"], interval='3h')
                        tomorrow = timestamps.tomorrow()
                        weather = daily_forecaster.get_weather_at(tomorrow)

                        cel = weather.temperature('celsius')  # Данные о температуре
                        feels_like = cel['feels_like']
                        max_temp = cel['temp_max']
                        ref = weather.pressure['press']
                        min_temp = cel['temp_min']

                        humidity = weather.humidity

                        w = mgr.weather_at_place(name=jsons["city"])

                        lcl = mgr.weather_at_place(name=jsons["city"]).location
                        # Получаем Список с гео-данными # Гео данные для постройки карты

                        lon = lcl.lon  # Получаем классы:Долгота и широта

                        lat = lcl.lat
                        '''
                        TODO:
                        dict_ = owm.weather_manager().weather_at_place(name='krasnodar').to_dict()
                        ref_time = formatting.timeformat(dict_['reception_time'], 'date')
                        '''
                        from tzwhere import tzwhere

                        mgr = owm.weather_manager()
                        locations_info = mgr.weather_at_place(name=jsons["city"]).location
                        country = locations_info.to_dict()

                        result = w.weather
                        windy = weather.wind()

                        wis = weather.visibility_distance
                        clouds = weather.clouds

                        ref_time = weather.reference_time('date')

                        data_cur = datetime.datetime.now().strftime('%Y %m %d').strip()  # Реформатируем время
                        ever_el = data_cur.split()

                        tzwhere = tzwhere.tzwhere()
                        timezone_str = tzwhere.tzNameAt(latitude=float(lat),
                                                        longitude=float(lon))  # Получаем часовой пояс

                        loc = LocationInfo(region=country["country"], name=jsons["city"],
                                           timezone=timezone_str, latitude=float(lat), longitude=float(lon))

                        s = sunset(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                   tzinfo=loc.timezone)
                        # По часовому поясу определяем когда начинается закат и рассвет

                        s2 = sunrise(loc.observer,
                                     date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                     tzinfo=loc.timezone)

                        minute = datetime.datetime.fromisoformat(str(s)).strftime('%H:%M').strip()

                        minute2 = datetime.datetime.fromisoformat(str(s2)).strftime('%H:%M').strip()

                        tomorrow_time__ = datetime.datetime.now() + timedelta(days=1)
                        temperature = Label(tk,
                                            text=f'Погода в городе {str(jsons["city"])} на завтра'
                                                 f'{str("-") + str(result.detailed_status)}\n'
                                                 f'Погода ощущается как {round(number=feels_like)}°С  \n'
                                                 f'Максимальная температура {round(number=max_temp)}°С \n'
                                                 f'Минимальная температура {round(number=min_temp)}°С  \n'
                                                 f'Температура прямо сейчас {round(number=cel["temp"])}°С\n'
                                                 f'Влажность-{round(number=humidity)} %\n'
                                                 f'Скорость ветра-{round(number=windy["speed"])}м/с  \n'
                                                 f'Количество облаков-{round(number=clouds)}%\n'
                                                 f'Средний статистический показатель погоды за '
                                                 f' {tomorrow_time__.strftime("%Y.%m.%d")} '
                                                 f'число {round(number=feels_like)}°С\n'
                                                 f'Видимость {round(number=wis / 1000)}'
                                                 f'км,Давление {ceil(float(ref / 1.33245033213))} '
                                                 f'мм.рт.ст,Закат начинается в {minute.lstrip()} '
                                                 f'Рассвет {minute2.rstrip()},'
                                                 f'\nПоследняя проверка погоды осуществлялась в {ref_time}',

                                            fg='gold', bg='SteelBlue4', width=200, height=10, foreground='gold',
                                            borderwidth=2, activeforeground='SteelBlue', font=("Rockwell", 17),
                                            justify='center')

                        win = round(number=float(str(windy).split()[1].replace(',', '')))

                        JsonWeather = [{f'Weather_type in {jsons["city"]}': result.detailed_status,
                                        'feels_like': f'{round(number=feels_like)}˚C',
                                        'max_temp': f'{round(number=max_temp)}˚C',
                                        'min_temp': f'{round(number=min_temp)}˚C',
                                        'cel_temp': f'{round(cel["temp"])}˚',
                                        'humidity': f'{round(number=humidity)}%',
                                        'windy_speed': f'{int(round(number=win))}m/s',
                                        'clouds': f'{round(number=clouds)}%',
                                        'visibility_distance': f'{round(number=wis / 1000)}km',
                                        'pressure': f'{round(number=float(ref / 1.33245033213))}mmHg',
                                        'sunrise': minute2.rstrip(),
                                        'sunset': minute.lstrip(),
                                        'ref_time': str(ref_time).strip()}]
                        sleep(0.1)
                        temperature.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)

                        with open(file='weather.json', mode='a', encoding='utf-8') as file:
                            file.writelines('\n' + str(JsonWeather) + '\t\n')

                        with open(file='weather.json', mode='w', encoding='utf-8') as file_js:
                            file_js.seek(0)
                            json.dump(JsonWeather, file_js, indent=2, ensure_ascii=False)  # Записываем в файл

                        def building_map():

                            sleep(0.5)

                            tk2 = Toplevel(tk)  # Создаем 2 окно
                            tk2['bg'] = 'mint cream'
                            label_for_map = LabelFrame(tk2, foreground='gray')
                            label_for_map.pack(pady=20, padx=10)

                            tk_map = TkinterMapView(label_for_map, width=425, height=350, corner_radius=0)

                            tk_map.set_position(deg_x=float(lat), deg_y=float(lon))

                            tk_map.set_marker(deg_x=float(lat), deg_y=float(lon),
                                              text=str(f'{jsons["city"] + "-" + result.detailed_status}'
                                                       f',{round(number=cel["temp"])}°С'))

                            tk_map.set_zoom(zoom=9)

                            tk_map.pack(anchor=SW, padx=10, expand=0, fill=BOTH)

                        b15 = Button(tk, text=f'Показать город {jsons["city"]} на карте', command=building_map
                                     , font=('Rockwell', 12), fg='gold', bg='SteelBlue4',
                                     foreground='SteelBlue4', background='SteelBlue4',
                                     width=190, highlightbackground='gold')  # Копка вызова функции

                        b15.pack(fill=BOTH, pady=2,
                                 padx=2, anchor=NW)
                        b15.lift()

                        def remove():

                            temperature.destroy()
                            b15.destroy()
                            b2.destroy()
                            return temperature, b15, b2

                        b2 = Button(tk, text='Скрыть результат поиска', command=remove, fg='gold', bg='SteelBlue4',
                                    foreground='SteelBlue4', background='SteelBlue4',
                                    width=190, highlightbackground='gold', font=('Rockwell', 12))
                        b2.pack(fill=BOTH, pady=2,
                                padx=2, anchor=NW)  # Скрыть результат

                    except exceptions.NotFoundError or exceptions.TimeoutError.__basicsize__ or ConnectTimeout \
                            or ConnectionError \
                            or HTTPSConnection or MaxRetryError:
                        # Исключения в виде задержки производительности запроса
                        # на сайт,соеденение с интернетом, при отсутствии региона
                        filterwarnings('ignore')
                        filterwarnings('ignore', category=DeprecationWarning)
                        filterwarnings('ignore', category=FutureWarning)
                        filterwarnings('ignore', category=Warning)

                        response_error2 = Label(tk,
                                                text=f'\nГород- {str(jsons["city"]).strip()}'
                                                     f' не найден , введите верное '
                                                     f' название'
                                                     f'города!\n',
                                                background='gold', fg='gold', bg='SteelBlue4',
                                                borderwidth=2, font=("Rockwell", 14),
                                                highlightbackground='gold', width=190, underline=True,
                                                takefocus=True, height=2)

                        response_error2.pack(anchor=NW, fill=BOTH, side=TOP)

                        def remove():
                            response_error2.destroy()
                            b120.destroy()
                            return response_error2, b120

                        b120 = Button(tk, text='Скрыть ошибку', command=remove,
                                      fg='SteelBlue4', bg='SteelBlue4',
                                      foreground='SteelBlue4', background='SteelBlue4',
                                      highlightbackground='gold', state='normal', font=('Rockwell', 17), height=2
                                      )
                        b120.pack(fill=BOTH, pady=2, padx=2)

                elif not jsons["city"]:

                    none_error2 = Label(tk, text='\nПожалуйста ,введите хотя бы что-то !\n', fg='gold',
                                        bg='SteelBlue4', borderwidth=2, state='normal',
                                        justify='center',font=('Rockwell', 14), background='SteelBlue4',
                                        highlightbackground='gold', width=190, height=2)
                    none_error2.pack(anchor=NW,
                                     fill=NONE, padx=2, pady=2, side=TOP)  # Если мы ничего не ввели - то:

                    def remove():
                        b19.destroy()
                        none_error2.destroy()
                        none_error2.pack_forget()
                        return none_error2, b19

                    b19 = Button(tk, text='Скрыть ошибку', command=remove,
                                 font=('Rockwell', 12), fg='SteelBlue4', bg='SteelBlue4',
                                 foreground='SteelBlue4', background='gold',
                                 highlightbackground='gold', state='normal', width=190, height=2)

                    b19.pack(fill=BOTH, pady=2, padx=2, side=TOP)  # Скрываем

            def tomorrows_weather():
                with open(file='weather.json', mode='w', encoding='utf-8') as del_file:
                    del_file.truncate()

                filterwarnings('ignore')
                filterwarnings('ignore', category=DeprecationWarning)

                filterwarnings('ignore', category=FutureWarning)
                filterwarnings('ignore', category=Warning)

                config_dict = get_default_config()
                config_dict['connection']['use_ssl'] = False
                config_dict['connection']["verify_ssl_certs"] = False

                text = ''
                inputs['text'] = inputs.get().strip()
                text += inputs['text']

                if inputs['text']:

                    try:
                        config_dicts = get_default_config()
                        config_dicts['language'] = 'RU'

                        conf = get_default_config_for_subscription_type(name='professional')
                        owm = OWM(api_key=token, config=config_dicts and conf)

                        mgr = owm.weather_manager()
                        daily_forecaster = mgr.forecast_at_place(name=inputs["text"], interval='3h')
                        tomorrow = timestamps.tomorrow()
                        weather = daily_forecaster.get_weather_at(tomorrow)

                        cel = weather.temperature('celsius')
                        feels_like = cel['feels_like']
                        max_temp = cel['temp_max']
                        ref = weather.pressure['press']
                        min_temp = cel['temp_min']

                        humidity = weather.humidity

                        w = mgr.weather_at_place(name=inputs['text'])

                        lcl = mgr.weather_at_place(name=inputs['text']).location

                        lcl_ = location(location=text.strip())
                        lot_ = lcl_.lng
                        lat_ = lcl_.lat

                        lon = lcl.lon
                        lat = lcl.lat
                        '''
                        TODO:
                        dict_ = owm.weather_manager().weather_at_place(name='krasnodar').to_dict()
                        ref_time = formatting.timeformat(dict_['reception_time'], 'date')
                        '''
                        from tzwhere import tzwhere

                        mgr = owm.weather_manager()
                        locations_info = mgr.weather_at_place(name=inputs['text']).location
                        country = locations_info.to_dict()

                        result = w.weather
                        windy = weather.wind()

                        wis = weather.visibility_distance
                        clouds = weather.clouds
                        ref_time = weather.reference_time('date')

                        data_cur = datetime.datetime.now().strftime('%Y %m %d').strip()
                        ever_el = data_cur.split()

                        tzwhere = tzwhere.tzwhere()
                        timezone_str = tzwhere.tzNameAt(latitude=float(lat), longitude=float(lon))

                        loc = LocationInfo(region=country["country"], name=text,
                                           timezone=timezone_str, latitude=float(lat), longitude=float(lon))

                        s = sunset(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                   tzinfo=loc.timezone)

                        s2 = sunrise(loc.observer,
                                     date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                     tzinfo=loc.timezone)

                        minute = datetime.datetime.fromisoformat(str(s)).strftime('%H:%M').strip()

                        minute2 = datetime.datetime.fromisoformat(str(s2)).strftime('%H:%M').strip()

                        tomorrow_time__ = datetime.datetime.now() + timedelta(days=1)

                        temperature = Label(tk,
                                            text=f'Погода в городе {str(inputs["text"])} на завтра'
                                                 f'{str("-") + str(result.detailed_status)}\n'
                                                 f'Погода ощущается как {round(number=feels_like)}°С  \n'
                                                 f'Максимальная температура {round(number=max_temp)}°С \n'
                                                 f'Минимальная температура {round(number=min_temp)}°С  \n'
                                                 f'Температура прямо сейчас {round(number=cel["temp"])}°С\n'
                                                 f'Влажность-{round(number=humidity)} %\n'
                                                 f'Скорость ветра-{round(number=windy["speed"])}м/с  \n'
                                                 f'Количество облаков-{round(number=clouds)}%\n'
                                                 f'Средний статистический показатель погоды за '
                                                 f' {tomorrow_time__.strftime("%Y.%m.%d")} '
                                                 f'число {round(number=feels_like)}°С\n'
                                                 f'Видимость {round(number=wis / 1000)}'
                                                 f'км,Давление {ceil(float(ref / 1.33245033213))} '
                                                 f'мм.рт.ст,Закат начинается в {minute.lstrip()} '
                                                 f'Рассвет {minute2.rstrip()},'
                                                 f'\nПоследняя проверка погоды осуществлялась в {ref_time}',

                                            fg='gold', bg='SteelBlue4', width=200, height=10, foreground='gold',
                                            borderwidth=2, activeforeground='SteelBlue', font=("Rockwell", 17),
                                            justify='center')
                        sleep(0.1)

                        temperature.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)

                        win = round(number=float(str(windy).split()[1].replace(',', '')))

                        JsonWeather = [{f'Weather_type in {inputs["text"]}': result.detailed_status,
                                        'feels_like': f'{round(number=feels_like)}˚C',
                                        'max_temp': f'{round(number=max_temp)}˚C',
                                        'min_temp': f'{round(number=min_temp)}˚C',
                                        'cel_temp': f'{round(cel["temp"])}˚',
                                        'humidity': f'{round(number=humidity)}%',
                                        'windy_speed': f'{int(round(number=win))}m/s',
                                        'clouds': f'{round(number=clouds)}%',
                                        'visibility_distance': f'{round(number=wis / 1000)}km',
                                        'pressure': f'{round(number=float(ref / 1.33245033213))}mmHg',
                                        'sunrise': minute2.rstrip(),
                                        'sunset': minute.lstrip(),
                                        'ref_time': str(ref_time).strip()}]
                        sleep(0.1)
                        with open(file='weather.json', mode='a', encoding='utf-8') as file:
                            file.writelines('\n' + str(JsonWeather) + '\t\n')

                        with open(file='weather.json', mode='w', encoding='utf-8') as file_js:
                            file_js.seek(0)
                            json.dump(JsonWeather, file_js, indent=2, ensure_ascii=False)

                        def building_map():
                            sleep(0.5)

                            tk2 = Toplevel(tk)
                            tk2['bg'] = 'mint cream'
                            label_for_map = LabelFrame(tk2, foreground='gray')
                            label_for_map.pack(pady=20, padx=10)
                            tk_map = TkinterMapView(label_for_map, width=425, height=350, corner_radius=0)

                            tk_map.set_position(deg_x=float(lat_), deg_y=float(lot_))

                            tk_map.set_marker(deg_x=float(lat_), deg_y=float(lot_),
                                              text=str(f'{text + "-" + result.detailed_status}'
                                                       f',{round(number=cel["temp"])}°С'))

                            tk_map.set_zoom(zoom=9)

                            tk_map.pack(anchor=SW, expand=0, fill=BOTH)

                        b15 = Button(tk, text=f'Показать город {text} на карте', command=building_map
                                     , font=('Rockwell', 12)
                                     , fg='gold', bg='SteelBlue4',
                                     foreground='SteelBlue4', background='SteelBlue4',
                                     width=190, highlightbackground='gold')
                        b15.pack(fill=BOTH, pady=2,
                                 padx=2, anchor=NW)
                        b15.lift()

                        def remove():

                            temperature.destroy()
                            b15.destroy()
                            b2.destroy()
                            return temperature, b15, b2

                        b2 = Button(tk, text='Скрыть результат поиска', command=remove,
                                    font=('Rockwell', 12), fg='gold', bg='SteelBlue4',
                                    foreground='SteelBlue4', background='SteelBlue4',
                                    width=190, highlightbackground='gold')

                        b2.pack(fill=BOTH, pady=2,
                                padx=2, anchor=NW)

                    except exceptions.NotFoundError or exceptions.TimeoutError.__basicsize__ or ConnectTimeout \
                            or ConnectionError \
                            or HTTPSConnection or MaxRetryError:

                        filterwarnings('ignore')
                        filterwarnings('ignore', category=DeprecationWarning)

                        filterwarnings('ignore', category=FutureWarning)
                        filterwarnings('ignore', category=Warning)

                        response_error2 = Label(tk,
                                                text=f'\nГород- {str(inputs["text"]).strip()}'
                                                     f' не найден , введите верное '
                                                     f' название'
                                                     f'города!\n',
                                                background='gold', fg='gold', bg='SteelBlue4',
                                                borderwidth=2, font=('Rockwell', 14),
                                                highlightbackground='gold', width=190, underline=True,
                                                takefocus=True, height=4)

                        response_error2.pack(anchor=NW, fill=BOTH, side=TOP)

                        def remove():
                            response_error2.destroy()
                            b199.destroy()
                            return response_error2, b199

                        b199 = Button(tk, text='Скрыть ошибку', command=remove,
                                      fg='SteelBlue4', bg='SteelBlue4',
                                      foreground='SteelBlue4', background='SteelBlue4',
                                      highlightbackground='gold', state='normal', font=('Rockwell', 12))
                        b199.pack(fill=BOTH, pady=2, padx=2)

                elif not inputs['text']:

                    none_error2 = Label(tk, text='\nПожалуйста ,введите хотя бы что-то !\n', fg='gold',
                                        bg='SteelBlue4', borderwidth=2, state='normal',
                                        justify='center', font=('Rockwell', 14), background='SteelBlue4',
                                        highlightbackground='gold', width=190, height=4)
                    none_error2.pack(anchor=NW,
                                     fill=NONE, padx=2, pady=2, side=TOP)

                    def remove():
                        b19.destroy()
                        none_error2.destroy()
                        none_error2.pack_forget()
                        return none_error2, b19

                    b19 = Button(tk, text='Скрыть ошибку', command=remove,
                                 fg='SteelBlue4', bg='SteelBlue4',
                                 foreground='SteelBlue4', background='gold',
                                 highlightbackground='gold', state='normal', width=190, font=('Rockwell', 12))

                    b19.pack(fill=BOTH, pady=2, padx=2, side=TOP)

            def clear():

                inputs['text'] = str(inputs.delete(0, END))

                return inputs['text']

            def today_weather():
                with open(file='weather.json', mode='w', encoding='utf-8') as del_file:
                    del_file.truncate()

                from tzwhere import tzwhere

                filterwarnings('ignore')
                filterwarnings('ignore', category=DeprecationWarning)

                filterwarnings('ignore', category=FutureWarning)
                filterwarnings('ignore', category=Warning)

                config_dict = get_default_config()
                config_dict['connection']['use_ssl'] = False
                config_dict['connection']["verify_ssl_certs"] = False

                text = ''
                inputs['text'] = inputs.get().strip()
                text += inputs['text']
                if inputs['text']:
                    try:

                        '''
                        здесь получаем данные о погоде
                        '''
                        config_dicts = get_default_config()
                        config_dicts['language'] = 'RU'
                        conf = get_default_config_for_subscription_type(name='professional')
                        owm = OWM(api_key=token, config=config_dicts and conf)
                        mgr = owm.weather_manager()
                        obs = mgr.weather_at_place(name=inputs['text'])
                        ready_weather = obs.weather
                        weather = obs.weather

                        cel = ready_weather.temperature('celsius')
                        feels_like = cel['feels_like']
                        max_temp = cel['temp_max']
                        ref = ready_weather.pressure['press']
                        min_temp = cel['temp_min']

                        humidity = ready_weather.humidity
                        lcl = mgr.weather_at_place(name=inputs['text']).location

                        mgr = owm.weather_manager()
                        locations_info = mgr.weather_at_place(name=inputs['text']).location
                        country = locations_info.to_dict()

                        # dict_ = owm.weather_manager().weather_at_place(name='krasnodar').to_dict()
                        # ref_time = formatting.timeformat(dict_['reception_time'], 'date')

                        lcl_ = location(location=text.strip())
                        lng_ = lcl_.latlng[1]
                        lat_ = lcl_.latlng[0]

                        lon = lcl.lon
                        lat = lcl.lat
                        windy = weather.wind()['speed']
                        wis = ready_weather.visibility_distance
                        clouds = weather.clouds

                        data_cur = datetime.datetime.now().strftime('%Y %m %d').strip()
                        ever_el = data_cur.split()

                        ref_time = weather.reference_time('date')

                        tzwhere = tzwhere.tzwhere()
                        timezone_str = tzwhere.tzNameAt(latitude=float(lat), longitude=float(lon))

                        loc = LocationInfo(name=country['country'], region=inputs["text"],
                                           timezone=timezone_str, latitude=float(lat), longitude=float(lon))

                        s = sunset(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                   tzinfo=loc.timezone)

                        s2 = sunrise(loc.observer,
                                     date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                     tzinfo=loc.timezone)

                        minute = datetime.datetime.fromisoformat(str(s)).strftime('%H:%M').strip()

                        minute2 = datetime.datetime.fromisoformat(str(s2)).strftime('%H:%M').strip()
                        temperature = Label(tk,
                                            text=f'       Погода в городе {str(inputs["text"])} сейчас '
                                                 f'{str(" - ") + str(ready_weather.detailed_status)}\n'
                                                 f'Погода ощущается как {round(number=feels_like)}°С  \n'
                                                 f'Максимальная температура {round(number=max_temp)}°С \n'
                                                 f'Минимальная температура {round(number=min_temp)}°С  \n'
                                                 f'Температура прямо сейчас {round(number=cel["temp"])}°С\n'
                                                 f'Влажность-{round(number=humidity)} %\n'
                                                 f'Скорость ветра-{round(number=windy)}м/с  \n'
                                                 f'Количество облаков-{round(number=clouds)}%\n'
                                                 f'Средний статистический показатель погоды за '
                                                 f'{datetime.datetime.now().year}.{datetime.datetime.today().month}'
                                                 f'.{datetime.datetime.now().day} число- {round(number=feels_like)}°С\n'
                                                 f'Видимость {round(number=wis / 1000)}км, '
                                                 f'Давление {ceil(float(ref / 1.33245033213))} '
                                                 f'мм.рт.ст,Закат начинается в {minute.lstrip()},'
                                                 f'Рассвет {minute2.rstrip()}'
                                                 f',\nПоследняя проверка погоды'
                                                 f' осуществлялась в {str(ref_time).strip()}',
                                            fg='gold', bg='SteelBlue4', width=200,
                                            height=10, foreground='gold',
                                            borderwidth=2, activeforeground='SteelBlue', font=("Rockwell", 17),
                                            justify='center')

                        temperature.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)

                        sleep(0.1)

                        win = round(number=float(str(windy).split()[0]))

                        JsonWeather = [{f'Weather_type in {jsons["city"]}': ready_weather.detailed_status,
                                        'feels_like': f'{round(number=feels_like)}˚C',
                                        'max_temp': f'{round(number=max_temp)}˚C',
                                        'min_temp': f'{round(number=min_temp)}˚C',
                                        'cel_temp': f'{round(cel["temp"])}˚',
                                        'humidity': f'{round(number=humidity)}%',
                                        'windy_speed': f'{int(round(number=win))}m/s',
                                        'clouds': f'{round(number=clouds)}%',
                                        'visibility_distance': f'{round(number=wis / 1000)}km',
                                        'pressure': f'{round(number=float(ref / 1.33245033213))}mmHg',
                                        'sunrise': minute2.rstrip(),
                                        'sunset': minute.lstrip(),
                                        'ref_time': str(ref_time).strip()}]
                        sleep(0.1)

                        with open(file='weather.json', mode='a', encoding='utf-8') as file:
                            file.writelines('\n' + str(JsonWeather) + '\t\n')

                        with open(file='weather.json', mode='w', encoding='utf-8') as file_js:
                            file_js.seek(0)
                            json.dump(JsonWeather, file_js, indent=2, ensure_ascii=False)

                        def building_map():
                            sleep(0.5)

                            tk2 = Toplevel(tk)
                            tk2['bg'] = 'mint cream'
                            label_for_map = LabelFrame(tk2, foreground='gray')
                            label_for_map.pack(pady=20, padx=10)
                            tk_map = TkinterMapView(label_for_map, width=425, height=350, corner_radius=0)

                            tk_map.set_position(deg_x=float(lat_), deg_y=float(lng_))

                            tk_map.set_marker(deg_x=float(lat_), deg_y=float(lng_),
                                              text=str(f'{text + "-" + ready_weather.detailed_status}'
                                                       f',{round(number=cel["temp"])}°С'))

                            tk_map.set_zoom(zoom=9)

                            tk_map.pack(anchor=SW, expand=0, fill=BOTH)

                        b17 = Button(tk, text=f'Показать город {text} на карте', command=building_map,
                                     fg='gold', bg='SteelBlue4',
                                     foreground='SteelBlue4', background='SteelBlue4',
                                     width=190, highlightbackground='gold', font=('Rockwell', 12))
                        b17.pack(fill=BOTH, pady=2,
                                 padx=2, anchor=NW)
                        b17.lift()

                        def remove():

                            temperature.destroy()
                            b15.destroy()
                            b17.destroy()
                            return temperature, b15, b17

                        b15 = Button(tk, text='Скрыть результат поиска', command=remove,
                                     font=('Rockwell', 12), fg='gold', bg='SteelBlue4',
                                     foreground='SteelBlue4', background='SteelBlue4',
                                     width=190, highlightbackground='gold')
                        b15.pack(fill=BOTH, pady=2,
                                 padx=2, anchor=NW)

                    except exceptions.NotFoundError or exceptions.TimeoutError or \
                            exceptions.TimeoutError.__basicsize__ \
                            or \
                            ConnectTimeout or \
                            ConnectionError or HTTPSConnection or MaxRetryError:

                        filterwarnings('ignore')
                        filterwarnings('ignore', category=DeprecationWarning)

                        filterwarnings('ignore', category=FutureWarning)
                        filterwarnings('ignore', category=Warning)

                        response_error = Label(tk,
                                               text=f'\nГород- {str(inputs["text"]).strip()} '
                                                    f'не найден , введите верное '
                                                    f'название'
                                                    f'города!\n',
                                               background='gold', fg='gold', bg='SteelBlue4',
                                               borderwidth=2, font=('Rockwell', 14),
                                               highlightbackground='gold', width=190, underline=True, takefocus=True,
                                               height=4)

                        response_error.pack(anchor=NW, fill=BOTH, side=TOP)

                        def remove():
                            response_error.destroy()
                            b4.destroy()
                            return response_error, b4

                        b4 = Button(tk, text='Скрыть ошибку', command=remove,
                                    fg='SteelBlue4', bg='SteelBlue4',
                                    foreground='SteelBlue4', background='SteelBlue4',
                                    highlightbackground='gold', state='normal')
                        b4.pack(fill=BOTH, pady=2, padx=2)

                elif not inputs['text']:

                    none_error = Label(tk, text='\nПожалуйста ,введите хотя бы что-то !\n', fg='gold',
                                       bg='SteelBlue4', borderwidth=2, state='normal',
                                       justify='center', font=('Rockwell', 14), background='SteelBlue4',
                                       highlightbackground='gold', width=190, height=4)
                    none_error.pack(anchor=NW,
                                    fill=X, padx=2, pady=2, side=TOP)

                    def remove():
                        b5.destroy()
                        none_error.destroy()
                        none_error.pack_forget()
                        return none_error, b5

                    b5 = Button(tk, text='Скрыть ошибку', command=remove,
                                font=('Rockwell', 12), fg='SteelBlue4', bg='SteelBlue4',
                                foreground='SteelBlue4', background='gold',
                                highlightbackground='gold', state='normal', width=190)

                    b5.pack(fill=BOTH, pady=2, padx=2, side=TOP)

            def __author__():

                tabs = open_new(url='https://github.com/Alexandro1112/')
                return tabs

            '''
            Ниже создание интерфейса,виджетов и т.д
            '''

            border = {
                "Made by 𝒜𝓁𝑒𝓍𝒜𝓃𝒹𝓇𝑜𝟣𝟣𝟣𝟤": RAISED,
            }

            for relief_name, relief in border.items():
                frame = Frame(tk, relief=relief, borderwidth=5, width=26, height=16, bg='gold2',
                              visual='truecolor', background='gold', takefocus=True, border=4
                              )
                frame.pack(side=TOP, anchor=SE)

                label = Label(master=frame, text=relief_name,
                              padx=-2, pady=4,
                              activeforeground='gold', takefocus=True, underline=True)
                label.pack(ipady=4, anchor=SE, expand=0)

            canvas = Canvas(tk, width=720, height=3, bg='SteelBlue4',
                            background='gold', takefocus=True,
                            selectforeground='SteelBlue')

            canvas.create_rectangle(-45, 240, 201, 203)

            canvas.pack(anchor=S, side=BOTTOM, fill=X)

            tk.title('Weather-Manager')
            tk.resizable(width=True, height=True)
            tk.geometry(newGeometry='720x1385')
            tk['bg'] = 'SteelBlue'

            b11 = Button(tk, text='Автор проекта на GitHub!', command=__author__, bg='gold',
                         foreground='gold', background='gold',
                         activeforeground='gold', activebackground='SteelBlue2',
                         font=('Rockwell', 12),
                         highlightbackground='SteelBlue4',

                         anchor=CENTER, width=21, default=NORMAL)

            b11.pack(side=TOP, anchor=E, expand=0)

            b12 = Button(tk, text='Удалить текст в поле ввода', command=clear, bg='blue',
                         foreground='gold', background='gold', activeforeground='gold',
                         activebackground='SteelBlue', font=('Arial Bold', 12),
                         highlightbackground='SteelBlue4', anchor=CENTER, width=25, height=2, fg='gold2')

            b12.pack(padx=0, pady=0, side=RIGHT and TOP, anchor=W, expand=False)

            b1 = Button(tk, text='Узнать погоду в регионе', bg='gold',
                        foreground='gold', background='gold',
                        activeforeground='gold', activebackground='SteelBlue1',
                        font=('Rockwell', 12), command=today_weather,
                        highlightbackground='SteelBlue4',
                        anchor=CENTER, width=26, height=2, justify='center', takefocus=True)
            b1.place(relx=0.350, rely=0.0886, anchor=NW)

            l1 = Label(tk, text="\t┏━━━━━━━━━━━━━━━━━━━┓\n"
                                "\t|   ↓Введите название города ниже↓    |\n"
                                "\t ┗━━━━━━━━━━━━━━━━━━━┛ ", bg='SteelBlue',
                       activebackground='gold', foreground='gold2',
                       highlightbackground='gold2', borderwidth=2, takefocus=True)

            l1.pack(side=LEFT and TOP, padx=4, pady=2, anchor=NW)

            b14 = Button(tk, text='Узнать погоду на завтра', command=tomorrows_weather, bg='blue',
                         foreground='gold', background='gold', activeforeground='gold',
                         activebackground='SteelBlue', font=('Rockwell', 12),
                         highlightbackground='SteelBlue4', anchor=CENTER, width=26, height=2, fg='gold2')

            b14.place(x=502, y=127)

            inputs = Entry(tk, width=24, background='gold', font=("Rockwell", 27),
                           selectborderwidth=3, selectforeground="gold4",
                           insertontime=3, relief=RAISED,
                           fg='SteelBlue3', state='normal', highlightcolor='SteelBlue', insertofftime=4, justify=LEFT,
                           takefocus=True, vcmd=NORMAL)

            inputs.pack(anchor=NW, side=TOP, pady=6, padx=4, expand=0)

            table_of_content = Label(tk, text='𝕎𝔼𝔸𝕋ℍ𝔼ℝ-𝕄𝔸ℕ𝔸𝔾𝔼ℝ', bg='SteelBlue', takefocus=True,
                                     activebackground='gold', foreground='gold2',
                                     highlightbackground='gold2', font=("Double Struck", 37))

            table_of_content.place(x=1.8, rely=0.03907, anchor=W)

            try:
                filterwarnings('ignore')
                filterwarnings('ignore', category=DeprecationWarning)

                filterwarnings('ignore', category=FutureWarning)
                filterwarnings('ignore', category=Warning)

                response = get(url='http://ip-api.com/json/')
                jsons = response.json(parse_constant=None)

            except requests.exceptions.ConnectionError or requests.exceptions.ConnectTimeout:

                break

            def yourself_region():
                with open(file='weather.json', mode='w', encoding='utf-8') as del_file:
                    del_file.truncate()

                if inputs['text']:

                    inputs['text'] = str(inputs.delete(0, END))

                else:

                    pass

                inputs['text'] += str(inputs.insert(0, jsons['city']))

                from tzwhere import tzwhere

                filterwarnings('ignore')
                filterwarnings('ignore', category=DeprecationWarning)

                filterwarnings('ignore', category=FutureWarning)
                filterwarnings('ignore', category=Warning)

                config_dict = get_default_config()
                config_dict['connection']['use_ssl'] = False
                config_dict['connection']['verify_ssl_certs'] = False

                config_dicts = get_default_config()
                config_dicts['language'] = 'RU'

                conf_obs = get_default_config_for_subscription_type(name='professional')
                owm = OWM(api_key=token, config=config_dicts and conf_obs)
                mgr = owm.weather_manager()
                obs = mgr.weather_at_place(name=f"{jsons['city']},{jsons['country']}")
                ready_weather = obs.weather

                loc = mgr.weather_at_coords(lat=float(jsons['lat']), lon=float(jsons['lon']))
                type_weather = loc.weather
                weather = obs.weather
                '''
                dict_ = owm.weather_manager().weather_at_place(name='krasnodar').to_dict()
                ref_time = formatting.timeformat(dict_['reception_time'], 'date')
                '''

                reg = owm.city_id_registry()

                list_city_info = reg.ids_for(jsons["city"], matching='like')

                lat = list_city_info[0][4]
                lon = list_city_info[0][5]

                lcl_ = location(location=jsons['city'].strip())
                lot_ = lcl_.latlng[1]
                lat_ = lcl_.latlng[0]

                cel = ready_weather.temperature('celsius')
                feels_like = cel['feels_like']
                max_temp = cel['temp_max']
                ref = ready_weather.pressure['press']

                min_temp = cel['temp_min']
                humidity = ready_weather.humidity
                windy = weather.wind()['speed']
                ref_time = weather.reference_time('date')

                wis = ready_weather.visibility_distance
                clouds = weather.clouds

                data_cur = datetime.datetime.now().strftime('%Y %m %d').strip()
                ever_el = data_cur.split()

                tzwhere = tzwhere.tzwhere()
                timezone_str = tzwhere.tzNameAt(latitude=float(lat), longitude=float(lon))

                loc = LocationInfo(name=jsons["city"], timezone=timezone_str,
                                   latitude=float(lat), longitude=float(lon), region=jsons['country'])

                s = sunset(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                           tzinfo=loc.timezone)

                s2 = sunrise(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                             tzinfo=loc.timezone)

                minute = datetime.datetime.fromisoformat(str(s)).strftime('%H:%M')

                minute2 = datetime.datetime.fromisoformat(str(s2)).strftime('%H:%M')

                temperatures = Label(tk,
                                     text=f'          Погода в {jsons["city"] + " "} '
                                          f'сейчас- {type_weather.detailed_status}        \n'
                                          f'Погода ощущается как {round(number=feels_like)}°С  \n'
                                          f'Максимальная температура {round(number=max_temp)}°С \n'
                                          f'Минимальная температура {round(number=min_temp)}°С  \n'
                                          f'Температура прямо сейчас {round(number=cel["temp"])}°С\n'
                                          f'Влажность-{round(number=humidity)} %\n'
                                          f'Скорость ветра-{round(number=windy.real)}м/с  \n'
                                          f'Количество облаков-{round(number=clouds)}%\n'
                                          f'Средний статистический показатель погоды за '
                                          f'{datetime.datetime.now().month}.{datetime.datetime.now().day} '
                                          f'число {round(number=cel["temp_min"])}°С\n'
                                          f'Видимость {round(number=wis / 1000)}км'
                                          f' Давление {ceil(float(ref / 1.33245033113))}'
                                          f'мм.рт.ст,Закат начинается в '
                                          f'{minute.lstrip()},Рассвет {minute2.rstrip()}\n'
                                          f'Последняя проверка погоды осуществлялась {str(ref_time).strip()}',
                                     fg='gold', bg='SteelBlue4', width=200, height=10, foreground='gold',
                                     borderwidth=2,
                                     activeforeground='SteelBlue', font=("Rockwell", 17), compound=TOP,
                                     activebackground='gold2')

                temperatures.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)

                sleep(0.1)
                win = round(number=float(str(windy).split()[0]))

                JsonWeather = [{f'Weather_type in {jsons["city"]}': type_weather.detailed_status,
                                'feels_like': f'{round(number=feels_like)}˚C',
                                'max_temp': f'{round(number=max_temp)}˚C',
                                'min_temp': f'{round(number=min_temp)}˚C',
                                'cel_temp': f'{round(cel["temp"])}˚',
                                'humidity': f'{round(number=humidity)}%',
                                'windy_speed': f'{int(round(number=win))}m/s',
                                'clouds': f'{round(number=clouds)}%',
                                'visibility_distance': f'{round(number=wis / 1000)}km',
                                'pressure': f'{round(number=float(ref / 1.33245033213))}mmHg',
                                'sunrise': minute2.rstrip(),
                                'sunset': minute.lstrip(),
                                'ref_time': str(ref_time).strip()}]
                sleep(0.1)

                with open(file='weather.json', mode='a', encoding='utf-8') as file:
                    file.writelines('\n' + str(JsonWeather) + '\t\n')

                with open(file='weather.json', mode='w', encoding='utf-8') as file_js:
                    file_js.seek(0)
                    json.dump(JsonWeather, file_js, indent=2, ensure_ascii=False)

                def building_map():

                    sleep(0.5)
                    tk2 = Toplevel(tk)
                    tk2['bg'] = 'mint cream'

                    label_for_map = LabelFrame(tk2, foreground='gray')
                    label_for_map.pack(pady=20, padx=10)

                    tk_map = TkinterMapView(label_for_map, width=425, height=350, corner_radius=0)

                    tk_map.set_position(deg_x=float(lat_), deg_y=float(lot_))

                    tk_map.set_marker(deg_x=float(lat_), deg_y=float(lot_),
                                      text=str(f'{jsons["city"] + "-" + ready_weather.detailed_status}'
                                               f',{round(number=cel["temp"])}°С'))

                    tk_map.set_zoom(zoom=9)

                    tk_map.pack(anchor=SW, padx=10, expand=0, fill=BOTH)

                b15 = Button(tk, text=f'Показать город {jsons["city"]} на карте', command=building_map,
                             fg='gold', bg='SteelBlue4',
                             foreground='SteelBlue4', background='SteelBlue4',
                             width=193, highlightbackground='gold', font=('Rockwell', 12))

                b15.pack(fill=BOTH, pady=2, padx=2, anchor=NW)
                b15.lift()

                def remove():
                    b4.destroy()
                    temperatures.destroy()
                    b15.destroy()

                b4 = Button(tk, text='Скрыть результат поиска', command=remove,
                            fg='SteelBlue4', bg='SteelBlue4',
                            foreground='SteelBlue4', background='SteelBlue4',
                            highlightbackground='gold', state='normal', activebackground='SteelBlue4',
                            font=('Rockwell', 12))

                b4.pack(fill=BOTH, pady=2, padx=2, anchor=S)
                return b4, temperatures, b15

            b13 = Button(tk, text='Узнать погоду в своем городе', bg='gold',
                         foreground='gold', background='gold',
                         activeforeground='gold', activebackground='SteelBlue1',
                         font=('Rockwell', 12), command=yourself_region,
                         highlightbackground='SteelBlue4',
                         anchor=CENTER, width=26, height=2, justify='center', takefocus=True)

            b13.place(relx=0.699, rely=0.09097)

            b18 = Button(tk, text='Узнать погоду в своем городе на завтра', bg='gold',
                         foreground='gold', background='gold',
                         activeforeground='gold', activebackground='SteelBlue1',
                         font=('Rockwell', 12), command=tomorrows_weather_in_yourself_region,
                         highlightbackground='SteelBlue4',
                         anchor=CENTER, width=32, height=2, justify='center', takefocus=True)

            b18.place(relx=0.638, rely=0.22)

            region = Label(text=f'Город, '
                                f'в котором вы проживаете-{jsons["city"]} '
                                f', Страна {jsons["country"]}\n',
                           bg='SteelBlue',
                           activebackground='SteelBlue3',
                           foreground='gold2',
                           highlightbackground='gold2',
                           takefocus=True, font=('Rockwell', 12))
            region.place(relx=0.213, rely=0.975)

            b_ex = Button(tk, text='Выйти', bg='gold',
                          foreground='gold', background='gold',
                          activeforeground='gold',
                          activebackground='SteelBlue',
                          font=('Rockwell', 12),
                          highlightbackground='SteelBlue',
                          anchor=CENTER, width=6, height=1,
                          justify='center', takefocus=True, command=exit)
            b_ex.place(x=650, y=777.5)

            try:

                image = ImageTk.PhotoImage(Image.open('sticker-png-python-logo-program.png'))

                panel_l = Label(tk, image=image,
                                bg='SteelBlue', takefocus=False)
                panel_l.place(x=470, y=3, height=65, width=65)

                image2 = ImageTk.PhotoImage(Image.open("ice_screenshot_20221010-201232-2-2.png"))

                panel_l = Label(tk, image=image2,
                                bg='SteelBlue', takefocus=False)
                panel_l.place(x=400, y=3, height=65, width=65)

            except FileNotFoundError:

                sleep(0.5)

                pprint(
                    'download png-sticker '
                    'png-python-logo-program.png and ice_screenshot_20221010-201232-2-2.png')
            else:
                mainloop()
                quit()


if __name__ == '__main__':
    sleep(0.5)
    main()
