# Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template, request, redirect, flash, url_for
import random
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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
        dp = request.form['indop']
        category = request.form['incategory']
        rating = request.form['inrating']
        description = request.form['indescription']
#        image = request.form['img']


        if not title or not authour or not genre or not category or not dp or not rating or not description:
            flash('All fields are required!')
        else:
            conn.execute('INSERT INTO library (title, authour, genre, category, published, rating, description) VALUES ( ?, ?, ?, ?, ?, ?, ?)', 
                         ( title, authour, genre, category, dp, rating, description))
            conn.commit()
            conn.close()
            return render_template('newbook.html')
            
    return render_template('newbook.html')

@app.route('/viewbooks', methods=('POST', 'GET'))
def viewbooks():
    conn = get_db_connection()
    sql = "SELECT * FROM library"
    books = conn.execute(sql).fetchall()
    conn.close()
    return render_template('allbooks.html', books=books)

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_game(id):
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        genre = request.form['genre']
        year = request.form['year']
        sales = request.form['sales']


        if not id or not title or not platform or not genre or not year or not sales: 
            flash('All fields are required!')
        else:
            conn.execute('UPDATE games SET title = ?, platform = ?, genre = ?, year = ?, sales = ? WHERE id = ?', 
                (title, platform, genre, year, sales, id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_games'))
            
    return render_template('edit_user.html', games=games)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_game(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('view_games.html'))

if __name__ == '__main__':
    app.run(debug=True,port=7496)