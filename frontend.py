from http.client import responses

import streamlit as st
import requests

st.set_page_config(page_title="FraudSim API",page_icon="🛡️",layout="centered")

st.title("🛡️ FraudGuard AI")
st.markdown("### Realtime Transaction Monitor")
st.info("System Status : **Online** | Model: **Neo4j Graph Engine**")
st.markdown("---")

col1,col2 = st.columns(2)
with col1:
    sender = st.text_input("📤 From Account (Sender)",value="ACC_100")
with col2:
    receiver = st.text_input("📥 To Account (Receiver)",value="ACC_200")

amount = st.number_input("💰 Amount ($)",min_value=1.0,value=500.0,step=100.0)

if st.button("🚀 Process Transaction",type="primary"):
    payload = {
        "from_acc": sender,
        "to_acc": receiver,
        "amount": amount
    }

    try:
        response = requests.post("http://127.0.0.1:8000/check_transaction",json=payload)
        result = response.json()

        if response.status_code == 200:
            status = result.get("status")
            reason = result.get("reason")

            if status == "BLOCKED":
                st.error("🛑 **Transaction Blocked**")
                st.write(f"**Reason:** {reason}")
                st.metric(label="Risk Level",value="CRITICAL",delta="-100")

            elif status == "APPROVED":
                st.success("✅ **Transaction Approved**")
                st.write(f"**Reason:** {reason}")
                st.balloons()

        else:
            st.error(f"⚠️ Server Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ **Connection Failed**")
        st.warning("Did you forget to run `uvicorn main:app --reload`?")

