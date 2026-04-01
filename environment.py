from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward
from models import CyberObservation   # ✅ FIXED IMPORT
import uuid

class CyberDefenseEnv:
    def __init__(self):
        self.current_input = None
        self.last_analysis = None
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.done = False
        self.history = []

    def reset(self):
        self.current_input = None
        self.last_analysis = None
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.done = False
        self.history = []

        return {
            "state": "Environment reset"
        }

    def step(self, input_data):
        self.current_input = input_data

        # Detection
        analysis = detect_attack(input_data)
        self.step_count += 1

        # ✅ DEFINE VARIABLES FIRST
        attack = analysis.get("attack", "none")
        confidence = analysis.get("confidence", 0.5)
        reason = analysis.get("reason", "No clear pattern")

        # ✅ NOW CREATE OBSERVATION
        observation = CyberObservation(
            input=input_data,
            attack=attack,
            confidence=confidence,
            message=reason
        )

        # Response
        response = respond_to_attack(analysis)
        action = response.get("action", "allow")

        # Reward
        expected_attack = analysis.get("expected_attack", attack)

        reward = calculate_reward(
            detected_attack=attack,
            expected_attack=expected_attack,
            action=action,
            confidence=confidence
        )

        # Save state
        self.last_analysis = analysis
        self.done = True

        # History
        self.history.append({
            "input": input_data,
            "attack": attack,
            "action": action,
            "confidence": confidence
        })

        return {
            "state": {
                "episode_id": self.episode_id,
                "input": input_data,
                "analysis": observation.dict(),  # ✅ FIXED
                "history": self.history[-5:]
            },
            "response": response,
            "reward": reward,
            "done": self.done
        }

    def state(self):
        return {
            "episode_id": self.episode_id,
            "current_input": self.current_input,
            "last_analysis": self.last_analysis,
            "history": self.history,
            "step_count": self.step_count,
            "done": self.done
        }