import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

import joblib
import numpy as np
import pandas as pd   # added to wrap features with names
import re

# Regex for numeric prefixes like '1.' or '2.1.'
NUM_PREFIX_RE = re.compile(r"^(\d+\.)+\s*")

def load_heading_model(model_dir):
    """Load trained heading classification model."""
    return joblib.load(f"{model_dir}/heading_model.pkl")

def compute_features(line):
    """
    Compute the exact 7 features used during training:
      avg_size, text_length, num_prefix, is_bold, is_upper, above_body, darkness
    """
    text = line.get("text", "")
    avg_size    = line.get("avg_size", 12.0)
    text_length = len(text)
    num_prefix  = int(bool(NUM_PREFIX_RE.match(text)))
    is_bold     = int(line.get("is_bold", 0))
    is_upper    = int(text.isupper())
    above_body  = int(avg_size > 12.0)
    darkness    = float(line.get("darkness", 0.5))

    return [avg_size, text_length, num_prefix, is_bold, is_upper, above_body, darkness]

def predict_heading(line, model):
    """Return True if this line is classified as a heading."""
    feats = compute_features(line)

    # Wrap features into DataFrame with correct column names to silence warnings
    feature_names = [
        "avg_size",
        "text_length",
        "num_prefix",
        "is_bold",
        "is_upper",
        "above_body",
        "darkness"
    ]
    X = pd.DataFrame([feats], columns=feature_names)

    return bool(model.predict(X)[0])
