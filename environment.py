from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward


class CyberDefenseEnv:
    def __init__(self):
        self.current_input = None
        self.last_analysis = None
        self.done = False
        self.history = []

    def reset(self):
        self.current_input = None
        self.last_analysis = None
        self.done = False
        self.history = []

        return {
            "state": "Environment reset"
        }

    def step(self, input_data):
        self.current_input = input_data

        # Detection
        analysis = detect_attack(input_data)

        # Ensure AI-like fields exist
        attack = analysis.get("attack", "none")
        confidence = analysis.get("confidence", 0.5)
        reason = analysis.get("reason", "No clear pattern")

        # Response
        response = respond_to_attack(analysis)
        action = response.get("action", "allow")

        # Reward (fixed)
        reward = calculate_reward(
            attack=attack,
            action=action,
            confidence=confidence
        )

        # Save state
        self.last_analysis = analysis
        self.done = True

        # 🔥 NEW: Store history (Day 2 upgrade)
        self.history.append({
            "input": input_data,
            "attack": attack,
            "action": action,
            "confidence": confidence
        })

        return {
            "state": {
                "input": input_data,
                "analysis": analysis,
                "history": self.history[-5:]  # last 5 actions
            },
            "response": response,
            "reward": reward,
            "done": self.done
        }

    def state(self):
        return {
            "current_input": self.current_input,
            "last_analysis": self.last_analysis,
            "history": self.history,
            "done": self.done
        }