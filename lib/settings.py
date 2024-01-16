import json


class Settings:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.s = {
            "NumArticles": 20,
            "RunReport": "Daily",
            "Running": False,
            "RScriptLocation": "Rscript.exe",
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
