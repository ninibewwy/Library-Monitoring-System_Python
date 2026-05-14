import tkinter as tk

import borrowing
import home
import main
import records
import returning

main.load_records_from_file()

root = tk.Tk()
root.title("Library Book Borrowing and Return Monitoring System with Late Penalty Calculator")
root.geometry("800x500")

# ----------------------------------------------- CONTAINER ----------------------------------------------- #
container = tk.Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

pages = {}

for page_name in ("home", "borrow", "return", "records"):
    frame = tk.Frame(container)
    frame.grid(row=0, column=0, sticky="nsew")
    pages[page_name] = frame

# open the selected page
def show_page(page):
    page.tkraise()

# always show updated records
def show_records_page():
    update_records_table()
    show_page(pages["records"])

# pages
home.create_page(pages["home"], show_page, pages, show_records_page)
update_records_table = records.create_page(pages["records"], show_page, pages["home"])
borrowing.create_page(pages["borrow"], show_page, pages["home"], update_records_table)
returning.create_page(pages["return"], show_page, pages["home"], update_records_table)

#show the home page first
show_page(pages["home"])

root.mainloop()
