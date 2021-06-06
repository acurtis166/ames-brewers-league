"""Processes brewing competitions and meeting minutes into a JavaScript file. Updated/new files are uploaded via FTP to the web server."""

import pandas as pd
import datetime as dt
import os
import json
import ftplib

import secrets


def get_competition_df(filepath:str='data.xlsx'):
    """Read competition data from an Excel file into a DataFrame.

    Args:
        filepath (str, optional): The path to the Excel file. Defaults to 'data.xlsx'.

    Returns:
        DataFrame: Competitions data.
    """

    df = pd.read_excel(filepath, sheet_name='Competitions', index_col='Date', usecols=['Date', 'Style', 'Category'])
    df['Year'] = df.index.year
    df['Date'] = df.index.strftime('%Y-%m-%d')
    df['FormattedDate'] = df.index.strftime('%B %Y')
    return df


def get_entry_df(filepath:str='data.xlsx'):
    """Read competition entries data from an Excel file into a DataFrame.

    Args:
        filepath (str, optional): The path to the Excel file. Defaults to 'data.xlsx'.

    Returns:
        DataFrame: Competition entries data.
    """

    df = pd.read_excel(filepath, sheet_name='Entries', index_col='Date')
    df = df.fillna('')
    return df


def create_competitions(competition_df:pd.DataFrame, entry_df:pd.DataFrame):
    """Create dictionaries for each brewing competition.

    Args:
        competition_df (pd.DataFrame): The competitions data.
        entry_df (pd.DataFrame): The competition entries data.

    Returns:
        list[dict]: The dictionaries, one for each competition.
    """

    # convert dataframe to list of dictionaries
    comps = competition_df.to_dict('records')

    for comp in comps:
        # filter the entries for the competition date (also remove date property from comp)
        comp_entries = entry_df[entry_df.index == comp.pop('Date')]
        # convert the filtered entries to a list of dictionaries
        comp['Entries'] = comp_entries.to_dict('records')
        # check if there are any records, if so set the winner to the entry with the max points
        if len(comp['Entries']):
            comp['Winner'] = max(comp['Entries'], key=lambda e: e['Points'])
        else:
            comp['Winner'] = {}

    return comps


def create_leaderboards(entry_df:pd.DataFrame):
    """Create dictionaries for each year of brewing competitions.

    Args:
        entry_df (pd.DataFrame): The competition entries data.

    Returns:
        list[dict]: The dictionaries, one for each leaderboard year.
    """

    # sum entries by year and brewer, then group by the year
    yr_brewersums = entry_df.groupby([entry_df.index.year, 'Name'])\
        .sum()\
        .reset_index(level='Name')\
        .groupby('Date')

    # for each year grouping, create dictionaries for each brewer total
    leaderboards = []
    for yr, bsums in yr_brewersums:
        brewersums = bsums.sort_values('Points', ascending=False)\
            .to_dict('records')
        leaderboards.append({
            'Year': yr,
            'Entries': brewersums
        })

    return leaderboards


def create_minutes():
    """Create dictionaries for each meeting minutes file.

    Returns:
        list[dict]: The dictionaries, one for each meeting minutes file.
    """

    # create minutes data from pdf files in minutes folder
    minutes = []
    for minute_file in os.listdir('..\\static\\minutes'):
        # construct date from file name
        date = dt.datetime.strptime(minute_file[0:-4], r'%Y-%m')
        minutes.append({
            'FileName': minute_file,
            'FormattedDate': date.strftime(r'%B %Y')
        })
    
    return sorted(minutes, key=lambda m: m['FileName'], reverse=True)


def create_distinct_years(competition_df:pd.DataFrame):
    """Create a list of distinct years of brewing competitions.

    Args:
        competition_df (pd.DataFrame): The competitions data.

    Returns:
        list[int]: Distinct years of brewing competitions.
    """

    distinct_years = competition_df.Year.unique().tolist()
    return distinct_years[::-1]


def create_data_dict(competition_df:pd.DataFrame, entry_df:pd.DataFrame):
    """Create a container for serializing all data to JSON.

    Args:
        competition_df (pd.DataFrame): The competitions data.
        entry_df (pd.DataFrame): The competition entries data.

    Returns:
        dict: The entity to be serialized to JSON.
    """
    
    return {
        'Competitions': create_competitions(competition_df, entry_df),
        'Leaderboards': create_leaderboards(entry_df),
        'Minutes': create_minutes(),
        'DistinctYears': create_distinct_years(competition_df)
    }


def create_js_file(data:dict, filepath:str='..\\static\\js\\data.js'):
    """Create a JavaScript file with a variable called "Data" to contain all site data.

    Args:
        data (dict): The data container.
        filepath (str, optional): The path to the output file. Defaults to '..\static\js\data.js'.
    """

    # convert data object to a compact json string
    json_str = json.dumps(data, indent=None, separators=(',', ':'))
    # write the json to a javascript file
    with open(filepath, 'w') as f:
        f.write('var Data = ' + json_str)


def ftp_upload(path_to_index:str='..\\index.html', path_to_data:str='..\\static\\js\\data.js', path_to_minutes:str='..\\static\\minutes'):
    """Upload the new data file and new meeting minutes files to the web server.

    Args:
        path_to_data (str, optional): The path to the data file. Defaults to '..\static\js\data.js'.
        path_to_minutes (str, optional): The path to the minutes directory. Defaults to '..\static\minutes'.
    """
    
    with ftplib.FTP(secrets.site) as ftp:
        # login to ftp server
        ftp.login(secrets.username, secrets.password)

        # transfer the index.html file
        ftp.storbinary('STOR index.html', open(path_to_index, 'rb'))

        # transfer the data.js file
        ftp.cwd('static/js')
        ftp.storbinary('STOR data.js', open(path_to_data, 'rb'))

        # check if any minutes files need to be transferred and transfer them
        ftp.cwd('../minutes')
        ftp_minutes = ftp.nlst()
        for fname in os.listdir(path_to_minutes):
            if fname in ftp_minutes: continue

            fpath = os.path.join(path_to_minutes, fname)
            ftp.storbinary('STOR {}'.format(fname), open(fpath, 'rb'))


def main():
    """Run the program.
    
    -Collects data from an Excel file and the meeting minutes directory\n
    -Processes data into a JSON string\n
    -Outputs the data to a JavaScript file\n
    -Uploads index.html, the data.js file, and new meeting minutes to the web server
    """

    # get the competition and entries data
    comp_df = get_competition_df()
    entry_df = get_entry_df()

    # create the data dictionary
    data = create_data_dict(comp_df, entry_df)

    # serialize the data to JSON and write to JS file
    create_js_file(data)

    # upload files
    ftp_upload()


if __name__ == '__main__':
    main()
    print('Successfully uploaded files to {}'.format(secrets.site))