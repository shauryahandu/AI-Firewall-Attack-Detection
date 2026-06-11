import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from autogluon.tabular import TabularPredictor

# =========================
# Load Dataset
# =========================

df = pd.read_csv(
    r"processed/master_web_attacks_v1.csv"
)

print("Dataset Shape:", df.shape)

# =========================
# Create Test Set
# =========================

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["attack_type"],
    random_state=42
)

print("Test Shape:", test_df.shape)

# =========================
# Load Trained AutoGluon Model
# =========================

predictor = TabularPredictor.load(
    r".\AutogluonModels\ag-20260609_072244"
)

# =========================
# Predict
# =========================

preds = predictor.predict(test_df)

# =========================
# Classification Report
# =========================

print("\nCLASSIFICATION REPORT\n")

print(
    classification_report(
        test_df["attack_type"],
        preds,
        digits=4
    )
)

# =========================
# Confusion Matrix
# =========================

print("\nCONFUSION MATRIX\n")

print(
    confusion_matrix(
        test_df["attack_type"],
        preds
    )
)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from autogluon.tabular import TabularPredictor

# =========================
# Load Dataset
# =========================

df = pd.read_csv(
    r"processed/master_web_attacks_v1.csv"
)

print("Dataset Shape:", df.shape)

# =========================
# Create Test Set
# =========================

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["attack_type"],
    random_state=42
)

print("Test Shape:", test_df.shape)

# =========================
# Load Trained AutoGluon Model
# =========================

predictor = TabularPredictor.load(
    r".\AutogluonModels\ag-20260609_072244"
)

# =========================
# Predict
# =========================

preds = predictor.predict(test_df)

# =========================
# Classification Report
# =========================

print("\nCLASSIFICATION REPORT\n")

print(
    classification_report(
        test_df["attack_type"],
        preds,
        digits=4
    )
)

# =========================
# Confusion Matrix
# =========================

print("\nCONFUSION MATRIX\n")

print(
    confusion_matrix(
        test_df["attack_type"],
        preds
    )
)