import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Single Prediction",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Single Flow Prediction")

st.write(
    "Upload a CSV containing exactly one network flow."
)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Input Features")

    st.dataframe(df)

    if len(df) != 1:

        st.error(
            "CSV must contain exactly one row."
        )

    elif st.button("🚀 Predict"):

        payload = {
            "features": df.iloc[0].to_dict()
        }

        try:

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:

                result = response.json()

                prediction = result["prediction"]
                confidence = result["binary_confidence"]

                if prediction == "BENIGN":
                    st.success(
                        f"🛡️ Prediction: {prediction}"
                    )

                elif prediction in ["DDoS", "Heartbleed"]:
                    st.error(
                        f"🚨 Prediction: {prediction}"
                    )

                elif prediction in ["DoS", "BruteForce"]:
                    st.warning(
                        f"⚠️ Prediction: {prediction}"
                    )

                else:
                    st.info(
                        f"🔍 Prediction: {prediction}"
                    )

                st.metric(
                    "Confidence",
                    f"{confidence * 100:.2f}%"
                )

                st.progress(confidence)

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.json(
                    response.json()
                )

        except Exception as e:

            st.error(
                f"Connection failed: {e}"
            )