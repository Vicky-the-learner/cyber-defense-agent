---
sdk: docker
app_file: app.py
---

# 🛡️ AI Cyber Defense Agent (OpenEnv)

## 🚀 Overview

AI Cyber Defense Agent is an OpenEnv-based environment that simulates real-world cyber attacks and allows an AI agent to detect and respond to them.

This project demonstrates how an AI system can:
- Detect malicious inputs (SQL Injection, etc.)
- Classify attack types
- Take automated defensive actions (block, allow, alert)

---

## 🎯 Objective

To build a realistic environment where an AI agent can:
- Observe incoming requests/logs
- Identify potential cyber threats
- Take appropriate defensive actions
- Be evaluated using a scoring system

---

## 🧠 How It Works

1. User provides an input (simulated request/log)
2. Environment processes the input
3. AI agent detects whether it's an attack
4. Agent decides an action
5. System returns structured output + score

---

## 🏗️ OpenEnv Architecture

### Core Endpoints

- `/reset` → Reset environment state  
- `/step` → Process input and return AI decision  
- `/tasks` → List available tasks (easy, medium, hard)  
- `/grader/{level}` → Evaluate performance  
- `/baseline` → Run baseline agent and return scores  

---

## 📊 Tasks

| Level   | Description |
|--------|------------|
| Easy   | Simple attack detection (e.g., SQL Injection) |
| Medium | Multi-pattern detection |
| Hard   | More realistic and complex inputs |

---

## 🧪 Example

### Input: