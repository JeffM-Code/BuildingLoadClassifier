import streamlit as st
import joblib
import numpy as np
import zipfile
import os

heating_zip_file_path = 'heating_load_classifier.zip'
cooling_zip_file_path = 'cooling_load_classifier.zip'

def unzip_model(zip_path, output_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()
    if not os.path.exists(output_name):
        return False
    return True

if not unzip_model(heating_zip_file_path, 'heating_load_classifier.bin') or not unzip_model(cooling_zip_file_path, 'cooling_load_classifier.bin'):
    st.stop()

try:
    clf_heating = joblib.load('heating_load_classifier.bin')
    clf_cooling = joblib.load('cooling_load_classifier.bin')
except Exception as e:
    st.error(f"Model failed to load: {e}")
    st.stop()

features = {
    "X1": "Relative Compactness",
    "X2": "Surface Area",
    "X3": "Wall Area",
    "X4": "Roof Area",
    "X5": "Overall Height",
    "X6": "Orientation",
    "X7": "Glazing Area",
    "X8": "Glazing Area Distribution"
}

st.title('Building Energy Efficiency Prediction')

inputs = {}
for feature, description in features.items():
    value = st.text_input(f'{description} ({feature})', '0')
    inputs[feature] = float(value)

if st.button('Predict'):
    input_values = np.array([list(inputs.values())])
    heating_prediction = clf_heating.predict(input_values)
    cooling_prediction = clf_cooling.predict(input_values)
    
    st.write(f'Predicted Heating Load Classification: {heating_prediction[0]}')
    st.write(f'Predicted Cooling Load Classification: {cooling_prediction[0]}')
