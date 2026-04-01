import random

class Attacker:
    def __init__(self):
        self.history = []
        self.difficulty = "easy"

    def set_difficulty(self, level):
        self.difficulty = level

    def generate_attack(self):
        if self.difficulty == "easy":
            attack = self._easy_attack()
        elif self.difficulty == "medium":
            attack = self._medium_attack()
        else:
            attack = self._hard_attack()

        self.history.append(attack)
        return attack

    # -------------------------
    # EASY ATTACKS
    # -------------------------
    def _easy_attack(self):
        return {
            "type": "sql_injection",
            "payload": "' OR 1=1 --",
            "severity": 0.3
        }

    # -------------------------
    # MEDIUM ATTACKS
    # -------------------------
    def _medium_attack(self):
        attacks = [
            {
                "type": "xss",
                "payload": "<script>alert(1)</script>",
                "severity": 0.6
            },
            {
                "type": "path_traversal",
                "payload": "../../etc/passwd",
                "severity": 0.6
            }
        ]
        return random.choice(attacks)

    # -------------------------
    # HARD ATTACKS
    # -------------------------
    def _hard_attack(self):
        attacks = [
            {
                "type": "command_injection",
                "payload": "&& rm -rf /",
                "severity": 0.9
            },
            {
                "type": "obfuscated_xss",
                "payload": "<scr<script>ipt>alert(1)</scr<script>ipt>",
                "severity": 0.95
            }
        ]
        return random.choice(attacks)