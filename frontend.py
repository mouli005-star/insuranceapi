import streamlit as st
import joblib
import pandas as pd

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job",
    ]
)

# Load model (assumes model.pkl is present in repo root)
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

tier_1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi",
    "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara",
    "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati",
    "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad",
    "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem",
    "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior",
    "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode",
    "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida",
    "Guntur", "Asansol", "Siliguri"
]

def compute_features(age, weight, height, income_lpa, smoker, city, occupation):
    bmi = weight / (height ** 2)
    if smoker and bmi > 30:
        lifestyle_risk = "high"
    elif smoker or bmi > 27:
        lifestyle_risk = "medium"
    else:
        lifestyle_risk = "low"

    if age < 25:
        age_group = "young"
    elif 25 <= age < 45:
        age_group = "adult"
    elif 45 <= age < 65:
        age_group = "middle_aged"
    else:
        age_group = "senior"

    if city in tier_1_cities:
        city_tier = 1
    elif city in tier_2_cities:
        city_tier = 2
    else:
        city_tier = 3

    return {
        "bmi": bmi,
        "age_group": age_group,
        "lifestyle_risk": lifestyle_risk,
        "city_tier": city_tier,
        "income_lpa": income_lpa,
        "occupation": occupation,
    }

if st.button("Predict Premium Category"):
    features = compute_features(age, weight, height, income_lpa, smoker, city, occupation)
    input_df = pd.DataFrame([features])
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted Premium Category: {prediction}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
