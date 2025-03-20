import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Code.Const import COLOR_YELLOW, WIN_WIDTH, MENU_OPTION, COLOR_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/menu.jpg')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Speedcar", COLOR_YELLOW, ((WIN_WIDTH / 2), 70))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], COLOR_YELLOW, ((WIN_WIDTH / 2), 110 + 25 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 110 + 25 * i))

            pygame.display.flip()

            # check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # close window
                    quit()  # end pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/VCR_OSD_MONO.ttf", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
