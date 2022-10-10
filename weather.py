
#encoding: utf-8
from tkinter import *
from pyowm import OWM
from pyowm.commons import exceptions
from pyowm.utils.config import get_default_config
from pyowm.utils.config import get_default_config_for_subscription_type
from webbrowser import open_new_tab
from requests import get
import datetime
from math import ceil
from PIL import ImageTk, Image
tk = Tk('Weather-Meneger')
while True:
    try:
        from OWMTOKENs import token
    except ModuleNotFoundError:
        print(f'Sing up in https://openweathermap.org and getting API key!')
        break


    """
    Функция где прописываются условия,часть с реализацией распознания города и менеджмент по погоде
    """




    def clear():

        inputs['text'] = inputs.delete(first=f'-{len(inputs["text"]*len(inputs["text"]))}')
        return str(inputs)



    def button_response():
        text = ''.lower()
        inputs['text'] = inputs.get()
        text += inputs['text']
        if inputs['text']:
            try:
                ''''
                здесь получаем данные о погоде
                '''
                config_dicts = get_default_config()
                config_dicts['language'] = 'RU'
                conf = get_default_config_for_subscription_type('professional')
                owm = OWM(api_key=token,config=config_dicts and conf)

                mgr = owm.weather_manager()

                obs = mgr.weather_at_place(inputs['text'])
                ready_weather = obs.weather
                weather = obs.weather
                stauts = weather.detailed_status
                cel = ready_weather.temperature('celsius')
                feels_like = cel['feels_like']
                max_temp = cel['temp_max']
                ref = ready_weather.pressure['press']
                min_temp = cel['temp_min']
                humidity = ready_weather.humidity
                windy = weather.wind()['speed']
                wis = ready_weather.visibility_distance
                clouds = weather.clouds
                ref_time = weather.reference_time('iso')


                temperature = Label(tk,text=
                    f'       {str(inputs["text"]) + str("-")+str(stauts)}          \n'
                    f'Погода ощущается как {round(feels_like)}°С  \n'
                    f'Максимальная температура {round(max_temp)}°С \n'
                    f'Минимальная температура {round(min_temp)}°С  \n'
                    f'Температура прямо сейчас {round(cel["temp"])}°С\n'
                    f'Влажность-{round(humidity)} %\n'
                    f'Скорость ветра-{round(windy)}м/с  \n'
                    f'Количество облаков-{round(clouds)}%\n'
                    f'Средний статистический показатель погоды за '
                    f'{str(datetime.datetime.now().year)}.{datetime.datetime.now().month}.{datetime.datetime.now().day} число- {round(cel["temp_min"])} °С\n'
                    f'Видимость {round(wis/1000)}км, Давление {ceil(ref/1.33245033113)} мм.рт.ст\n'
                    f'Последняя проверка погоды {ref_time.strip()}'
                                    ,fg='gold', bg='SteelBlue4', width=200, height=11,foreground='gold',
                                     borderwidth=2,activeforeground='SteelBlue', font=("Arial Bold", 17),justify='center')

                temperature.pack(fill=BOTH,anchor=SW,ipadx=4,ipady=4,side=TOP)



                def remove():
                    temperature.destroy()
                    b2.destroy()
                    return temperature

                b2 = Button(tk, text='Скрыть результат поиска', command=remove,
                            font=200, fg='gold', bg='SteelBlue4',
                            foreground='SteelBlue4', background='SteelBlue4',
                            width=200,highlightbackground='gold')
                b2.pack(fill=BOTH,pady=2,
                        padx=2,anchor=NW)





            except exceptions.NotFoundError or exceptions.APIRequestError or exceptions.ParseAPIResponseError:
                response_error = Label(tk, text='\nПожайлуста , введите верное название города!\n',
                                       background='gold',fg='gold',bg='SteelBlue4',
                                       borderwidth=2, font=("Arial Bold", 17),
                                       highlightbackground='gold',width=200)
                response_error.pack(anchor=NW,
                                    fill=BOTH)

                def remove():
                    response_error.destroy()
                    b4.destroy()
                    return response_error

                b4 = Button(tk, text='Скрыть ошибку', command=remove,
                            fg='SteelBlue4', bg='SteelBlue4',
                            foreground='SteelBlue4', background='SteelBlue4',
                            highlightbackground='gold', state='normal')
                b4.pack(fill=BOTH, pady=2, padx=2)
















        else:

            void_error = Label(tk, text='\nПожайлуста ,введите хотя бы что-то !\n', fg='gold',
                                bg='SteelBlue4', borderwidth=2, state='normal',
                                justify='left', font=("Arial Bold", 17),background='SteelBlue4',
                                highlightbackground='gold',width=200)
            void_error.pack(anchor=NW,
                            fill=BOTH,padx=2,pady=2,side=TOP)

            def remove():
                b5.destroy()
                void_error.destroy()
                void_error.pack_forget()
                return void_error,b5
            b5 = Button(tk, text='Скрыть ошибку', command=remove,
                        font=200, fg='SteelBlue4', bg='SteelBlue4',
                        foreground='SteelBlue4', background='gold',
                        highlightbackground='gold',state='normal',width=200)

            b5.pack(fill=BOTH, pady=2, padx=2,side=TOP)


    def author():
        TAB=open_new_tab(url='https://github.com/Alexandro1112').imag
        return TAB


    """
    Ниже создание интерфейса,виджетов и т.д
    """

    border = {
        "Made by 𝒜𝓁𝑒𝓍𝒜𝓃𝒹𝓇𝑜𝟣𝟣𝟣𝟤": RAISED,
    }

    for relief_name, relief in border.items():
        frame = Frame(tk, relief=relief,borderwidth=5
                      ,width=26,height=15,bg='gold2',
                      visual='truecolor',class_='ds', background='gold',takefocus=True
                      )
        frame.pack(side=TOP,anchor=SE)



        label = Label(master=frame, text=relief_name,
                      padx=-2,pady=4)
        label.pack(ipady=4,anchor=SE)


    canvas = Canvas(tk, width=720 ,height=4, bg='SteelBlue4', background='gold2')
    canvas.create_rectangle(-45,230,200,200)
    canvas.pack(anchor=S,side=BOTTOM,fill=X)

    tk.title('Weather-Manager')
    tk.resizable(width=True,height=True)
    tk.geometry('720x1320')
    tk['bg'] = 'SteelBlue'








    b11 = Button(tk, text='Автор пректа  на  GitHub!', command=author, bg='gold',
                 foreground='gold', background='gold',
                 activeforeground='gold', activebackground='SteelBlue2',
                 font=('Arial Bold', 12),
    highlightbackground='SteelBlue4',
                 anchor=CENTER, width=21,default='normal')


    b11.pack(side=TOP,anchor=E)
    b12 = Button(tk, text='Удалить текст в поле ввода', command=clear, bg='blue',
                foreground='gold', background='gold', activeforeground='gold', activebackground='SteelBlue',
                font=('Arial Bold', 12),
     highlightbackground='SteelBlue4',
                anchor=CENTER, width=25, height=2, fg='gold2')
    b12.pack(padx=0, pady=0, side=RIGHT and TOP, anchor=W,expand=False )

    b1 = Button(tk, text='Узнать погоду в регионе', bg='gold',
                 foreground='gold', background='gold',
                 activeforeground='gold', activebackground='SteelBlue1',
                 font=('Arial Bold', 12), command=button_response,
                 highlightbackground='SteelBlue4',
                 anchor=CENTER, width=26, height=2, justify='center',takefocus=True)
    b1.place(relx=0.350, rely=0.09157, anchor=NW)


    L1 = Label(tk, text="\t┏━━━━━━━━━━━━━━━━━━━┓\n" 
                        "\t↓Введите название города ниже↓ \n"
                        "\t┗━━━━━━━━━━━━━━━━━━━┛ ",bg='SteelBlue',
               activebackground='gold',foreground='gold2',highlightbackground='gold2',borderwidth=2)
    L1.pack(side=LEFT and TOP,anchor=W,pady=1,padx=3)


    inputs = Entry(tk, width=26, background='gold', font=("Arial Bold", 26),
            selectborderwidth=3, selectforeground="gold4",
            insertontime=3,relief=SUNKEN,
            fg='SteelBlue3',state='normal',highlightcolor='SteelBlue')
    inputs.pack(anchor=NW,side=TOP,
                pady=6, padx=4,)


    Table_Of_Content = Label(tk,text='𝕎𝔼𝔸𝕋ℍ𝔼ℝ-𝕄𝔸ℕ𝔸𝔾𝔼ℝ',bg='SteelBlue',takefocus=True,
               activebackground='gold',foreground='gold2',
                highlightbackground='gold2',font=("Double Struck", 41))
    Table_Of_Content.place(relx=0.033,rely=0.03907,anchor=W)

    response = get(url='http://ip-api.com/json')
    jsons = response.json()


    def yorself_region():
        ''''
                        здесь получаем данные о погоде
                        '''
        config_dicts = get_default_config()
        config_dicts['language'] = 'RU'
        conf = get_default_config_for_subscription_type('professional')
        owm = OWM(api_key=token, config=config_dicts and conf)
        mgr = owm.weather_manager()
        obs = mgr.weather_at_place(jsons['city'])
        ready_wether = obs.weather
        weather = obs.weather
        stauts = weather.detailed_status
        cel = ready_wether.temperature('celsius')
        feels_like = cel['feels_like']
        max_temp = cel['temp_max']
        ref = ready_wether.pressure['press']
        min_temp = cel['temp_min']
        humidity = ready_wether.humidity
        windy = weather.wind()['speed']
        wis = ready_wether.visibility_distance
        clouds = weather.clouds
        ref_time = weather.reference_time('iso')


        temperatures = Label(tk, text=
                                     f'         {str(jsons["city"]) + str("-") + str(stauts)}          \n'
                                     f'Погода ощущается как {round(feels_like)}°С  \n'
                                     f'Максимальная температура {round(max_temp)}°С \n'
                                     f'Минимальная температура {round(min_temp)}°С  \n'
                                     f'Температура прямо сейчас {round(cel["temp"])}°С\n'
                                     f'Влажность-{round(humidity)} %\n'
                                     f'Скорость ветра-{round(windy)}м/с  \n'
                                     f'Количество облаков-{round(clouds)}%\n'
                                     f'Средний статистический показатель погоды за '
                                     f'{str(datetime.datetime.now().year)}.{datetime.datetime.now().month}.{datetime.datetime.now().day} число- {round(cel["temp_min"])} °С\n'
                                     f'Видимость {round(wis/1000)}км, Давление {ceil(ref/1.33245033113)} мм.рт.ст\n'
                                     f'Последняя проверка погоды {ref_time.strip()}'
                            , fg='gold', bg='SteelBlue4', width=200, height=11, foreground='gold',
                            borderwidth=2, activeforeground='SteelBlue', font=("Arial Bold", 17), compound='top')
        temperatures.pack(fill=BOTH, anchor=SW, ipadx=4, ipady=4, side=TOP)




        def remove():
            b4.destroy()
            temperatures.destroy()
        b4 = Button(tk, text='Скрыть результат поиска', command=remove,
                    fg='SteelBlue4', bg='SteelBlue4',
                    foreground='SteelBlue4', background='SteelBlue4',
                    highlightbackground='gold', state='normal')
        b4.pack(fill=BOTH, pady=2, padx=2)




    Region = Label(text=' ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n'
                                    f'|Город, в котором вы проживаете-{jsons["city"]} , Страна {jsons["country"]}|\n'
                                  f'┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛',bg='SteelBlue',
               activebackground='SteelBlue3',foreground='gold2',highlightbackground='gold2',width=0,height=2,takefocus=True)
    Region.place(relx=0.21,rely=0.94)


    b13 = Button(tk, text='Узнать погоду в своем городе', bg='gold',
                         foreground='gold', background='gold',
                         activeforeground='gold', activebackground='SteelBlue1',
                         font=('Arial Bold', 12), command=yorself_region,
                         highlightbackground='SteelBlue4',
                         anchor=CENTER, width=26, height=2,justify='center',takefocus=True)
    b13.place(relx=0.713, rely=0.0902)











    image = ImageTk.PhotoImage(Image.open("sticker-png-python-logo-programm.png"))
    panel = Label(tk, image=image,bg='SteelBlue',text='//\\',takefocus=False,highlightcolor='SteelBlue')
    panel.place(x=459,y=3,height=65,width=65)


    quit(code=mainloop())
'''
Update 1.0.0 version | 08.10.2022 | Was added first version Weather-Manager.Fixed bugs with connection error,Base exeptions.
Update 1.0.1 version | 10.10.2022 | Was added Python logotype.Changed styles of buttons.In label of weather information was added parametrs pressure.
'''
























