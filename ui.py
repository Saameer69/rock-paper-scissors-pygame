import pygame
import random
import math
import io
from PIL import Image
import matplotlib.pyplot as plt
from game import Game

pygame.init()
pygame.mixer.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rock Paper Scissors")

# ---------------- COLORS ----------------
BG = (18, 18, 22)
PANEL = (28, 28, 35)
ACCENT = (100, 150, 255)
SUCCESS = (80, 200, 120)
DANGER = (255, 90, 90)
TEXT = (230, 230, 240)
MUTED = (160, 160, 170)
GRAPH_BG = (40, 40, 50)

# ---------------- FONTS ----------------
TITLE_FONT = pygame.font.SysFont("segoeui", 38, bold=True)
FONT = pygame.font.SysFont("segoeui", 24)
SMALL = pygame.font.SysFont("segoeui", 18)

# ---------------- ASSETS ----------------
IMG_ROCK = pygame.image.load("assets/images/rock.png").convert_alpha()
IMG_PAPER = pygame.image.load("assets/images/paper.png").convert_alpha()
IMG_SCISSORS = pygame.image.load("assets/images/scissors.png").convert_alpha()

ICON_MAP = {
    "rock": IMG_ROCK,
    "paper": IMG_PAPER,
    "scissors": IMG_SCISSORS
}

CLICK_SOUND = pygame.mixer.Sound("assets/sounds/click.wav")
WIN_SOUND = pygame.mixer.Sound("assets/sounds/win.wav")
LOSE_SOUND = pygame.mixer.Sound("assets/sounds/lose.wav")

# ---------------- HELPERS ----------------
def draw_panel(surface, rect, radius=12, color=PANEL):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def ease_out(t):
    return 1 - (1 - t) ** 3

def draw_icon(surface, image, x, y, scale, width, height):
    size = int(min(width, height) * 0.12 * scale)
    img = pygame.transform.smoothscale(image, (size, size))
    rect = img.get_rect(center=(x, y))
    surface.blit(img, rect)

