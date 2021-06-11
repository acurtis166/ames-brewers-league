"""Processes brewing competitions and meeting minutes into JSON files."""

import pandas as pd
import datetime as dt
import os
from pathlib import Path
import json


def get_competition_df(filepath:str='data.xlsx'):
    """Read competition data from an Excel file into a dict of {year (int): DataFrame}.

    Args:
        filepath (str, optional): The path to the Excel file. Defaults to 'data.xlsx'.

    Returns:
        dict: Competitions data grouped into years. Keys are the years of competitions and values are DataFrames.
    """

    df = pd.read_excel(filepath, sheet_name='Competitions', index_col='Date', usecols=['Date', 'Style', 'Category'])
    df['Year'] = df.index.year
    df['Date'] = df.index.strftime('%Y-%m-%d')
    df['Month'] = df.index.strftime('%B')
    yr_grps = {yr: g for yr, g in df.groupby(df.index.year)}
    return yr_grps


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


def create_brewer_totals(entry_df:pd.DataFrame):
    """Create dictionaries of brewer leaderboard standings.

    Args:
        entry_df (pd.DataFrame): The competition entries data.

    Returns:
        list[dict]: The dictionaries, one for each brewer total.
    """

    # create totals for each brewer
    brewersums = entry_df\
        .groupby('Name')\
        .sum()\
        .reset_index()\
        .sort_values('Points', ascending=False)
    
    # add a field with the ranking of each brewer
    brewersums['Place'] = brewersums.Points\
        .rank(method='min', ascending=False)\
        .astype(int)

    return brewersums.to_dict('records')


def create_minutes(year:int):
    """Create dictionaries for each meeting minutes file.

    Returns:
        list[dict]: The dictionaries, one for each meeting minutes file.
    """

    path = 'www\\static\\minutes\\{}'.format(year)
    make_dir(path)

    # create minutes data from pdf files in minutes folder
    minutes = []
    for minute_fn in os.listdir(path):
        # construct date from file name
        date = dt.datetime.strptime(minute_fn[0:-4], r'%Y-%m')
        minutes.append({
            'FileName': minute_fn,
            'FormattedDate': date.strftime(r'%B %Y')
        })
    
    return sorted(minutes, key=lambda m: m['FileName'])


def create_competition_files(competition_dfs:list, entry_df:pd.DataFrame):
    """Create JSON data files for each year of competitions.

    Args:
        competition_dfs (list): Dictionaries of {year (int): DataFrame} for each year of competitions.
        entry_df (pd.DataFrame): The entries data.
    """

    # for each year in competitions df, create the competition and leaderboard data files
    for yr, comp_df in competition_dfs.items():
        entries = entry_df[entry_df.index.year == yr]
        # create directory if not exists
        make_dir('www\\static\\data\\{}'.format(yr))
        # create competition list
        comps = create_competitions(comp_df, entries)
        create_json_file(comps, 'www\\static\\data\\{}\\competitions.txt'.format(yr))
        # create brewer totals list, only include top 5
        totals = create_brewer_totals(entries)
        create_json_file(totals, 'www\\static\\data\\{}\\totals.txt'.format(yr))

    # create the competition years data file
    create_json_file(sorted(competition_dfs.keys(), reverse=True), 'www\\static\\data\\competition_years.txt')


def create_minutes_files():
    """Create JSON data files for each year of minutes files.
    """

    # get all the years of minutes from the minutes directory
    minute_yrs = [int(y) for y in os.listdir('www\\static\\minutes')]

    for yr in minute_yrs:
        # create directory if not exists
        make_dir('www\\static\\data\\{}'.format(yr))
        # create minutes
        minutes = create_minutes(yr)
        create_json_file(minutes, 'www\\static\\data\\{}\\minutes.txt'.format(yr))

    # create the minutes years data file
    create_json_file(sorted(minute_yrs, reverse=True), 'www\\static\\data\\minutes_years.txt')


def make_dir(path:str):
    """Create a directory if it doesn't yet exist.

    Args:
        path (str): The path to create.
    """

    Path(path).mkdir(parents=True, exist_ok=True)


def create_json_file(data, path:str):
    """Create a JSON file at the `path` with the given `data`.

    Args:
        data (JSON-serializable type): The data to serialize to JSON.
        path (str): The path of the file to write.
    """

    with open(path, 'w') as fp:
        # specify indent and separators to create a minified file
        json.dump(data, fp, indent=None, separators=(',', ':'))


def main():
    """Run the program.
    
    -Collects data from an Excel file and the meeting minutes directory\n
    -Processes data into a JSON-serializable format\n
    -Outputs the data to JSON files
    """

    # get the competition and entries data
    comp_dfs = get_competition_df()
    entry_df = get_entry_df()

    create_competition_files(comp_dfs, entry_df)
    create_minutes_files()


if __name__ == '__main__':
    print('Creating JSON data files')
    main()
    print('Success')