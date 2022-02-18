#import csv - for use with revolut csv
import os.path
import pandas as pd

import nbp_req
import time_manager

d_exchanges = { 'Binance': ['UTC_Time', 'Operation', 'Coin', 'Change'],
 'Coinbase': ['Timestamp', 'Transaction Type', 'Spot Price Currency', 'Total (inclusive of fees)'],
 'Coinbase Pro': ['time', 'type', 'amount/balance unit', 'amount'] }

l_transactions = ['Buy', 'match', 'fee', 'Transaction Related', 'Small assets exchange BNB']

l_fields = ['Exchange','Coin', 'Value', 'Transaction Date','Tax Date','Convert Rate','Converted Value']

def coinbase_csv_rebuild(csv_name):

    df = pd.read_csv(csv_name,skiprows=7)

    return df

def csv_pandas_report(csv_name, str_exchange, str_currency):
    
    l_report = list()

    if str_exchange == 'Coinbase':
        df = coinbase_csv_rebuild(csv_name)
    else:
        df = pd.read_csv(csv_name)

    df = df.loc[(df[d_exchanges[str_exchange][2]] == str_currency) & (df[d_exchanges[str_exchange][1]].isin(l_transactions))]
    
    l_contents = df.to_dict(orient='records')
    for l_content in l_contents:
        d_rows = dict()
        d_rows[l_fields[0]] = str_exchange
        d_rows[l_fields[1]] = l_content[d_exchanges[str_exchange][2]]
        d_rows[l_fields[2]] = l_content[d_exchanges[str_exchange][3]]
        d_rows[l_fields[3]] = time_manager.convert_to_local_time(l_content[d_exchanges[str_exchange][0]], str_exchange)
        d_rows[l_fields[5]], d_rows[l_fields[4]] = nbp_req.nbp_exchange_rates(d_rows[l_fields[3]],str_currency,True)
        d_rows[l_fields[6]] = abs(round(float(d_rows[l_fields[2]]) * float(d_rows[l_fields[5]]),2))
        l_report.append(d_rows)

    return l_report

def excel_savefile(l_content,excel_name,str_exchange):
    dirname = os.path.dirname(excel_name)
    excel_write_name = os.path.join(dirname,str_exchange + '_' + time_manager.return_timestamp() + '.xlsx')
    writer = pd.ExcelWriter(excel_write_name)
    df = pd.DataFrame.from_dict(l_content)
    df.to_excel(writer,index=False)
    writer.save()
    return excel_write_name

# for future use with revolut csv
'''
def csv_open(csv_name):

    csv_filename_open = open(csv_name)
    csv_fiat = csv.DictReader(csv_filename_open)

    return csv_fiat

def csv_loop_for_fiat(csv_name, str_exchange, str_currency):
    l_content= list(),
    if str_exchange == 'Coinbase':
        csv_name = coinbase_csv_rebuild(csv_name)
    csv_fiat = csv_open(csv_name)
    for d_row in csv_fiat:
        if d_row[d_exchanges[str_exchange][2]] == str_currency:
            d_rows = dict()
            if d_row[d_exchanges[str_exchange][1]] in l_transactions:
                d_rows[l_fields[0]] = str_exchange
                d_rows[l_fields[1]] = d_row[d_exchanges[str_exchange][2]]
                d_rows[l_fields[2]] = d_row[d_exchanges[str_exchange][3]]
                d_rows[l_fields[3]] = time_manager.convert_to_local_time(d_row[d_exchanges[str_exchange][0]], str_exchange)
                d_rows[l_fields[5]], d_rows[l_fields[4]] = nbp_req.nbp_exchange_rates(d_rows[l_fields[3]],str_currency,True)
                d_rows[l_fields[6]] = abs(round(float(d_rows[l_fields[2]]) * float(d_rows[l_fields[5]]),2))
                l_content.append(d_rows)
    return l_content, l_fields

def csv_savefile(content, fields, csvname, str_exchange):
    dirname = os.path.dirname(csvname)
    csv_filename_write = os.path.join(dirname,str_exchange + '_' + time_manager.return_timestamp() +'.csv')
    with open(csv_filename_write, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(content)
    return csv_filename_write
'''