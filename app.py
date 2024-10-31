# Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template, request, redirect, flash, url_for
import random
import sqlite3



app = Flask(__name__)
app.secret_key = "supersecretkey" 

@app.route('/')
def index():
    conn = get_db_connection()
    sql = "SELECT * FROM library ORDER BY id DESC"
    books = conn.execute(sql).fetchall()
    conn.close()
    return render_template('index.html', books=books)

def get_db_connection():
    conn = sqlite3.connect('book.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    conn = get_db_connection() 
    with app.open_resource('schema.sql') as f:
        conn.executescript (f.read().decode('utf8'))
    conn.close()

@app.route('/newbook', methods=('GET', 'POST'))
def newbook():
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM library').fetchone()

    if request.method == 'POST':
        title = request.form['intitle']
        authour = request.form['inauthour']
        genre = request.form['ingenre']
        category = request.form['incategory']
        dp = request.form['indop']
        rating = request.form['inrating']
        description = request.form['indescription']
#        image = request.form['img']


        if not title or not authour or not genre or not category or not dp or not rating or not description:
            flash('All fields are required!')
        else:
            conn.execute('INSERT INTO library (title, authour, genre, category, published, rating, description) VALUES ( ?, ?, ?, ?, ?, ?, ?)', 
                         ( title, authour, genre, category, dp, rating, description))
            sql = "SELECT * FROM library ORDER BY id DESC"
            books = conn.execute(sql).fetchall()
            conn.close()
            return render_template('index.html', books=books)
            
    return render_template('newbook.html')

@app.route('/viewbooks', methods=('POST', 'GET'))
def viewbooks():
    conn = get_db_connection()
    sql = "SELECT * FROM library"
    books = conn.execute(sql).fetchall()
    conn.close()
    return render_template('allbooks.html', books=books)

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM library WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['intitle']
        authour = request.form['inauthour']
        genre = request.form['ingenre']
        dp = request.form['indop']
        category = request.form['incategory']
        rating = request.form['inrating']
        description = request.form['indescription']

        if not id or not title or not authour or not genre or not dp or not category or not rating or not description: 
            flash('All fields are required!')
        else:
            conn.execute('UPDATE library SET title = ?, authour = ?, genre = ?, published = ?, category = ?, rating = ?, description = ? WHERE id = ?', 
                (title, authour, genre, dp, category, rating, description, id))
            conn.commit()
            conn.close()
            return redirect(url_for('bookinfo', id=id))
            
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>', methods=('POST', 'GET'))
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM library WHERE id = ?', (id,))
    conn.commit()
    sql = "SELECT * FROM library ORDER BY id DESC"
    books = conn.execute(sql).fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/bookinfo/<int:id>', methods=('GET', 'POST'))
def bookinfo(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM library WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('bookinfo.html', book=book)


if __name__ == '__main__':  
    app.run(debug=True,port=7496) 