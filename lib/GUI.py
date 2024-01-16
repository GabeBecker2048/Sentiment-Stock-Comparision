import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading

from lib.commands import generate_sentiment_report
from lib.settings import Settings


class Terminal:
    def __init__(self, right_frame):
        self.output = ScrolledText(
            right_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            bg='black',  # Set background color to black
            fg='white'  # Set text color to white
        )

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
        self.output.place(relx=0.5, rely=0.4, anchor=tk.N)

    def writelines(self, lines):
        for line in lines:
            self.write(line)


class SettingsGUI:
    def __init__(self, settings: Settings, right_frame: tk.Frame):
        self.settings = settings
        self.frame = right_frame
        self.widget_list = []

        # create the widgets
        self.create_widgets()

    def reset_widgets(self):
        # Reset widget values to dictionary values
        self.num_articles_entry.delete(0, tk.END)
        self.num_articles_entry.insert(0, str(self.settings["NumArticles"]))

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


class Root:
    def __init__(self, settings: Settings):

        # sets up the window
        self.root = tk.TK()
        self.root.geometry("1000x500")

        temp_frame = ttk.Frame(self.root)
        temp_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        canvas = tk.Canvas(temp_frame, width=200, height=500, borderwidth=2, relief=tk.GROOVE)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        self.left_frame = ttk.Frame(canvas)
        self.left_frame.pack(fill=tk.X)

        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        buttons = [
            "Run",
            "Generate Sentiment Report",
            "Generate Stock Report",
            "Generate Graph",
            "Graphs",
            "Settings",
        ]

        self.terminals = [Terminal(self.right_frame) for i in range(3)]

        for index, text in enumerate(buttons, start=1):
            button = ttk.Button(self.left_frame, text=text, padding=(10, 10),
                                command=lambda i=index: self.on_item_click(i, settings))
            button.pack(fill=tk.X)

    def on_item_click(self, index, settings: Settings):
        settings.hide_widgets()

        for widget in self.right_frame.winfo_children():
            widget.place_forget()

        if index == 1:
            run_button = ttk.Button(self.right_frame, padding=(10, 10), text="Run", command="")
            run_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
            self.terminals[0].output.place(relx=0.5, rely=0.4, anchor=tk.N)

        elif index == 2:
            gen_sent_report_button = ttk.Button(self.right_frame,
                                                padding=(10, 10),
                                                text="Generate Sentiment Report",
                                                command=lambda: threading.Thread(
                                                    target=generate_sentiment_report,
                                                    args=(settings, self.terminals[1])).start()
                                                )
            gen_sent_report_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
            self.terminals[1].output.place(relx=0.5, rely=0.4, anchor=tk.N)

        elif index == 3:
            gen_stock_report_button = ttk.Button(self.right_frame,
                                                 padding=(10, 10),
                                                 text="Generate Sentiment Report",
                                                 command=lambda: threading.Thread(
                                                    target=generate_sentiment_report,
                                                    args=(settings, self.terminals[2])).start()
                                                 )
            gen_stock_report_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
            self.terminals[2].output.place(relx=0.5, rely=0.4, anchor=tk.N)

        elif index == 6:
            settings.show_widgets()
            settings.reset_widgets()
