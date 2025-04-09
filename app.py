import streamlit as st
import pandas as pd
import numpy as np
import pennylane as qml
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(layout="wide")
st.title("🌎 Quantum Glacier Melting Analysis")

# Upload CSV
uploaded_file = st.file_uploader("final_expanded_glacier_dataset.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    expected_columns = ["Location", "Latitude", "Longitude", "Temperature (C)", "Glacier Melt Rate (%)"]
    if not all(col in df.columns for col in expected_columns):
        st.error(f"❌ Required columns not found. Found columns: {df.columns.tolist()}")
        st.stop()

    glacier_names = df["Location"].tolist()
    temperatures = df["Temperature (C)"].tolist()
    melting_rates = df["Glacier Melt Rate (%)"].tolist()
    locations = list(zip(df["Longitude"], df["Latitude"]))

    # Normalize and Quantum Circuit
    def normalize_data(values):
        return np.array(values) / max(values) * np.pi

    data = normalize_data(temperatures[:4])
    weights = np.random.uniform(0, np.pi, (2, 4, 3))
    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def quantum_circuit(data, weights):
        for i in range(len(data)):
            qml.RX(data[i], wires=i)
            qml.RZ(data[i], wires=i)
        qml.templates.StronglyEntanglingLayers(weights, wires=range(4))
        return qml.probs(wires=[0, 1, 2, 3])

    result = quantum_circuit(data, weights)

    # Quantum Output Plot
    st.subheader("Quantum Output Probabilities")
    fig1, ax1 = plt.subplots()
    ax1.bar(range(len(result)), result)
    ax1.set_title("Quantum Analysis of Glacier Melting")
    ax1.set_xlabel("Quantum States")
    ax1.set_ylabel("Probability")
    st.pyplot(fig1)

    # Show Circuit
    st.subheader("Quantum Circuit Structure")
    st.code(qml.draw(quantum_circuit)(data, weights))

    # Risk Classification
    def classify_risk(temp):
        if temp < -5:
            return "Low Risk"
        elif -5 <= temp < 0:
            return "Moderate Risk"
        else:
            return "High Risk"

    # Interactive Map
    st.subheader("Interactive Glacier Map")
    fig2 = go.Figure(data=go.Scattergeo(
        lon=[loc[0] for loc in locations],
        lat=[loc[1] for loc in locations],
        text=[f"{name}<br>Temperature: {temp}°C<br>Melting Rate: {rate}%<br>Risk Level: {classify_risk(temp)}" 
              for name, temp, rate in zip(glacier_names, temperatures, melting_rates)],
        marker=dict(
            size=[rate * 10 for rate in melting_rates],
            color=temperatures,
            colorscale="Viridis",
            colorbar_title="Temperature (°C)",
        )
    ))

    fig2.update_layout(
        title="🌎 Global Glacier Melting Analysis",
        geo=dict(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(217, 217, 217)",
            oceancolor="rgb(200, 225, 255)",
            showocean=True,
            lakecolor="rgb(200, 225, 255)",
            coastlinecolor="black",
            countrycolor="black"
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Gemini-like static recommendation (placeholder)
    st.subheader("Recommendations for Glacier Preservation")
    st.markdown("""
    - *Reduce Greenhouse Emissions*: Transition to renewable energy sources.
    - *Glacier Monitoring*: Invest in remote sensing and quantum climate models.
    - *Raise Awareness*: Educate communities and leaders.
    - *Policy Making*: Enforce glacier protection laws and cut emissions.
    - *Support Green Projects*: Participate in or fund reforestation & clean water campaigns.
    """)

else:
    st.info("final_expanded_glacier_dataset.csv")