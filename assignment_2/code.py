import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from genetic_selection import GeneticSelectionCV
from sklearn.linear_model import LinearRegression

# Load the dataset
data = pd.read_csv("Housing_Prices_dataset.csv")

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

estimator = LinearRegression()

selector = GeneticSelectionCV(estimator, cv=5, verbose=1, scoring='neg_mean_squared_error',
                                n_population=100, crossover_proba=0.5, mutation_proba=0.2,
                                n_generations=40, crossover_independent_proba=0.5,
                                mutation_independent_proba=0.05, tournament_size=3,
                                n_gen_no_change=10, caching=True, n_jobs=-1)

selector.fit(X_train, y_train)

selected_features = X.columns[selector.support_]

regressor = LinearRegression()
regressor.fit(X_train[selected_features], y_train)

y_pred = regressor.predict(X_test[selected_features])
mse = mean_squared_error(y_test, y_pred)
print("Mean squared error on testing set: ", mse)
