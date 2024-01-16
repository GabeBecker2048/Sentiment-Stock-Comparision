import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
from lib.commands import RedirectText, generate_sentiment_report
from lib.settings import Settings


def on_item_click(index, right_frame, terminal: RedirectText, settings: Settings):
    settings.hide_widgets()

    for widget in right_frame.winfo_children():
        widget.place_forget()

    if index == 1:
        run_button = ttk.Button(right_frame, padding=(10, 10), text="Run", command="")
        run_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        terminal.output.place(relx=0.5, rely=0.4, anchor=tk.N)

    elif index == 2:
        gen_sent_report_button = ttk.Button(right_frame,
                                            padding=(10, 10),
                                            text="Generate Sentiment Report",
                                            command=lambda: threading.Thread(target=generate_sentiment_report, args=(settings, terminal)).start()
                                            )
        gen_sent_report_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        terminal.output.place(relx=0.5, rely=0.4, anchor=tk.N)

    elif index == 6:
        settings.show_widgets()
        settings.reset_widgets()


def main():
    root = tk.Tk()
    root.geometry("1000x500")

    left_frame = ttk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

    canvas = tk.Canvas(left_frame, width=200, height=500, borderwidth=2, relief=tk.GROOVE)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH)

    frame = ttk.Frame(canvas)
    frame.pack(fill=tk.X)

    right_frame = ttk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    settings = Settings("./lib/settings.json", right_frame)

    buttons = [
        "Run",
        "Generate Sentiment Report",
        "Generate Stock Report",
        "Generate Graph",
        "Graphs",
        "Settings",
    ]

    # create terminal
    terminal_text = ScrolledText(
        right_frame,
        wrap=tk.WORD,
        width=80,
        height=15,
        bg='black',  # Set background color to black
        fg='white'   # Set text color to white
    )
    terminal = RedirectText(terminal_text)

    for index, text in enumerate(buttons, start=1):
        button = ttk.Button(frame, text=text, padding=(10, 10), command=lambda i=index: on_item_click(i, right_frame, terminal, settings))
        button.pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    main()
