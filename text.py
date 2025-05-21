import pygame

class TextManager:
    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.small_font = pygame.font.Font("fonts/gameboy.ttf", 24)
        self.big_font = pygame.font.Font("fonts/gameboy.ttf", 48)
        self.__screen_rect = screen_rect

    def drawGameOver(self, client_won: bool, screen: pygame.Surface) -> None:
        if (client_won):
            text = self.big_font.render("¡GANASTE!", True, "blue")
        else:
            text = self.big_font.render("PERDISTE.", True, "red")
        text_rect = text.get_rect()
        text_rect.center = self.__screen_rect.center
        screen.blit(text, text_rect)