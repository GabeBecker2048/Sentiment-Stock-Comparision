import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import threading

from lib.utils import *
from lib.settings import Settings


class Terminal:
    def __init__(self, right_frame):
        self.output = ScrolledText(
            right_frame,
            wrap=tk.WORD,
            bg='black',  # Set background color to black
            fg='white'  # Set text color to white
        )

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def writelines(self, lines):
        for line in lines:
            self.write(line)


class SettingsGUI(Settings):
    def __init__(self, filepath: str, right_frame: tk.Frame):
        super().__init__(filepath)
        self.frame = right_frame
        self.widget_list = []

        self.num_articles_entry = tk.Entry(self.frame)
        self.run_report_var = tk.StringVar(self.frame)
        self.run_report_dropdown = ttk.Combobox(self.frame, values=["Daily", "Weekly", "Monthly", "Yearly"],
                                                state="readonly")
        self.rscript_location_entry = tk.Entry(self.frame)
        self.search_terms_entry = tk.Text(self.frame, height=15, width=80)
        self.save_button = tk.Button(self.frame, text="Save", command=self.save_settings)

        # create the widgets
        self.create_widgets()

    def create_widgets(self):
        # NumArticles
        l1 = tk.Label(self.frame, text="NumArticles:")
        self.widget_list.append(l1)
        self.num_articles_entry.insert(0, str(self["NumArticles"]))
        self.num_articles_entry.config(validate="key", validatecommand=(self.frame.register(self.validate_num_articles), '%P'))
        self.widget_list.append(self.num_articles_entry)

        # RunReport
        l2 = tk.Label(self.frame, text="RunReport:")
        self.widget_list.append(l2)
        self.run_report_var.set(self["RunReport"])
        self.run_report_dropdown.set(self["RunReport"])
        self.widget_list.append(self.run_report_dropdown)

        # RScriptLocation
        l3 = tk.Label(self.frame, text="RScriptLocation:")
        self.widget_list.append(l3)
        self.rscript_location_entry.insert(0, self["RScriptLocation"])
        self.widget_list.append(self.rscript_location_entry)
        browse = tk.Button(self.frame, text="Browse", command=self.browse_rscript_location)
        self.widget_list.append(browse)

        # SearchTerms
        l4 = tk.Label(self.frame, text="SearchTerms:")
        self.widget_list.append(l4)

        # sets up the search term string for viewing
        search_entries = ""
        for stock_symbol, search_terms in self["SearchTerms"].items():
            stock_str = stock_symbol + ':'
            for term in search_terms:
                if stock_str != (stock_symbol + ':'):
                    stock_str += ','
                stock_str += term
            search_entries += stock_str + "\n"
        search_entries = search_entries[:-1]
        self.search_terms_entry.insert(tk.END, search_entries)

    def reset_widgets(self):
        # Reset widget values to dictionary values
        self.num_articles_entry.delete(0, tk.END)
        self.num_articles_entry.insert(0, str(self["NumArticles"]))

        self.run_report_var.set(self["RunReport"])
        self.run_report_dropdown.set(self["RunReport"])

        self.rscript_location_entry.delete(0, tk.END)
        self.rscript_location_entry.insert(0, self["RScriptLocation"])

        self.search_terms_entry.delete("1.0", tk.END)
        # sets up the search term string for viewing
        search_entries = ""
        for stock_symbol, search_terms in self["SearchTerms"].items():
            stock_str = stock_symbol + ':'
            for term in search_terms:
                if stock_str != (stock_symbol + ':'):
                    stock_str += ','
                stock_str += term
            search_entries += stock_str + "\n"
        search_entries = search_entries[:-1]
        self.search_terms_entry.insert(tk.END, search_entries)

    def show_widgets(self):
        for widget in self.widget_list:
            widget.pack()
        self.search_terms_entry.pack(fill=tk.BOTH, expand=True)
        self.save_button.pack()

    def browse_rscript_location(self):
        # Open a file dialog to select RScriptLocation
        file_path = filedialog.askopenfilename()
        self.rscript_location_entry.delete(0, tk.END)
        self.rscript_location_entry.insert(0, file_path)

    def save_settings(self):
        # Save settings based on user input
        self["NumArticles"] = int(self.num_articles_entry.get())
        self["RunReport"] = self.run_report_var.get()
        self["RScriptLocation"] = self.rscript_location_entry.get()

        SearchTerms = {}
        for term in self.search_terms_entry.get("1.0", tk.END).splitlines():
            splitterm = term.split(":")
            subterms = [subterm for subterm in splitterm[1].split(",")]
            SearchTerms[splitterm[0]] = subterms
        self["SearchTerms"] = SearchTerms

        # Save settings to file
        self.save()

    @staticmethod
    def validate_num_articles(new_value):
        # Validation callback to allow only numeric input for NumArticles
        try:
            if new_value == "":
                return True  # Allow empty entry
            int_value = int(new_value)
            return True
        except ValueError:
            return False


