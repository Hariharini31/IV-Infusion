import streamlit as st
import pandas as pd
import numpy as np
from model import predict_infusion_time, classify_flow_rate
from utils import simulate_fluid_level  # Optional if you need custom logic

# Page configuration
st.set_page_config(page_title="IVSimAI", layout="centered")
st.title("💉 IVSimAI: Smart IV Infusion Simulation System")

# Sidebar inputs
st.sidebar.header("🧾 Patient & IV Input")
age = st.sidebar.number_input("Age", 0, 120, 65)
weight = st.sidebar.number_input("Weight (kg)", 1, 200, 70)
condition = st.sidebar.selectbox("Medical Condition", ["General", "Surgery", "Dehydration", "ICU"])
volume = st.sidebar.number_input("IV Volume (ml)", 100, 1000, 500, step=50)
drip_rate = st.sidebar.slider("Drip Rate (ml/hr)", 10, 100, 25)

# ML Predictions
time_left = predict_infusion_time(volume, drip_rate)
risk = classify_flow_rate(age, weight, drip_rate)

st.markdown(f"🧠 **Predicted Infusion Time:** :blue[{time_left:.1f} hours]")
st.markdown(f"⚠️ **Risk Assessment:** :red[{risk}]")

# Simulation section
st.subheader("📉 IV Fluid Level Simulation")
chart_placeholder = st.empty()
alert_placeholder = st.empty()

# Generate fluid level data over time
time_points = np.linspace(0, time_left, num=100)
fluid_levels = volume - drip_rate * time_points
fluid_levels = np.clip(fluid_levels, 0, volume)

# Create DataFrame
df = pd.DataFrame({
    "Time (hr)": time_points,
    "IV Fluid Level (ml)": fluid_levels
}).set_index("Time (hr)")

# Plot the chart
chart_placeholder.line_chart(df)

# Alert if final fluid level is critically low
if fluid_levels[-1] < 50:
    alert_placeholder.warning("⚠️ IV Fluid critically low!")
else:
    alert_placeholder.empty()
