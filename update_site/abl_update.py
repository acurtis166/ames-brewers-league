import pandas as pd
import numpy as np
from datetime import datetime as dt
from json import dumps
from os import listdir
from ftplib import FTP
import secrets

file_name = 'AblData.xlsx'

# read excel file for competition data
df_c = pd.read_excel(file_name, sheet_name='Competitions')
# convert dataframe to list of dictionaries
competitions = df_c.to_dict('records')

# read excel file for entries data
df_e = pd.read_excel(file_name, sheet_name='Entries',
                     index_col='Date', parse_dates=True)
# replace NaN with empty string
df_e = df_e.replace(np.nan, '', regex=True)
# add year column
df_e['Year'] = pd.DatetimeIndex(df_e.index).year

# create leaderboards
leaderboards = []
for year, df_year_grp in df_e.groupby('Year'):
    leaderboard = {
        'Year': year,
        'Entries': []
    }
    for name, df_name_grp in df_year_grp.groupby('Name'):
        leaderboard['Entries'].append({
            'Name': name,
            'Points': df_name_grp['Points'].sum()
        })
    leaderboard['Entries'] = sorted(
        leaderboard['Entries'], key=lambda i: i['Points'], reverse=True)
    leaderboards.append(leaderboard)

# populate competition data
for competition in competitions:
    # get the date from the competition
    date = competition.get('Date')

    # query df_e for date
    df_e_comp = df_e.loc[date.strftime(r'%Y-%m-%d')]

    # convert df_e_comp to list of dicts
    entries = df_e_comp.to_dict('records')

    # find and set the winner
    winner = {'Points': 0}
    for entry in entries:
        # drop unnecessary data
        entry.pop('Date', None)
        entry.pop('Year', None)
        # set the winner to the current entry if highest points
        if entry['Points'] > winner['Points']:
            winner = entry
    competition['Winner'] = winner

    # set properties of competition
    competition['Entries'] = entries
    competition['FormattedDate'] = date.strftime(r'%B %Y')
    competition['Year'] = date.year

    # drop unnecessary data
    competition.pop('Date', None)
    competition.pop('BjcpYear', None)

# create minutes data from pdf files in minutes folder
minutes = []
for minute_file in listdir('..\\static\\minutes'):
    # construct date from file name
    date = dt.strptime(minute_file[0:-4], r'%Y-%m')
    minute = {
        'FileName': minute_file,
        'FormattedDate': date.strftime(r'%B %Y')
    }
    minutes.append(minute)

# prepare distinct years
distinct_years = df_e['Year'].unique().tolist()
distinct_years.sort(reverse=True)

# construct data dictionary
data = {
    'Competitions': competitions,
    'Leaderboards': leaderboards,
    'Minutes': sorted(minutes, key=lambda i: i['FileName'], reverse=True),
    'DistinctYears': distinct_years
}

# convert data object to json string and remove unnecessary spaces
json_str = dumps(data)\
    .replace('" ', '"')\
    .replace(' "', '"')\
    .replace(' :', ':')\
    .replace(': ', ':')\
    .replace(' {', '{')\
    .replace('} ', '}')

# write the json to a javascript file
data_js_path = '..\\static\\js\\data.js'
with open(data_js_path, 'w') as js_file:
    js_file.write('var Data = ' + json_str)

# perform ftp transfer of minutes and data
with FTP(secrets.site) as ftp:
    # login to ftp server
    ftp.login(secrets.username, secrets.password)

    # transfer the new data file
    ftp.cwd('static/js')
    ftp.storbinary('STOR ' + 'data.js', open(data_js_path, 'rb'))

    # check if any minutes files need to be transferred and transfer them
    minutes_dir = '..\\static\\minutes'
    ftp.cwd('../minutes')
    ftp_minutes = ftp.nlst()
    for fname in listdir(minutes_dir):
        if fname not in ftp_minutes:
            ftp.storbinary('STOR ' + fname,
                           open(minutes_dir + '\\' + fname, 'rb'))
