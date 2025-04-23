import pygame as pg
import time
import sys
import os
import json
from bird import Bird
from pipes import PipeManager
from interface import UI, Button
from score_system import ScoreSystem
from leaderboard import LeaderboardButton
            
class Game:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pg.display.set_mode((settings.width, settings.height))
        self.clock = pg.time.Clock()
        pg.display.set_caption('Flappy Bird')

        # game state variables
        self.game_active = False  # changed to false as default for start menu
        self.game_paused = False
        self.show_size_menu = False
        self.clicked = False
        self.last_click_time = 0

        # start menu variables
        self.in_start_menu = True
        self.countdown_active = False
        self.countdown_start_time = 0
        self.countdown_duration = 3  # seconds

        # leaderboard display state
        self.show_leaderboard = False

        self.floor_pos = 0

        self.load_background_floor()

        # game components - Bird | Pipes | Interface (UI,Button) | ScoreSystem | LeaderboardButton
        self.bird = Bird(settings)
        self.pipe_manager = PipeManager(settings)
        self.ui = UI(settings)
        self.score_system = ScoreSystem(settings)
        self.leaderboard_button = LeaderboardButton(settings)

        os.makedirs("../data", exist_ok=True) # ensure data dir exists for leaderboard

        # set up timers
        pg.time.set_timer(settings.SPAWNPIPE, settings.pipe_spawn_time)
        pg.time.set_timer(settings.BIRDFLAP, settings.bird_flap_time)

    def load_background_floor(self):
        """load & scale background and floor images"""
        # --------------- Background Image --------------- #
        self.bg = pg.image.load("../assets/img/background.jpg").convert_alpha()
        self.bg.set_colorkey(self.settings.WHITE)
        self.bg = pg.transform.scale(self.bg, (self.settings.width, self.settings.height))

        # --------------- Floor Image --------------- #
        self.floor = pg.image.load("../assets/img/floor.jpg").convert_alpha()
        self.floor.set_colorkey(self.settings.WHITE)
        self.floor = pg.transform.scale(self.floor, (self.settings.width, self.settings.height // 8))

    def draw_floor(self):
        """draw the scrolling floor"""
        floor_height = self.settings.height - self.settings.height // 10
        self.screen.blit(self.floor, (self.floor_pos, floor_height))
        self.screen.blit(self.floor, (self.floor_pos + self.settings.width, floor_height))

    def resize_game(self, size):
        """resize all game elements for a new screen size"""
        if self.settings.update_screen_size(size):
            # update screen
            self.screen = pg.display.set_mode((self.settings.width, self.settings.height))

            # reload background and floor
            self.load_background_floor()

            # update all game components
            self.bird.resize(self.settings)
            self.pipe_manager.resize(self.settings)
            self.ui.resize(self.settings)
            self.score_system.resize(self.settings)
            self.leaderboard_button.resize(self.settings)
        
    def start_countdown(self):
        """start the 3-second countdown before game begins"""
        self.countdown_active = True
        self.countdown_start_time = time.time()

    def update_countdown(self):
        """update countdown timer and start game when finished"""
        if self.countdown_active:
            elapsed = time.time() - self.countdown_start_time
            remaining = self.countdown_duration - elapsed

            if remaining <= 0:
                # countdown finished -> start game
                self.countdown_active = False
                self.in_start_menu = False
                self.game_active = True
                self.bird.reset()

    def draw_countdown(self):
        """draw countdown timer"""
        if self.countdown_active:
            elapsed = time.time() - self.countdown_start_time
            remaining = self.countdown_duration - elapsed

            if remaining > 0:
                overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                self.screen.blit(overlay, (0, 0))

                countdown_font = pg.font.SysFont('Arial', 120)
                number = str(max(1, int(remaining) + 1))
                text_surface = countdown_font.render(number, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.settings.width // 2, self.settings.height // 2))
                self.screen.blit(text_surface, text_rect)

                # get ready text
                ready_font = pg.font.SysFont('Arial', 60)
                ready_text = ready_font.render("Get Ready!", True, (255, 255, 255))
                ready_rect = ready_text.get_rect(center=(self.settings.width // 2, self.settings.height // 3))
                self.screen.blit(ready_text, ready_rect)

    def handle_events(self):
        cur_time = time.time()

        for event in pg.event.get():
            if event.type == pg.QUIT: pg.quit(); sys.exit()

            # pause with P key -- only when game is active
            if event.type == pg.KEYDOWN and event.key == pg.K_p and self.game_active and not self.countdown_active:
                self.game_paused = not self.game_paused

            # handle pipe spawning and bird animation
            if event.type == self.settings.SPAWNPIPE and self.game_active and not self.game_paused:
                self.pipe_manager.spawn_pipe()

            if event.type == self.settings.BIRDFLAP and not self.game_paused:
                self.bird.flap_animation()

            # double click detection for pausing -- only when game IS ACTIVE
            if event.type == pg.MOUSEBUTTONDOWN and self.game_active and not self.countdown_active:
                if event.button == 1:  # left mouse button
                    click_interval = cur_time - self.last_click_time
                    if click_interval < self.settings.double_click_interval:
                        self.game_paused = not self.game_paused
                
                    self.last_click_time = cur_time
                
            # handle name input for leaderboard
            if not self.game_active and not self.in_start_menu:
                result = self.score_system.handle_input_events(event)
                if result == "submitted":
                    self.score_system.show_name_input = False # clean input box after submission

        # handle space key for bird jumping -- only when game is active
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.game_active and not self.game_paused and not self.countdown_active:
            self.bird.jump()

    def update(self):
        """update game state -- including all of micro and meta processes"""
        if self.countdown_active: # update countdown if active
            self.update_countdown()
            return

        # move floor | always update even in menus for animation
        speedf = self.settings.scale_factor # speed factor 
        self.floor_pos -= int(1 * speedf)
        if self.floor_pos <= -self.settings.width: self.floor_pos = 0
        # skip other updates if game IS NOT ACTIVE or IS PAUSED
        if not self.game_active or self.game_paused: return

        # update pipes
        self.pipe_manager.update()

        # check score increases
        scored_pipe = self.pipe_manager.check_score(self.bird.rect.centerx)
        if scored_pipe:
            self.score_system.increase_score()
            self.score_system.add_score_message(
                self.bird.rect.centerx + 20,
                self.bird.rect.centery - 30
            )

        # bird update
        self.bird.update()

        # score message update
        self.score_system.update_score_messages()

        # collisions check
        if not self.check_collisions():
            self.game_active = False
            self.score_system.update_high_score()

    def check_collisions(self):
        # check pipe collisions
        if self.pipe_manager.check_collision(self.bird.rect): return False

        # check boundary collisions
        floor_height = self.settings.height - self.settings.height // 10
        if self.bird.rect.top <= -100 or self.bird.rect.bottom >= floor_height: return False

        return True

    def draw(self):
        """ draw all game elements based on 3 states:
             • game not started
             • countdown state
             • game is active or over
        """
        self.screen.blit(self.bg, (0, 0)) # draw background

        self.draw_floor()

        # -------------- START MENU -------------- #
        if self.in_start_menu and not self.countdown_active:
            self.ui.draw_start_menu(self.screen)
            
            # leaderboard button
            if self.leaderboard_button.draw_button(self.screen):
                self.show_leaderboard = not self.show_leaderboard

            
            if self.show_leaderboard:
                self.draw_leaderboard(self.screen)
            elif self.ui.start_button.draw_button(self.screen): # display only start button if leaderboard is not shown
                self.start_countdown()

        # -------------- COUNTDOWN -------------- #
        elif self.countdown_active: # 3..2..1
            self.bird.draw(self.screen) # bird during countdown
            self.draw_countdown() # countdown itself

        # -------------- Game IN PROGRESS or OVER -------------- #
        else:
            self.pipe_manager.draw(self.screen) # displaying pipes

            if self.game_active: self.bird.draw(self.screen) # bird if game is active

            self.score_system.draw_score_messages(self.screen) # score message

            # score display
            if not self.game_paused: self.score_system.draw_score(self.screen, 'a_game' if self.game_active else 'game_over')

            # pause overlay
            if self.game_paused and self.game_active:
                self.ui.draw_pause_overlay(self.screen)
                if self.ui.resume_button.draw_button(self.screen): self.game_paused = False

            # draw UI elements depending on game state
            if not self.game_active:
                if self.ui.again_button.draw_button(self.screen):
                    self.restart_game()
                if self.ui.quit_button.draw_button(self.screen):
                    pg.quit();
                    sys.exit()
                if self.ui.menu_button.draw_button(self.screen):
                    self.return_to_menu()

        # size button always available except COUNTDOWN SCREEN
        if not self.countdown_active:
            if self.ui.size_button.draw_button(self.screen):
                self.show_size_menu = not self.show_size_menu

            if self.show_size_menu:
                if self.ui.small_button.draw_button(self.screen):
                    self.resize_game("small")
                    self.show_size_menu = False
                if self.ui.medium_button.draw_button(self.screen):
                    self.resize_game("medium")
                    self.show_size_menu = False
                if self.ui.large_button.draw_button(self.screen):
                    self.resize_game("large")
                    self.show_size_menu = False

    def draw_leaderboard(self, screen):
        """draw the leaderboard screen with simplified layout - no dates"""
        # create semi-transparent background overlay
        overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # create leaderboard panel
        leaderboard_width = self.settings.width * 0.8
        leaderboard_height = self.settings.height * 0.8
        leaderboard_bg = pg.Surface((leaderboard_width, leaderboard_height), pg.SRCALPHA)
        leaderboard_bg.fill((40, 40, 60, 230))

        # position the leaderboard in the center
        bg_rect = leaderboard_bg.get_rect(center=(self.settings.width // 2, self.settings.height // 2))
        screen.blit(leaderboard_bg, bg_rect)

        # display the title
        title_font = pg.font.SysFont('Impact', int(50 * self.settings.scale_factor))
        title_text = title_font.render("LEADERBOARD", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.settings.width // 2, bg_rect.top + 50))
        screen.blit(title_text, title_rect)

        top_scores = self.get_leaderboard_scores() # get top scores

        # draw headers -- | RANK | NAME | SCORE |
        header_y = title_rect.bottom + 30
        column_width = (leaderboard_width - 60) / 3
        header_font = pg.font.SysFont('Arial', int(30 * self.settings.scale_factor))

        rank_text = header_font.render("RANK", True, (200, 200, 200))
        name_text = header_font.render("NAME", True, (200, 200, 200))
        score_text = header_font.render("SCORE", True, (200, 200, 200))

        screen.blit(rank_text, (bg_rect.left + column_width / 2 - rank_text.get_width() / 2, header_y))
        screen.blit(name_text, (bg_rect.left + column_width * 1.5 - name_text.get_width() / 2, header_y))
        screen.blit(score_text, (bg_rect.left + column_width * 2.5 - score_text.get_width() / 2, header_y))

        # draw horizontal line below headers
        pg.draw.line(
            screen,
            (200, 200, 200),
            (bg_rect.left + 30, header_y + 35),
            (bg_rect.right - 30, header_y + 35),
            2
        )

        # draw each score entry
        start_y = header_y + 60
        for i, entry in enumerate(top_scores):
            row_color = (60, 60, 80) if i % 2 == 0 else (80, 80, 100)
            row_rect = pg.Rect(bg_rect.left + 30, start_y, bg_rect.width - 60, 40)
            pg.draw.rect(screen, row_color, row_rect, border_radius=5)

            rank_text = header_font.render(f"{i + 1}", True, (255, 255, 255))
            screen.blit(rank_text, (bg_rect.left + column_width / 2 - rank_text.get_width() / 2, start_y + 5))

            name_text = header_font.render(entry["name"], True, (255, 255, 255))
            screen.blit(name_text, (bg_rect.left + column_width * 1.5 - name_text.get_width() / 2, start_y + 5))
            
            score_text = header_font.render(str(entry["score"]), True, (255, 215, 0))
            screen.blit(score_text, (bg_rect.left + column_width * 2.5 - score_text.get_width() / 2, start_y + 5))

            start_y += 50
        # -------- CLOSE BUTTON -------- #
        close_rect = pg.Rect(bg_rect.centerx - 75, bg_rect.bottom - 60, 150, 40)
        pg.draw.rect(screen, (180, 50, 50), close_rect, border_radius=10)
        close_text = header_font.render("Close", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_rect.center)
        screen.blit(close_text, close_text_rect)

        mouse_pos = pg.mouse.get_pos()
        if close_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]: # check for button click
            self.show_leaderboard = False

    def get_leaderboard_scores(self):
        """get the leaderboard scores from file or create empty if does not exist"""
        leaderboard_file = "../data/leaderboard.json"
        try:
            os.makedirs(os.path.dirname(leaderboard_file), exist_ok=True) # ensure directory exists | also done in main.py

            if os.path.exists(leaderboard_file):
                with open(leaderboard_file, 'r') as file:
                    data = json.load(file)
                    if "scores" in data:
                        return data["scores"]
                    elif "leaderboard" in data:
                        return data["leaderboard"]
                    else:
                        return []
            else:
                # create default leaderboard with scores key to match score_system.py
                default_leaderboard = {"scores": []}
                with open(leaderboard_file, 'w') as file:
                    json.dump(default_leaderboard, file)
                return []
        except Exception as e:
            print(f"error loading leaderboard: {e}")
            return []

    def restart_game(self):
        """reset the game state -> new game"""
        self.game_active = True
        self.game_paused = False
        self.pipe_manager.reset()
        self.bird.reset()
        self.score_system.reset_score()

    def return_to_menu(self):
        """return -> start menu"""
        self.in_start_menu = True
        self.game_active = False
        self.game_paused = False
        self.pipe_manager.reset()
        self.bird.reset()
        self.score_system.reset_score()

    def run(self):
        """main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(self.settings.FPS)
