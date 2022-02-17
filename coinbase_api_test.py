
import PySimpleGUI as sg

import nbp_req
import raport_generator

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Choose fiat currency:'), sg.Combo(['USD','EUR','PLN'], key='-curr-')],
            [sg.Text('Choose your exchange:'), sg.Combo(['Binance','Coinbase','Coinbase Pro','Revolut'], key='-exch-')],
            [sg.Text('Choose file with statements:'), sg.InputText(key='-filename-', visible = False), sg.FileBrowse(file_types=(("Comma Separated Value", "*.csv"),))],
            [sg.InputText(key='-date-', visible = False, enable_events = True), sg.CalendarButton('Calendar', target = '-date-', key = '-calendar-', format = '%Y-%m-%d', begin_at_sunday_plus = 1), sg.Checkbox('Dla potrzeb podatku', default = False, key = '-tax-')],
            [sg.Button('Generate'), sg.Button('Cancel')],
            [sg.Text('', key='-out-' ,visible = False), sg.Button('Exit', key='-exit-',visible = False) ]
            ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == '-exit-': # if user closes window or clicks cancel
        break
    if event == 'Generate':
        #try:
            str_curr = values['-curr-']
            f_filename = values['-filename-']
            str_exchange = values['-exch-']
            csv_rows, csv_head = raport_generator.csv_loop_for_fiat(f_filename, str_exchange, str_curr)
            csv_output = raport_generator.csv_savefile(csv_rows,csv_head,f_filename)
            window['-out-'].update('File generated. Name: {0} , currency: {1}'.format(csv_output, str_curr),visible=True)
            window['-exit-'].update(visible = True)
        #except:
            print("You entered non currency value")
    if event == '-date-':
        if values['-curr-'] == '':
            sg.Popup('Currency has not been chosen', keep_on_top = True)
        else:
            print(nbp_req.nbp_exchange_rates(values['-date-'],values['-curr-'],values['-tax-']))

    
window.close()