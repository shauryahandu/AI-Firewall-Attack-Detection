import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Batch Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Batch CSV Analysis")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df.replace(
        [float("inf"), float("-inf")],
        0,
        inplace=True
    )

    df.fillna(
        0,
        inplace=True
    )

    st.write(f"Loaded {len(df)} flows")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    if st.button("🚀 Analyze"):

        payload = {
            "flows": [
                {
                    "features": row.to_dict()
                }
                for _, row in df.iterrows()
            ]
        }

        try:

            response = requests.post(
                f"{API_URL}/batch-predict",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:

                results = response.json()

                df["Prediction"] = [
                    r["prediction"]
                    for r in results
                ]

                st.success("Analysis complete")

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Total Flows",
                    len(df)
                )

                c2.metric(
                    "Attacks Detected",
                    (df["Prediction"] != "BENIGN").sum()
                )

                c3.metric(
                    "Unique Classes",
                    df["Prediction"].nunique()
                )

                st.subheader("Prediction Summary")

                summary = (
                    df["Prediction"]
                    .value_counts()
                    .reset_index()
                )

                summary.columns = [
                    "Attack Type",
                    "Count"
                ]

                st.dataframe(
                    summary,
                    use_container_width=True
                )

                st.subheader("Detailed Results")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                attack_colors = {
                    "BENIGN": "#60A5FA",
                    "DDoS": "#2563EB",
                    "DoS": "#F59E0B",
                    "PortScan": "#EAB308",
                    "Bot": "#EF4444",
                    "BruteForce": "#FB923C",
                    "Heartbleed": "#DC2626",
                    "WebAttack": "#F9A8D4",
                    "Infiltration": "#A855F7"
                }

                counts = df["Prediction"].value_counts()

                fig = px.pie(
                    values=counts.values,
                    names=counts.index,
                    title="Attack Distribution",
                    color=counts.index,
                    color_discrete_map=attack_colors
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=600
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                csv = df.to_csv(index=False)

                st.download_button(
                    "⬇ Download Results",
                    csv,
                    "predictions.csv",
                    "text/csv"
                )

            else:

                st.error(response.text)

        except Exception as e:

            st.error(
                f"Connection failed: {e}"
            )