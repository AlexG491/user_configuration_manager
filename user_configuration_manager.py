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

test_settings = {
    'theme': 'light'

}


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

def update_setting(dictionary, key_value):

    key, value = key_value

    key, value = key.lower(), value.lower()

    if key in dictionary:

        dictionary[key] = value

        return f"Setting '{key}' updated to '{value}' successfully!"

    else:

        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

def delete_setting(dictionary, key):

    key = key.lower()

    if key in dictionary:

        dictionary.pop(key) # pop() cancella quel singolo elemento che vuoi cancellare

        return f"Setting '{key}' deleted successfully!"

    else:

        return "Setting not found!"

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

tuple2 = ('theme', 'dark')

print(add_setting(tuple1))

print(update_setting(test_settings, tuple2))

print(view_settings())