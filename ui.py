import streamlit as st
import requests

API_URL = "http://localhost:8080"

st.set_page_config(page_title="AI Cyber Defense Agent", layout="wide")

st.title("🛡️ AI Cyber Defense Agent")

task = st.selectbox("Select Task Level", ["easy", "medium", "hard"])

user_input = st.text_area("Enter request / log", height=150)

if st.button("Run Simulation"):
    try:
        requests.post(f"{API_URL}/reset")

        response = requests.post(
            f"{API_URL}/step",
            json={"task": task, "input": user_input}
        )

        result = response.json()

        st.subheader("🧠 AI Decision")

        attack = result.get("attack", "none")
        action = result.get("action", "none")

        if attack != "none":
            st.error(f"🚨 Attack Detected: {attack.upper()}")
        else:
            st.success("✅ No Attack Detected")

        st.info(f"Action Taken: {action}")

    except Exception as e:
        st.error(str(e))
        
if st.button("Run Baseline"):
    try:
        baseline = requests.get(f"{API_URL}/baseline").json()
        st.subheader("📊 Scores")
        st.write(baseline)
    except Exception as e:
        st.error(str(e))
        