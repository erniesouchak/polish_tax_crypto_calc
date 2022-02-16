import requests
import PySimpleGUI as sg
import csv
import os.path


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Choose fiat currency:'), sg.Combo(['USD','EUR','PLN'], key='-curr-')],
            [sg.Text('Enter crypto:'), sg.InputText(key='-input-')],
            [sg.InputText(key='-filename-', visible = False), sg.FileBrowse(file_types=(("Comma Separated Value", "*.csv"),))],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Text('You entered: ', key='-out-')] ]

def csv_loop_for_fiat(csvname):
    content, fields = list(), list()
    csv_filename_open = open(csvname)
    csv_fiat = csv.DictReader(csv_filename_open)
    fields = ['Coin', 'Value', 'Date']
    for row in csv_fiat:
        if row[fields[0]] == 'EUR':
            rows = dict()
            rows[fields[0]] = row['Coin']
            rows[fields[1]] = row['Change']
            rows[fields[2]] = row['UTC_Time']
            content.append(rows)
    print(content)
    return content, fields

def csv_savefile(content, fields, csvname):
    dirname = os.path.dirname(csvname)
    csv_filename_write = os.path.join(dirname,'binance.csv')
    with open(csv_filename_write, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(content)

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    url  = f"https://api.coinbase.com/v2/exchange-rates?currency={values['-input-']}"
    if event == 'Ok':
        #try:
            input_text = values['-input-']
            curr = values['-curr-']
            rate = requests.get(url).json()['data']['rates'][curr]
            filename = values['-filename-']
            csv_rows, csv_head = csv_loop_for_fiat(filename)
            csv_savefile(csv_rows,csv_head,filename)
            window['-out-'].update('You entered {0} and is worth {1} {2}'.format(input_text, rate, curr))
        #except:
            print("You entered non currency value")

    
window.close()