from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key

# Database setup
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
''')
conn.commit()
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return render_template('home.html', notes=notes)


@app.route('/add_note', methods=['POST'])
def add_note():
    content = request.form['content']
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute('UPDATE notes SET content = ? WHERE id = ?', (content, note_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    conn.close()
    return render_template('edit_note.html', note=note)


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