class Root:
    def __init__(self, filepath: str):

        # sets up the window
        self.root = tk.Tk()
        self.root.title("Sentiment Stock Comparison")
        self.root.geometry("1000x500")

        temp_frame = ttk.Frame(self.root)
        temp_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        canvas = tk.Canvas(temp_frame, width=200, height=500, borderwidth=2, relief=tk.GROOVE)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        self.left_frame = ttk.Frame(canvas)
        self.left_frame.pack(fill=tk.X)

        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.settings = SettingsGUI(filepath, self.right_frame)

        self.buttons = [ttk.Button(self.right_frame,
                                   padding=(10, 10),
                                   text="Run",
                                   command=lambda: threading.Thread(
                                       target=run_all,
                                       args=[self.settings, self.terminals[0]]).start()
                                   ),
                        ttk.Button(self.right_frame,
                                   padding=(10, 10),
                                   text="Generate Sentiment Report",
                                   command=lambda: threading.Thread(
                                       target=generate_sentiment_report,
                                       args=[self.settings, self.terminals[1]]).start()
                                   ),
                        ttk.Button(self.right_frame,
                                   padding=(10, 10),
                                   text="Generate Stock Report",
                                   command=lambda: threading.Thread(
                                       target=generate_stock_report,
                                       args=[self.settings, self.terminals[2]]).start()
                                   )
                        ]
        self.terminals = [Terminal(self.right_frame) for i in range(3)]

        button_strs = [
            "Run",
            "Generate Sentiment Report",
            "Generate Stock Report",
            "Data",
            "Graphs",
            "Settings",
        ]

        for index, text in enumerate(button_strs, start=1):
            button = ttk.Button(self.left_frame, text=text, padding=(10, 10),
                                command=lambda i=index: self.on_item_click(i))
            button.pack(fill=tk.X)

    def on_item_click(self, index):

        for widget in self.right_frame.winfo_children():
            widget.pack_forget()
            widget.place_forget()

        if index == 1:
            self.buttons[0].place(relwidth=0.33, relheight=0.15, relx=0.5, rely=0.25, anchor=tk.CENTER)
            self.terminals[0].output.place(relwidth=0.9, relheight=0.55, relx=0.5, rely=0.4, anchor=tk.N)

        elif index == 2:
            self.buttons[1].place(relwidth=0.33, relheight=0.15, relx=0.5, rely=0.25, anchor=tk.CENTER)
            self.terminals[1].output.place(relwidth=0.9, relheight=0.55, relx=0.5, rely=0.4, anchor=tk.N)

        elif index == 3:
            self.buttons[2].place(relwidth=0.33, relheight=0.15, relx=0.5, rely=0.25, anchor=tk.CENTER)
            self.terminals[2].output.place(relwidth=0.9, relheight=0.55, relx=0.5, rely=0.4, anchor=tk.N)

        elif index == 6:
            self.settings.show_widgets()
            self.settings.reset_widgets()
