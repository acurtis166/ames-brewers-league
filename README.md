# Ames Brewers League Website

http://www.amesbrewersleague.org

## About

This repository includes code for the Ames Brewers League website. The website's purpose is to inform potential new members about the group as well as provide a medium for meeting minutes and competition results to be shared.

Meetings take place monthly and the website is updated when those meeting minutes are available.

## Getting Started

- Clone this repository
```shell
git clone https://github.com/acurtis166/ames-brewers-league.git
```

- Install [Python 3.11](https://www.python.org/downloads/). During installation you will have the option to add Python to your `PATH` environment variable. The remaining steps assume you have done so.

- Navigate to the root directory of the repository in your shell.

- Create a virtual environment
```shell
python -m venv venv
```

- Activate the virtual environment

Windows
```shell
venv\Scripts\activate
```

MacOS/Linux
```shell
source venv/Scripts/activate
```

- Install dependencies
```shell
python -m pip install -r requirements.txt --update
```

- Save the JSON configuration file as `config.json` into the root of the repository. It should have the following structure.
```json
{
    "ftp": {
        "site": "amesbrewersleague.org",
        "username": "[USERNAME HERE]",
        "password": "[PASSWORD HERE]"
    },
    "paths": {
        "competitions": "path/to/competitions.csv",
        "entries": "path/to/entries.csv",
        "minutes": "path/to/minutes",
        "sponsors": "path/to/raffle_sponsors.json"
    }
}
```

## Data Files

Ensure that the data files and directory referenced in the `config.json` file line up to their location in your file system.

### competitions.csv

This CSV contains records for each monthly competition. The column names and a couple example records are shown below.

```
date,style,category,bjcp_year
2018-01-09,Open to All Styles,All,2015
2018-02-06,Belgians,24-26,2015
```

### entries.csv

This CSV contains records for each brewer submission to competitions. The column names and a couple example records are shown below. Dates here need to line up to a date in the competitions file.

```
date,brewer,beer,points
2018-01-09,Ron Nelson,"English Porter, 13C",3.0
2018-01-09,Pete Crow,"American Amber Ale, 19A",2.0
```

### Minutes directory

Store PDF files of recorded meeting minutes in this directory. The file structure should mirror the one below.


```
├── minutes
│   ├── 2016
│   │   ├── 2016-01.pdf
│   │   ├── 2016-02.pdf
│   │   ├── ...
│   ├── 2017
│   ├── ...
```

### raffle_sponsors.json

This file contains an array of raffle sponsors. An example is shown below.

```json
[
    {
        "name": "Super Awesome Brewing Supply Co.",
        "url": "http://.../",
        "logo_url": "https://.../logo.jpg"
    },
    ...
]
```

## Monthly Update

- Create a PDF of the meeting minutes.

- Name the file according to the year and month of the meeting, e.g. `2023-03.pdf`.

- Save the file under the appropriate year in the `minutes` directory.

- Add to or update the `competitions.csv` file, if necessary.

- Append the brewer submissions for the month to the `entries.csv` file.

- Navigate to the root directory of the repository in your shell.

- Activate the virtual environment

Windows
```shell
venv\Scripts\activate
```

MacOS/Linux
```shell
source venv/Scripts/activate
```

- Run the static site generator script.

```shell
python scripts/generator.py
```

- Review the `public` directory to make sure that files were generated. If you use VS code you can install the [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) to preview the site before pushing to the web server. You may need to adjust the extension settings to set the `public` directory as the web root.

- Transfer files to the web server via FTP.

```shell
python scripts/ftp.py
```

# 🍻 Cheers! 🍻