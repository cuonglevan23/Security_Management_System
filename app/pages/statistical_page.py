import tkinter as tk

def statistical_page(main_frame):
    statistics_frame = tk.Frame(main_frame, bg="#FFFFFF", width=1200, height=500)

    # Increase font size to 40
    lb = tk.Label(statistics_frame, text="Statistical Page\n\n Page 1", font=('Bold', 30))
    lb.pack()

    return statistics_frame