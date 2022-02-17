import csv
import os.path
import pandas as pd

import nbp_req
import time_manager

def csv_open(csv_name):

    csv_filename_open = open(csv_name)
    csv_fiat = csv.DictReader(csv_filename_open)

    return csv_fiat

def csv_loop_for_fiat(csv_name, str_exchange, str_currency):
    l_content, l_fields = list(), list()
    csv_fiat = csv_open(csv_name)
    l_fields = ['Exchange','Coin', 'Value', 'Transaction Date','Tax Date','Convert Rate','Converted Value']
    for d_row in csv_fiat:
        if d_row[l_fields[1]] == str_currency:
            d_rows = dict()
            d_rows[l_fields[0]] = str_exchange
            d_rows[l_fields[1]] = d_row[l_fields[1]]
            d_rows[l_fields[2]] = d_row['Change']
            d_rows[l_fields[3]] = time_manager.convert_to_local_time(d_row['UTC_Time'])
            d_rows[l_fields[5]], d_rows[l_fields[4]] = nbp_req.nbp_exchange_rates(d_rows[l_fields[3]],str_currency,True)
            d_rows[l_fields[6]] = round(float(d_rows[l_fields[2]]) * float(d_rows[l_fields[5]]),2)
            l_content.append(d_rows)
    return l_content, l_fields

def csv_savefile(content, fields, csvname):
    dirname = os.path.dirname(csvname)
    csv_filename_write = os.path.join(dirname,'binance.csv')
    with open(csv_filename_write, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(content)
    return csv_filename_write