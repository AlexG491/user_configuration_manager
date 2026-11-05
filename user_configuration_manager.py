import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Collego questo programma con mysql
# I connect this program to MySQL

conn = mysql.connector.connect(

    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")

)

cursor = conn.cursor()

# aggiunge la chiave nella tabella, solo se la chiave è nuova.
# add the key in the table, only if the key is new.

def add_setting(key_value):

    key, value = key_value
    key, value = key.lower(), value.lower()


    try:

        cursor.execute(
            "INSERT INTO settings (setting_name, setting_value) VALUES (%s, %s)",
            (key, value)
        )

        conn.commit()

        return f"Setting '{key}' added with value '{value}' successfully!"

    except mysql.connector.IntegrityError:

        return f"Setting '{key}' already exists! Cannot add a new setting with this name."

# aggiorna le chiavi esistenti
# updates existing keys

def update_setting(key_value):

    key, value = key_value
    key, value = key.lower(), value.lower()

    cursor.execute(
        "SELECT setting_name FROM settings WHERE setting_name = %s",
        (key,)
    )

    row = cursor.fetchone()

    if row is None:

        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

    cursor.execute(
        "UPDATE settings SET setting_value = %s WHERE setting_name = %s",
        (value, key)
    )

    conn.commit()

    return f"Setting '{key}' updated to '{value}' successfully!"

# cancella le chiavi esistenti
# deletes existing keys

def delete_setting(key):

    key = key.lower()

    cursor.execute(
            "SELECT setting_name FROM settings WHERE setting_name = %s",
            (key,)
        )
    
    row = cursor.fetchone()
    
    if row is None:
    
        return f"Setting '{key}' does not exist! Cannot delete a non-existing setting."
    
    cursor.execute(
        "DELETE FROM settings WHERE setting_name = %s",
        (key,)
    )
    
    conn.commit()
    
    return f"'{key}' was deleted successfully!"

# visualizza le chiavi
# views the keys

def view_settings():

    cursor.execute("SELECT setting_name, setting_value FROM settings")

    rows = cursor.fetchall()

    if not rows:

        return "No settings available."

    result = "Current User Settings:\n"

    for key, value in rows:

        result += f"{key.capitalize()}: {value}\n"

    return result

tuple1 = ('volume', 'high')

tuple2 = ('theme', 'light')


print(add_setting(tuple1))

print(update_setting(tuple2))

print(view_settings())
