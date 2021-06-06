# Ames Brewers League Website
http://www.amesbrewersleague.org

## About
This repository includes code for the Ames Brewers League website. The website's purpose is to inform potential new members about the group as well as provide a medium for meeting minutes and competition results to be shared.

The website is simple and was therefore created using basic HTML/CSS/JS. Bootstrap 4 was used for most of the styling. Competitions data is stored as an Excel file and converted to a JavaScript data file for use on the website. This is performed by Python code in the "...\ABL\ABL 3.0\abl" directory. JavaScript is used to render the data on the webpage. Minutes are stored as PDF files to be viewed in the browser.

Meetings take place monthly and the website is updated when those meeting minutes are available.

## Getting Started
In order to update the website automatically as intended, you need to use Python. Python is a programming language. Python files (or scripts) are text files ending in ".py" and contain Python code, as you will find in "...\ABL\ABL 3.0\abl\abl.py". In order to run the code in this file, a Python interpreter along with a few 1st and 3rd party "libraries" of code are required. Download and install Python (version >=3.9) from "https://www.python.org/downloads/". Be sure to download the installer appropriate for your operating system. When installing Python, be sure to check the box that adds Python to your "PATH" environment variable. This will allow you to run Python files from the command prompt without having to specify the location of the interpreter. Installing Python will provide access to the interpreter and its "standard libraries" of code.

### Windows 10
1. Install Python as described above.
1. Navigate to the "...\ABL\ABL 3.0\abl" directory. Click in the address bar and copy the text.
1. Click in the search textbox in the taskbar. Search for "cmd" and press enter or click on "Command Prompt". This will open up the basic Windows shell software, using which we can install the code libraries needed.
    1. In Command Prompt, type the following commands and press "Enter" to execute them.
    1. "cd " and paste the file path copied above before executing - This will change the working directory to "...\ABL\ABL 3.0\abl".
    1. "python -m venv venv" - This will create a "virtual environment" in the folder, which will allow us to the install the 3rd party code packages locally to this project and not pollute the global environment. If it doesn't recognize "python", you may have forgotten to add Python to the "PATH" environment variable.
    1. "venv\Scripts\activate" - This will activate the virtual environment. You should now see "(venv)" at the beginning of the command prompt line.
    1. "pip install -r requirements.txt" - This will install the required code libraries.
1. You are now ready to update the site.

## Updating the Site
Following are instructions for making monthly updates to the website.

### Windows 10
1. Save the meeting minutes as a PDF file in "...\ABL\ABL 3.0\static\minutes". Name the file as "YYYY-MM.pdf" (e.g. "2021-06.pdf" for June 2021). This style is necessary for the Python file to properly parse the date.
1. Update the Excel file, "...\ABL\ABL 3.0\abl\data.xlsx", with any competitions, competition entries, or brewers as necessary. Note that the dropdown for brewers in the "Entries" tab pulls from the "Brewers" list, so add any new brewers first.
1. Make any updates necessary to the "...\ABL\ABL 3.0\index.html" webpage. This can be done with a basic text editor like "Notepad" or software with more features like syntax highlighting, such as "Visual Studio Code" (https://code.visualstudio.com/download). To open the file in Notepad, right-click on the file and hover over "Open with...". If Notepad is available, select it; otherwise, select "Choose another app" and find Notepad.
1. Navigate to the "...\ABL\ABL 3.0\abl" directory. Click in the address bar and copy the text.
1. Click in the search textbox in the taskbar. Search for "cmd" and press enter or click on "Command Prompt". This will open up the basic Windows shell software, where we can run the Python script.
    1. In Command Prompt, type the following commands and press "Enter" to execute them.
    1. "cd " and paste the file path copied above before executing - This will change the working directory to "...\ABL\ABL 3.0\abl".
    1. "venv\Scripts\activate" - This will activate the virtual environment. You should now see "(venv)" at the beginning of the command prompt line.
    1. "python abl.py" - This will run the Python script. It should print a statement saying that files were successfully uploaded.
1. Open up the webpage and confirm that changes took effect. You may need to clear the cache to see changes, which in Google Chrome can be done by holding "Ctrl" and clicking the refresh icon at the top left of the browser.

## Maintenance
One thing to be aware of is that the website files are uploaded to the web server using "FTP", or "file transfer protocol". This method requires the domain name, a username, and a password. These items are stored in the Python file "...\ABL\ABL 3.0\abl\secrets.py" and imported by the "abl.py" script when it runs. If the domain name or credentials change, it will be necessary to change those items in this file. This can be done with a basic text editor like "Notepad". To open the file in Notepad, right-click on the file and hover over "Open with...". If Notepad is available, select it; otherwise, select "Choose another app" and find Notepad.

## Dependencies
The following CSS and JS libraries are loaded via "CDN", or "content delivery network", in the index.html file, and are required for the website to look and behave as intended. Older or newer versions may work as well.

* Bootstrap 4.3.1
* jQuery 3.3.1
