from flask import Flask, render_template, request
import sqlite3
import os
app=Flask(__name__)

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH=os.path.join(BASE_DIR, '../product_data.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])

def submit():
    name=request.form['name']
    email=request.form['email']
    url=request.form['url']
    desired_price=request.form['desired_price']
    product_name = request.form['product_name']
    try:
        conn=sqlite3.connect(DATABASE_PATH)
        cursor=conn.cursor()
        cursor.execute("INSERT INTO products(name, email, url, desired_price, product_name) VALUES (?, ?, ?, ?, ?)",(name, email, url, desired_price, product_name))
        conn.commit()
        conn.close()
        return "data submitted successfully"
    except Exception as e:
        print(f"error: {e}")
        return f"an error occured {e}"

if __name__=='__main__':
    app.run(debug=True)