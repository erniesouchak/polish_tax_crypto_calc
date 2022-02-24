import os.path
import pandas as pd

import nbp_req
import time_manager

d_exchanges = { 'Binance': ['UTC_Time', 'Operation', 'Coin', 'Change'],
 'Coinbase': ['Timestamp', 'Transaction Type', 'Spot Price Currency', 'Total (inclusive of fees)'],
 'Coinbase Pro': ['time', 'type', 'amount/balance unit', 'amount'], 'Revolut': ['Completed Date', 'Description', 'Amount', 'Currency'] }

l_transactions = ['Buy', 'match', 'fee', 'Transaction Related', 'Small assets exchange BNB', 'Exchange to']

l_fields = ['Exchange','Coin', 'Value', 'Transaction Date','Tax Date','Convert Rate','Converted Value']

def check_float(val):
    try:
        val = float(val)
        return val
    except:
        return val

def coinbase_csv_rebuild(csv_name):

    df = pd.read_csv(csv_name,skiprows=7)

    return df

def open_statement(csv_tup, to_dict=True):
    csv_name, str_exchange, str_currency = csv_tup
    df = pd.DataFrame()
    if not to_dict:
        df = pd.read_csv(csv_name)
        df = df[d_exchanges[str_exchange]]
        df[d_exchanges[str_exchange][2]] = df[d_exchanges[str_exchange][2]].apply(lambda x: '%.8f' % x)
        headers = [df.columns.tolist()]
        rows = df.values.tolist()
        output = headers + rows
    else:
        if str_exchange == 'Coinbase':
            df = coinbase_csv_rebuild(csv_name)
        else:
            df = pd.read_csv(csv_name)
        if not str_exchange == 'Revolut':
            df = df.loc[(df[d_exchanges[str_exchange][2]] == str_currency) & (df[d_exchanges[str_exchange][1]].isin(l_transactions))]
        output = df.to_dict(orient='records')

    return output


def csv_pandas_report(csv_tup, *args):
    
    csv_name, str_exchange, str_currency = csv_tup

    l_report = list()

    l_contents = open_statement(csv_tup,True)
    
    index = 0
    
    for l_content in l_contents:
        d_rows = dict()
        if not str_exchange == 'Revolut':
            d_rows[l_fields[0]] = str_exchange
            d_rows[l_fields[1]] = l_content[d_exchanges[str_exchange][2]]
            d_rows[l_fields[2]] = l_content[d_exchanges[str_exchange][3]]
            d_rows[l_fields[3]] = time_manager.convert_to_local_time(l_content[d_exchanges[str_exchange][0]], str_exchange)
            d_rows[l_fields[5]], d_rows[l_fields[4]] = nbp_req.nbp_exchange_rates(d_rows[l_fields[3]],str_currency,True)
            d_rows[l_fields[6]] = abs(round(float(d_rows[l_fields[2]]) * float(d_rows[l_fields[5]]),2))
            l_report.append(d_rows)
        else:
            d_rows[l_fields[0]] = str_exchange
            if(len(args) > 0):
                try:
                    d_rows[l_fields[1]] = args[0][index]
                    d_rows[l_fields[2]] = check_float(args[1][index])
                except:
                    print('Not a list!')
                    break
            d_rows[l_fields[3]] = time_manager.convert_to_local_time(l_content[d_exchanges[str_exchange][0]], str_exchange)
            if not d_rows[l_fields[1]] == 'PLN':
                d_rows[l_fields[5]],d_rows[l_fields[4]]= nbp_req.nbp_exchange_rates(d_rows[l_fields[3]],d_rows[l_fields[1]],True)
                d_rows[l_fields[6]] = abs(round(float(d_rows[l_fields[2]]) * float(d_rows[l_fields[5]]),2))
            else:
                d_rows[l_fields[6]] = d_rows[l_fields[2]]
            index += 1
            l_report.append(d_rows)

    return l_report

def excel_savefile(l_content,excel_name,str_exchange):
    dirname = os.path.dirname(excel_name)
    excel_write_name = os.path.join(dirname, str_exchange + '_' + time_manager.return_timestamp() + '.xlsx')
    writer = pd.ExcelWriter(excel_write_name)
    df = pd.DataFrame.from_dict(l_content)
    df.to_excel(writer, index = False)
    writer.save()
    return excel_write_name

def csv_revolut_reader(csv_tup):

    csv_rev = open_statement(csv_tup,False)

    return csv_rev

def get_filename(name,replace_space):
    if replace_space:
        return os.path.basename(name.replace(' ','_'))
    else:
        return os.path.basename(name)