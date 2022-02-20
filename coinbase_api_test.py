
import PySimpleGUI as sg
from pandas import value_counts

import nbp_req
import raport_generator

sg.theme('DarkAmber')   # Add a touch of color

def sg_main_window(): # Creation of main window

    layout = [ [sg.Text('Choose your exchange:'), sg.Combo(['Binance','Coinbase','Coinbase Pro','Revolut'], key='-exch-')],
            [sg.Text('Choose fiat currency:'), sg.Combo(['USD','EUR','PLN'], key='-curr-')],
            [sg.Text('Choose file with statements:'), sg.InputText(key='-filename-', visible = False), sg.FileBrowse(file_types=(("Comma Separated Value", "*.csv"),))],
            [sg.InputText(key='-date-', visible = False, enable_events = True), sg.CalendarButton('Calendar', target = '-date-', key = '-calendar-', format = '%Y-%m-%d', begin_at_sunday_plus = 1), sg.Checkbox('Dla potrzeb podatku', default = False, key = '-tax-')],
            [sg.Button('Generate'), sg.Button('Cancel')],
            [sg.Text('', key='-out-' ,visible = False), sg.Button('Exit', key='-exit-',visible = False) ]
            ]
    return sg.Window('Set-up your report', layout, finalize = True)

def sg_revolut_window(csv_revolut,str_curr):
    rows, layout = list(), list()
    i_index = 0
    for fiat in csv_revolut:
        row = list()
        for i_fiat in fiat:
            row += [sg.Text(i_fiat, size=(25, 3))]
        if i_index > 0:
            row += [sg.InputText(key='-rev-' + str(i_index - 1), size=(15,3)), sg.Combo(['USD','EUR','PLN'], key='-revcurr-' + str(i_index - 1),default_value=str_curr)]
        else:
            row += [sg.Text('Amount of fiat currency', size=(15,3)), sg.Text('Fiat currency \n(change if needed)',size=(15,3))]
        rows += [row]
        i_index += 1
    layout = [rows,[sg.Button('Save'),sg.Button('Cancel')]]
    return sg.Window('Revolut CSV Statement', layout, finalize = True)

# Create the main window
window_main, window_revolut = sg_main_window(), None
# Event Loop to process "events" and get the "values" of the inputs
while True:
    windows, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == '-exit-': # if user closes window or clicks cancel
        windows.close()
        if windows == window_revolut:
            window_revolut = None
        elif windows == window_main:
            break
    elif event == 'Generate':
        #try:
            str_curr = values['-curr-']
            f_filename = values['-filename-']
            str_exchange = values['-exch-']
            if str_exchange != 'Revolut':
                csv_rows = raport_generator.csv_pandas_report(f_filename, str_exchange, str_curr)
                if len(csv_rows) == 0:
                    sg.Popup('Empty raport', keep_on_top = True)
                else:
                    excel_output = raport_generator.excel_savefile(csv_rows,f_filename,str_exchange)
                    windows['-out-'].update('File generated. Name: {0} , currency: {1}'.format(excel_output, str_curr),visible=True)
            else:
                window_revolut = sg_revolut_window(raport_generator.csv_revolut_reader(f_filename, str_exchange, str_curr),str_curr)
            windows['-exit-'].update(visible = True)
        #except:
            #sg.Popup('Error is somewhere', keep_on_top = True)
    elif event == '-date-':
        if values['-curr-'] == '':
            sg.Popup('Currency has not been chosen', keep_on_top = True)
        else:
            print(nbp_req.nbp_exchange_rates(values['-date-'],values['-curr-'],values['-tax-']))
    elif event == 'Save':
        vals = []
        for i in range(int(len(values)/2)):
            vals.extend(values['-rev-' + str(i)])
        print(vals)
    
windows.close()