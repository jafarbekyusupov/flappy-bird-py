import pygame as pg

class LeaderboardButton:
    def __init__(self, settings):
        self.settings = settings

        # button dimensions
        self.button_width = int(150 * settings.scale_factor)
        self.button_height = int(40 * settings.scale_factor)
        self.button_x = 20
        self.button_y = 20

        # colors
        self.normal_color = (124, 100, 150)
        self.hover_color = (100, 100, 255)
        self.clicked_color = (80, 80, 200)
        self.clicked = False

        self.font = pg.font.SysFont('Arial', int(20 * settings.scale_factor))

    def resize(self, settings):
        """update width & height when Screen Size changes"""
        self.settings = settings
        self.button_width = int(150 * settings.scale_factor)
        self.button_height = int(40 * settings.scale_factor)
        self.font = pg.font.SysFont('Arial', int(20 * settings.scale_factor))

    def draw_button(self, screen):
        """leaderboard button  & handle clicks"""
        action = False

        mouse_pos = pg.mouse.get_pos()
        button_rect = pg.Rect(self.button_x, self.button_y, self.button_width, self.button_height)

        # mouse over and clicked conditions
        if button_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pg.draw.rect(screen, self.clicked_color, button_rect, border_radius=10)
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            else:
                pg.draw.rect(screen, self.hover_color, button_rect, border_radius=10)
        else:
            pg.draw.rect(screen, self.normal_color, button_rect, border_radius=10)

        # ---------- LEADERBOARD BUTTON ---------- #
        pg.draw.rect(screen, (255, 255, 255), button_rect, width=2, border_radius=10) # circular border for Leaderboard button
        
        text = self.font.render("Leaderboard", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        return action
