# Projet_final_Bihar

Projet
Le projet consiste en une API FastAPI pour la prédiction de données météorologiques à partir d'un modèle ARIMA. L'API permet de recevoir des requêtes avec des intervalles de dates spécifiques, d'effectuer des prédictions à l'aide du modèle ARIMA et de renvoyer les résultats aux utilisateurs.

# Data flow & architecture

L'architecture de l'application repose sur FastAPI pour la création des endpoints API, SQLite pour la gestion de la base de données des prédictions, et un modèle ARIMA pré-entraîné pour effectuer les prédictions météorologiques.

# Flux de Données

L'utilisateur envoie une requête avec des dates de début et de fin à l'API via un endpoint spécifique.
L'API reçoit la requête, effectue les prédictions à l'aide du modèle ARIMA pour chaque intervalle de 3 heures, et enregistre les résultats dans la base de données SQLite.
L'utilisateur peut également récupérer les prédictions à partir de la base de données via un autre endpoint de l'API.
Instructions d'Installation, Exécution, Construction et Test

# Running locally

Installation des Dépendances

pip install -r requirements.txt

Exécution de l'Application

uvicorn main:app --reload

Construction de l'Image Docker

docker build -t projetserietemporelle -f Dockerfile.txt .

Exécution de l'Image Docker dans un Conteneur

docker run -d --name projetbihar -p 8000:8000 projetserietemporelle

Exécution des Tests

pytest test/


# CI/CD steps
Le pipeline CI/CD est basé sur GitHub Actions et est défini dans le fichier .github/workflows/ci-cd.yml. Ce pipeline automatise les étapes suivantes :

1. Construction de l'image Docker à partir du Dockerfile.
2. Exécution des tests automatisés pour garantir l'intégrité du code.
3. Publication de l'image sur Docker Hub.
4. Déploiement de l'image sur un serveur distant.

Consultez le fichier ci-cd.yml ainsi que les commentaires dans le code pour plus de détails sur la configuration spécifique du pipeline CI/CD.


