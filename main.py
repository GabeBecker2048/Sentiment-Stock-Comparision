import tkinter as tk
from tkinter import ttk
import json

def on_validate(value, action):
    if action == '1':  # Insert
        try:
            int(value)
            return True
        except ValueError:
            return False
    return True


def on_item_click(index, right_frame):

    for widget in right_frame.winfo_children():
        widget.destroy()

    if index == 1:
        run_button = ttk.Button(right_frame, padding=(10, 10), text="Run", command="")
        run_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    elif index == 2:
        gen_sent_report_button = ttk.Button(right_frame, padding=(10, 10), text="Generate Sentiment Report", command="")
        gen_sent_report_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    elif index == 3:
        gen_stock_report_button = ttk.Button(right_frame, padding=(10, 10), text="Generate Stock Report", command="")
        gen_stock_report_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    elif index == 4:
        gen_graph1_button = ttk.Button(right_frame, padding=(10, 10), text="Generate graph type 1", command="")
        gen_graph1_button.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

        gen_graph2_button = ttk.Button(right_frame, padding=(10, 10), text="Generate graph type 2", command="")
        gen_graph2_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        gen_graph3_button = ttk.Button(right_frame, padding=(10, 10), text="Generate graph type 3", command="")
        gen_graph3_button.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

    elif index == 5:
        pass
    elif index == 6:

        filename = "lib/settings.json"
        try:
            with open(filename, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            print(f"Settings file '{filename}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

        # Create a list of options for the dropdown
        options = ["Hourly", "Daily", "Weekly", "Monthly"]

        # Create a Combobox
        runreport_combobox = ttk.Combobox(right_frame, values=options, state="readonly")
        runreport_combobox.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        # Set a default value
        runreport_combobox.set(settings["RunReport"])

        validate_cmd = (right_frame.register(on_validate), '%P', '%d')
        numarticles_entry = ttk.Entry(right_frame, validate='key', validatecommand=validate_cmd)
        numarticles_entry.place(relx=0.75, rely=0.25)
        numarticles_entry.insert(0, str(settings["NumArticles"]))

        save_button = ttk.Button(right_frame, padding=(2, 2), text="Save", command='')
        save_button.place(relx=0.95, rely=0.97, anchor=tk.CENTER)

    else:
        print("Invalid index!")

def main():
    root = tk.Tk()
    root.geometry("1000x500")

    # Left frame for buttons and canvas
    left_frame = ttk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

    canvas = tk.Canvas(left_frame, width=200, height=500, borderwidth=2, relief=tk.GROOVE)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH)

    frame = ttk.Frame(canvas)
    frame.pack(fill=tk.X)

    right_frame = ttk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    buttons = [
        "Run",
        "Generate Daily Sentiment Report",
        "Generate Daily Stock Report",
        "Graph Generation",
        "Sentiment vs Stock",
        "Settings",
    ]

    for index, text in enumerate(buttons, start=1):
        button = ttk.Button(frame, text=text, padding=(10, 10), command=lambda i=index: on_item_click(i, right_frame))
        button.pack(fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
