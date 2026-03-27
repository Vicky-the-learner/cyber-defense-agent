---
title: Cyber Defense Agent
emoji: 🌍
colorFrom: purple
colorTo: indigo
sdk: docker
pinned: false
license: mit
short_description: AI-powered cyber defense environment using OpenEnv
---

# AI Cyber Defense Agent (OpenEnv)

## Overview
This environment simulates a real-world cyber defense system that detects and responds to attacks such as SQL Injection and XSS.

## Features
- AI + rule-based hybrid detection
- Response engine (block, sanitize, allow)
- Reward system (0.0–1.0)
- Tasks: easy, medium, hard
- Grader + baseline evaluation

## Endpoints
- /reset
- /step
- /state
- /tasks
- /grader
- /baseline

## Setup
```bash
pip install -r requirements.txt
python -m uvicorn app:app --reload