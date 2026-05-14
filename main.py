import csv
import datetime
from pathlib import Path

#data sotrager
borrowing_records = []
RECORDS_FILE = Path("records.csv")
CSV_HEADER = ["Name", "Title", "Borrowed Date", "Due Date", "Return Date", "Status", "Penalty"]

DAILY_PENALTY_RATE = 10.00 #penalty rate per day for late returns
DELETE_RECORD_PASSWORD = "admin123" #password to delete records 

# -----------------------------------------------FILE HANDLING----------------------------------------------- #

def _format_date(value):
    return value.isoformat() if value else ""

def _parse_date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%d").date() if value else None

def save_records_to_file():
    with RECORDS_FILE.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)

        for record in borrowing_records:
            writer.writerow([
                record["name"],
                record["title"],
                _format_date(record["borrow_date"]),
                _format_date(record["due_date"]),
                _format_date(record["return_date"]),
                record["status"],
                record["penalty"],
            ])

def load_records_from_file():
    global borrowing_records
    borrowing_records = []

    if not RECORDS_FILE.exists():
        return

    with RECORDS_FILE.open("r", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            if row == CSV_HEADER:
                continue
            
            # name,title,due_date,status,penalty
            if len(row) == 5:
                borrowing_records.append({
                    "name": row[0],
                    "title": row[1],
                    "borrow_date": None,
                    "due_date": _parse_date(row[2]),
                    "return_date": None,
                    "status": row[3],
                    "penalty": float(row[4]),
                })
                continue

            if len(row) != 7:
                continue

            borrowing_records.append({
                "name": row[0],
                "title": row[1],
                "borrow_date": _parse_date(row[2]),
                "due_date": _parse_date(row[3]),
                "return_date": _parse_date(row[4]),
                "status": row[5],
                "penalty": float(row[6]),
            })
# -----------------------------------------------FUNCTIONS----------------------------------------------- #


def calculate_penalty(due_date, return_date): # Calculate penalty based on how many days late
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        return overdue_days * DAILY_PENALTY_RATE, overdue_days
    return 0, 0

def borrow_book(name, title, days): # Handles borrowing logic and will create a new record
    name = name.strip()
    title = title.strip()
    days = days.strip()

    if not name or not title or not days:
        return "ERROR"

    try:
        days_to_borrow = int(days)
    except ValueError:
        return "ERROR"

    if days_to_borrow == 0:
        return "ERROR"

    borrow_date = datetime.date.today()
    due_date = borrow_date + datetime.timedelta(days=days_to_borrow)

    record = {
        "name": name,
        "title": title,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None,
        "penalty": 0.0,
        "status": "Borrowed"
    }

    borrowing_records.append(record)
    save_records_to_file()

    return "SUCCESS"

def return_book(name, title): # Handles returning logic and updates record status
    normalized_name = name.strip().lower()
    normalized_title = title.strip().lower()

    for record in borrowing_records:
        if (
            record["name"].lower() == normalized_name
            and record["title"].lower() == normalized_title
            and record["status"] == "Borrowed"
        ):
            return_date = datetime.date.today()
            penalty, days_late = calculate_penalty(record["due_date"], return_date)

            record["return_date"] = return_date
            record["penalty"] = penalty

            if penalty > 0:
                record["status"] = "Returned Late"
                save_records_to_file()
                return "LATE", penalty, days_late

            record["status"] = "Returned On Time"
            save_records_to_file()
            return "ONTIME", 0, 0

    return "NOT_FOUND"

def get_records(): # Returns all records (used GUI table)
    return borrowing_records

def remove_record(index, password): # Removes a record by index
    if password != DELETE_RECORD_PASSWORD:
        return "INVALID_PASSWORD"

    if index < 0 or index >= len(borrowing_records):
        return "NOT_FOUND"

    borrowing_records.pop(index)
    save_records_to_file()
    return "REMOVED"
