from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Change this for production
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS guests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name1 TEXT NOT NULL,
                id_type1 TEXT NOT NULL,
                id_number1 TEXT NOT NULL,
                phone_number1 TEXT NOT NULL,
                id_images1 TEXT,
                name2 TEXT,
                id_type2 TEXT,
                id_number2 TEXT,
                phone_number2 TEXT,
                id_images2 TEXT,
                in_time TEXT NOT NULL,
                out_time TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Process form data
        name1 = request.form.get('name1', '').strip()
        id_type1 = request.form.get('id_type1', '').strip()
        id_number1 = request.form.get('id_number1', '').strip()
        phone_number1 = request.form.get('phone_number1', '').strip()
        
        name2 = request.form.get('name2', '').strip()
        id_type2 = request.form.get('id_type2', '').strip()
        id_number2 = request.form.get('id_number2', '').strip()
        phone_number2 = request.form.get('phone_number2', '').strip()
        
        in_time = request.form.get('in_time', '').strip()
        out_time = request.form.get('out_time', '').strip()

        # Process uploaded files
        def save_images(files):
            saved = []
            for file in files:
                if file and file.filename:
                    filename = f"{datetime.now().timestamp()}-{secure_filename(file.filename)}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    saved.append(filename)
            return ','.join(saved) if saved else None

        images1 = save_images(request.files.getlist('id_images1'))
        images2 = save_images(request.files.getlist('id_images2'))

        # Save to database
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO guests (
                    name1, id_type1, id_number1, phone_number1, id_images1,
                    name2, id_type2, id_number2, phone_number2, id_images2,
                    in_time, out_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name1, id_type1, id_number1, phone_number1, images1,
                name2, id_type2, id_number2, phone_number2, images2,
                in_time, out_time
            ))
            conn.commit()

        flash('Guest information saved successfully!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error saving guest data: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/guests')
def view_guests():
    search = request.args.get('search', '').strip()
    query = '''
        SELECT * FROM guests
        WHERE name1 LIKE ? OR name2 LIKE ? 
        OR id_number1 LIKE ? OR id_number2 LIKE ?
        OR phone_number1 LIKE ? OR phone_number2 LIKE ?
        ORDER BY created_at DESC
    '''
    params = (f'%{search}%',) * 6

    with get_db_connection() as conn:
        guests = conn.execute(query, params).fetchall()

    # Process guests for template
    guests_list = []
    for guest in guests:
        guests_list.append({
            'id': guest['id'],
            'name1': guest['name1'],
            'id_type1': guest['id_type1'],
            'id_number1': guest['id_number1'],
            'phone_number1': guest['phone_number1'],
            'images1': guest['id_images1'].split(',') if guest['id_images1'] else [],
            'name2': guest['name2'],
            'id_type2': guest['id_type2'],
            'id_number2': guest['id_number2'],
            'phone_number2': guest['phone_number2'],
            'images2': guest['id_images2'].split(',') if guest['id_images2'] else [],
            'in_time': guest['in_time'],
            'out_time': guest['out_time']
        })

    return render_template('guests.html', guests=guests_list, search_query=search)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)