import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import threading
from math import floor
from os import listdir
from PIL import Image, ImageTk

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
    def __init__(self, right_frame: tk.Frame, filepath: str):
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
        self.num_articles_entry.config(validate="key",
                                       validatecommand=(self.frame.register(self.validate_num_articles), '%P'))
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

    def reset(self):
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

    def show(self):
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


class csvGUI:
    def __init__(self, right_frame: tk.Frame):
        self.frame = right_frame

        # These are the widgets for data browsing
        self.top = tk.Frame(self.frame)
        self.bottom = tk.Frame(self.frame)

        button_strs = [
            "News Data",
            "Sentiment Data",
            "Stock Data",
            "Correlation Data"
        ]
        self.data_buttons = [tk.Button(self.top, text=button, command=lambda i=button: self.on_data_button_click(i)) for button in button_strs]
        self.csv_list = tk.Listbox(self.bottom)
        self.csv_list.bind('<<ListboxSelect>>', self.on_csv_click)

        # These are the widgets for displaying the csv
        self.back_button = ttk.Button(self.frame, text="<- Back", command=self.on_back_click)
        self.tree = ttk.Treeview(self.frame, show="headings")
        self.cell_display = tk.Label(right_frame, text="", padx=20, pady=10)
        self.status_label = tk.Label(right_frame, text="", padx=20, pady=10)
        self.x_scroll = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.x_scroll.set)

    def on_data_button_click(self, button: str):
        self.csv_list.delete(0, tk.END)

        folder = f"./lib/csv_data/{button.lower().replace(' ', '_')}/"
        for i, file in enumerate(listdir(folder)):
            if file.endswith(".csv"):
                self.csv_list.insert(i, file)

    def on_csv_click(self, evt):
        self.hide_all()

        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        folder = None
        if value.startswith("news"):
            folder = "news_data"
        elif value.startswith("sentiment"):
            folder = "sentiment_data"
        elif value.startswith("prices"):
            folder = "stock_data"
        elif value.startswith("correlation") or value.startswith("coorelation"):
            folder = "correlation_data"

        filepath = f"./lib/csv_data/{folder}/{value}"
        self.display_csv_data(filepath)

    def on_cell_click(self, event):

        col_id = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)

        cell_value = self.tree.item(row_id)['values'][int(col_id[1:]) - 1]
        self.cell_display.config(text=str(cell_value))

    def on_back_click(self):
        self.hide_all()
        self.show()

    def display_csv_data(self, file_path):
        self.cell_display.config(text="")
        try:
            with open(file_path, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Read the header row
                self.tree.delete(*self.tree.get_children())  # Clear the current data

                self.tree["columns"] = header
                for col in header:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=100)

                for row in csv_reader:
                    self.tree.insert("", "end", values=row)

                self.status_label.config(text=f"CSV file loaded: {file_path}")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

        # Bind a function to the treeview that gets called when a cell is clicked
        self.tree.bind("<Button-1>", self.on_cell_click)

        self.back_button.pack(pady=10)
        self.tree.pack(padx=20, fill="both", expand=True)
        self.x_scroll.pack(padx=20, fill='x')
        self.cell_display.pack()
        self.status_label.pack()

    def show(self):
        self.top.place(relx=0, rely=0, relwidth=1, relheight=0.3)
        self.bottom.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

        for button in self.data_buttons:
            button.pack()

        self.csv_list.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

    def hide_all(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()
            widget.place_forget()


class graphGUI:
    def __init__(self, right_frame: tk.Frame):
        self.frame = right_frame
        self.files = tk.Listbox(self.frame)
        for i, file in enumerate(listdir("./lib/graphs/")):
            if file.endswith(".png"):
                self.files.insert(i, file)
        self.files.bind('<<ListboxSelect>>', self.on_graph_click)

        self.back_button = tk.Button(self.frame, text="<- Back", command=self.on_back_click)
        self.graph = None
        self.graph_widget = tk.Label(self.frame)

    def on_graph_click(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        self.hide_all()

        self.back_button.pack()
        raw_graph = Image.open(f"./lib/graphs/{value}")
        graph_width, graph_height = raw_graph.size
        ratio1, ratio2 = self.frame.winfo_width()/graph_width, self.frame.winfo_height()/graph_height
        resized_graph = raw_graph.resize((floor(graph_width*ratio1), floor(graph_height*ratio1)))
        self.graph = ImageTk.PhotoImage(resized_graph)
        self.graph_widget.config(image=self.graph)
        self.graph_widget.pack()

    def on_back_click(self):
        self.hide_all()
        self.show()

    def hide_all(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()
            widget.place_forget()

    def show(self):
        self.files.pack(pady=10, fill=tk.BOTH, expand=True)


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

        self.settings = SettingsGUI(self.right_frame, filepath)
        self.csvGUI = csvGUI(self.right_frame)
        self.graphGUI = graphGUI(self.right_frame)

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

        elif index == 4:
            self.csvGUI.show()

        elif index == 5:
            self.graphGUI.show()

        elif index == 6:
            self.settings.show()
            self.settings.reset()
