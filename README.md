# User Configuration Manager

*Italiano: see [README.it.md](README.it.md)*

A small Python program that manages user settings (key-value pairs such as `theme: dark`) and stores them in a MySQL database. It started as a dictionary-based exercise and was then extended to persist its data with MySQL.

## What it does

- **Add** a new setting (refused if the name already exists)
- **Update** the value of an existing setting (refused if the name does not exist)
- **Delete** an existing setting (refused if the name does not exist)
- **View** all the current settings

Names and values are saved in lowercase, and every operation returns a clear message describing what happened.

## Tech stack

- Python 3
- MySQL / MariaDB
- [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/) to talk to the database
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) to read the credentials from a `.env` file

## Project structure

```
.
├── user_configuration_manager.py    # the program: connection + the four functions
├── table_user_config_manager.sql    # creates the database and the settings table
├── .env.example                     # template of the environment variables
├── .gitignore                       # keeps .env out of Git
└── README.md
```

## Database design

The script `table_user_config_manager.sql` creates the database `user_config_manager` and a single table:

| Column          | Type           | Notes                                  |
|-----------------|----------------|----------------------------------------|
| `id`            | `INT`          | Primary key, auto-increment            |
| `setting_name`  | `VARCHAR(100)` | `NOT NULL`, **`UNIQUE`**               |
| `setting_value` | `VARCHAR(100)` | `NOT NULL`                             |

The `UNIQUE` constraint on `setting_name` is what prevents two settings from having the same name.

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install the dependencies**

   ```bash
   pip install mysql-connector-python python-dotenv
   ```

3. **Create the database and the table**

   Make sure MySQL (or MariaDB) is running, then run the contents of `table_user_config_manager.sql` with your favourite client (MySQL command line, Beekeeper Studio, phpMyAdmin...).

4. **Configure the credentials**

   Copy `.env.example` to `.env` and fill in your own values:

   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=user_config_manager
   ```

   The `.env` file is listed in `.gitignore`, so your credentials are never committed.

5. **Run the program**

   ```bash
   python user_configuration_manager.py
   ```

## Usage

Each function takes the setting as a `(name, value)` tuple, except `delete_setting`, which only needs the name.

```python
add_setting(('volume', 'high'))      # "Setting 'volume' added with value 'high' successfully!"
update_setting(('volume', 'low'))    # "Setting 'volume' updated to 'low' successfully!"
delete_setting('volume')             # "'volume' was deleted successfully!"
view_settings()                      # "Current User Settings: ..."
```

Example calls are also included at the bottom of `user_configuration_manager.py`.

## How it works

- `add_setting` tries the `INSERT` and catches `mysql.connector.IntegrityError`: if the name already exists, the database rejects the row because of the `UNIQUE` constraint.
- `update_setting` and `delete_setting` first run a `SELECT` to check that the name exists, then run the `UPDATE` / `DELETE` limited by a `WHERE` clause.
- All queries use `%s` placeholders instead of string formatting, so values are passed to the database safely.
- Every change is saved with `conn.commit()`.

## Known limitations

- The database connection is opened when the file is loaded and is never closed explicitly.
- The example calls at the bottom of the file run every time the script is executed.
- There are no automated tests yet.
- Names and values are limited to 100 characters and are always saved in lowercase.
