import sqlite3

def init_database():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    
    # Create guests table
    c.execute('''
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
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()