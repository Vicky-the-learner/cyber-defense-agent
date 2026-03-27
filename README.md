---

title: AI Cyber Defense Agent
emoji: 🛡️
colorFrom: red
colorTo: purple
sdk: docker
license: mit
short_description: "AI-powered cyber attack detection and response environment using OpenEnv"
# 🛡️ AI Cyber Defense Agent (OpenEnv)

## 🚀 Overview

This project simulates a **real-world cyber defense system** that detects and responds to cyber attacks such as:

* SQL Injection
* Cross-Site Scripting (XSS)

It is built as an **OpenEnv-compatible reinforcement learning environment**.

---

## 🧠 Key Features

### 🔍 Hybrid Detection Engine

* AI-based detection (LLM reasoning)
* Rule-based fallback system
* Conflict resolution (AI vs rules)

### ⚡ Response System

* BLOCK_IP for SQL Injection
* SANITIZE_INPUT for XSS
* ALLOW for normal traffic

### 🎯 Reward System (Advanced)

* +0.5 → correct detection
* +0.3 → correct response
* +confidence-based scoring
* penalties for wrong actions

## 🧪 Tasks

| Level  | Description        |
| ------ | ------------------ |
| Easy   | Basic attacks      |
| Medium | Obfuscated attacks |
| Hard   | Advanced payloads  |

## 📊 Performance (Baseline)


easy:   0.98
medium: 0.98
hard:   0.98

## 🔌 API Endpoints

* `/reset` → reset environment
* `/step` → take action
* `/state` → get current state
* `/tasks` → list tasks
* `/grader/{level}` → evaluate level
* `/baseline` → run full evaluation

## ⚙️ Setup

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 🌍 Real-World Use Case

* Web Application Firewall (WAF)
* SOC automation systems
* AI-based intrusion detection
* Bug bounty automation

---

## 🏁 Why This Project Stands Out

* Real-world cyber defense simulation
* Hybrid AI + deterministic logic
* Proper RL reward shaping
* Fully OpenEnv compliant
* Deployable & scalable

---

## 🔥 Future Improvements

* Add more attack types (RCE, SSRF)
* Integrate real traffic logs
* Train RL agents on environment
* Add dashboard UI

---

## 🧑‍💻 Author

Built for OpenEnv Hackathon 🚀
