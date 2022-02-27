import os.path
import pandas as pd

import extras

d_exchanges = { 'Binance': ['UTC_Time', 'Operation', 'Coin', 'Change'],
 'Coinbase': ['Timestamp', 'Transaction Type', 'Spot Price Currency', 'Total (inclusive of fees)'],
 'CoinbasePro': ['time', 'type', 'amount/balance unit', 'amount'], 'Revolut': ['Completed Date', 'Description', 'Amount', 'Currency'] }

l_transactions = ['Buy', 'match', 'fee', 'Transaction Related', 'Small assets exchange BNB', 'Exchange to']

l_fields = ['Exchange','Coin', 'Value', 'Transaction Date','Tax Date','Convert Rate','Converted Value']

def check_float(val):
    try:
        val = float(val)
        return val
    except:
        return val

def coinbase_csv_rebuild(csv_name): # coinbase csv has extra empty rows

    df = pd.read_csv(csv_name,skiprows=7)

    return df

def open_statement(csv_tup, to_dict=True): # open csv file and reads needed info
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
        output = df.reset_index(drop=True)

    return output

def calc_val(x,y,exchange):
    if exchange == 'Coinbase':
        return -(round((x) * (y),2))
    else:
        return (round((x) * (y),2))


def csv_pandas_report(csv_tup, *args): # create list of dicts with data from csv's
    
    _, str_exchange, str_currency = csv_tup

    d_rows = pd.DataFrame()

    l_contents = open_statement(csv_tup,True)
        
    if not str_exchange == 'Revolut':   # non revolut csv
        l_exchange = [str_exchange for x in range(l_contents.shape[0])]
        d_rows[l_fields[0]] = l_exchange
        d_rows[l_fields[1]] = l_contents[d_exchanges[str_exchange][2]]
        d_rows[l_fields[2]] = l_contents[d_exchanges[str_exchange][3]]
        d_rows[l_fields[3]] = l_contents[d_exchanges[str_exchange][0]].map(lambda x: extras.convert_to_local_time(x, str_exchange))
        d_rows[[l_fields[5],l_fields[4]]] = [extras.nbp_exchange_rates(a,b,True) for a, b in zip(d_rows[l_fields[3]],d_rows[l_fields[1]])]
        d_rows[l_fields[6]] = calc_val(pd.to_numeric(d_rows[l_fields[2]]),pd.to_numeric(d_rows[l_fields[5]]),str_exchange)
    else:                               # revolut csv
        l_exchange = [str_exchange for x in range(l_contents.shape[0])]
        d_rows[l_fields[0]] = l_exchange
        if(len(args) > 0):
            #try:
                d_rows[l_fields[1]] = args[0]
                d_rows[l_fields[2]] = [x.replace(',','.') for x in args[1]]
            #except:
                print('Not a list!')
        d_rows[l_fields[3]] = l_contents[d_exchanges[str_exchange][0]].map(lambda x: extras.convert_to_local_time(x, str_exchange))
        d_rows[[l_fields[5],l_fields[4]]] = [extras.nbp_exchange_rates(a,b,True) for a, b in zip(d_rows[l_fields[3]],d_rows[l_fields[1]])]
        print(d_rows)
        d_rows[l_fields[6]] = calc_val(pd.to_numeric(d_rows[l_fields[2]]),pd.to_numeric(d_rows[l_fields[5]]),str_exchange)

    return d_rows

def excel_savefile(l_content,dirname): # generate file with report

    excel_write_name = os.path.join(dirname, 'Report_' + extras.return_timestamp() + '.xlsx')
    writer = pd.ExcelWriter(excel_write_name)
    df_report = pd.concat(l_content,ignore_index=True)
    new_df = pd.DataFrame()
    new_df['Bought crypto for:'] = [df_report.loc[df_report[l_fields[6]] <= 0,l_fields[6]].sum()]
    new_df['Sold crypto for:'] = [df_report.loc[df_report[l_fields[6]] >= 0,l_fields[6]].sum()]
    df_report.to_excel(writer, index = False, sheet_name='Details')
    new_df.to_excel(writer, index = False, sheet_name='Overall')
    writer.save()
    return excel_write_name

def csv_revolut_reader(csv_tup): # reader of revolut csv for gui purposes

    csv_rev = open_statement(csv_tup,False)

    return csv_rev

def get_filename(name,replace_space):
    if replace_space:
        return os.path.basename(name.replace(' ','_'))
    else:
        return os.path.basename(name)