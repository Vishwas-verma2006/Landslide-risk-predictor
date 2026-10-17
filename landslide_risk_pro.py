import joblib 
import pandas as pd 
import streamlit as st 

st.header("Landslide Risk Prediction")
st.write('''_This is ML based model that predicts the risk of landslides based on varouis enviromental factors. 
        This project is basically dataset of north eastern states of India._''')

with st.container(border=True):
    st.write('''_**This project is only for educational purpose.  
    The model should not be used for any real world application.**_''')

# load the trained model 
with open('D:/CODING/ML using Python/Venv/Code/projects/landslide_risk_model.joblib', 'rb') as f:
    model = joblib.load(f)

# taking user input for prediction 
def user_input():
    st.write("**Please enter the following parameters:-**")
    rainfall = st.number_input("Rainfall (in mm)", min_value=0.0, max_value=1000.0, value=5.0, step=1.0, key='rainfall')
    slope = st.number_input("Slope (in degrees)", min_value=0.0, value=15.0, step=1.0, key='slope')
    soil = st.slider('Soil Saturation (in %)', min_value=0.0, max_value=1.0, value=0.40, step=0.01, key='soil_saturation', help='Values between 0 and 1')
    vegetation = st.slider('Vegetation Curve (in %)', min_value=0.0, max_value=1.0, value=0.50, step=0.01, key='vegetation_curve', help='Values between 0 and 1')
    earthquake = st.number_input("Earthquake Activity (in Richter scale)", min_value=0.000000, max_value=10.0, step=0.001, key='earthquake_activity', help='Values between 0 and 10')
    water = st.number_input("Proximity to water", min_value=0.00000, max_value=2.0, value=0.80, step=0.001, key='proximity_to_water', help='Values between 0 and 2')
    st.session_state.soil_type = st.selectbox("Soild Type", options=['Gravel', 'Sand', 'Slit', 'None'])

    dic = {'Gravel':0, 'Sand':0, 'Slit':0}
    if st.session_state.soil_type is not None:
        if st.session_state.soil_type == 'Gravel':
            dic['Gravel'] = 1
        elif st.session_state.soil_type == 'Sand':
            dic['Sand'] = 1
        elif st.session_state.soil_type == 'Slit':
            dic['Slit'] = 1
        else:
            dic['Gravel'] = 0
            dic['Sand'] = 0
            dic['Slit'] = 0
        st.session_state.soil_type = dic

    features = {
        'Rainfall_mm': [rainfall],
        'Slope_Angle': [slope],
        'Soil_Saturation': [soil],
        'Vegetation_Cover': [vegetation],
        'Earthquake_Activity': [earthquake],
        'Proximity_to_Water': [water],
        'Soil_Type_Gravel': [st.session_state.soil_type['Gravel']],
        'Soil_Type_Sand': [st.session_state.soil_type['Sand']],
        'Soil_Type_Silt': [st.session_state.soil_type['Slit']]
    }

    return pd.DataFrame(features, index=[0])

input_df = user_input()

# show information about the parameters
with st.expander("**Parameters inforation:-**"):
        st.write("*Raninfall_mm: Rainfall in millimeters*")
        st.write("*Slope_Angle: slope angle of the land in degrees*")
        st.write("*Soil_Saturation: Measures how much water is trapped in the soil.*")
        st.write("*Vegetation_Cover: Measures the density of vegetation in the area.*")
        st.write("*Earthquake_Activity: Measures the earhthquake activity in the area on the Richter scale.*")
        st.write("*Proximity_to_Water: Measures the distance to the nearest water body like lake or river.*")
        st.write("*Soil_Type: the type of soil in the area, which can affect the stability of the land.*")


if 'prediction' not in st.session_state:
    st.session_state.prediction = None

if 'probablity' not in st.session_state:
    st.session_state.probablity = None

# button to predict the landslide risk
if st.button("**Predict**", help="Click to predict the landslide risk"):
    st.session_state.prediction = model.predict(input_df)

if st.session_state.prediction is not None:
    st.write("**Prediction:-**")
    if st.session_state.prediction[0] == 1:
        st.write("**🔴 High risk of landslide**")
    else:
        st.write("**🟢 Low risk of landslide**")

# button to show the probablity of landslide risk
if st.button("**Probablity**", help='Click to see the probablity of landslide risk'):
    st.session_state.probablity = model.predict_proba(input_df)

if st.session_state.probablity is not None:
    # how can i get the emoji in vs code 
    st.write("**Probablity of landslide risk:-**")
    st.write(f"**🔴 High risk of landslide:- {st.session_state.probablity[0][1]*100:.2f}%**")
    st.write(f"**🟢 Low risk of landslide:- {st.session_state.probablity[0][0]*100:.2f}%**")

# button to clear the prediction and probablity
if st.button("**Clear**", help='Click to clear the prediction and probablity'):
    st.session_state.prediction = None
    st.session_state.probablity = None
    st.rerun()