import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
import requests

from shap_utils import (
    get_shap_values,
    get_top_features
)


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="SHAP Explainability",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 SHAP Explainability")

st.write(
    "Upload a CSV containing exactly one network flow to understand why the model made its decision."
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

    elif st.button("🔍 Explain Prediction"):

        payload = {
            "features": df.iloc[0].to_dict()
        }

        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=10
        )

        if response.status_code != 200:

            st.error(response.text)

        else:

            result = response.json()

            prediction = result["prediction"]
            confidence = result["binary_confidence"]

            st.subheader("Model Decision")

            if prediction == "BENIGN":

                st.success(
                    f"🛡️ Prediction: {prediction}"
                )

            elif prediction in ["DDoS", "Heartbleed"]:

                st.error(
                    f"🚨 Prediction: {prediction}"
                )

            else:

                st.warning(
                    f"⚠️ Prediction: {prediction}"
                )

            st.metric(
                "Confidence",
                f"{confidence:.4f}"
            )

            st.progress(confidence)

            st.divider()

            with st.spinner(
                "Computing SHAP values..."
            ):

                shap_values = get_shap_values(df)

                top_features = get_top_features(
                    df,
                    top_k=10
                )

            st.subheader(
                "Top 10 Most Important Features"
            )

            st.dataframe(
                top_features,
                use_container_width=True
            )

            st.subheader(
                "Why did the model predict this?"
            )

            st.info(
                """
                Features with larger SHAP values contributed more strongly
                to the final prediction.

                Positive values push the model toward detecting an attack,
                while negative values push toward benign traffic.
                """
            )

            fig, ax = plt.subplots(
                figsize=(14, 8)
            )

            explanation = shap.Explanation(
                values=shap_values[0],
                base_values=0,
                data=df.iloc[0].values,
                feature_names=df.columns
            )

            shap.plots.bar(
                explanation,
                max_display=10,
                show=False
            )

            st.pyplot(fig)

            plt.close(fig)