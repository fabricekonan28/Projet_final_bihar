import sqlite3
import csv

# Connexion à la base de données
conn = sqlite3.connect('temperature_yamoussoukro.db')
cursor = conn.cursor()

# Création de la table temperature si elle n'existe pas déjà
cursor.execute('''CREATE TABLE IF NOT EXISTS temperature (
                    date TEXT,
                    temperature_2m REAL
                )''')

# Création de la table temperature1 si elle n'existe pas déjà
cursor.execute('''CREATE TABLE IF NOT EXISTS temperature1 (
                    relative_humidity_2m REAL
                )''')

# Fonction pour insérer les données du CSV dans la table temperature
def enregistrer_temperature(date, temperature_2m):
    cursor.execute('''INSERT INTO temperature (date, temperature_2m) VALUES (?, ?)''', (date, temperature_2m))
    conn.commit()

# Fonction pour insérer les données du CSV dans la table temperature1
def enregistrer_humidity(relative_humidity_2m):
    cursor.execute('''INSERT INTO temperature1 (relative_humidity_2m) VALUES (?)''', (relative_humidity_2m,))
    conn.commit()

# Lecture du fichier CSV et insertion des données dans la table temperature
with open('hourly_data.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        date = row['date']
        temperature_2m = float(row['temperature_2m'])
        enregistrer_temperature(date, temperature_2m)

#print("Données de la table temperature enregistrées avec succès.")

# Lecture du fichier CSV et insertion des données dans la table temperature1
with open('hourly_data_2iemeVariable111.csv', 'r') as csv_file1:
    csv_reader = csv.DictReader(csv_file1)
    for row in csv_reader:
        relative_humidity_2m = float(row['relative_humidity_2m'])
        enregistrer_humidity(relative_humidity_2m)

#print("Données de la table temperature1 enregistrées avec succès1111111.")

# Concaténation des tables temperature et temperature1 pour créer temperature_yakro
cursor.execute('''CREATE TABLE IF NOT EXISTS temperature_yakro AS
                    SELECT temperature.date, temperature.temperature_2m, temperature1.relative_humidity_2m
                    FROM temperature
                    INNER JOIN temperature1 ON temperature.rowid = temperature1.rowid''')

print("Table temperature_yakro créée avec succès.")


'''
# Fonction pour afficher les données de la table temperature_yakro
def afficher_temperature_yakro():
    cursor.execute('''SELECT * FROM temperature_yakro''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)  # Afficher chaque ligne de résultat

# Appel de la fonction pour afficher les données de la table temperature_yakro
afficher_temperature_yakro()

'''
# Fermeture de la connexion à la base de données
conn.close()
