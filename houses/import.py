import sys
import csv
from cs50 import SQL

if len(sys.argv) != 2:
    print("Usage: import.py file.csv")
    sys.exit(1)

open("students.db", "w").close()
db = SQL("sqlite:///students.db")

db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

with open(sys.argv[1], "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        full_name = row["name"].split()
        if len(full_name) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       full_name[0], full_name[1], full_name[-1], row["house"], row["birth"])
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       full_name[0], None, full_name[-1], row["house"], row["birth"])