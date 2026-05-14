import tkinter as tk

def create_page(parent, show_page, pages, show_records_page):
    tk.Label(parent, text="Library Management System",
             font=("Arial", 24, "bold")).pack(pady=50)

    tk.Label(parent,
             text="What would you like to do?",
             font=("Arial", 14)).pack(pady=10)

    button_frame = tk.Frame(parent)
    button_frame.pack(pady=40)

    tk.Button(button_frame, text="Borrow a Book", width=25, height=2,
              command=lambda: show_page(pages["borrow"])).pack(pady=10) #lambda is used to delay calling a function until it is needed.

    tk.Button(button_frame, text="Return a Book", width=25, height=2,
              command=lambda: show_page(pages["return"])).pack(pady=10)

    tk.Button(button_frame, text="View Records", width=25, height=2,
              command=show_records_page).pack(pady=10)
