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

        pos = pg.mouse.get_pos()         # mouse pos

        button_rect = Rect(self.x, self.y, self.width, self.height)         # rect for button

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                cur_time = pg.time.get_ticks() # preventing multiple clicks by checking time
                if cur_time - self.last_click_time > 200:  # ms debounce
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

        # font size based on btn size (width, height)
        font_size = min(int(self.height * 0.6), int(self.width * 0.2))
        button_font = pg.font.SysFont('Constantia', font_size)

        # text for btns
        text_img = button_font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        text_height = text_img.get_height()

        # centering text insdie btn
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
        """create all ui buttons BASED ON crnt screen size"""
        w = self.settings.width
        h = self.settings.height
        button_scale_w = w / self.settings.SCREEN_SIZES["medium"][0]
        button_scale_h = h / self.settings.SCREEN_SIZES["medium"][1]

        # ------------ PLAY ------------ start menu btn
        start_width = int(250 * button_scale_w)
        start_height = int(100 * button_scale_h)
        start_x = (w - start_width) // 2
        start_y = h * 0.55
        self.start_button = Button(start_x, start_y, 'Play', start_width, start_height, (0, 180, 50))


        """ ----------------------- GAME OVER  btns ----------------------- """
        # ------------ Play Again ------------ main game buttons
        again_width = int(180 * button_scale_w)
        again_height = int(70 * button_scale_h)
        again_x = (w - again_width) // 4
        again_y = h * 0.65
        self.again_button = Button(again_x, again_y, 'Play Again', again_width, again_height)

        # ------------ Quit ------------ 
        quit_width = int(180 * button_scale_w)
        quit_height = int(70 * button_scale_h)
        quit_x = w - quit_width - (w - quit_width) // 4
        quit_y = h * 0.65
        self.quit_button = Button(quit_x, quit_y, 'Quit', quit_width, quit_height)
        """ ----------------------- GAME OVER  btns ----------------------- """

        # ------------ Main Menu ------------ menu button for returning to start menu // for game over screen
        menu_width = int(350 * button_scale_w)
        menu_height = int(100 * button_scale_h)
        menu_x = (w - menu_width) // 2
        menu_y = h * 0.75
        self.menu_button = Button(menu_x, menu_y, 'Main Menu', menu_width, menu_height, (255, 165, 0))

        # continue / resume button
        continue_width = int(180 * button_scale_w)
        continue_height = int(70 * button_scale_h)
        continue_x = (w - continue_width) // 2
        continue_y = h * 0.6
        self.continue_button = Button(continue_x, continue_y, 'Resume', continue_width, continue_height, (255, 165, 0))

        # size menu buttons
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
        self.small_button = Button(small_x, size_opt_y, 'Small', size_opt_width, size_opt_height, (80, 80, 200))

        medium_x = w - size_opt_width * 2 - 15
        self.medium_button = Button(medium_x, size_opt_y, 'Medium', size_opt_width, size_opt_height, (80, 80, 200))

        large_x = w - size_opt_width - 10
        self.large_button = Button(large_x, size_opt_y, 'Large', size_opt_width, size_opt_height, (80, 80, 200))

    def resize(self, settings):
        """upd interfaec for new screen size if changed"""
        self.settings = settings
        self.create_buttons()
        self.game_font = pg.font.SysFont('Impact', int(40 * settings.scale_factor))
        self.title_font = pg.font.SysFont('Impact', int(80 * settings.scale_factor))

    def draw_start_menu(self, screen):
        """draw start menu scree"""
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

        # subtitle -- Press to start da game
        subtitle_font = pg.font.SysFont('Arial', int(30 * self.settings.scale_factor))
        subtitle_text = subtitle_font.render("Press Play to start the Game!", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.settings.width // 2, self.settings.height * 0.35))
        screen.blit(subtitle_text, subtitle_rect)

        # highest score // if exists
        if hasattr(self, 'high_score') and self.high_score > 0:
            high_score_text = self.game_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center=(self.settings.width // 2, self.settings.height * 0.45))
            screen.blit(high_score_text, high_score_rect)

        # now start btn is drawn by game loop

    def draw_pause_overlay(self, screen):
        """draw pause menu overlay"""
        # semi-transparent overlay
        overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # PAUSED txt
        paused_text = self.pause_font.render("PAUSED", True, (255, 255, 255))
        shadow_text = self.pause_font.render("PAUSED", True, (80, 80, 80))

        text_rect = paused_text.get_rect(center=(self.settings.width // 2, pause_y + 60))
        shadow_rect = shadow_text.get_rect(center=(self.settings.width // 2 + 4, pause_y + 64))

        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, text_rect)

        # hint text
        hint_font = pg.font.SysFont('Arial', int(18 * self.settings.scale_factor))
        hint_text = hint_font.render("Press P or double-click to Pause the Game", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(self.settings.width // 2, text_rect.bottom + 20))
        screen.blit(hint_text, hint_rect)

    def draw_game_over_menu(self, screen, score=0):
        """draw game over screen with final score and buttons"""
        # semi-transparent overlay for text visibility
        overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # slightly darker overlay than start menu
        screen.blit(overlay, (0, 0))

        # Game Over text with shadow effect
        gameover_shadow = self.title_font.render("GAME OVER", True, (150, 0, 0))
        gameover_text = self.title_font.render("GAME OVER", True, (255, 0, 0))

        shadow_rect = gameover_shadow.get_rect(center=(self.settings.width // 2 + 5, self.settings.height // 4 + 5))
        gameover_rect = gameover_text.get_rect(center=(self.settings.width // 2, self.settings.height // 4))

        screen.blit(gameover_shadow, shadow_rect)
        screen.blit(gameover_text, gameover_rect)

        # Display final score with shadow
        score_font = pg.font.SysFont('Impact', int(50 * self.settings.scale_factor))
        score_shadow = score_font.render(f"Score: {score}", True, (80, 80, 80))
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        
        shadow_rect = score_shadow.get_rect(center=(self.settings.width // 2 + 3, self.settings.height * 0.45 + 3))
        score_rect = score_text.get_rect(center=(self.settings.width // 2, self.settings.height * 0.45))
        
        screen.blit(score_shadow, shadow_rect)
        screen.blit(score_text, score_rect)

        # Display high score if available (with shadow)
        if hasattr(self, 'high_score') and self.high_score > 0:
            if score > self.high_score:
                self.high_score = score
                high_score_shadow = self.game_font.render(f"NEW HIGH SCORE: {self.high_score}", True, (150, 120, 0))
                high_score_text = self.game_font.render(f"NEW HIGH SCORE: {self.high_score}", True, (255, 215, 0))
            else:
                high_score_shadow = self.game_font.render(f"High Score: {self.high_score}", True, (80, 80, 80))
                high_score_text = self.game_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            
            shadow_rect = high_score_shadow.get_rect(center=(self.settings.width // 2 + 3, self.settings.height * 0.55 + 3))
            high_score_rect = high_score_text.get_rect(center=(self.settings.width // 2, self.settings.height * 0.55))
            
            screen.blit(high_score_shadow, shadow_rect)
            screen.blit(high_score_text, high_score_rect)

        # Draw the buttons and check for clicks
        if self.again_button.draw_button(screen):
            self.restart_game()
        
        if self.quit_button.draw_button(screen):
            pg.quit()
            sys.exit()
        
        if self.menu_button.draw_button(screen):
            self.return_to_menu()

