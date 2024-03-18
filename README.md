# Sentiment-Stock Comparison

## Project Description
The "Sentiment-Stock Comparison" project is designed to compare the sentiment of a company, as determined by Google News, with the company's stock prices. This is achieved using the GNews and YFinance Python modules.

## Requirements
To run this project, you will need the following:

1. **Python 3 or above**: The codebase is written in Python, so you will need to have Python 3 or above installed on your system.

2. **R**: Some parts of the project require R, so ensure that you have it downloaded and installed.

3. **GNews and YFinance Python modules**: These modules are used to fetch the data. You can install them using pip:
    ```bash
    pip install gnewsclient yfinance
    ```
   
4. **dplyr, tidytext, ggplot2, and tidyr R modules**: These modules are used to analyze the data. You can install them by first launching R then running the following command:
    ```bash
    install.packages(c("dplyr", "tidytext", "ggplot2", "tidyr"))
    ```

You install all requirements at once by running `setup.sh` (or `setup.bat` if you are on Windows)

## Usage
Running main.py will launch the GUI version of the program. If you include the -nogui
flag, it will allow you to use the CLI version

NOTE: If you don't add the -nogui flag, the program will 
launch the GUI and ignore all CLI flags except for -settings

### Flags

- -nogui : Runs the program in CLI mode
- -settings=directory/to/your/settings.json : Changes the settings file that you are using
- -settingsmod [settingname]=[newsetting] : Changes a setting
- -sentiment : Generates the news and sentiment report for the day
- -stock : Generates the stock report for the day
- -news : Only generates the news report, without running an analysis of it.
- -sentimentonly : Only generates the sentiment report
NOTE: This will only work if the news report for the day has been generated.

## Contributors
- Gabe Becker, gabebecker2048@gmail.com, @GabeBecker2048
- Wyatt Burch-Celentano, wyatt@wyatt.wyatt, @wyatthbc
- Sam Chapoton, sam@sam.sam, @samchapoton

## Copyright
Copyright © 2024. All rights reserved.
