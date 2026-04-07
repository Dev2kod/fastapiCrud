# app/data/data.py
from app.data.data import violation_data

def get_data():
    """Return full violation_data dict."""
    return violation_data

def get_violations():
    """Return only violations list."""
    return violation_data.get("violations", [])

def get_sites():
    """Return sites list."""
    return violation_data.get("sites", [])
