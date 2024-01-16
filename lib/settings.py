import json
import tkinter as tk
from tkinter import ttk, filedialog


class Settings:
    def __init__(self, filepath: str, right_frame: tk.Frame):
        self.filepath = filepath
        self.s = self.load()
        self.frame = right_frame
        self.widget_list = []

        # create the widgets
        self.create_widgets()

    def __getitem__(self, item: str):
        return self.s[item]

    def __setitem__(self, key: str, value):
        self.s[key] = value

    def reset_widgets(self):
        # Reset widget values to dictionary values
        self.num_articles_entry.delete(0, tk.END)
        self.num_articles_entry.insert(0, str(self.s["NumArticles"]))

        self.run_report_var.set(self.s["RunReport"])
        self.run_report_dropdown.set(self.s["RunReport"])

        self.rscript_location_entry.delete(0, tk.END)
        self.rscript_location_entry.insert(0, self.s["RScriptLocation"])

        self.search_terms_entry.delete("1.0", tk.END)
        self.search_terms_entry.insert(tk.END, "\n".join(self.s["SearchTerms"]))

    def hide_widgets(self):
        for widget in self.widget_list:
            widget.forget()

    def show_widgets(self):
        for widget in self.widget_list:
            widget.pack()

    def validate_num_articles(self, new_value):
        # Validation callback to allow only numeric input for NumArticles
        try:
            if new_value == "":
                return True  # Allow empty entry
            int_value = int(new_value)
            return True
        except ValueError:
            return False

    def create_widgets(self):
        # NumArticles
        l1 = tk.Label(self.frame, text="NumArticles:")
        self.widget_list.append(l1)
        self.num_articles_entry = tk.Entry(self.frame)
        self.num_articles_entry.insert(0, str(self.s["NumArticles"]))
        self.num_articles_entry.config(validate="key", validatecommand=(self.frame.register(self.validate_num_articles), '%P'))
        self.widget_list.append(self.num_articles_entry)

        # RunReport
        l2 = tk.Label(self.frame, text="RunReport:")
        self.widget_list.append(l2)
        self.run_report_var = tk.StringVar(self.frame)
        self.run_report_var.set(self.s["RunReport"])
        self.run_report_dropdown = ttk.Combobox(self.frame, values=["Daily", "Weekly", "Monthly", "Yearly"],
                                                state="readonly")
        self.run_report_dropdown.set(self.s["RunReport"])
        self.widget_list.append(self.run_report_dropdown)

        # RScriptLocation
        l3 = tk.Label(self.frame, text="RScriptLocation:")
        self.widget_list.append(l3)
        self.rscript_location_entry = tk.Entry(self.frame)
        self.rscript_location_entry.insert(0, self.s["RScriptLocation"])
        self.widget_list.append(self.rscript_location_entry)
        browse = tk.Button(self.frame, text="Browse", command=self.browse_rscript_location)
        self.widget_list.append(browse)

        # SearchTerms
        l4 = tk.Label(self.frame, text="SearchTerms:")
        self.widget_list.append(l4)
        self.search_terms_entry = tk.Text(self.frame, height=8, width=40)  # Adjusted size
        self.search_terms_entry.insert(tk.END, "\n".join(self.s["SearchTerms"]))
        self.widget_list.append(self.search_terms_entry)

        # Save button
        save_button = tk.Button(self.frame, text="Save", command=self.save_settings)
        self.widget_list.append(save_button)

    def browse_rscript_location(self):
        # Open a file dialog to select RScriptLocation
        file_path = filedialog.askopenfilename()
        self.rscript_location_entry.delete(0, tk.END)
        self.rscript_location_entry.insert(0, file_path)

    def save_settings(self):
        # Save settings based on user input
        self.s["NumArticles"] = int(self.num_articles_entry.get())
        self.s["RunReport"] = self.run_report_var.get()
        self.s["RScriptLocation"] = self.rscript_location_entry.get()
        self.s["SearchTerms"] = [term.strip() for term in self.search_terms_entry.get("1.0", tk.END).splitlines()]

        # Save settings to file
        self.save()

    def save(self):
        with open(self.filepath, 'w') as json_file:
            json.dump(self.s, json_file, indent=4)

    def load(self):
        settings = {
            "NumArticles": 20,
            "RunReport": "Daily",
            "Running": False,
            "RScriptLocation": "C:/Program Files/R/R-4.3.2/bin/Rscript.exe",
            "SearchTerms": ["Apple", "Microsoft", "Alphabet (Google)", "Amazon", "NVIDIA", "Meta Platforms (Facebook)",
                            "Berkshire Hathaway", "Tesla", "Eli Lilly", "Visa", "Broadcom", "UnitedHealth",
                            "JPMorgan Chase", "Walmart", "Exxon Mobil", "Mastercard", "Johnson & Johnson",
                            "Procter & Gamble", "Oracle", "Home Depot", "Adobe", "Chevron", "Costco", "Merck",
                            "Coca-Cola", "AbbVie", "Bank of America", "Pepsico", "Salesforce", "Netflix", "McDonald",
                            "AMD", "Cisco", "Thermo Fisher Scientific", "Intel", "Abbott Laboratories", "T-Mobile US",
                            "Pfizer", "Comcast", "Walt Disney", "Nike", "Danaher", "Intuit", "Verizon", "Wells Fargo",
                            "Philip Morris", "QUALCOMM", "Amgen", "IBM", "Texas Instruments"]
        }

        try:
            with open(self.filepath, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            print(f"Settings file '{self.filepath}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        return settings
