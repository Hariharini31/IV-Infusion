import streamlit as st
import time
import numpy as np
import pandas as pd

# Dummy replacements for predict_infusion_time, classify_flow_rate, and simulate_fluid_level

def predict_infusion_time(volume, drip_rate):
    return volume / drip_rate  # Simple time = volume / rate

def classify_flow_rate(age, weight, drip_rate):
    if drip_rate > 80:
        return "High Risk"
    elif drip_rate > 50:
        return "Moderate Risk"
    else:
        return "Low Risk"

def simulate_fluid_level(volume, drip_rate, time_left):
    steps = int(time_left * 10)
    return np.linspace(volume, 0, steps)

# Streamlit App
st.set_page_config(page_title="IVSimAI", layout="centered")
st.title("💉 IVSimAI: Smart IV Infusion Simulation System")

# Sidebar input
st.sidebar.header("🧾 Patient & IV Input")
age = st.sidebar.number_input("Age", 0, 120, 65)
weight = st.sidebar.number_input("Weight (kg)", 1, 200, 70)
condition = st.sidebar.selectbox("Medical Condition", ["General", "Surgery", "Dehydration", "ICU"])
volume = st.sidebar.number_input("IV Volume (ml)", 100, 1000, 500, step=50)
drip_rate = st.sidebar.slider("Drip Rate (ml/hr)", 10, 100, 25)

# Predictions
time_left = predict_infusion_time(volume, drip_rate)
risk = classify_flow_rate(age, weight, drip_rate)

st.markdown(f"**Predicted Infusion Time:** {time_left:.1f} hours")
st.markdown(f"**Risk Assessment:** :red[{risk}]")

# Simulation section
st.subheader("📉 IV Fluid Level Simulation")
chart_placeholder = st.empty()
alert_placeholder = st.empty()

fluid_levels = simulate_fluid_level(volume, drip_rate, time_left)

# Create DataFrame with time axis
time_series = [round(i * 0.1, 2) for i in range(len(fluid_levels))]
df = pd.DataFrame({
    "Time (hr)": time_series,
    "IV Fluid Level (ml)": fluid_levels
})
df.set_index("Time (hr)", inplace=True)

# Animate the line chart frame-by-frame
for i in range(2, len(df)+1):
    chart_placeholder.line_chart(df.iloc[:i])

    current_level = df.iloc[i - 1]["IV Fluid Level (ml)"]
    if current_level < 50:
        alert_placeholder.warning("⚠️ IV Fluid critically low!")
    else:
        alert_placeholder.empty()

    time.sleep(0.2)
