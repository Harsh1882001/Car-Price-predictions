import pickle
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained model
model = pickle.load(open("LinearRegressionModel.pkl", 'rb'))

# Load car dataset
car = pd.read_csv("Cleaned car data.csv")


@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()
    companies.insert(0, "Select Company")

    return render_template('index.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type)


# New route to dynamically fetch car models based on selected company
@app.route('/get_models', methods=['POST'])
def get_models():
    data = request.get_json()
    company = data.get("company")

    # Filter models by selected company
    models = sorted(car[car['company'] == company]['name'].unique().tolist())

    return jsonify({"models": models})


@app.route('/predict', methods=['POST'])
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_model')
    year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel_type')

    try:
        kms_driven = int(request.form.get('kilo_driven').replace(',', ''))
    except ValueError:
        return "Invalid Kilometers Driven Input"

    # Make prediction
    prediction = model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]],
                                            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))

    return str(np.round(prediction[0], 2))


if __name__ == "__main__":
    app.run(debug=True)
