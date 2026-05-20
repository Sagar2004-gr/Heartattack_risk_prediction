import pickle
import streamlit as st
import pandas as pd
from xgboost import XGBClassifier

# Load Model
model = pickle.load(open('xgboost_model.pkl', 'rb'))

# Page Config
st.set_page_config(page_title="Heart Attack Risk Prediction",page_icon="❤️",layout="centered")

# Load External CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Title
st.title("Heart Attack Risk Prediction")

st.write("Enter patient details to predict heart attack risk")

# Input Fields
Age = st.number_input('Age',min_value=20,max_value=100,value=25)
RestingBP = st.number_input('Resting Blood Pressure',min_value=0,max_value=250,value=120)
Cholesterol = st.number_input('Cholesterol',min_value=0,max_value=650,value=200)
MaxHR = st.number_input('Maximum Heart Rate',min_value=60,max_value=250,value=150)
Oldpeak = st.number_input('Oldpeak',min_value=-3.0,max_value=7.0,value=1.0)
FastingBS = st.selectbox('Fasting Blood Sugar',(1, 0))
ChestPainType = st.selectbox('Chest Pain Type',('ATA - Atypical Angina','NAP - Non-Anginal Pain','ASY - Asymptomatic','TA - Typical Angina'))
RestingECG = st.selectbox('Resting ECG',('Normal', 'ST', 'LVH'))
ExerciseAngina = st.selectbox('Exercise Angina',('N', 'Y'))
ST_Slope = st.selectbox('ST Slope',('Up', 'Flat', 'Down'))
Gender = st.selectbox('Gender',('M', 'F'))
Smoker = st.selectbox('Smoker',('Yes', 'No'))
FoodConsumption = st.selectbox('Food Consumption',('High', 'Less'))

# Encoding
Sex = 1 if Gender == 'M' else 0
ExerciseAngina = 1 if ExerciseAngina == 'Y' else 0
Smoker = 1 if Smoker == 'Yes' else 0
FoodConsumption = 1 if FoodConsumption == 'High' else 0

# Chest Pain Encoding
ChestPainType_ASY = 1 if ChestPainType == 'ASY - Asymptomatic' else 0
ChestPainType_ATA = 1 if ChestPainType == 'ATA - Atypical Angina' else 0
ChestPainType_NAP = 1 if ChestPainType == 'NAP - Non-Anginal Pain' else 0
ChestPainType_TA = 1 if ChestPainType == 'TA - Typical Angina' else 0

# Resting ECG Encoding
RestingECG_LVH = 1 if RestingECG == 'LVH' else 0
RestingECG_Normal = 1 if RestingECG == 'Normal' else 0
RestingECG_ST = 1 if RestingECG == 'ST' else 0

# ST Slope Encoding
ST_Slope_dict = {
    'Up': 0,
    'Flat': 1,
    'Down': 2
}
ST_Slope = ST_Slope_dict[ST_Slope]

# Input DataFrame
input_features = pd.DataFrame({
    'Age': [Age],
    'Sex': [Sex],
    'RestingBP': [RestingBP],
    'Cholesterol': [Cholesterol],
    'FastingBS': [FastingBS],
    'MaxHR': [MaxHR],
    'ExerciseAngina': [ExerciseAngina],
    'Oldpeak': [Oldpeak],
    'ST_Slope': [ST_Slope],
    'Smoker': [Smoker],
    'FoodConsumption': [FoodConsumption],
    'ChestPainType_ASY': [ChestPainType_ASY],
    'ChestPainType_ATA': [ChestPainType_ATA],
    'ChestPainType_NAP': [ChestPainType_NAP],
    'ChestPainType_TA': [ChestPainType_TA],
    'RestingECG_LVH': [RestingECG_LVH],
    'RestingECG_Normal': [RestingECG_Normal],
    'RestingECG_ST': [RestingECG_ST]
})

# Prediction
if st.button('Predict Heart Risk'):

    prediction = model.predict(input_features)

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Heart Attack")
    else:
        st.success("✅ Low Risk of Heart Attack")