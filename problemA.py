import PySimpleGUI as sg

# listas para 2a janela
list_min=[*range(0,60,1)]
list_hour=[*range(0,24,1)]
list_freq=['Daily', 'Weekly', 'Monthly', 'Yearly']

# layout 1a janela
def login():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Login', font=('Courier 20'))],
        [sg.Text('')],
        [sg.Text('Email'), sg.Input(key= 'user', size=(20, 1))],
        [sg.Text('Password'), sg.Input(key= 'password', password_char='*', size=(20, 1))],
        [sg.Button('Enter')]
    ]
    return sg.Window('Login', layout=layout, finalize=True)

# layout 2a janela
def to_do():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Planner', font = 'Courier 20')],
        [sg.Text('')],
        [sg.Text('Event:'), sg.Input(key= 'event', size=(25, 1))],
        [sg.Text('Date:'), sg.Button('Date')],
        [sg.Text('Time:'), sg.Spin(list_hour, readonly=True, size=(3,1), key='hour'),sg.Text('h'),
            sg.Spin(list_min, readonly=True, size=(3,1), key='minute'), sg.Text('m')],
        [sg.Text('Frequency:'), sg.Combo(list_freq, readonly=True,size=(9,1),key='freq')],
        [sg.Button('ADD EVENT', size=(25,2))]
    ]
    return sg.Window('Tasks', layout=layout, finalize=True)

# Mostrar janela 1, esconder janela 2
window1, window2 = login(), None

while True:
    # ler interações
    window, events, values = sg.read_all_windows()

    # fechar janela
    if (window == window1 or window == window2) and events == sg.WINDOW_CLOSED:
        break

    # mudar da 1a para a 2a
    if window == window1 and events == 'Enter':
        user = values['user'] # guardar utilizador para usar na próxima janela
        window1.hide()
        window2 = to_do()

    # Calendario
    if window == window2 and events == 'Date':
        date_in_tuple = sg.popup_get_date()

        if date_in_tuple == None:
            sg.popup('No date was chosen')
        else:
            # Data em str
            day = str(date_in_tuple[1])
            month = str(date_in_tuple[0])
            year = str(date_in_tuple[2])

    # botão 'ADD EVENT'
    if window == window2 and events == 'ADD EVENT':
        if values['event']=='' or values['hour']=='' or values['minute']=='' or day == 0 or month == 0 or year == 0:
            sg.popup('Blank Boxes')

        elif int(values['hour']) >23 or int(values['minute']) > 59:
            sg.popup('Invalid Time')

        elif day == 0:
            sg.popup('No date was chosen')

        else:
            if values['hour'] < 10:
                values['hour'] = str(values['hour'])
                values['hour'] = '0'+ values['hour']
            if values['minute'] < 10:
                values['minute'] = str(values['minute'])
                values['minute'] = '0'+ values['minute']

            sg.popup('Event: ' + values['event'], 
                        'Date: ' + day +'/'+ month +'/'+ year, 
                        'Hour: ' + str(values['hour']) +"h" + str(values['minute']),
                        'Frequency: ' + values['freq']
                )