import sqlite3

def setup_db():
    # This creates the database file 'campus.db'
    conn = sqlite3.connect('campus.db')
    cursor = conn.cursor()

    # 1. Create a table for Faculty
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            status TEXT,
            room TEXT
        )
    ''')

    # 2. Add some sample data (Run this once)
    faculty_data = [
        (1, 'Mr.R S kamble', 'AIML', 'Available', 'Lab 102'),
        (2, 'Mr.Nresh Kamble', 'CS', 'In Lecture', 'Room 305'),
        (3, 'Mr. Todkar', 'AIML', 'In Meeting', 'HOD Office')
    ]

    cursor.executemany('INSERT OR REPLACE INTO faculty VALUES (?,?,?,?,?)', faculty_data)
    
    conn.commit()
    conn.close()
    print("Database created and faculty data added!")

if __name__ == "__main__":
    setup_db()