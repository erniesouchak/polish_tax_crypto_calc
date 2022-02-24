
import PySimpleGUI as sg

import nbp_req
import raport_generator

class Report:

    def __init__(self, filename):
        self.filename = filename
        self._generated = False

    def setData(self, tuple_data):
        self.filepath, self.exchange, self.currency = tuple_data
    
    def getData(self, *bool):
        if bool:
            tuple_data = raport_generator.get_filename(self.filename,True), self.exchange, self.currency
        else:
            tuple_data = self.filepath, self.exchange, self.currency
        return tuple_data

    def getCurrency(self):
        return self.currency

    @property
    def generated(self):
        return self._generated
    
    @generated.setter
    def generated(self, bool):
        self._generated = bool

    def isRevolut(self):
        if self.exchange == 'Revolut':
            return True
        else:
            return False

    def setReportData(self, report_list):
        self.report_list = report_list

    def getReportData(self):
        return self.report_list


sg.theme('DarkAmber')   # Add a touch of color

l_currencies = ['USD','EUR','PLN']
l_report = []
l_data = []
l_csv_data = []

def sg_main_window(): # Creation of main window

    table = [[sg.Table(l_data,headings=['File','Exchange','Currency'],auto_size_columns=False,key='-table-')]]
    layout = [ [sg.Frame('List of files',table,visible=True,key='-frame1-')], [sg.Text('Choose your exchange:'), sg.Combo(['Binance','Coinbase','Coinbase Pro','Revolut'], key='-exch-')],
            [sg.Text('Choose fiat currency:'), sg.Combo(l_currencies, key='-curr-')],
            [sg.Text('Choose file with statements:'), sg.InputText(key='-filename-', enable_events=True, visible = False), sg.FileBrowse(file_types=(("Comma Separated Value", "*.csv"),),target='-filename-')],
            [sg.Button('Generate'), sg.Button('Cancel')],
            [sg.Button('Manage Revolut CSV',key='-manage-', visible = False)],
            [sg.Text('', key='-out-' ,visible = False), sg.Button('Exit', key='-exit-',visible = False) ]
            ]
    return sg.Window('Set-up your report', layout, finalize = True)

def sg_revolut_manager(l_revoluts): # Creation of all revolut files manager

    labels = [[raport_generator.get_filename(x,False) for ind, x in enumerate(cols) if ind == 0] for cols in l_revoluts]
    col2 = [[sg.Button(''.join(labels[i]), metadata = ''.join(labels[i]), key='-load-' + str(i))] for i in range(len(l_revoluts))]

    layout = [ [sg.Frame('List of loaded csv',col2)], [sg.Button('Exit', key='-manexit-')]]

    return sg.Window('Revolut CSV Manager', layout, finalize = True)

def sg_revolut_window(csv_revolut,str_curr): # Creation of individual csv file from revolut
    cols_1, cols_2, cols_3= list(), list(), list()
    i_index = 0
    wid = [18,15,12,7]
    for fiat in csv_revolut:
        col_1 = list()
        col_2 = list()
        col_3 = list()
        for j,i_fiat in enumerate(fiat):
            if i_index > 0:
                col_1 += [sg.Text(i_fiat, size = wid[j])]
            else:
                col_1 += [sg.Text(i_fiat, size = (wid[j],3))]
        if i_index > 0:
            col_2 += [sg.InputText(key='-rev-' + str(i_index - 1), size = 10)]
            col_3 += [sg.Combo(l_currencies, key='-rvcurr-' + str(i_index - 1),default_value=str_curr, size = 10, enable_events=True)]
        else:
            col_2 += [sg.Text('Amount of fiat currency', size = (10,3))]
            col_3 += [sg.Text('Fiat currency (change if needed)', size = (10,3))]
        cols_1 += [col_1]
        cols_2 += [col_2]
        cols_3 += [col_3]
        i_index += 1
    layout = [sg.Frame('Revolut CSV',cols_1),sg.Frame('Input values',cols_2),sg.Frame('Currency',cols_3)],[sg.Button('Save'),sg.Button('Cancel')]
    return sg.Window('Revolut CSV Statement', layout, finalize = True,resizable=True)

# Create the main window
window_main, window_revolut, window_manager = sg_main_window(), None, None
# Event Loop to process "events" and get the "values" of the inputs
while True:
    windows, event, values = sg.read_all_windows()
    print(event)
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == '-exit-' or event == '-manexit-': # if user closes window or clicks cancel
        print(l_csv_data)
        windows.close()
        if windows == window_revolut:
            window_revolut = None
        elif windows == window_manager:
            window_manager = None
        elif windows == window_main:
            break
    elif event == '-filename-':
        report = Report(raport_generator.get_filename(values['-filename-'],False))
        l_report += [report]
        r_data = (values['-filename-'],values['-exch-'],values['-curr-'])
        report.setData(r_data)
        l_newdata = [ " ".join(r.getData(True)) for r in l_report ] 
        windows['-table-'].update(values = l_newdata)
        rev_check = [ r for r in l_report if r.isRevolut() ]
        if not rev_check == '':
            windows['-manage-'].update(visible = True)
    elif event == 'Generate':
        #try:
        for i,j in enumerate(l_data):
            str_curr = l_data[i][2]
            f_filename = l_data[i][0]
            str_exchange = l_data[i][1]
            if str_exchange != 'Revolut':
                l_csv_data.append(raport_generator.csv_pandas_report(f_filename, str_exchange, str_curr))
                if len(l_csv_data) == 0:
                    sg.Popup('Empty raport', keep_on_top = True)
                else:
                    #excel_output = raport_generator.excel_savefile(csv_rows,f_filename,str_exchange)
                    windows['-out-'].update('File generated. Name: {0} , currency: {1}'.format("excel_output", str_curr),visible=True)
            else:
                if window_revolut is None:
                    window_revolut = sg_revolut_window(raport_generator.csv_revolut_reader(f_filename, str_exchange, str_curr),str_curr)
            windows['-exit-'].update(visible = True)
        #except:
            #sg.Popup('Error is somewhere', keep_on_top = True)
    elif event == '-manage-':
        rev_check = [r.getData() for r in l_report if r.isRevolut()]
        window_manager = sg_revolut_manager(rev_check)
    elif '-load-' in event:
        for r in l_report:
            if windows[event].metadata == r.filename:
                if window_revolut is None:
                    window_revolut = sg_revolut_window(raport_generator.csv_revolut_reader(r.getData()),r.getCurrency())
                    window_revolut.metadata = windows[event].metadata
                    break
    elif event == 'Save':
        revs = []
        revcurrs = []
        for k,v in values.items():
            if '-rev-' in k:
                revs.append(v)
            if '-rvcurr-' in k:
                revcurrs.append(v)
        for i in revcurrs:
            if not i in l_currencies:
                sg.Popup('Error in currencies')
                break
        else:
            for r in l_report:
                if window_revolut.metadata == r.filename and r.generated == False:
                    l_csv_data.append(raport_generator.csv_pandas_report(r.getData(), revcurrs, revs))
                    r.generated = True
                    print(r.generated)
                    window_revolut.close()
                    window_revolut = None
                    break

                
            #excel_output = raport_generator.excel_savefile(csv_rows,f_filename,str_exchange)



windows.close()