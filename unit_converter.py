import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Function to load Lottie animation from URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animation
lottie_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ysbzrgxe.json")

# Streamlit Page Config
st.set_page_config(page_title="Unit Converter", page_icon="🔄")

# Add CSS for animations
st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    .title {
        animation: fadeIn 2s ease-in-out;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #ad8707;
        font-family: 'sans-serif';
    }
    .heading {
    animation: fadeIn 2s ease-in-out;
    text-align: center;
    font-weight: 900;
    font-size: 1.5em;
    font-family: 'sans-serif';
}

    
    .stNumberInput input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        color: #333;
        background-color: #f9f9f9;
    }

    .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #ff9800;
        border-radius: 10px;
        font-size: 16px;
        padding: 5px;
        color: #333;
    }

    .stSelectbox:hover div[data-baseweb="select"] {
        border-color: #e65100;
    }
    .button {
        animation: fadeIn 2s ease-in-out;
        background-color: #ff9800;
        border-radius: 10px;
        padding: 10px;
        font-size: 1.2em;
        color: white;
        text-align: center;
        display: inline-block;
        width: 100%;
        transition: 0.3s;
    }

    .button:hover {
        background-color: #e65100;
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Title & Animation
st.markdown('<div class="title">🌟 Ultimate Pro Unit Converter</div>', unsafe_allow_html=True)
st.write('<div class="heading">Convert various units instantly 🚀</div>', unsafe_allow_html=True)


# Conversion categories
conversion_types = [
    "Length", "Weight and Mass", "Volume", "Temperature", "Area", "Pressure",
    "Energy", "Power", "Force", "Time", "Speed", "Angle",
    "Fuel Consumption", "Data Storage", "Frequency", "Electricity"
]

conversion_choice = st.sidebar.radio("Select Conversion Type", conversion_types)

# Conversion units dictionary
conversion_units = {
    "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
    "Weight and Mass": ["Kilogram", "Gram", "Pound", "Ounce", "Ton"],
    "Volume": ["Liter", "Milliliter", "Gallon", "Pint", "Cubic Meter"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Area": ["Square Meter", "Square Kilometer", "Square Foot", "Acre", "Hectare"],
    "Pressure": ["Pascal", "Bar", "PSI", "Atmosphere"],
    "Energy": ["Joule", "Calorie", "Kilowatt-hour", "BTU"],
    "Power": ["Watt", "Kilowatt", "Horsepower"],
    "Force": ["Newton", "Kilonewton", "Pound-force"],
    "Time": ["Second", "Minute", "Hour", "Day"],
    "Speed": ["Meter per second", "Kilometer per hour", "Mile per hour", "Knot"],
    "Angle": ["Degree", "Radian"],
    "Fuel Consumption": ["Kilometers per liter", "Miles per gallon"],
    "Data Storage": ["Bit", "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte"],
    "Frequency": ["Hertz", "Kilohertz", "Megahertz", "Gigahertz"],
    "Electricity": ["Ampere", "Volt", "Ohm", "Watt"]
}

# Input fields
value = st.number_input("Enter Value", min_value=0.0, value=1.0, step=0.1)
from_unit = st.selectbox("From", conversion_units[conversion_choice])
to_unit = st.selectbox("To", conversion_units[conversion_choice])

# Conversion logic
def convert(value, from_unit, to_unit, category):
    conversion_factors = {
        "Length": {"Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000, "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084, "Inch": 39.3701},
        "Weight and Mass": {"Kilogram": 1, "Gram": 1000, "Pound": 2.20462, "Ounce": 35.274, "Ton": 0.001},
        "Volume": {"Liter": 1, "Milliliter": 1000, "Gallon": 0.264172, "Pint": 2.11338, "Cubic Meter": 0.001},
        "Temperature": {"Celsius": (lambda x: x, lambda x: x), "Fahrenheit": (lambda x: (x * 9/5) + 32, lambda x: (x - 32) * 5/9), "Kelvin": (lambda x: x + 273.15, lambda x: x - 273.15)},
        "Area": {"Square Meter": 1, "Square Kilometer": 1e-6, "Square Foot": 10.7639, "Acre": 0.000247105, "Hectare": 0.0001},
        "Pressure": {"Pascal": 1, "Bar": 1e-5, "PSI": 0.000145038, "Atmosphere": 9.8692e-6},
        "Energy": {"Joule": 1, "Calorie": 0.239006, "Kilowatt-hour": 2.7778e-7, "BTU": 0.000947817},
        "Power": {"Watt": 1, "Kilowatt": 0.001, "Horsepower": 0.00134102},
        "Force": {"Newton": 1, "Kilonewton": 0.001, "Pound-force": 0.224809},
        "Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400},
        "Speed": {"Meter per second": 1, "Kilometer per hour": 3.6, "Mile per hour": 2.23694, "Knot": 1.94384},
        "Angle": {"Degree": 1, "Radian": 0.0174533},
        "Fuel Consumption": {"Kilometers per liter": 1, "Miles per gallon": 2.35215},
        "Data Storage": {"Bit": 1, "Byte": 8, "Kilobyte": 8000, "Megabyte": 8e6, "Gigabyte": 8e9, "Terabyte": 8e12},
        "Frequency": {"Hertz": 1, "Kilohertz": 0.001, "Megahertz": 1e-6, "Gigahertz": 1e-9},
        "Electricity": {"Ampere": 1, "Volt": 1, "Ohm": 1, "Watt": 1}
    }
    
    if category == "Temperature":
        return conversion_factors[category][to_unit][1](conversion_factors[category][from_unit][0](value))
    else:
        return value * conversion_factors[category][to_unit] / conversion_factors[category][from_unit]

# Perform conversion
if st.button("Convert Now 🚀", key="convert_button"):
    result = convert(value, from_unit, to_unit, conversion_choice)
    st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")



 
