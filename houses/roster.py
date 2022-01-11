import sys
from cs50 import SQL

if len(sys.argv) != 2:
    print("Usage: import.py House")
    sys.exit(1)

with open("students.db", "r"):
    db = SQL("sqlite:///students.db")
    roster = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", sys.argv[1])

for i in range(len(roster)):
    student = roster[i]
    if student["middle"] == None:
        print(f'{student["first"]} {student["last"]}, born {student["birth"]}')
    else:
        print(f'{student["first"]} {student["middle"]} {student["last"]}, born {student["birth"]}')