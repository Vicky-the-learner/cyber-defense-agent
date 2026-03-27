from detector import detect_attack
from responder import respond_to_attack
from reward import calculate_reward


class CyberDefenseEnv:
    def __init__(self):
        self.current_input = None
        self.last_analysis = None
        self.done = False

    def reset(self):
        self.current_input = None
        self.last_analysis = None
        self.done = False

        return {
            "state": "Environment reset"
        }

    def step(self, input_data):
        self.current_input = input_data

        # Detection
        analysis = detect_attack(input_data)

        # Response
        response = respond_to_attack(analysis)

        # Reward
        reward = calculate_reward(analysis, response)

        # Save state
        self.last_analysis = analysis
        self.done = True

        return {
            "state": {
                "input": input_data,
                "analysis": analysis
            },
            "response": response,
            "reward": reward,
            "done": self.done
        }

    def state(self):
        return {
            "current_input": self.current_input,
            "last_analysis": self.last_analysis,
            "done": self.done
        }