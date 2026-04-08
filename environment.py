from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward
from models import CyberObservation
from attacker import Attacker
import uuid


class CyberDefenseEnv:
    def __init__(self):
        self.attacker = Attacker()
        self.current_input = None
        self.last_analysis = None
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.max_steps = 5
        self.done = False
        self.history = []

    def reset(self, task="easy"):
        self.step_count = 0
        self.done = False
        self.history = []
        self.episode_id = str(uuid.uuid4())
        self.attacker.set_difficulty(task)
        attack = self.attacker.generate_attack()
        self.current_input = attack
        return {
            "observation": attack,
            "message": "New attack generated",
            "episode_id": self.episode_id
        }

    def step(self, action=None):
    if self.done:
        return {
            "message": "Episode already finished. Call reset().",
            "done": True
        }

    attack = self.current_input
    analysis = detect_attack(attack)
    self.last_analysis = analysis

    # ✅ USE AGENT ACTION (FIXED)
    if action and isinstance(action, dict) and "action" in action:
        act = action["action"]

        if act == "BLOCK_IP":
            response = {
                "action": act,
                "blocked": True,
                "confidence": analysis.get("confidence", 0.5),
                "message": "Agent blocked the attack"
            }
        elif act == "SANITIZE_INPUT":
            response = {
                "action": act,
                "blocked": True,
                "confidence": analysis.get("confidence", 0.5),
                "message": "Agent sanitized input"
            }
        else:
            response = {
                "action": "ALLOW",
                "blocked": False,
                "confidence": analysis.get("confidence", 0.5),
                "message": "Agent allowed request"
            }
    else:
        # fallback (should not be used in inference)
        response = respond_to_attack(analysis)

    reward_data = calculate_reward(analysis, response, attack)
    reward = reward_data["reward"]

    observation = CyberObservation(
        input=str(attack),
        attack=analysis.get("attack_type", "Unknown"),
        confidence=analysis.get("confidence", 0.5),
        message=analysis.get("explanation", "")
    )

    self.history.append({
        "step": self.step_count + 1,
        "attack": attack,
        "analysis": analysis,
        "response": response,
        "reward": reward
    })

    # difficulty adjustment
    if reward > 0.7:
        self.attacker.set_difficulty("hard")
    elif reward > 0.4:
        self.attacker.set_difficulty("medium")
    else:
        self.attacker.set_difficulty("easy")

    next_attack = self.attacker.generate_attack()
    self.current_input = next_attack
    self.step_count += 1
    self.done = self.step_count >= self.max_steps

    return {
        "observation": next_attack,
        "reward": reward,
        "done": self.done,
        "info": {
            "analysis": observation.dict(),
            "response": response,
            "reward_details": reward_data["details"],
            "step": self.step_count,
            "episode_id": self.episode_id
        }
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
