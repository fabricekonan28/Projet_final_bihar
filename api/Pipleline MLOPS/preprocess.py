import connectiondb
import pandas as pd 
from sklearn.model_selection import train_test_split

def preprocessing(data1):
    data = pd.read_csv(data1, index_col=None)
    # Convertir la colonne de dates en type datetime
    data['date'] = pd.to_datetime(data['date'])
    # Supprimer la partie "+00:00" du format de date
    data['date'] = data['date'].dt.strftime('%Y-%m-%d %H:%M')
    data1 = data.copy()
    data.drop(columns=['relative_humidity_2m'], inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    data1['date'] = pd.to_datetime(data1['date'])
    # Définir la colonne 'date' comme index
    data.set_index('date', inplace=True)
    data1.set_index('date', inplace=True)
    # Calculer la moyenne des valeurs à chaque intervalle de 3 heures
    new_series = data.resample('3h').mean()
    new_series.index.names = ['Timestamp']

    new_series_2variables = data.resample('3h').mean()
    new_series_2variables.index.names = ['Timestamp']

    # Fractionner les données en 80% pour l'entraînement et 20% pour le test
    train_size = int(len(new_series) * 0.8)

    train_data = new_series[:train_size]
    test_data = new_series[train_size:]

    return new_series_2variables,new_series, train_data, test_data


column_value ='temperature_2m'

def preprocessingML(dataset):

    # Réinitialiser l'index
    new_series1 = dataset.copy()
    new_series_ML= dataset.copy()
    test= dataset.copy()

    #Importation de train_test_split pour la division des données
    from sklearn.model_selection import train_test_split
    # Fractionner les données en 80% pour l'entraînement et 20% pour le test pour le modèle SARIMAX
    train_size_2variable = int(len(new_series1) * 0.8)
    train_data_2variable = new_series1[:train_size_2variable]
    test_data_2variable = new_series1[train_size_2variable:]

    # Les Methodes ML(Regression Lineaire & Random Forest regression
    for i in range(1, 10):
        new_series_ML[f"lag_{i}"] = new_series_ML[column_value].shift(i)
    new_series_ML.dropna(inplace=True)
    # Fractionner les données en 80% pour l'entraînement et 20% pour le test
    X = new_series_ML.drop(column_value, axis=1)
    y = new_series_ML[column_value]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    
    return X_train, X_test, y_train, y_test, train_data_2variable, test_data_2variable
    

###################################################################################################

