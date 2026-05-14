import datetime
import tkinter as tk
from tkinter import messagebox
import main

def create_page(parent, show_page, page_home, update_table): #creates the borrowing page
    def show_success_popup(): #popup after successful borrowing
        popup = tk.Toplevel(parent)
        popup.title("Book Borrowed")
        popup.geometry("360x180")
        popup.resizable(False, False)
        popup.transient(parent.winfo_toplevel())
        popup.grab_set()

        tk.Label(
            popup,
            text="Book borrowed successfully!",
            font=("Arial", 16, "bold")
        ).pack(pady=(20, 10))

        tk.Label(
            popup,
            text="The record has been saved.",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(popup, text="OK", width=12, command=popup.destroy).pack(pady=20)

    def gui_borrow(): #handles borrow logic
        name = entry_name.get()
        title = entry_title.get()
        days = entry_days.get()
        result = main.borrow_book(name, title, days)

        if result == "ERROR":
            messagebox.showwarning(
                "Input Error",
                "Enter a name, title, and a valid number of borrowing days."
            )
            return

        show_success_popup()
        update_table()
        clear_entries()

    def clear_entries(): #clears the input 
        entry_name.delete(0, tk.END)
        entry_title.delete(0, tk.END)
        entry_days.delete(0, tk.END)

    tk.Label(parent, text="Borrow a Book",
             font=("Arial", 22, "bold")).pack(pady=30)

    today = datetime.date.today().strftime("%B %d, %Y")
    tk.Label(parent, text=f"Today: {today}",
             font=("Arial", 14)).pack(pady=5)

    frame = tk.Frame(parent)
    frame.pack(pady=25)

    tk.Label(frame, text="Borrower Name").grid(row=0, column=0, pady=8, padx=8, sticky="e")
    entry_name = tk.Entry(frame, width=30)
    entry_name.grid(row=0, column=1, pady=8)

    tk.Label(frame, text="Book Title").grid(row=1, column=0, pady=8, padx=8, sticky="e")
    entry_title = tk.Entry(frame, width=30)
    entry_title.grid(row=1, column=1, pady=8)

    tk.Label(frame, text="Days To Borrow").grid(row=2, column=0, pady=8, padx=8, sticky="e")
    entry_days = tk.Entry(frame, width=30)
    entry_days.grid(row=2, column=1, pady=8)

    button_frame = tk.Frame(parent)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Borrow", width=15,
              command=gui_borrow).grid(row=0, column=0, padx=8)
    tk.Button(button_frame, text="Clear", width=15,
              command=clear_entries).grid(row=0, column=1, padx=8)
    tk.Button(button_frame, text="Back to Home", width=15,
              command=lambda: show_page(page_home)).grid(row=0, column=2, padx=8)
