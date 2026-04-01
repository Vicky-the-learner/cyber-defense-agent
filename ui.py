import streamlit as st
import requests

API_URL = "http://localhost:8080"

st.set_page_config(page_title="AI Cyber Defense Agent", layout="wide")

st.title("🛡️ AI Cyber Defense Agent")

# -------------------- TASK SELECT --------------------

task = st.selectbox("Select Task Level", ["easy", "medium", "hard"])

st.markdown("### 🔍 Simulation")

if st.button("Run Simulation"):
    try:
        # Reset environment
        requests.post(f"{API_URL}/reset")

        st.write("🚀 Starting simulation...\n")

        for step in range(5):
            response = requests.post(f"{API_URL}/step", json={})
            result = response.json()

            analysis = result["info"]["analysis"]
            response_data = result["info"]["response"]
            reward = result.get("reward", 0.0)

            attack = analysis.get("attack", "Normal")
            confidence = analysis.get("confidence", 0.0)
            action = response_data.get("action", "ALLOW")

            st.markdown(f"### Step {step + 1}")

            # Attack status
            if attack.lower() != "normal":
                st.error(f"🚨 Attack Detected: {attack}")
            else:
                st.success("✅ No Attack Detected")

            # Details
            st.write(f"🛡️ Action: {action}")
            st.write(f"🎯 Confidence: {confidence}")
            st.write(f"🏆 Reward: {reward}")

            st.divider()

            if result.get("done"):
                break

        st.success("✅ Simulation Complete")

    except Exception as e:
        st.error(f"Error: {str(e)}")


# -------------------- BASELINE --------------------

st.markdown("### 📊 Baseline Evaluation")

if st.button("Run Baseline"):
    try:
        baseline = requests.get(f"{API_URL}/baseline").json()
        st.subheader("📊 Scores")
        st.json(baseline)
    except Exception as e:
        st.error(str(e))