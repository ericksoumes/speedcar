import sys
import sqlite3
from datetime import datetime
import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from Code.Const import COLOR_YELLOW, COLOR_WHITE, WIN_WIDTH, WIN_HEIGHT


class Score:
    def __init__(self, db_name="DBScore"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_score(self, name, score):
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO scores (name, score, date) VALUES (?, ?, ?)", (name, score, date))
            conn.commit()

    def get_top_scores(self, limit=10):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, score, date FROM scores ORDER BY score DESC LIMIT ?", (limit,))
            return cursor.fetchall()


class ScoreScreen:
    def __init__(self, window: Surface, score: int = None):
        self.window = window
        self.score = score
        self.surf = pygame.image.load("./assets/bg.png").convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.name = ""
        self.db = Score()

    def run(self):
        # Tela salvar score
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.draw_text("Game Over!", 32, COLOR_YELLOW, (WIN_WIDTH / 2, 20))
            self.draw_text(f"Score: {self.score}", 20, COLOR_WHITE, (WIN_WIDTH / 2, 50))
            self.draw_text("Enter your name (4 letters):", 14, COLOR_WHITE, (WIN_WIDTH / 2, 100))
            self.draw_text(self.name, 14, COLOR_YELLOW, (WIN_WIDTH / 2, 150))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(self.name) == 4:
                        self.db.save_score(self.name, self.score)
                        self.show_high_scores()
                        return
                    elif event.key == K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < 4 and event.unicode.isalpha():
                        self.name += event.unicode.upper()

    def show_high_scores(self):
        # Tela 10 melhores
        self.window.blit(source=self.surf, dest=self.rect)
        self.draw_text("High Scores", 20, COLOR_YELLOW, (WIN_WIDTH / 2, 30))

        top_scores = self.db.get_top_scores()
        y_offset = 50
        for name, score, date in top_scores:
            self.draw_text(f"{name} - {score} - {date}", 14, COLOR_WHITE, (WIN_WIDTH / 2, y_offset))
            y_offset += 15

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return

    def draw_text(self, text, size, color, pos):
        font = pygame.font.Font("./assets/VCR_OSD_MONO.ttf", size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        self.window.blit(text_surf, text_rect)
