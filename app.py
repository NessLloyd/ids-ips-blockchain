import streamlit as st
import pandas as pd
from blockchain import Blockchain, Source
import joblib
import os

st.set_page_config(page_title="AI + Blockchain IDS/IPS", layout="wide")
st.title("🚨 AI Intrusion Detection with Blockchain Logging")

blockchain = Blockchain(difficulty=3)

uploaded_file = st.file_uploader("Upload a single-row network log (CSV)", type=["csv"])

if uploaded_file:
    log_df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:", log_df)

    # Load saved model
    model_data = joblib.load("network_security_model.joblib")
    model = model_data['model']
    scaler = model_data['scaler']
    label_encoders = model_data['label_encoders']

    drop_cols = ['srcip', 'dstip', 'attack_cat', 'label']  # columns not used for prediction
    feature_cols = [col for col in log_df.columns if col not in drop_cols]

    # Encode only necessary columns (exclude dropped columns)
    for col, encoder in label_encoders.items():
        if col in drop_cols:
            continue
        if col in log_df.columns:
            try:
                log_df[col] = encoder.transform(log_df[col].astype(str))
            except ValueError:
                st.error(f"❌ Uploaded file contains unknown value in column: '{col}'")
                st.stop()

    # Only keep numeric columns for scaler
    log_df = log_df.select_dtypes(include=["number"])

    # Scale and predict
    X = scaler.transform(log_df[feature_cols])
    prediction = model.predict(X)[0]

    if prediction == 1:
        st.error("⚠️ Intrusion Detected!")
        source = Source(user_id="uploaded_user", transaction_id="stream_txn_001", cookie="stream_cookie")
        blockchain.add_block(source)
        st.success("🔒 Logged to Blockchain.")
    else:
        st.success("✅ No intrusion detected.")

# Tracing interface
st.subheader("🔍 Trace Incidents")
query = st.text_input("Enter cookie / user_id / transaction_id")
if st.button("Trace"):
    results = blockchain.trace_source(query)
    if results:
        for block in results:
            st.text(str(block))
    else:
        st.warning("No matches found.")
