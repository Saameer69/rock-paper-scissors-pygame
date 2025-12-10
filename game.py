import random

class AI:
    def __init__(self):
        self.moves = ["rock", "paper", "scissors"]
        self.history = []

    def choose(self):
        return random.choice(self.moves)

    def update(self, player_move):
        self.history.append(player_move)

class Game:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.ties = 0
        self.ai = AI()
        self.moves_history = []  # Keep history for stats

    def winner(self, player, ai):
        self.moves_history.append((player, ai))
        if player == ai:
            self.ties += 1
            return "Tie"
        elif (player == "rock" and ai == "scissors") or \
             (player == "paper" and ai == "rock") or \
             (player == "scissors" and ai == "paper"):
            self.player_score += 1
            return "Player Wins"
        else:
            self.ai_score += 1
            return "AI Wins"

    # AI-vs-AI simulation step
    def ai_vs_ai_step(self):
        player = self.ai.choose()
        ai = self.ai.choose()
        result = self.winner(player, ai)
        return player, ai, result
