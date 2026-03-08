"""Model training and evaluation module."""

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def train_model(X_train, y_train, model_type="xgboost"):
    """Train selected model."""

    if model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)

    elif model_type == "xgboost":
        model = XGBClassifier(n_estimators=100, random_state=42)

    else:
        raise ValueError("Unsupported model type")

    model.fit(X_train, y_train)

    return model