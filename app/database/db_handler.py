import sqlite3
from assets.constants import DATABASE_PATH

def initialize_database():
    """Calls SCHEMA.SQL and Creates a default value in in display_mode if there is none"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    with open("app/database/schema.sql", 'r') as sql_file:
        conn.executescript(sql_file.read())  # Run the SQL schema file

    c.execute("SELECT * FROM display_mode")
    
    items = c.fetchall() # Create a list of all items from table
    
    if len(items) == 0:
        c.execute("INSERT INTO display_mode (mode) VALUES ('light')")
        print("Default Mode Set to Light")
    
    else: 
        for item in items:
            print(f"DEFAULT DISPLAY MODE: {item[1]}\n")

    conn.commit()  # Save changes to the database (if any)
    conn.close()   # Close the connection



def get_display_mode():
    """Querys the database and Returns mode varible from display_mode table"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * from display_mode")
    current_mode = c.fetchone()
    print(f"CURRENT DISPLAY MODE: {current_mode[1]}\n")
    
    conn.commit()  # Save changes to the database (if any)
    conn.close()   # Close the connection

    return current_mode[1]


def update_display_mode(mode):
    """Update mode in display_mode table to received mode varible"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("UPDATE display_mode SET mode = ? WHERE rowid = 1", (mode,))
    c.execute("SELECT * from display_mode")
    
    current_mode = c.fetchone()

    print(f"NEW DISPLAY MODE: {current_mode[1]} \nUPDATED TO DATABASE\n")
    
    conn.commit()  # Save changes to the database (if any)
    conn.close()   # Close the connection

