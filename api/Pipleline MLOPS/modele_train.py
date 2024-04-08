import connectiondb
import preprocess




############################################ Modèle ARIMA #######################################################################

from statsmodels.tsa.arima.model import ARIMA

def Model_ARIMA(train_data):
    # Définissez le modèle SARIMA
    order=(22,1,22)
    model = ARIMA(train_data, order=order)
    # Entraînez le modèle
    model_fit2 = model.fit()

    return model_fit2

########################################## Modele SARIMA #######################################################################

from statsmodels.tsa.statespace.sarimax import SARIMAX

def Model_SARIMA(train_data):
    order=(22,1,22)
    seasonal_order =(0,0,0,0)
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()
    return model_fit



######################################### Modele SARIMAX avec la deuxieme variable###########################################################################

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error 

def Model_SARIMAX(train_data,test_data,train_data_2variable,test_data_2variable):
    from sklearn.metrics import mean_squared_error
    order = (8, 1, 8)
    seasonal_order = (1, 1, 3, 9)
    model_sarimax_exog = SARIMAX(train_data, exog=train_data_2variable, order=order,seasonal_order=seasonal_order).fit()
    ts_pred_exog = model_sarimax_exog.predict(start=test_data.index[0], end=test_data.index[-1],exog=test_data_2variable)
    rmse = mean_squared_error(test_data.values, ts_pred_exog.values, squared=False)
    return rmse, ts_pred_exog

###################################### Modele de Regression Lineaire ################################################################
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def Model_RegressionLineaire(X_train,y_train,X_test,y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Linear regression\n R^2={r2_score(y_test, y_pred):.2f}")
    return model



############################################ RandomForest ############################################################

from sklearn.ensemble import RandomForestRegressor

def Model_RandomForest(X_train,y_train,X_test,y_test):
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Random Forest regression\n R^2={r2_score(y_test, y_pred):.2f}")
    return model


################################ persitance des models ##################################################

import os
import joblib

def sauvegarder_modele(modele, chemin_dossier, nom_fichier):

    # Créer le dossier s'il n'existe pas
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)

    # Chemin complet du fichier de sauvegarde
    chemin_complet = os.path.join(chemin_dossier, nom_fichier)

    # Sauvegarde du modèle
    joblib.dump(modele, chemin_complet)

    return chemin_complet


############################### TRAIN ###############################################################



directory = 'Modele'

Ladata = connectiondb.Connexion()
data1, data, train_data, test_data = preprocess.preprocessing(Ladata)
X_train, X_test, y_train, y_test, train_data_2variable, test_data_2variable = preprocess.preprocessingML(data1)

Model_ARIMA = Model_ARIMA(train_data)
sauvegarder_modele(Model_ARIMA, directory, 'model_arima')

Model_SARIMA=Model_SARIMA(train_data)
sauvegarder_modele(Model_SARIMA, directory, 'model_sarima')

Model_SARIMAX = Model_SARIMAX(train_data,test_data,train_data_2variable,test_data_2variable)
sauvegarder_modele(Model_SARIMAX, directory, 'Model_sarimax')

Model_RegressionLineaire = Model_RegressionLineaire(X_train,y_train,X_test,y_test)
sauvegarder_modele(Model_RegressionLineaire, directory, 'model_regression')

Model_RandomForest = Model_RandomForest(X_train,y_train,X_test,y_test)
sauvegarder_modele(Model_RandomForest, directory, 'randomforest')

