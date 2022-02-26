
import PySimpleGUI as sg

import raport_generator
import extras

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

    def getExchange(self):
        return self.exchange

    def getPath(self):
        return self.filepath

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

    def setRevolutgenerators(self, rev_revs, rev_currevs):
        self.rev_revs = rev_revs
        self.rev_currevs = rev_currevs

    def getRevolutgenerators(self):
        return self.rev_revs, self.rev_currevs


sg.theme('DarkAmber')   # Add a touch of color

l_currencies = ['USD','EUR','PLN']
l_report = []

def sg_main_window(): # Creation of main window

    table = [[sg.Table(l_report,headings=['File','Exchange','Currency'],auto_size_columns=False,key='-table-')]]
    layout = [ [sg.Frame('List of files',table,visible=True,key='-frame1-')], [sg.Text('Choose your exchange:'), sg.Combo(['Binance','Coinbase','Coinbase Pro','Revolut'], key='-exch-')],
            [sg.Text('Choose fiat currency:'), sg.Combo(l_currencies, key='-curr-')],
            [sg.Text('Add file with statements:'), sg.InputText(key='-filename-', enable_events=True, visible = True), sg.FileBrowse(file_types=(("Comma Separated Value", "*.csv"),),target='-filename-')],
            [sg.Button('Manage Revolut CSV',key='-manage-', visible = False)],
            [sg.Button('Generate', key='-generate-')],
            [sg.InputText(key='-out-',enable_events=True,visible=True),sg.FolderBrowse('Choose path', key='-path-',target = '-out-'), sg.Button('Exit', key='-exit-') ],
            [sg.Text('', key='-saved-',visible=False)]
            ]
    return sg.Window('Set-up your report', layout, finalize = True)

def sg_revolut_manager(l_revoluts): # Creation of all revolut files manager

    labels = [[raport_generator.get_filename(x,False) for ind, x in enumerate(cols) if ind == 0] for cols in l_revoluts]
    col2 = [[sg.Button(''.join(labels[i]), metadata = ''.join(labels[i]), key='-load-' + str(i))] for i in range(len(l_revoluts))]

    layout = [ [sg.Frame('List of loaded csv',col2)], [sg.Button('Exit', key='-manexit-')]]

    return sg.Window('Revolut CSV Manager', layout, finalize = True)

def sg_revolut_window(csv_revolut,str_curr,r): # Creation of individual csv file from revolut
    cols_1, cols_2, cols_3= list(), list(), list()
    i_index = 0
    wid = [18,15,12,7]
    if r.generated:
        revs,revscurr = r.getRevolutgenerators()
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
            if r.generated:
                col_2 += [sg.InputText(key='-rev-' + str(i_index - 1),default_text=revs[i_index - 1], size = 10)]
                col_3 += [sg.Combo(l_currencies, key='-rvcurr-' + str(i_index - 1),default_value=revscurr[i_index - 1], size = 10, enable_events=True)]
            else:
                col_2 += [sg.InputText(key='-rev-' + str(i_index - 1), size = 10)]
                col_3 += [sg.Combo(l_currencies, key='-rvcurr-' + str(i_index - 1),default_value=str_curr, size = 10, enable_events=True)]
        else:
            col_2 += [sg.Text('Amount of fiat currency', size = (10,3))]
            col_3 += [sg.Text('Fiat currency (change if needed)', size = (10,3))]
        cols_1 += [col_1]
        cols_2 += [col_2]
        cols_3 += [col_3]
        i_index += 1
    layout = [sg.Frame('Revolut CSV',cols_1),sg.Frame('Input values',cols_2),sg.Frame('Currency',cols_3)],[sg.Button('Save',key='-saverev-'),sg.Button('Cancel',key='-cancel-')]
    return sg.Window('Revolut CSV Statement', layout, finalize = True,resizable=True)

# Create the main window
window_main, window_revolut, window_manager = sg_main_window(), None, None
# Event Loop to process "events" and get the "values" of the inputs
while True:
    windows, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == '-cancel-' or event == '-exit-' or event == '-manexit-': # if user closes window or clicks cancel
        windows.close()
        if windows == window_revolut:
            window_revolut = None
        elif windows == window_manager:
            window_manager = None
        elif windows == window_main:
            break
    elif event == '-filename-': # fill the table in gui
        report = Report(raport_generator.get_filename(values['-filename-'],False))
        l_report += [report]
        r_data = (values['-filename-'],values['-exch-'],values['-curr-'])
        report.setData(r_data)
        l_newdata = [ " ".join(r.getData(True)) for r in l_report ] 
        windows['-table-'].update(values = l_newdata)
        rev_check = [ r for r in l_report if r.isRevolut() ]
        if rev_check:
            windows['-manage-'].update(visible = True)
        windows['-filename-'].update(value='')
    elif event == '-generate-': # generate report from non-revolut statements
        start_time = extras.timelapse()
        for r in l_report:
            if not r.isRevolut():
                r.setReportData(raport_generator.csv_pandas_report(r.getData()))
                r.generated = True
        end_time = extras.timelapse()
        print(extras.count_time(start_time,end_time))
    elif event == '-out-': # save generated report in folder chosen by user
        list_report = [r.getReportData() for r in l_report]
        excel_output = raport_generator.excel_savefile(list_report,values['-out-'])
        windows['-saved-'].update(excel_output,visible=True)
    elif event == '-manage-': # generate gui manager for revolut csv
        rev_check = [r.getData() for r in l_report if r.isRevolut()]
        window_manager = sg_revolut_manager(rev_check)
    elif '-load-' in event: # generate gui manager for individual revolut csv
        for r in l_report:
            if windows[event].metadata == r.filename:
                if window_revolut is None:
                    window_revolut = sg_revolut_window(raport_generator.csv_revolut_reader(r.getData()),r.getCurrency(),r)
                    window_revolut.metadata = windows[event].metadata
                    break
    elif event == '-saverev-': # save extra fills for revolut csv's
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
                if window_revolut.metadata == r.filename:
                        r.setRevolutgenerators(revs,revcurrs)
                        r.setReportData(raport_generator.csv_pandas_report(r.getData(), revcurrs, revs))
                        r.generated = True
                        window_revolut.close()
                        window_revolut = None
                        break
            
windows.close()