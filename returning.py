import datetime
import tkinter as tk
from tkinter import messagebox
import main

def create_page(parent, show_page, page_home, update_table): #creates return page
    def gui_return():
        name = entry_name.get().strip()
        title = entry_title.get().strip()

        if not name or not title:
            messagebox.showwarning("Input Error", "Enter borrower name and book title.")
            return

        result = main.return_book(name, title)

        if result == "NOT_FOUND":
            messagebox.showerror("Error", "Record not found")
            return

        if result[0] == "LATE":
            _, penalty, days_late = result
            messagebox.showinfo(
                "Late Return",
                f"Days Late: {days_late}\nPenalty: {penalty:.2f}"
            )
        else:
            messagebox.showinfo("Success", "Returned on time!")

        update_table()
        clear_entries()

    def clear_entries(): #clears the input
        entry_name.delete(0, tk.END)
        entry_title.delete(0, tk.END)

    tk.Label(parent, text="Return a Book",
             font=("Arial", 22, "bold")).pack(pady=30)

    today = datetime.date.today().strftime("%B %d, %Y")
    tk.Label(parent, text=f"Today: {today}",
             font=("Arial", 14)).pack(pady=5)

    frame = tk.Frame(parent)
    frame.pack(pady=30)

    tk.Label(frame, text="Borrower Name").grid(row=0, column=0, pady=8, padx=8, sticky="e")
    entry_name = tk.Entry(frame, width=30)
    entry_name.grid(row=0, column=1, pady=8)

    tk.Label(frame, text="Book Title").grid(row=1, column=0, pady=8, padx=8, sticky="e")
    entry_title = tk.Entry(frame, width=30)
    entry_title.grid(row=1, column=1, pady=8)

    button_frame = tk.Frame(parent)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Return", width=15,
              command=gui_return).grid(row=0, column=0, padx=8)
    tk.Button(button_frame, text="Clear", width=15,
              command=clear_entries).grid(row=0, column=1, padx=8)
    tk.Button(button_frame, text="Back to Home", width=15,
              command=lambda: show_page(page_home)).grid(row=0, column=2, padx=8)
