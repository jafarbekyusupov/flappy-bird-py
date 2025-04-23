import pygame as pg
from pygame.locals import *

class Button:
    def __init__(self, x, y, text, width=None, height=None, color=(17, 208, 51)):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.height = height
        self.button_col = color
        self.hover_col = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.click_col = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
        self.text_col = (255, 255, 255)
        self.clicked = False
        self.last_click_time = 0

    def draw_button(self, screen):
        action = False

        pos = pg.mouse.get_pos() # mouse position

        button_rect = Rect(self.x, self.y, self.width, self.height) # rect for button

        # check mouseover & clicked conditions
        if button_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                cur_time = pg.time.get_ticks() # preventing multiple clicks by checking time
                if cur_time - self.last_click_time > 200:  # ms in debounce
                    self.clicked = True
                    self.last_click_time = cur_time
                pg.draw.rect(screen, self.click_col, button_rect)

            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True

            else:
                pg.draw.rect(screen, self.hover_col, button_rect)

        else:
            pg.draw.rect(screen, self.button_col, button_rect)

        # shading
        pg.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(screen, (0, 0, 0), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 3)
        pg.draw.line(screen, (0, 0, 0), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 3)

        # font size based on button size -- width, height
        font_size = min(int(self.height * 0.6), int(self.width * 0.2))
        button_font = pg.font.SysFont('Constantia', font_size)

        # text for buttons
        text_img = button_font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        text_height = text_img.get_height()

        # centering text inside button
        screen.blit(text_img, (self.x + (self.width - text_len) // 2, self.y + (self.height - text_height) // 2))
        return action


class UI:
    def __init__(self, settings):
        self.settings = settings
        self.create_buttons()

        # font setups
        self.game_font = pg.font.SysFont('Impact', int(40 * settings.scale_factor))
        self.pause_font = pg.font.SysFont('Arial', 72)
        self.title_font = pg.font.SysFont('Impact', int(80 * settings.scale_factor))

    def create_buttons(self):
        """create all UI buttons BASED ON current screen size"""
        w = self.settings.width
        h = self.settings.height
        button_scale_w = w / self.settings.SCREEN_SIZES["medium"][0]
        button_scale_h = h / self.settings.SCREEN_SIZES["medium"][1]

        # ------------ PLAY BUTTON ------------ #
        start_width = int(250 * button_scale_w)
        start_height = int(100 * button_scale_h)
        start_x = (w - start_width) // 2
        start_y = h * 0.55
        self.start_button = Button(start_x, start_y, 'Play', start_width, start_height, (0, 180, 50))


        """ -------------- GAME OVER  BUTTONS  --------------"""
        ### -------------- PLAY AGAIN BUTTON ------------ ###
        again_width = int(180 * button_scale_w)
        again_height = int(70 * button_scale_h)
        again_x = (w - again_width) // 4
        again_y = h * 0.65
        self.again_button = Button(again_x, again_y, 'Play Again', again_width, again_height)

        ### -------------- QUIT BUTTON -------------- ###  
        quit_width = int(180 * button_scale_w)
        quit_height = int(70 * button_scale_h)
        quit_x = w - quit_width - (w - quit_width) // 4
        quit_y = h * 0.65
        self.quit_button = Button(quit_x, quit_y, 'Quit', quit_width, quit_height)

        ### -------------- MAIN MENU BUTTON -------------- ###
        menu_width = int(350 * button_scale_w)
        menu_height = int(100 * button_scale_h)
        menu_x = (w - menu_width) // 2
        menu_y = h * 0.75
        self.menu_button = Button(menu_x, menu_y, 'Main Menu', menu_width, menu_height, (255, 165, 0))

        # -------------- Pause Screen :: RESUME BUTTON  -------------- #
        resume_width = int(180 * button_scale_w)
        resume_height = int(70 * button_scale_h)
        resume_x = (w - resume_width) // 2
        resume_y = h * 0.6
        self.resume_button = Button(resume_x, resume_y, 'Resume', resume_width, resume_height, (255, 165, 0))

        # -------------- SIZE subBUTTONs  -------------- #
        size_button_width = int(100 * button_scale_w)
        size_button_height = int(50 * button_scale_h)
        self.size_button = Button(
            w - size_button_width - 10,
            h - size_button_height - 10,
            'Size', size_button_width, size_button_height, (100, 100, 255)
        )

        size_opt_width = int(80 * button_scale_w)
        size_opt_height = int(40 * button_scale_h)
        size_opt_y = h - size_opt_height * 2 - 15

        small_x = w - size_opt_width * 3 - 20
        self.small_button = Button(small_x, size_opt_y - 10, 'Small', size_opt_width, size_opt_height, (80, 80, 200))

        medium_x = w - size_opt_width * 2 - 15
        self.medium_button = Button(medium_x, size_opt_y - 10, 'Medium', size_opt_width, size_opt_height, (80, 80, 200))

        large_x = w - size_opt_width - 10
        self.large_button = Button(large_x, size_opt_y - 10, 'Large', size_opt_width, size_opt_height, (80, 80, 200))

    def resize(self, settings):
        """update interface for new screen size if changed"""
        self.settings = settings
        self.create_buttons()
        self.game_font = pg.font.SysFont('Impact', int(40 * settings.scale_factor))
        self.title_font = pg.font.SysFont('Impact', int(80 * settings.scale_factor))

    def draw_start_menu(self, screen):
        """draw start menu screen"""
        # semi-transparent overlay for text visibility
        overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        screen.blit(overlay, (0, 0))

        # game title
        title_shadow = self.title_font.render("FLAPPY BIRD", True, (100, 100, 0))
        title_text = self.title_font.render("FLAPPY BIRD", True, (255, 255, 0))

        shadow_rect = title_shadow.get_rect(center=(self.settings.width // 2 + 5, self.settings.height // 4 + 5))
        title_rect = title_text.get_rect(center=(self.settings.width // 2, self.settings.height // 4))

        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)

        # subtitle -- Press to Start the game
        subtitle_font = pg.font.SysFont('Arial', int(30 * self.settings.scale_factor))
        subtitle_text = subtitle_font.render("Press Play to start the Game!", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.settings.width // 2, self.settings.height * 0.35))
        screen.blit(subtitle_text, subtitle_rect)

        # highest score -- if exists
        if hasattr(self, 'high_score') and self.high_score > 0:
            high_score_text = self.game_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center=(self.settings.width // 2, self.settings.height * 0.45))
            screen.blit(high_score_text, high_score_rect)

    def draw_pause_overlay(self, screen):
        """draw pause menu overlay"""
        overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # box background
        pause_width = int(300 * self.settings.scale_factor)
        pause_height = int(200 * self.settings.scale_factor)
        pause_x = (self.settings.width - pause_width) // 2
        pause_y = (self.settings.height - pause_height) // 2

        # rounded rect -- for PAUSED menu text
        pause_rect = pg.Rect(pause_x, pause_y, pause_width, pause_height)
        pg.draw.rect(screen, (60, 60, 80, 220), pause_rect, border_radius=15)
        pg.draw.rect(screen, (100, 100, 120), pause_rect, width=3, border_radius=15)

        # PAUSED text with shadowing
        paused_text = self.pause_font.render("PAUSED", True, (255, 255, 255))
        shadow_text = self.pause_font.render("PAUSED", True, (80, 80, 80))

        text_rect = paused_text.get_rect(center=(self.settings.width // 2, pause_y + 60))
        shadow_rect = shadow_text.get_rect(center=(self.settings.width // 2 + 4, pause_y + 64))

        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, text_rect)

        # hint text
        hint_font = pg.font.SysFont('Arial', int(18 * self.settings.scale_factor))
        hint_text = hint_font.render("Press P or double-click to resume", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(self.settings.width // 2, text_rect.bottom + 20))
        screen.blit(hint_text, hint_rect)
