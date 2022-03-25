import sqlite3

connection = sqlite3.connect("accounting.db")
cursor = connection.cursor()

def push(price, month, day, year, cat, det, user):
    command = 'INSERT INTO records (price, month, day, year, user, category, detail) VALUES (?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(command, (price, month, day, year, user, cat, det))
    connection.commit()

def show_all():
    rows = cursor.execute("SELECT * FROM records").fetchall()
    print(rows)

def total(month, day, year, user):
    command = 'SELECT SUM(price) FROM records WHERE month = ? AND day = ? AND year = ? AND user = ?;'
    sum_price = cursor.execute(command, (month, day, year, user)).fetchone()[0]
    return sum_price if sum_price else 0
