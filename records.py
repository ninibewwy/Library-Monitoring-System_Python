import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import main

def create_page(parent, show_page, page_home): #creates the records page
    tk.Label(parent, text="Records",
             font=("Arial", 18, "bold")).pack(pady=20)

    columns = ("Name", "Title", "Borrowed Date", "Due Date", "Status", "Penalty")

    table_frame = tk.Frame(parent)
    table_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=140)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def update_table(): #refreshes the table with current records 
        for row in tree.get_children():
            tree.delete(row)

        for index, record in enumerate(main.get_records()):
            borrow_date = (
                record["borrow_date"].strftime("%b %d, %Y")
                if record["borrow_date"] else "-"
            )
            tree.insert("", "end", values=(
                record["name"],
                record["title"],
                borrow_date,
                record["due_date"].strftime("%b %d, %Y"),
                record["status"],
                f"{record['penalty']:.2f}"
            ), iid=str(index))

    def clear_selected_record(): # deletes selected record after password confirmation
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Select a record to remove.")
            return

        password = simpledialog.askstring(
            "Password Required",
            "Enter password to remove the selected record:",
            show="*",
            parent=parent
        )

        if password is None:
            return

        result = main.remove_record(int(selected_item[0]), password)

        if result == "INVALID_PASSWORD":
            messagebox.showerror("Access Denied", "Incorrect password.")
            return

        if result == "NOT_FOUND":
            messagebox.showerror("Error", "Selected record no longer exists.")
            update_table()
            return

        update_table()
        messagebox.showinfo("Record Removed", "The selected record was removed.")

    update_table()

    tk.Button(parent, text="Clear Selected Record", width=20,
              command=clear_selected_record).pack(pady=(10, 5))
    tk.Button(parent, text="← Back to Home", width=15,
              command=lambda: show_page(page_home)).pack(pady=10)

    return update_table
