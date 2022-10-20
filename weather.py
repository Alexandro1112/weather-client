# encoding: utf-8
from pprint import pprint
from time import sleep
import requests.exceptions
from tqdm import tqdm
from tkinter import *
import pyowm.commons.exceptions
from pyowm import OWM
from pyowm.commons import exceptions
from pyowm.utils.config import get_default_config
from pyowm.utils.config import get_default_config_for_subscription_type
from webbrowser import open_new, register
from requests import get
from urllib3.connection import HTTPSConnection
from requests.exceptions import ConnectTimeout, ConnectionError, JSONDecodeError
from pyowm.utils import timestamps
from math import ceil
from PIL import ImageTk, Image
from tkintermapview import TkinterMapView

tk = Tk()

try:
    from OWMTOKENs import token

except ModuleNotFoundError:

    pprint(f'Sing up in https://openweathermap.org and getting API key!')

for i in tqdm(range(100)):
    pass

    while True:

        def tomorrows_weather():

            text = ''.lower()
            inputs['text'] = inputs.get()
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

                    import datetime
                    import pytz
                    from tzwhere import tzwhere
                    from astral import LocationInfo
                    from astral.sun import sunset, sunrise

                    lat = lcl.lat
                    lon = lcl.lon

                    result = w.weather
                    windy = weather.wind()

                    wis = weather.visibility_distance
                    clouds = weather.clouds

                    data_cur = datetime.datetime.now().strftime('%Y %m %d')
                    ever_el = data_cur.split()

                    tzwhere = tzwhere.tzwhere()
                    timezone_str = tzwhere.tzNameAt(latitude=lat, longitude=lon)

                    loc = LocationInfo(timezone=timezone_str, latitude=jsons['lat'], longitude=jsons['lon'])

                    s = sunset(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                               tzinfo=loc.timezone)

                    s2 = sunrise(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                                 tzinfo=loc.timezone)

                    minute = datetime.datetime.fromisoformat(str(s)).strftime('%H:%M').strip()

                    minute2 = datetime.datetime.fromisoformat(str(s2)).strftime('%H:%M').strip()

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
                                             f' {datetime.datetime.today().month}'
                                             f'.{datetime.datetime.now().day + 1} число {round(number=feels_like)} °С\n'
                                             f'Видимость {round(number=wis / 1000)}'
                                             f'км,Давление {ceil(ref / 1.33245033213)} '
                                             f'мм.рт.ст,\nЗакат начинается в {minute.lstrip()} '
                                             f'Рассвет {minute2.lstrip()}',
                                        fg='gold', bg='SteelBlue4', width=200, height=10, foreground='gold',
                                        borderwidth=2, activeforeground='SteelBlue', font=("Arial Bold", 17),
                                        justify='center')
                    sleep(0.1)

                    temperature.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)
                    with open('weather', 'a', encoding='utf-8') as file:
                        file.write('\t' + str(temperature['text']).upper() + '\t\n')

                    def building_map():

                        tk2 = Toplevel(tk)
                        label_for_map = LabelFrame(tk2)
                        label_for_map.pack(pady=20)
                        tk_map = TkinterMapView(label_for_map, width=450, height=350, corner_radius=0)

                        tk_map.set_position(deg_x=lat, deg_y=lon)

                        tk_map.set_zoom(10)

                        marker = tk_map.set_marker(deg_x=lat, deg_y=lon,
                                                   text=str(f'{inputs["text"] + "-" + result.detailed_status},'
                                                            f'{round(number=cel["temp"])}°С'))
                        marker.set_position(deg_y=lon, deg_x=lat)

                        tk_map.pack(anchor=SW)

                    b15 = Button(tk, text=f'Показать город {inputs["text"]} на карте', command=building_map,
                                 font=200, fg='gold', bg='SteelBlue4',
                                 foreground='SteelBlue4', background='SteelBlue4',
                                 width=190, highlightbackground='gold')

                    b15.pack(fill=BOTH, pady=2,
                             padx=2, anchor=NW)

                    def remove():

                        temperature.destroy()
                        b15.destroy()
                        b2.destroy()
                        return temperature

                    b2 = Button(tk, text='Скрыть результат поиска', command=remove,
                                font=200, fg='gold', bg='SteelBlue4',
                                foreground='SteelBlue4', background='SteelBlue4',
                                width=190, highlightbackground='gold')
                    b2.pack(fill=BOTH, pady=2,
                            padx=2, anchor=NW)

                except exceptions.NotFoundError or exceptions.TimeoutError.__basicsize__ or ConnectTimeout or \
                        pyowm.commons.exceptions.InvalidSSLCertificateError or ConnectionError \
                        or HTTPSConnection or JSONDecodeError:

                    response_error2 = Label(tk,
                                            text=f'\nГород- {str(inputs["text"]).strip()} не найден , введите верное '
                                                 f' название'
                                                 f'города!\n',
                                            background='gold', fg='gold', bg='SteelBlue4',
                                            borderwidth=2, font=("Arial Bold", 17),
                                            highlightbackground='gold', width=190, underline=True, takefocus=True)

                    response_error2.pack(anchor=NW, fill=BOTH, side=TOP)

                    def remove():
                        response_error2.destroy()
                        b18.destroy()
                        return response_error2, b18

                    b18 = Button(tk, text='Скрыть ошибку', command=remove,
                                 fg='SteelBlue4', bg='SteelBlue4',
                                 foreground='SteelBlue4', background='SteelBlue4',
                                 highlightbackground='gold', state='normal')
                    b18.pack(fill=BOTH, pady=2, padx=2)

            elif not inputs['text']:

                none_error2 = Label(tk, text='\nПожалуйста ,введите хотя бы что-то !\n', fg='gold',
                                    bg='SteelBlue4', borderwidth=2, state='normal',
                                    justify='center', font=("Arial Bold", 17), background='SteelBlue4',
                                    highlightbackground='gold', width=190)
                none_error2.pack(anchor=NW,
                                 fill=NONE, padx=2, pady=2, side=TOP)

                def remove():
                    b19.destroy()
                    none_error2.destroy()
                    none_error2.pack_forget()
                    return none_error2, b19

                b19 = Button(tk, text='Скрыть ошибку', command=remove,
                             font=200, fg='SteelBlue4', bg='SteelBlue4',
                             foreground='SteelBlue4', background='gold',
                             highlightbackground='gold', state='normal', width=190)

                b19.pack(fill=BOTH, pady=2, padx=2, side=TOP)


        def clear():
            inputs['text'] = inputs.delete((len(inputs.get()) - 1))


        def today_weather():
            import datetime
            from tzwhere import tzwhere
            from astral import LocationInfo
            from astral.sun import sunset, sunrise

            text = ''.lower()
            inputs['text'] = inputs.get()
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

                    lon = lcl.lon
                    lat = lcl.lat
                    windy = weather.wind()['speed']
                    wis = ready_weather.visibility_distance
                    clouds = weather.clouds
                    data_cur = datetime.datetime.now().strftime('%Y %m %d')
                    ever_el = data_cur.split()

                    tzwhere = tzwhere.tzwhere()
                    timezone_str = tzwhere.tzNameAt(latitude=lat, longitude=lon)

                    loc = LocationInfo(name='SJC', timezone=timezone_str, latitude=jsons['lat'], longitude=jsons['lon'])

                    s = sunset(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
                               tzinfo=loc.timezone)

                    s2 = sunrise(loc.observer, date=datetime.date(int(ever_el[0]), int(ever_el[1]), int(ever_el[2])),
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
                                             f'.{datetime.datetime.now().day} число- {round(number=feels_like)} °С\n'
                                             f'Видимость {round(number=wis / 1000)}км, '
                                             f'Давление {ceil(ref / 1.33245033213)} '
                                             f'мм.рт.ст,\nЗакат начинается в {minute.lstrip()},'
                                             f'Рассвет {minute2.lstrip()} ', fg='gold', bg='SteelBlue4', width=200,
                                        height=10, foreground='gold',
                                        borderwidth=2, activeforeground='SteelBlue', font=("Arial Bold", 17),
                                        justify='center')

                    temperature.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)

                    sleep(0.1)

                    with open('weather', 'a', encoding='utf-8') as file:
                        file.write('\t' + str(temperature['text']).upper() + '\t\n')

                    def building_map():

                        tk2 = Toplevel(tk)
                        label_for_map = LabelFrame(tk2)
                        label_for_map.pack(pady=20)
                        tk_map = TkinterMapView(label_for_map, width=450, height=350,
                                                corner_radius=0)

                        tk_map.set_position(deg_x=lat, deg_y=lon)

                        tk_map.set_marker(deg_x=lat, deg_y=lon,
                                          text=str(f'{inputs["text"] + "-" + ready_weather.detailed_status}'
                                                   f',{round(number=cel["temp"])}°С'))

                        tk_map.set_zoom(10)

                        tk_map.pack(anchor=SW)

                    b17 = Button(tk, text=f'Показать город {inputs["text"]} на карте', command=building_map,
                                 font=200, fg='gold', bg='SteelBlue4',
                                 foreground='SteelBlue4', background='SteelBlue4',
                                 width=190, highlightbackground='gold')
                    b17.pack(fill=BOTH, pady=2,
                             padx=2, anchor=NW)

                    def remove():

                        temperature.destroy()
                        b15.destroy()
                        b17.destroy()
                        return temperature

                    b15 = Button(tk, text='Скрыть результат поиска', command=remove,
                                 font=200, fg='gold', bg='SteelBlue4',
                                 foreground='SteelBlue4', background='SteelBlue4',
                                 width=190, highlightbackground='gold')
                    b15.pack(fill=BOTH, pady=2,
                             padx=2, anchor=NW)

                except exceptions.NotFoundError or exceptions.TimeoutError or exceptions.TimeoutError.__basicsize__ or \
                        ConnectTimeout or \
                        pyowm.commons.exceptions.InvalidSSLCertificateError or ConnectionError or HTTPSConnection or \
                        JSONDecodeError:

                    response_error = Label(tk,
                                           text=f'\nГород- {str(inputs["text"]).strip()} не найден , введите верное '
                                                f'название'
                                                f'города!\n',
                                           background='gold', fg='gold', bg='SteelBlue4',
                                           borderwidth=2, font=("Arial Bold", 17),
                                           highlightbackground='gold', width=190, underline=True, takefocus=True)

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
                                   justify='center', font=("Arial Bold", 17), background='SteelBlue4',
                                   highlightbackground='gold', width=190)
                none_error.pack(anchor=NW,
                                fill=X, padx=2, pady=2, side=TOP)

                def remove():
                    b5.destroy()
                    none_error.destroy()
                    none_error.pack_forget()
                    return none_error, b5

                b5 = Button(tk, text='Скрыть ошибку', command=remove,
                            font=200, fg='SteelBlue4', bg='SteelBlue4',
                            foreground='SteelBlue4', background='gold',
                            highlightbackground='gold', state='normal', width=190)

                b5.pack(fill=BOTH, pady=2, padx=2, side=TOP)


        def __author__():

            tabs = open_new(url='https://github.com/Alexandro1112/')
            register(tabs)
            return tabs


        '''
        Ниже создание интерфейса,виджетов и т.д
        '''

        border = {
            "Made by 𝒜𝓁𝑒𝓍𝒜𝓃𝒹𝓇𝑜𝟣𝟣𝟣𝟤": RAISED,
        }

        for relief_name, relief in border.items():
            frame = Frame(tk, relief=relief, borderwidth=5, width=26, height=16, bg='gold2',
                          visual='truecolor', class_='ds', background='gold', takefocus=True
                          )
            frame.pack(side=TOP, anchor=SE)

            label = Label(master=frame, text=relief_name,
                          padx=-2, pady=4, activeforeground='gold', takefocus=True)
            label.pack(ipady=4, anchor=SE)

        canvas = Canvas(tk, width=720, height=3, bg='SteelBlue4', background='gold')
        canvas.create_rectangle(-45, 240, 201, 203)

        canvas.pack(anchor=S, side=BOTTOM, fill=X)

        tk.title('Weather-Manager')
        tk.resizable(width=True, height=True)
        tk.geometry('720x1380')
        tk['bg'] = 'SteelBlue'

        b11 = Button(tk, text='Автор проекта  на  GitHub!', command=__author__, bg='gold',
                     foreground='gold', background='gold',
                     activeforeground='gold', activebackground='SteelBlue2',
                     font=('Arial Bold', 12),
                     highlightbackground='SteelBlue4',

                     anchor=CENTER, width=21, default=NORMAL)

        b11.pack(side=TOP, anchor=E)
        b12 = Button(tk, text='Удалить текст в поле ввода', command=clear, bg='blue',
                     foreground='gold', background='gold', activeforeground='gold',
                     activebackground='SteelBlue', font=('Arial Bold', 12),
                     highlightbackground='SteelBlue4', anchor=CENTER, width=25, height=2, fg='gold2')
        b12.pack(padx=0, pady=0, side=RIGHT and TOP, anchor=W, expand=False)

        b1 = Button(tk, text='Узнать погоду в регионе', bg='gold',
                    foreground='gold', background='gold',
                    activeforeground='gold', activebackground='SteelBlue1',
                    font=('Arial Bold', 12), command=today_weather,
                    highlightbackground='SteelBlue4',
                    anchor=CENTER, width=26, height=2, justify='center', takefocus=True)
        b1.place(relx=0.350, rely=0.0896, anchor=NW)

        L1 = Label(tk, text="\t┏━━━━━━━━━━━━━━━━━━━┓\n"
                            "\t|   ↓Введите название города ниже↓    |\n"
                            "\t ┗━━━━━━━━━━━━━━━━━━━┛ ", bg='SteelBlue',
                   activebackground='gold', foreground='gold2', highlightbackground='gold2', borderwidth=2)

        L1.pack(side=LEFT and TOP, padx=4, pady=2, anchor=NW)

        b14 = Button(tk, text='Узнать погоду на завтра', command=tomorrows_weather, bg='blue',
                     foreground='gold', background='gold', activeforeground='gold',
                     activebackground='SteelBlue', font=('Arial Bold', 12),
                     highlightbackground='SteelBlue4', anchor=CENTER, width=26, height=2, fg='gold2')
        b14.place(x=502, y=131)

        inputs = Entry(tk, width=26, background='gold', font=("Arial Bold", 27),
                       selectborderwidth=3, selectforeground="gold4",
                       insertontime=3, relief=RAISED,
                       fg='SteelBlue3', state='normal', highlightcolor='SteelBlue', insertofftime=4, justify=LEFT)

        inputs.pack(anchor=NW, side=TOP, pady=6, padx=4, expand=0)

        Table_Of_Content = Label(tk, text='𝕎𝔼𝔸𝕋ℍ𝔼ℝ-𝕄𝔸ℕ𝔸𝔾𝔼ℝ', bg='SteelBlue', takefocus=True,
                                 activebackground='gold', foreground='gold2',
                                 highlightbackground='gold2', font=("Double Struck", 37))

        Table_Of_Content.place(x=1, rely=0.03909, anchor=W)
        try:

            response = get(url='http://ip-api.com/json')
            jsons = response.json(parse_constant=None, object_pairs_hook=None)

        except requests.exceptions.ConnectionError.__basicsize__ or requests.exceptions.ConnectTimeout.__basicsize__:

            break


        def yourself_region():
            import datetime
            from tzwhere import tzwhere
            from astral import LocationInfo
            from astral.sun import sunset, sunrise
            config_dicts = get_default_config()
            config_dicts['language'] = 'RU'

            conf = get_default_config_for_subscription_type(name='professional')
            owm = OWM(api_key=token, config=config_dicts and conf)
            mgr = owm.weather_manager()
            obs = mgr.weather_at_place(jsons['city'])
            ready_weather = obs.weather
            loc = mgr.weather_at_coords(lat=jsons['lat'], lon=jsons['lon'])
            type_weather = loc.weather
            weather = obs.weather

            cel = ready_weather.temperature('celsius')
            feels_like = cel['feels_like']
            max_temp = cel['temp_max']
            ref = ready_weather.pressure['press']

            min_temp = cel['temp_min']
            humidity = ready_weather.humidity
            windy = weather.wind()['speed']

            wis = ready_weather.visibility_distance
            clouds = weather.clouds

            data_cur = datetime.datetime.now().strftime('%Y %m %d')
            ever_el = data_cur.split()

            tzwhere = tzwhere.tzwhere()
            timezone_str = tzwhere.tzNameAt(latitude=jsons['lat'], longitude=jsons['lon'])

            loc = LocationInfo(name='SJC', timezone=timezone_str, latitude=jsons['lat'], longitude=jsons['lon'])

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
                                      f'число- {round(number=cel["temp_min"])}°С\n'
                                      f'Видимость {round(number=wis / 1000)}км, Давление {ceil(ref / 1.33245033113)}'
                                      f'мм.рт.ст,\nЗакат начинается в {minute.lstrip()},Рассвет {minute2.lstrip()}',
                                 fg='gold', bg='SteelBlue4', width=200, height=10, foreground='gold',
                                 borderwidth=2, activeforeground='SteelBlue', font=("Arial Bold", 17), compound=TOP)

            temperatures.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)

            sleep(0.1)

            with open('weather', 'a', encoding='utf-8') as file:
                file.write('\n' + str(temperatures['text']).upper() + '\t\n')

            def building_map():
                tk2 = Toplevel(tk)
                label_for_map = LabelFrame(tk2)
                label_for_map['bg'] = 'SteelBlue'
                label_for_map.grid()
                label_for_map.pack(pady=20)

                tk_map = TkinterMapView(label_for_map, width=450, height=350, corner_radius=0)

                tk_map.set_position(jsons['lat'], jsons['lon'])

                tk_map.set_marker(deg_x=jsons["lat"], deg_y=jsons["lon"],
                                  text=str(f'{jsons["city"] + "-" + type_weather.detailed_status},'
                                           f'{round(cel["temp"])}°С'))

                tk_map.set_zoom(10)

                tk_map.pack(anchor=SW)

            b15 = Button(tk, text=f'Показать город {jsons["city"]} на карте', command=building_map,
                         font=200, fg='gold', bg='SteelBlue4',
                         foreground='SteelBlue4', background='SteelBlue4',
                         width=190, highlightbackground='gold')

            b15.pack(fill=BOTH, pady=2, padx=2, anchor=NW)

            def remove():
                b4.destroy()
                temperatures.destroy()
                b15.destroy()

            b4 = Button(tk, text='Скрыть результат поиска', command=remove,
                        fg='SteelBlue4', bg='SteelBlue4',
                        foreground='SteelBlue4', background='SteelBlue4',
                        highlightbackground='gold', state='normal', activebackground='SteelBlue4')

            b4.pack(fill=BOTH, pady=2, padx=2, anchor=S)
            return b4, temperatures, b15


        b13 = Button(tk, text='Узнать погоду в своем городе', bg='gold',
                     foreground='gold', background='gold',
                     activeforeground='gold', activebackground='SteelBlue1',
                     font=('Arial Bold', 12), command=yourself_region,
                     highlightbackground='SteelBlue4',
                     anchor=CENTER, width=26, height=2, justify='center', takefocus=True)

        b13.place(relx=0.699, rely=0.09093)

        try:

            image = ImageTk.PhotoImage(Image.open('sticker-png-python-logo-programm.png'))
            panel_l = Label(tk, image=image, bg='SteelBlue', takefocus=False)
            panel_l.place(x=470, y=3, height=65, width=65)

            image2 = ImageTk.PhotoImage(Image.open("ice_screenshot_20221010-201232-2-2.png"))
            panel_l = Label(tk, image=image2, bg='SteelBlue', takefocus=False)
            panel_l.place(x=400, y=3, height=65, width=65)

        except FileNotFoundError:

            pprint(
                'download png-sticker '
                'png-python-logo-programm.png и ice_screenshot_20221010-201232-2-2.png')

        if __name__ == '__main__':
            quit(mainloop())
            continue

        '''
        Update 1.0.0 version | 08.10.2022 | Was added first version Weather-Manager.Fixed bugs with connection 
        error,Base exceptions.|
        Update 1.0.1 version | 10.10.2022 | Was added Python logotype.Changed styles of buttons.In label of weather 
        information was added parameters pressure.
        Update 1.0.2 version | 16.10.2022 | Was added Functions adding text in weather.txt.You can save this 
        weather forecast.|
        Update 1.0.3 version | 18.10.2022 | Was added weather-forecast on tomorrow.He is most 
        exact for weather observation.|
        Update 1.0.4 version | 20.10.2022 | Was added world-map with markers to denote weather at
         currently region.|
        '''
        # TODO;
        # 1)Add more weather-parametrs.
