from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Cargar el modelo
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
print("Modelo cargado correctamente")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Preguntas para las cuales recibimos respuestas "Sí" o "No"
        boolean_fields = [
            'mainroad', 'guestroom', 'basement', 'hotwaterheating', 
            'airconditioning', 'prefarea', 'furnished'
        ]

        # Convertir "Sí" y "No" en 1 y 0
        for field in boolean_fields:
            if field in data:
                if isinstance(data[field], str):  # Solo aplicar .lower() si es una cadena
                    data[field] = 1 if data[field].lower() in ["sí", "si"] else 0
                elif isinstance(data[field], int):  # Si ya es un número, asignar 1 o 0 según el valor
                    data[field] = 1 if data[field] == 1 else 0

        # Crear DataFrame con las respuestas
        input_data = pd.DataFrame([[data[field] for field in [
            'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 
            'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnished'
        ]]], columns=['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 
                     'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnished'])

        # Realizar la predicción
        prediction = model.predict(input_data)[0]

        # Devolver la predicción como un JSON
        return jsonify({'predicted_price': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)