# ---------------- BUTTON ----------------
class Button:
    def __init__(self, text, rel_x, rel_y, rel_w=0.15, rel_h=0.08):
        self.text = text
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.rel_w = rel_w
        self.rel_h = rel_h
        self.rect = pygame.Rect(0,0,0,0)

    def update_rect(self, width, height):
        self.rect.width = int(width * self.rel_w)
        self.rect.height = int(height * self.rel_h)
        self.rect.center = (int(width * self.rel_x), int(height * self.rel_y))

    def draw(self, surface, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = ACCENT if hovered else PANEL
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        label = FONT.render(self.text, True, TEXT)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------- PARTICLES ----------------
class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(2,5)
        self.speed = random.uniform(0.5, 2)
        self.color = (random.randint(50,100), random.randint(50,100), random.randint(200,255))
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# ---------------- UI ----------------
class UI:
    def __init__(self):
        self.game = Game()
        self.player_move = None
        self.ai_move = None
        self.result = "Choose your move"
        self.anim_progress = 0
        self.ai_vs_ai_mode = False
        self.showing_graph = False
        self.graph_surface = None
        self.graph_rect = None

        # Particles
        self.particles = [Particle() for _ in range(50)]

        # Buttons
        self.move_buttons = [
            Button("ROCK", 0.2, 0.85),
            Button("PAPER", 0.5, 0.85),
            Button("SCISSORS", 0.8, 0.85)
        ]
        self.control_buttons = [
            Button("STATS", 0.25, 0.93, 0.18, 0.06),
            Button("AI vs AI", 0.5, 0.93, 0.18, 0.06),
            Button("RESET", 0.75, 0.93, 0.18, 0.06)
        ]
        self.close_button = Button("CLOSE", 0.9, 0.1, 0.12, 0.05)

    def handle_click(self, pos):
        if self.showing_graph:
            if self.close_button.clicked(pos):
                self.showing_graph = False
            return

        if not self.ai_vs_ai_mode:
            for btn in self.move_buttons:
                if btn.clicked(pos):
                    CLICK_SOUND.play()
                    self.player_move = btn.text.lower()
                    self.ai_move = self.game.ai.choose()
                    self.result = self.game.winner(self.player_move, self.ai_move)
                    self.game.ai.update(self.player_move)
                    self.game.moves_history.append((self.player_move, self.ai_move))
                    self.anim_progress = 0
                    if self.result == "Player Wins":
                        WIN_SOUND.play()
                    elif self.result == "AI Wins":
                        LOSE_SOUND.play()

        for btn in self.control_buttons:
            if btn.clicked(pos):
                if btn.text == "STATS":
                    self.show_stats()
                elif btn.text == "AI vs AI":
                    self.ai_vs_ai_mode = not self.ai_vs_ai_mode
                    self.result = "AI-vs-AI Mode ON" if self.ai_vs_ai_mode else "AI-vs-AI Mode OFF"
                elif btn.text == "RESET":
                    self.reset_game()

    def reset_game(self):
        self.game.player_score = 0
        self.game.ai_score = 0
        self.game.ties = 0
        self.game.moves_history = []
        self.player_move = None
        self.ai_move = None
        self.result = "Choose your move"
        self.ai_vs_ai_mode = False
        self.showing_graph = False

    def show_stats(self):
        moves = ["rock", "paper", "scissors"]
        player_counts = [0,0,0]
        ai_counts = [0,0,0]

        for p,a in self.game.moves_history:
            player_counts[moves.index(p)] +=1
            ai_counts[moves.index(a)] +=1

        plt.figure(figsize=(4,3))
        x = range(len(moves))
        plt.bar([i-0.15 for i in x], player_counts, width=0.3, color='blue', label='Player')
        plt.bar([i+0.15 for i in x], ai_counts, width=0.3, color='red', label='AI')
        plt.xticks(x, moves)
        plt.title("Moves Frequency")
        plt.legend()
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        img = Image.open(buf)
        mode = img.mode
        size = img.size
        data = img.tobytes()
        self.graph_surface = pygame.image.fromstring(data, size, mode)
        self.graph_rect = self.graph_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.showing_graph = True

    def draw_scores(self):
        # Top panels for scores
        score_w, score_h = int(WIDTH*0.18), int(HEIGHT*0.06)
        x_positions = [0.2, 0.5, 0.8]
        labels = [f"Player: {self.game.player_score}", f"AI: {self.game.ai_score}", f"Tie: {self.game.ties}"]
        colors = [SUCCESS, DANGER, MUTED]
        for i in range(3):
            rect = pygame.Rect(0,0,score_w,score_h)
            rect.center = (int(WIDTH*x_positions[i]), 110)
            draw_panel(SCREEN, rect, radius=15, color=colors[i])
            text = SMALL.render(labels[i], True, TEXT)
            SCREEN.blit(text, text.get_rect(center=rect.center))

    def draw_background(self):
        for p in self.particles:
            p.move()
            p.draw(SCREEN)

    def draw(self):
        global WIDTH, HEIGHT
        WIDTH, HEIGHT = SCREEN.get_size()
        SCREEN.fill(BG)
        self.draw_background()

        # ---------------- Title ----------------
        title = TITLE_FONT.render("Rock • Paper • Scissors", True, ACCENT)
        SCREEN.blit(title, title.get_rect(center=(WIDTH//2, 40)))
        pygame.draw.line(SCREEN, ACCENT, (WIDTH//4, 70), (3*WIDTH//4, 70), 3)

        # ---------------- Scores ----------------
        self.draw_scores()

        # ---------------- Icon Panels ----------------
        panel_w, panel_h = int(WIDTH*0.4), int(HEIGHT*0.45)
        draw_panel(SCREEN, pygame.Rect(int(WIDTH*0.05), int(HEIGHT*0.25), panel_w, panel_h), radius=20)
        draw_panel(SCREEN, pygame.Rect(int(WIDTH*0.55), int(HEIGHT*0.25), panel_w, panel_h), radius=20)

        # ---------------- AI-vs-AI ----------------
        if self.ai_vs_ai_mode:
            if pygame.time.get_ticks() % 50 == 0:  # slower steps
                self.player_move = self.game.ai.choose()
                self.ai_move = self.game.ai.choose()
                self.result = self.game.winner(self.player_move, self.ai_move)
                self.game.moves_history.append((self.player_move, self.ai_move))
                if self.result == "Player Wins":
                    self.game.player_score += 1
                elif self.result == "AI Wins":
                    self.game.ai_score += 1
                else:
                    self.game.ties += 1
                self.anim_progress = 0

        # ---------------- Animate Icons ----------------
        self.anim_progress = min(self.anim_progress + 0.03, 1)
        scale = ease_out(self.anim_progress)
        offset = math.sin(pygame.time.get_ticks()/150)*15  # bounce
        if self.player_move:
            draw_icon(SCREEN, ICON_MAP[self.player_move], int(WIDTH*0.25), int(HEIGHT*0.45)+offset, scale, WIDTH, HEIGHT)
        if self.ai_move:
            draw_icon(SCREEN, ICON_MAP[self.ai_move], int(WIDTH*0.75), int(HEIGHT*0.45)+offset, scale, WIDTH, HEIGHT)

        # ---------------- Result Box ----------------
        result_color = SUCCESS if self.result=="Player Wins" else DANGER if self.result=="AI Wins" else MUTED
        result_rect = pygame.Rect(WIDTH//4, int(HEIGHT*0.72), WIDTH//2, 50)
        draw_panel(SCREEN, result_rect, radius=15, color=(40,40,50))
        result_text = FONT.render(self.result, True, result_color)
        SCREEN.blit(result_text, result_text.get_rect(center=result_rect.center))

        # ---------------- Buttons ----------------
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.move_buttons + self.control_buttons:
            btn.update_rect(WIDTH, HEIGHT)
            if btn.rect.collidepoint(mouse_pos):
                pygame.draw.rect(SCREEN, ACCENT, btn.rect.inflate(10,10), border_radius=12)
            btn.draw(SCREEN, mouse_pos)

        # ---------------- Hint ----------------
        hint = SMALL.render("Click a move | ESC: Quit", True, MUTED)
        SCREEN.blit(hint, hint.get_rect(center=(WIDTH//2, int(HEIGHT*0.83))))

        # ---------------- Stats Overlay ----------------
        if self.showing_graph and self.graph_surface:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            SCREEN.blit(overlay, (0,0))
            SCREEN.blit(self.graph_surface, self.graph_surface.get_rect(center=(WIDTH//2, HEIGHT//2)))
            self.close_button.update_rect(WIDTH, HEIGHT)
            self.close_button.draw(SCREEN, mouse_pos)

        pygame.display.update()
