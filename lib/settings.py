import json


class Settings:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.s = {
            "NumArticles": 20,
            "RunReport": "Daily",
            "Running": False,
            "RScriptLocation": "Rscript",
            "SearchTerms": {
                "Apple": "AAPL", "Microsoft": "MSFT", "Alphabet (Google)": "GOOGL", "Amazon": "AMZN", "NVIDIA": "NVDA",
                "Meta Platforms (Facebook)": "META", "Berkshire Hathaway": "BRK.B", "Tesla": "TSLA", "Eli Lilly": "LLY",
                "Visa": "V", "Broadcom": "AVGO", "UnitedHealth": "UNH", "JPMorgan Chase": "JPM", "Walmart": "WMT",
                "Exxon Mobil": "XOM", "Mastercard": "MA", "Johnson & Johnson": "JNJ", "Procter & Gamble": "PG",
                "Oracle": "ORCL", "Home Depot": "HD", "Adobe": "ADBE", "Chevron": "CVX", "Costco": "COST",
                "Merck": "MRK", "Coca-Cola": "KO", "AbbVie": "ABBV", "Bank of America": "BAC", "Pepsico": "PEP",
                "Salesforce": "CRM", "Netflix": "NFLX", "McDonald": "MCD", "AMD": "AMD", "Cisco": "CSCO",
                "Thermo Fisher Scientific": "TMO", "Intel": "INTC", "Abbott Laboratories": "ABT", "T-Mobile US": "TMUS",
                "Pfizer": "PFE", "Comcast": "CMCSA", "Walt Disney": "DIS", "Nike": "NKE", "Danaher": "DHR",
                "Intuit": "INTU", "Verizon": "VZ", "Wells Fargo": "WFC", "Philip Morris": "PM", "QUALCOMM": "QCOM",
                "Amgen": "AMGN", "IBM": "IBM", "Texas Instruments": "TXN"
            }
        }
        self.load()

    def __getitem__(self, item: str):
        return self.s[item]

    def __setitem__(self, key: str, value):
        self.s[key] = value

    def save(self):
        with open(self.filepath, 'w') as json_file:
            json.dump(self.s, json_file, indent=4)

    def load(self):
        try:
            with open(self.filepath, 'r') as file:
                self.s = json.load(file)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return

    def settingsmod(self, settingsmod: str):
        try:

            # this splits settingsmod at the first '='
            settingsmod_changed = False
            for j, ichar in enumerate(settingsmod):
                if ichar == '=':
                    settingsmod = [settingsmod[:j], settingsmod[j + 1:]]
                    settingsmod_changed = True
                    break
            # if no '=' was detected, the program raising an error
            if not settingsmod_changed:
                raise SettingsException

            # if the user is attempting to change a setting that doesn't exist, raise an error
            if settingsmod[0] not in self.s.keys():
                raise SettingsException

            # the search terms can only be edited in the settings.json file or the GUI, not with settingsmod
            if settingsmod[0] == 'SearchTerms':
                raise SettingsException

            # Must account for settings that are not saved as strings
            # Therefore, they must be converted into their correct data type
            if settingsmod[0] in ['Running', 'NumArticles']:
                # converts to bool
                if settingsmod[0] == 'Running':
                    if settingsmod[1].lower() == 'true':
                        settingsmod[1] = True
                    elif settingsmod[1].lower() == 'false':
                        settingsmod[1] = False
                    else:
                        raise SettingsException

                # converts to int
                elif settingsmod[0] == 'NumArticles':
                    settingsmod[1] = int(settingsmod[1])

            # finally, we overwrite the current settings and save
            self[settingsmod[0]] = settingsmod[1]
            self.save()
            return True

        except SettingsException:
            return False


class SettingsException(Exception):
    pass
