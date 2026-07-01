# ============================================================
# Firewall IDS V1.0 API
# ============================================================

from fastapi import FastAPI
import pandas as pd
import numpy as np

from api.inference import (
    predict_single,
    predict_batch,
    FEATURE_NAMES
)

from api.schemas import (
    FlowRequest,
    BatchRequest
)


app = FastAPI(

    title="Firewall IDS API",

    description="""
    Intrusion Detection System using:

    - Binary CatBoost
    - Multiclass CatBoost

    Supported attacks:

    - DoS
    - DDoS
    - PortScan
    - Bot
    - BruteForce
    - WebAttack
    - Heartbleed
    - Infiltration
    """,

    version="1.0.0"
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# MODEL INFO
# ============================================================

@app.get("/model-info")
def model_info():

    return {

        "version": "1.0.0",

        "num_features": len(FEATURE_NAMES),

        "supported_attacks": [

            "DoS",
            "DDoS",
            "PortScan",
            "Bot",
            "BruteForce",
            "WebAttack",
            "Heartbleed",
            "Infiltration"
        ]
    }


# ============================================================
# SINGLE FLOW PREDICTION
# ============================================================

@app.post("/predict")
def predict(payload: FlowRequest):

    return predict_single(
        payload.features
    )


# ============================================================
# BATCH FLOW PREDICTION
# ============================================================

@app.post("/batch-predict")
def batch_predict(payload: BatchRequest):

    df = pd.DataFrame(
        [flow.features for flow in payload.flows]
    )

    df.replace(
        [np.inf, -np.inf],
        0,
        inplace=True
    )

    df.fillna(
        0,
        inplace=True
    )

    predictions = predict_batch(df)

    if isinstance(predictions, pd.DataFrame):

        predictions.replace(
            [np.inf, -np.inf],
            0,
            inplace=True
        )

        predictions.fillna(
            0,
            inplace=True
        )

        return predictions.to_dict(
            orient="records"
        )

    return predictions


# ============================================================
# DEMO: DDoS
# ============================================================

@app.get("/demo/ddos")
def demo_ddos():

    sample = {
        feature: 0
        for feature in FEATURE_NAMES
    }

    sample.update({
        "Destination Port": 80,
        "Flow Duration": 2000,
        "Total Fwd Packets": 20000,
        "Flow Packets/s": 1000000,
        "SYN Flag Count": 20000,
        "Packet Length Mean": 60,
        "Fwd Packet Length Mean": 60,
        "Subflow Fwd Packets": 20000,
        "Subflow Fwd Bytes": 1200000,
        "Active Mean": 2000
    })

    return predict_single(sample)


# ============================================================
# DEMO: PORTSCAN
# ============================================================

@app.get("/demo/portscan")
def demo_portscan():

    sample = {
        feature: 0
        for feature in FEATURE_NAMES
    }

    sample.update({
        "Destination Port": 22,
        "Flow Duration": 100,
        "Total Fwd Packets": 2,
        "Flow Packets/s": 20000,
        "SYN Flag Count": 2,
        "Fwd Packet Length Mean": 40,
        "Packet Length Mean": 40
    })

    return predict_single(sample)


# ============================================================
# DEMO: BOT
# ============================================================

@app.get("/demo/bot")
def demo_bot():

    sample = {
        feature: 0
        for feature in FEATURE_NAMES
    }

    sample.update({
        "Destination Port": 8080,
        "Flow Duration": 50000,
        "Total Fwd Packets": 300,
        "Total Backward Packets": 300,
        "Flow Packets/s": 6000,
        "Packet Length Mean": 700,
        "Init_Win_bytes_forward": 8192,
        "Init_Win_bytes_backward": 8192
    })

    return predict_single(sample)