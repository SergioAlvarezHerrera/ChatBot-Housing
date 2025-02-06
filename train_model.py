import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Cargar dataset

df = pd.read_csv("dataset_housing_price.csv", index_col=0)


# Convertir variables categóricas en numéricas
label_encoders = {}
categorical_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnished']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Guardamos los LabelEncoders por si los necesitamos luego

# Seleccionar características y variable objetivo
X = df.drop(columns=['price'])  # Todas las columnas menos "price"
y = df['price']

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Guardar el modelo entrenado
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Modelo entrenado y guardado como 'model.pkl'")
