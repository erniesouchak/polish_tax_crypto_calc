
import nbp_req
import PySimpleGUI as sg
import csv
import os.path


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Choose fiat currency:'), sg.Combo(['USD','EUR','PLN'], key='-curr-')],
            [sg.Text('Choose your exchange:'), sg.Combo(['Binance','Coinbase','Coinbase Pro','Revolut'], key='-exch-')],
            [sg.Text('Choose file with statements:'), sg.InputText(key='-filename-', visible = False), sg.FileBrowse(file_types=(("Comma Separated Value", "*.csv"),))],
            [sg.InputText(key='-date-', visible = False, enable_events = True), sg.CalendarButton('Calendar', target = '-date-', key = '-calendar-', format = '%Y-%m-%d', begin_at_sunday_plus = 1), sg.Checkbox('Dla potrzeb podatku', default = False, key = '-tax-')],
            [sg.Button('Generate'), sg.Button('Cancel')],
            [sg.Text('', key='-out-' ,visible = False)] ]

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
            rows[fields[2]] = nbp_req.convert_to_local_time(row['UTC_Time'])
            content.append(rows)
    return content, fields

def csv_savefile(content, fields, csvname):
    dirname = os.path.dirname(csvname)
    csv_filename_write = os.path.join(dirname,'binance.csv')
    with open(csv_filename_write, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(content)
    return csv_filename_write

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Generate':
        #try:
            curr = values['-curr-']
            filename = values['-filename-']
            csv_rows, csv_head = csv_loop_for_fiat(filename)
            csv_output = csv_savefile(csv_rows,csv_head,filename)
            window['-out-'].update('File generated. Name: {0} , currency: {1}'.format(csv_output, curr),visible=True)
        #except:
            print("You entered non currency value")
    if event == '-date-':
        if values['-curr-'] == '':
            sg.Popup('Currency has not been chosen', keep_on_top = True)
        else:
            print(nbp_req.nbp_exchange_rates(values['-date-'],values['-curr-'],values['-tax-']))

    
window.close()