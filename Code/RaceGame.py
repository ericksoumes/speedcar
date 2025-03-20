import pygame
import random

from Code.Const import WIN_WIDTH, WIN_HEIGHT
from Code.Score import ScoreScreen


class RaceGame:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = pygame.image.load('./assets/ui.png')
        self.bg = pygame.image.load('./assets/bg.png')
        self.road = pygame.image.load('./assets/road.png')
        self.road = pygame.transform.scale(self.road, (self.road.get_width(), WIN_HEIGHT))

        self.car = pygame.image.load('./assets/car-player.png')
        self.car_x = WIN_WIDTH // 2 - 25
        self.car_y = WIN_HEIGHT - 30
        self.car_speed = 5

        # Lista para armazenar obstáculos
        self.obstacles = []
        self.obstacle_images = [
            pygame.image.load('./assets/car-enemy.png'),  # Carro inimigo
            pygame.image.load('./assets/car-enemy2.png')  # Carro inimigo 2
        ]

        self.road_y = 60
        self.road_speed = 2
        self.score = 0
        self.frame_count = 0  # Contador de frames para controlar a pontuação
        self.last_speed_increment = 0  # Guarda a última pontuação em que a velocidade foi aumentada

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.car_x > 75:
            self.car_x -= self.car_speed
        if keys[pygame.K_RIGHT] and self.car_x < WIN_WIDTH - 150:
            self.car_x += self.car_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        self.frame_count += 1

        # Move a estrada
        self.road_y += self.road_speed
        if self.road_y >= WIN_HEIGHT:
            self.road_y = 0

        # Aumenta a pontuação
        if self.frame_count % 5 == 0:
            self.score += 1

        # Aumentar a velocidade a cada 400 pontos
        if self.score >= self.last_speed_increment + 400:
            self.road_speed += 1
            self.last_speed_increment = self.score

        # Gera obtaculos
        if random.randint(1, 60) == 1:
            obstacle_img = random.choice(self.obstacle_images)
            obstacle_x = random.randint(80, WIN_WIDTH - 160)
            self.obstacles.append([obstacle_img, obstacle_x, -100])

        # Mover obstáculos para baixo
        for obstacle in self.obstacles:
            obstacle[2] += self.road_speed

        # Remover obstáculos que saíram da tela
        self.obstacles = [ob for ob in self.obstacles if ob[2] < WIN_HEIGHT]

        # Verificar colisão com obstáculos
        for obstacle in self.obstacles:
            if (self.car_x < obstacle[1] + obstacle[0].get_width() and
                    self.car_x + self.car.get_width() > obstacle[1] and
                    self.car_y < obstacle[2] + obstacle[0].get_height() and
                    self.car_y + self.car.get_height() > obstacle[2]):
                self.game_over()
                return

    def game_over(self):
        score_screen = ScoreScreen(self.window, self.score)
        score_screen.run()
        self.running = False

    def render(self):
        self.window.blit(self.bg, (0, 0))  # Desenha o fundo fixo
        self.window.blit(self.road, (60, self.road_y))  # Desenha a estrada sobre o fundo
        self.window.blit(self.road, (60, self.road_y - WIN_HEIGHT))  # Loop na estrada
        self.window.blit(self.road, (60, self.road_y - 2 * WIN_HEIGHT))

        # Desenha obstáculos
        for obstacle in self.obstacles:
            self.window.blit(obstacle[0], (obstacle[1], obstacle[2]))

        self.window.blit(self.ui, (0, 0))
        self.window.blit(self.car, (self.car_x, self.car_y))  # Desenha o carrinho

        # Renderiza o Score
        font = pygame.font.Font(None, 14)
        score_text = font.render(f"{self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (280, 20))

        font = pygame.font.Font(None, 14)
        speed_text = font.render(f"{self.road_speed}", True, (255, 255, 255))
        self.window.blit(speed_text, (285, 80))

        pygame.display.update()
