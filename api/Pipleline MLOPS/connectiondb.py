
import pandas as pd
import sqlite3
from io import StringIO

def Connexion():

    con = sqlite3.connect('temperature_yamoussoukro.db')
    data_test = pd.read_sql('SELECT * FROM temperature_yakro', con)

    con.close()

    # Convertir le DataFrame en une chaîne CSV
    csv_buffer = StringIO()
    data_test.to_csv(csv_buffer, index=False)
    print(data_test)

    # Réinitialiser la position du curseur dans le buffer
    csv_buffer.seek(0)
    print("La connexion a été etablie avec succès")
    return csv_buffer


Connexion()
