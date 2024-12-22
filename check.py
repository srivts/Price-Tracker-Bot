import sqlite3
def clear_table():
    conn=sqlite3.connect("product_data.db")
    c=conn.cursor()
    c.execute("DELETE FROM products")
    conn.commit()
    rows=c.fetchall()
    conn.close()
    print("ALL RECORDS HAVE BEEN DELETED")

clear_table()

def check_database():
    conn=sqlite3.connect("product_data.db")
    c=conn.cursor()
    c.execute("SELECT * FROM products")
    rows=c.fetchall()
    conn.close()
    return rows

rows = check_database()
if not rows:
    print("The table is empty.")
else:
    print("Remaining records:")
    for row in rows:
        print(row)
