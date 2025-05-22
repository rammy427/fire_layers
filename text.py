import pygame
from fighter import *

class TextManager:
    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.small_font = pygame.font.Font("fonts/gameboy.ttf", 19)
        self.big_font = pygame.font.Font("fonts/gameboy.ttf", 48)
        self.screen_rect = screen_rect

    def drawControls(self, screen: pygame.Surface) -> None:
        move_text = self.small_font.render("WASD:\nMover", True, "green")
        atk_text = self.small_font.render("Z: Atacar", True, "green")
        pass_text = self.small_font.render("ENTER: Pasar", True, "green")

        move_rect = move_text.get_rect()
        atk_rect = atk_text.get_rect()
        pass_rect = pass_text.get_rect()
        pass_rect.bottom = self.screen_rect.bottom
        atk_rect.bottom = pass_rect.top
        move_rect.bottom = atk_rect.top

        screen.blit(move_text, move_rect)
        screen.blit(atk_text, atk_rect)
        screen.blit(pass_text, pass_rect)
    
    def drawTeamInfo(self, fighters: list[list[Fighter]], screen: pygame.Surface) -> None:
        header1_text = self.small_font.render("Eq. 1 - ", True, "red")
        header1_rect = header1_text.get_rect()
        team1_texts: list[pygame.Surface] = []
        team1_rects: list[pygame.Rect] = []
        for i in range(len(fighters[0])):
            text = self.small_font.render("HP %d: %d " % (i + 1, fighters[0][i].hp), True, "red")
            team1_texts.append(text)
            team1_rects.append(text.get_rect())

        header2_text = self.small_font.render("Eq. 2 - ", True, "#3FD0F2")
        header2_rect = header2_text.get_rect()
        team2_texts: list[pygame.Surface] = []
        team2_rects: list[pygame.Rect] = []
        for i in range(len(fighters[1])):
            text = self.small_font.render("HP %d: %d" % (i + 1, fighters[1][i].hp), True, "#3FD0F2")
            team2_texts.append(text)
            team2_rects.append(text.get_rect())

        team2_rects[-1].bottomright = self.screen_rect.bottomright
        for i in range(len(fighters[1]) - 2, -1, -1):
            team2_rects[i].right = self.screen_rect.right
            team2_rects[i].bottom = team2_rects[i + 1].top
        header2_rect.topright = team2_rects[0].topleft

        team1_rects[-1].bottom = self.screen_rect.bottom
        team1_rects[-1].right = header2_rect.left - 10
        for i in range(len(fighters[0]) - 2, -1, -1):
            team1_rects[i].right = header2_rect.left - 10
            team1_rects[i].bottom = team1_rects[i + 1].top
        header1_rect.topright = team1_rects[0].topleft

        screen.blit(header1_text, header1_rect)
        screen.blit(header2_text, header2_rect)
        for i in range(len(team1_texts)):
            screen.blit(team1_texts[i], team1_rects[i])
        for i in range(len(team2_texts)):
            screen.blit(team2_texts[i], team2_rects[i])

    def drawGameOver(self, client_won: bool, screen: pygame.Surface) -> None:
        if (client_won):
            text = self.big_font.render("¡GANASTE!", True, "blue")
        else:
            text = self.big_font.render("PERDISTE.", True, "red")
        text_rect = text.get_rect()
        text_rect.center = self.screen_rect.center
        screen.blit(text, text_rect)