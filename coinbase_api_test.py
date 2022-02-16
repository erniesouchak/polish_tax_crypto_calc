import requests
import PySimpleGUI as sg


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Choose fiat currency:'), sg.Combo(['USD','EUR','PLN'], key='-curr-')],
            [sg.Text('Enter crypto:'), sg.InputText(key='-input-')],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Text('You entered: ', key='-out-')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    url  = f"https://api.coinbase.com/v2/exchange-rates?currency={values['-input-']}"
    if event == 'Ok':
        try:
            input_text = values['-input-']
            curr = values['-curr-']
            rate = requests.get(url).json()['data']['rates'][curr]
            window['-out-'].update('You entered {0} and is worth {1} {2}'.format(input_text, rate, curr))
        except:
            print("You entered non currency value")
    
window.close()