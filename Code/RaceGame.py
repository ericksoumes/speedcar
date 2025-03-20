import pygame
import pygame.time

from Code.Const import WIN_WIDTH, WIN_HEIGHT


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

        self.road_y = 60
        self.road_speed = 5

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.car_x > 65:
            self.car_x -= self.car_speed
        if keys[pygame.K_RIGHT] and self.car_x < WIN_WIDTH - 150:
            self.car_x += self.car_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        self.road_y += self.road_speed
        if self.road_y >= WIN_HEIGHT:
            self.road_y -= WIN_HEIGHT  # Em vez de zerar, reduza para manter continuidade

    def render(self):
        self.window.blit(self.bg, (0, 0))  # Desenha o fundo fixo

        # Adicionando uma quarta estrada para evitar lacunas
        self.window.blit(self.road, (60, self.road_y))
        self.window.blit(self.road, (60, self.road_y - WIN_HEIGHT))
        self.window.blit(self.road, (60, self.road_y - 2 * WIN_HEIGHT))
        self.window.blit(self.road, (60, self.road_y - 3 * WIN_HEIGHT))

        self.window.blit(self.ui, (0, 0))
        self.window.blit(self.car, (self.car_x, self.car_y))  # Desenha o carro
        pygame.display.update()



