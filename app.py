from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# =========================
# BUAT DATABASE & TABEL
# =========================
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    judul TEXT,
    penulis TEXT
)
""")

conn.commit()
conn.close()


def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# ROUTE INDEX
# =========================
@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=data)


# =========================
# TAMBAH DATA
# =========================
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (judul, penulis) VALUES (?, ?)',
            (judul, penulis)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')


# =========================
# EDIT DATA
# =========================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    book = conn.execute(
        'SELECT * FROM books WHERE id = ?', (id,)
    ).fetchone()

    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']

        conn.execute(
            'UPDATE books SET judul = ?, penulis = ? WHERE id = ?',
            (judul, penulis, id)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    conn.close()
    return render_template('edit.html', book=book)


# =========================
# HAPUS DATA
# =========================
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
