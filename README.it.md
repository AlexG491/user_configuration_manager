# User Configuration Manager

*English: vedi [README.md](README.md)*

Un piccolo programma Python che gestisce le impostazioni di un utente (coppie chiave-valore come `theme: dark`) e le salva in un database MySQL. Nasce come esercizio basato su un dizionario ed è stato poi esteso per rendere i dati persistenti con MySQL.

## Cosa fa

- **Aggiunge** una nuova impostazione (rifiutata se il nome esiste già)
- **Aggiorna** il valore di un'impostazione esistente (rifiutato se il nome non esiste)
- **Cancella** un'impostazione esistente (rifiutato se il nome non esiste)
- **Mostra** tutte le impostazioni attuali

Nomi e valori vengono salvati in minuscolo, e ogni operazione restituisce un messaggio chiaro su cosa è successo.

## Tecnologie

- Python 3
- MySQL / MariaDB
- [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/) per comunicare con il database
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) per leggere le credenziali da un file `.env`

## Struttura del progetto

```
.
├── user_configuration_manager.py    # il programma: connessione + le quattro funzioni
├── table_user_config_manager.sql    # crea il database e la tabella settings
├── .env.example                     # modello delle variabili d'ambiente
├── .gitignore                       # tiene .env fuori da Git
└── README.it.md
```

## Struttura del database

Lo script `table_user_config_manager.sql` crea il database `user_config_manager` e una sola tabella:

| Colonna         | Tipo           | Note                                   |
|-----------------|----------------|----------------------------------------|
| `id`            | `INT`          | Chiave primaria, auto-incremento       |
| `setting_name`  | `VARCHAR(100)` | `NOT NULL`, **`UNIQUE`**               |
| `setting_value` | `VARCHAR(100)` | `NOT NULL`                             |

Il vincolo `UNIQUE` su `setting_name` impedisce che due impostazioni abbiano lo stesso nome.

## Installazione

1. **Clona il repository**

   ```bash
   git clone <url-del-repository>
   cd <cartella-del-repository>
   ```

2. **Installa le dipendenze**

   ```bash
   pip install mysql-connector-python python-dotenv
   ```

3. **Crea il database e la tabella**

   Assicurati che MySQL (o MariaDB) sia acceso, poi esegui il contenuto di `table_user_config_manager.sql` con il tuo client preferito (riga di comando MySQL, Beekeeper Studio, phpMyAdmin...).

4. **Configura le credenziali**

   Copia `.env.example` in `.env` e inserisci i tuoi valori:

   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=user_config_manager
   ```

   Il file `.env` è nel `.gitignore`, quindi le tue credenziali non finiscono mai in un commit.

5. **Avvia il programma**

   ```bash
   python user_configuration_manager.py
   ```

## Utilizzo

Ogni funzione riceve l'impostazione come tupla `(nome, valore)`, tranne `delete_setting`, che ha bisogno solo del nome.

```python
add_setting(('volume', 'high'))      # "Setting 'volume' added with value 'high' successfully!"
update_setting(('volume', 'low'))    # "Setting 'volume' updated to 'low' successfully!"
delete_setting('volume')             # "'volume' was deleted successfully!"
view_settings()                      # "Current User Settings: ..."
```

In fondo a `user_configuration_manager.py` ci sono anche alcune chiamate di esempio.

## Come funziona

- `add_setting` prova l'`INSERT` e intercetta `mysql.connector.IntegrityError`: se il nome esiste già, il database rifiuta la riga grazie al vincolo `UNIQUE`.
- `update_setting` e `delete_setting` eseguono prima una `SELECT` per controllare che il nome esista, poi l'`UPDATE` / `DELETE` limitato da una clausola `WHERE`.
- Tutte le query usano i segnaposto `%s` invece della formattazione delle stringhe, così i valori arrivano al database in modo sicuro.
- Ogni modifica viene salvata con `conn.commit()`.

## Limiti noti

- La connessione al database viene aperta quando il file viene caricato e non viene chiusa esplicitamente.
- Le chiamate di esempio in fondo al file vengono eseguite a ogni avvio dello script.
- Non ci sono ancora test automatici.
- Nomi e valori sono limitati a 100 caratteri e vengono sempre salvati in minuscolo.
