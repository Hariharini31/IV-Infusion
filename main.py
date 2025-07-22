import streamlit as st
import time
import pandas as pd
from model import predict_infusion_time, classify_flow_rate
from utils import simulate_fluid_level

# Page configuration
st.set_page_config(page_title="IVSimAI", layout="centered")
st.title("💉 IVSimAI: Smart IV Infusion Simulation System")

# Sidebar inputs
st.sidebar.header("🧾 Patient & IV Input")
age = st.sidebar.number_input("Age", 0, 120, 65)
weight = st.sidebar.number_input("Weight (kg)", 1, 200, 70)
condition = st.sidebar.selectbox("Medical Condition", ["Stable", "Critical", "Recovering"])
volume = st.sidebar.number_input("IV Volume (ml)", 100, 1000, 500, step=50)
drip_rate = st.sidebar.slider("Drip Rate (ml/hr)", 10, 100, 25)

# Predict button

if st.sidebar.button("Run Simulation"):
    # ML Predictions
    time_left = predict_infusion_time(age, weight, condition, volume, drip_rate)
    risk = classify_flow_rate(age, weight, condition, volume, drip_rate)

    st.markdown(f"### 🧠 Predicted Infusion Time: :blue[{time_left:.1f} hours]")
    st.markdown(f"### ⚠️ Risk Assessment: :red[{risk}]")

    # Simulation section
    st.subheader("📉 IV Fluid Level Simulation")
    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    fluid_levels = simulate_fluid_level(volume, drip_rate, time_left)

    chart_data = []

    for i, level in enumerate(fluid_levels):
        chart_data.append({"Time (hr)": i * 0.1, "IV Fluid Level (ml)": level})
        df = pd.DataFrame(chart_data)
        chart_placeholder.line_chart(df.set_index("Time (hr)"))

        if level < 50:
            alert_placeholder.warning("⚠️ IV Fluid critically low!")
        else:
            alert_placeholder.empty()

        time.sleep(0.2)
else:
    st.info("👈 Enter patient details and click 'Run Simulation' to begin.")
