from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from datetime import datetime
import pandas as pd
import sqlite3
from loguru import logger  # Importer Loguru
import uvicorn
from fastapi import Query
from typing import Optional

# Définition de la classe pour le corps de la requête
class DonneesEntree(BaseModel):
    step: int
    start_date: str  # Date de début de l'intervalle au format YYYY-MM-DD HH:MM:SS
    end_date: str    # Date de fin de l'intervalle au format YYYY-MM-DD HH:MM:SS

# Charger le modèle ARIMA
modele = joblib.load('Modele/model_arima')

# Créer une instance de l'application FastAPI
app = FastAPI()

chemin_fichier_log = "data/logs.log"
logger.add(chemin_fichier_log, rotation="500 MB", retention="10 days", level="INFO")

# Fonction pour enregistrer les prédictions dans un DataFrame
def enregistrer_prediction_dataframe(dates, predictions):
    df = pd.DataFrame({'date': dates, 'prediction': predictions})
    return df

# Fonction pour enregistrer les prédictions dans la base de données SQLite
def enregistrer_prediction_sqlite(df, chemin='data'):

    try:
        conn = sqlite3.connect(chemin)
        df.to_sql('predictions', conn, if_exists='append', index=False)
        conn.close()
        print("Prédictions enregistrées avec succès dans la base de données.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des prédictions : {str(e)}")


@app.get("/")
def root():
    logger.info("Endpoint racine appelé")
    return {"message": "API réalisé par KRA FABRICE!"}

# Définir le point de terminaison pour les prédictions
@app.post("/predict")
async def predict(data: DonneesEntree):
    try:
        logger.info(f"Prédictions demandées pour les dates {data.start_date} à {data.end_date}")
        # Convertir les dates en format datetime
        start_date = datetime.strptime(data.start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(data.end_date, "%Y-%m-%d %H:%M:%S")

        # Liste pour stocker les dates et les prédictions
        dates = []
        predictions = []

        # Boucle pour calculer les prédictions pour chaque intervalle de 3 heures
        current_date = start_date
        while current_date <= end_date:
            # Faire la prédiction pour l'intervalle actuel
            prediction = modele.predict(start=current_date, end=current_date, dynamic=False)  # Sans prédiction dynamique

            # Ajouter la date et la prédiction aux listes
            dates.append(current_date)
            predictions.append(prediction[0])  # Prendre le premier élément de la prédiction

            # Passer à l'intervalle de 3 heures suivant
            current_date += pd.Timedelta(hours=3)  # Utiliser Pandas Timedelta pour ajouter 3 heures
        logger.info("Prédictions effectuées avec succès")
        # Enregistrer les prédictions dans un DataFrame
        df_predictions = enregistrer_prediction_dataframe(dates, predictions)
        chemin_base_de_donnees = 'data/predictions.db'
        # Enregistrer les prédictions dans la base de données SQLite
        enregistrer_prediction_sqlite(df_predictions, chemin_base_de_donnees)

        return {"predictions": df_predictions.to_dict(orient='records')}  # Convertir le DataFrame en format JSON

    except Exception as e:
        logger.error(f"Erreur lors des prédictions : {str(e)}")
        return {"error": str(e)}

@app.get("/predictions")
async def get_predictions(start_date: Optional[str] = Query(None, description="Date de début au format YYYY-MM-DD"),
                          end_date: Optional[str] = Query(None, description="Date de fin au format YYYY-MM-DD")):
    try:
        logger.info("Début de la récupération des prédictions depuis la base de données")

        # Construction de la requête SQL en fonction des paramètres
        conn = sqlite3.connect('data/predictions.db')
        if start_date and end_date:
            query = f"SELECT * FROM predictions WHERE date BETWEEN '{start_date}' AND '{end_date}'"
        elif start_date:
            query = f"SELECT * FROM predictions WHERE date >= '{start_date}'"
        elif end_date:
            query = f"SELECT * FROM predictions WHERE date <= '{end_date}'"
        else:
            query = "SELECT * FROM predictions"

        # Exécution de la requête SQL
        df_predictions = pd.read_sql_query(query, conn)
        conn.close()

        predictions_list = df_predictions.to_dict(orient='records')
        logger.info("Prédictions récupérées avec succès depuis la base de données")
        return {"predictions": predictions_list}

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prédictions : {str(e)}")
        return {"error": "Erreur lors de la récupération des prédictions"}

# Endpoint pour récupérer les prédictions combinées avec les données réelles

def get_data_from_csv(start_date=None, end_date=None):
    try:
        # Lire les données depuis le fichier CSV
        df = pd.read_csv('data/hourly_data_réel.csv')

        # Convertir la colonne 'time' en format datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        # Filtrer les données en fonction de l'intervalle de dates spécifié
        if start_date and end_date:
            mask = (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)
        elif start_date:
            mask = df['Timestamp'] >= start_date
        elif end_date:
            mask = df['Timestamp'] <= end_date
        else:
            # Si aucune date n'est spécifiée, retourner toutes les données
            return df.to_dict(orient='records')

        filtered_data = df.loc[mask]
        return filtered_data.to_dict(orient='records')

    except Exception as e:
        # Gérer les erreurs de lecture ou de traitement des données
        return {"error": str(e)}

@app.get("/predictionsFabio")
async def get_predictionsFabio(start_date: Optional[str] = Query(None, description="Date de début au format YYYY-MM-DD"),
                               end_date: Optional[str] = Query(None, description="Date de fin au format YYYY-MM-DD")):
    try:
        logger.info("Début de la récupération des données")

        # Obtenir les données filtrées à partir du fichier CSV
        predictions_data_csv = get_data_from_csv(start_date, end_date)

        if "error" in predictions_data_csv:
            # Gérer les erreurs provenant de la fonction get_data_from_csv
            logger.error(f"Erreur lors de la récupération des données CSV : {predictions_data_csv['error']}")
            return predictions_data_csv

        # Construction de la requête SQL en fonction des paramètres
        conn = sqlite3.connect('data/predictions.db')
        if start_date and end_date:
            query = f"SELECT * FROM predictions WHERE date BETWEEN '{start_date}' AND '{end_date}'"
        elif start_date:
            query = f"SELECT * FROM predictions WHERE date >= '{start_date}'"
        elif end_date:
            query = f"SELECT * FROM predictions WHERE date <= '{end_date}'"
        else:
            query = "SELECT * FROM predictions"

        # Exécution de la requête SQL
        df_predictions_db = pd.read_sql_query(query, conn)
        conn.close()

        predictions_list_db = df_predictions_db.to_dict(orient='records')

        # Convertir les valeurs flottantes en chaînes de caractères pour la réponse JSON
        for item in predictions_data_csv:
            item['temperature_2m'] = str(item['temperature_2m'])

        # Associer les résultats du fichier CSV et de la base de données
        combined_predictions = {"predictions_csv": predictions_data_csv, "predictions_db": predictions_list_db}

        logger.info("Données récupérées avec succès")
        return combined_predictions

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prédictions : {str(e)}")
        return {"error": "Erreur lors de la récupération des prédictions"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
