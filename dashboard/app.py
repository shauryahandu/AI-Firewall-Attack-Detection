import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Firewall IDS",
    page_icon="",
    layout="wide"
)
with st.sidebar:

    st.title("🛡️ AI Firewall IDS")

    st.success("System Operational")

    st.divider()

    st.markdown("""
    ### Current Modules

    ✅ Binary Detection

    ✅ Multiclass Classification

    (done) SHAP Explainability

    🔜 Live Monitoring

    🔜 Docker Deployment
    """)

    st.divider()

    st.caption("Version 1.0")

st.title("AI Firewall IDS v1.0")
st.caption("Machine Learning Powered Intrusion Detection System")

try:
    r = requests.get(f"{API_URL}/health", timeout=3)
    api_status = "🟢 Online" if r.status_code == 200 else "🔴 Offline"
except:
    api_status = "🔴 Offline"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("API Status", api_status)

with col2:
    st.metric("Models Loaded", "2/2")

with col3:
    st.metric("Attack Classes", "8")

st.divider()

st.subheader("Detection Pipeline")

st.markdown("""
<div style='
    background:#0F172A;
    padding:30px;
    border-radius:20px;
    width:700px;
    margin:auto;
    text-align:center;
    font-size:26px;
    line-height:1.8;
    box-shadow:0px 8px 20px rgba(0,0,0,0.3);
'>

🖧 <b>Network Flow</b><br>

⬇️<br>

🤖 <b>Binary CatBoost</b><br>

⬇️<br>

⚠️ <b>Intrusion Decision</b><br>

⬇️<br>

🧠 <b>Multiclass CatBoost</b><br>

⬇️<br>

🛡️ <b>Attack Classification</b>

</div>
""", unsafe_allow_html=True)
st.subheader("Supported Attacks")

attacks = [
    "DoS",
    "DDoS",
    "PortScan",
    "Bot",
    "BruteForce",
    "Heartbleed",
    "WebAttack",
    "Infiltration"
]

attack_colors = {
    "DoS": "#F59E0B",
    "DDoS": "#EF4444",
    "PortScan": "#EAB308",
    "Bot": "#8B5CF6",
    "BruteForce": "#FB923C",
    "Heartbleed": "#DC2626",
    "WebAttack": "#FACC15",
    "Infiltration": "#A855F7"
}

cols = st.columns(4)

for i, attack in enumerate(attacks):

    cols[i % 4].markdown(
        f"""
        <div style="
            background:{attack_colors[attack]};
            padding:18px;
            border-radius:12px;
            text-align:center;
            color:white;
            font-weight:bold;
            margin-bottom:12px;
            box-shadow:0px 4px 12px rgba(0,0,0,0.3);
        ">
        {attack}
        </div>
        """,
        unsafe_allow_html=True
    )

st.info("SHAP explainability and real time monitoring will be added in future phases.")
st.divider()

st.caption(
    "🛡️ Firewall IDS v1.0 | FastAPI • CatBoost • Streamlit"
)

st.caption(
    "Built using CIC IDS 2017 network traffic datasets."
)

