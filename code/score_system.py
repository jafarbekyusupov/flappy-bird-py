import pygame as pg
import json
import os

class ScoreMessage:
    def __init__(self, x, y, lifetime=60):
        self.x = x
        self.y = y
        self.lifetime = lifetime

    def update(self):
        self.lifetime -= 1
        self.y -= 1

    def draw(self, screen, font):
        message = font.render("+1", True, (0, 255, 0))
        shadow = font.render("+1", True, (0, 100, 0))  # shadow effect
        screen.blit(shadow, (self.x + 2, self.y + 2))
        screen.blit(message, (self.x, self.y))

    def is_expired(self):
        return self.lifetime <= 0

class ScoreSystem:
    def __init__(self, settings):
        self.settings = settings
        self.score = 0
        self.high_score = 0
        self.score_messages = []

        self.leaderboard_file = "data/leaderboard.json"  # leaderboard file

        top_scores = self.get_top_scores(1)  # top score from leaderboard
        if top_scores: self.high_score = top_scores[0]["score"]

        # username input for leaderboard
        self.username = ""
        self.active_input = False
        self.show_name_input = False

        # load fonts
        self.game_font = pg.font.SysFont('Impact', int(40 * settings.scale_factor))
        self.score_message_font = pg.font.SysFont('Impact', int(30 * settings.scale_factor))
        self.score_display_font = pg.font.SysFont('Impact', int(48 * settings.scale_factor))
        self.input_font = pg.font.SysFont('Arial', int(32 * settings.scale_factor))

    def resize(self, settings): 
        """update interface for new screen size if changed"""
        self.settings = settings
        self.game_font = pg.font.SysFont('Impact', int(40 * settings.scale_factor))
        self.score_message_font = pg.font.SysFont('Impact', int(30 * settings.scale_factor))
        self.score_display_font = pg.font.SysFont('Impact', int(48 * settings.scale_factor))
        self.input_font = pg.font.SysFont('Arial', int(32 * settings.scale_factor))

    def increase_score(self): self.score += 1

    def add_score_message(self, x, y): self.score_messages.append(ScoreMessage(x, y))

    def update_score_messages(self):
        """update & remove expired score messages"""
        for msg in self.score_messages[:]:
            msg.update()
            if msg.is_expired(): self.score_messages.remove(msg)

    def draw_score_messages(self, screen):
        """draw all score messages"""
        for msg in self.score_messages: msg.draw(screen, self.score_message_font)

    def draw_score(self, screen, game_state):
        """score display based on game state"""
        if game_state == 'a_game':
            # half transparent score bubble
            score_text = str(int(self.score))
            score_surface = self.score_display_font.render(score_text, True, (255, 255, 255))

            # calc dimensions for bubble
            padding = 20 * self.settings.scale_factor
            bubble_width = score_surface.get_width() + padding * 2
            bubble_height = score_surface.get_height() + padding

            # pos bubble at top center
            bubble_x = (self.settings.width - bubble_width) // 2
            bubble_y = 20 * self.settings.scale_factor

            # bubble background
            bubble_rect = pg.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
            pg.draw.rect(screen, (0, 0, 0, 128), bubble_rect, border_radius=int(bubble_height // 2))
            pg.draw.rect(screen, (255, 200, 0), bubble_rect, width=3, border_radius=int(bubble_height // 2))

            # score text
            text_x = bubble_x + (bubble_width - score_surface.get_width()) // 2
            text_y = bubble_y + (bubble_height - score_surface.get_height()) // 2
            screen.blit(score_surface, (text_x, text_y))

        elif game_state == 'game_over':
            # half transparent overlay for text visibility
            overlay = pg.Surface((self.settings.width, self.settings.height), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            # game over txt
            gameover_shadow = pg.font.SysFont('Impact', int(50 * self.settings.scale_factor)).render(
                "GAME OVER", True, (150, 0, 0))
            gameover_text = pg.font.SysFont('Impact', int(50 * self.settings.scale_factor)).render(
                "GAME OVER", True, (255, 50, 50))

            shadow_rect = gameover_shadow.get_rect(center=(self.settings.width // 2 + 5, self.settings.height // 10 + 3))        
            gameover_rect = gameover_text.get_rect(center=(self.settings.width // 2, self.settings.height // 10))

            screen.blit(gameover_shadow, shadow_rect)
            screen.blit(gameover_text, gameover_rect)

            # curr score display w/ shadow effect -- font.render
            score_text = f'Your Score: {int(self.score)}'
            score_shadow = self.game_font.render(score_text, True, (100, 0, 0))
            score_surface = self.game_font.render(score_text, True, (255, 50, 50))

            score_rect = score_surface.get_rect(center=(self.settings.width // 2, self.settings.height // 5))
            screen.blit(score_shadow, (score_rect.x + 2, score_rect.y + 2))
            screen.blit(score_surface, score_rect)

            # display max score
            top_score_txt = f'Highest Score: {int(self.high_score)}'
            top_score_shadow = self.game_font.render(top_score_txt, True, (100, 50, 0))
            top_score_surface = self.game_font.render(top_score_txt, True, (255, 165, 0))

            top_score_rect = top_score_surface.get_rect(
                center=(self.settings.width // 2, self.settings.height // 5 + score_rect.height * 1.5))
            screen.blit(top_score_shadow, (top_score_rect.x + 2, top_score_rect.y + 2))
            screen.blit(top_score_surface, top_score_rect)

            # display name input if score is high enough for leaderboard
            is_ts = self.isTopScore(self.score) # is top score
            if self.show_name_input and is_ts: self.draw_name_input(screen)

    def draw_name_input(self, screen):
        """input field for player name when game is Over and user scored at least one pt"""
        # input box bg
        input_width = 400 * self.settings.scale_factor
        input_height = 50 * self.settings.scale_factor
        input_x = (self.settings.width - input_width) // 2
        input_y = self.settings.height // 3 + 75  # positioned higher to make room for buttons below

        input_rect = pg.Rect(input_x, input_y, input_width, input_height)

        # instruct text 
        label_text = "Enter your name for the leaderboard:"
        label_surface = self.input_font.render(label_text, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(self.settings.width // 2, input_y - 25))
        screen.blit(label_surface, label_rect)

        # input box
        pg.draw.rect(screen, (50, 50, 50), input_rect)
        if self.active_input: pg.draw.rect(screen, (0, 200, 0), input_rect, 3)
        else: pg.draw.rect(screen, (100, 100, 100), input_rect, 3)

        # input txt
        input_surface = self.input_font.render(self.username, True, (255, 255, 255))
        screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

        # blinking cursor when active
        if self.active_input and int(pg.time.get_ticks() / 500) % 2 == 0:
            cursor_pos = self.input_font.size(self.username)[0]
            pg.draw.line(
                screen, (255, 255, 255),
                (input_rect.x + 10 + cursor_pos, input_rect.y+10),
                (input_rect.x + 10 + cursor_pos, input_rect.y + input_height - 10),
                2
            )

        # -------------- SUBMIT BUTTON -------------- #
        submit_width = 150 * self.settings.scale_factor
        submit_height = 40 * self.settings.scale_factor
        submit_x = (self.settings.width - submit_width) // 2
        submit_y = input_y + input_height + 20

        submit_rect = pg.Rect(submit_x, submit_y, submit_width, submit_height)

        # button rect
        pg.draw.rect(screen, (0, 150, 0), submit_rect, border_radius=int(submit_height // 4))
        pg.draw.rect(screen, (0, 200, 0), submit_rect, 3, border_radius=int(submit_height // 4))

        # button text
        submit_text = self.input_font.render("Submit", True, (255, 255, 255))
        submit_text_rect = submit_text.get_rect(center=submit_rect.center)
        screen.blit(submit_text, submit_text_rect)

        return submit_rect

    def handle_input_events(self, event):
        """handle input events for name entry"""
        if not self.show_name_input: return None

        input_width = 400 * self.settings.scale_factor
        input_height = 50 * self.settings.scale_factor
        input_x = (self.settings.width - input_width) // 2
        input_y = self.settings.height // 3 
        
        submit_width = 150 * self.settings.scale_factor
        submit_height = 40 * self.settings.scale_factor
        submit_x = (self.settings.width - submit_width) // 2
        submit_y = input_y + input_height + 20

        submit_rect = pg.Rect(submit_x, submit_y, submit_width, submit_height)
        input_rect = pg.Rect(input_x, input_y, input_width, input_height)

        if event.type == pg.MOUSEBUTTONDOWN:
            # if clicked on input box
            self.active_input = True if input_rect.collidepoint(event.pos) else False

            # submit button clicked
            if submit_rect.collidepoint(event.pos):
                self.submit_score()
                return "submitted"

        elif event.type == pg.KEYDOWN and self.active_input:
            if event.key == pg.K_RETURN:
                self.submit_score()
                return "submitted"
            elif event.key == pg.K_BACKSPACE:
                self.username = self.username[:-1]
            else:
                if len(self.username) < 15:
                    self.username += event.unicode

        return None

    def submit_score(self):
        """submit score to leaderboard & hide input"""
        if self.show_name_input and self.score > 0:
            self.add_score(self.username, self.score)
            self.show_name_input = False
            self.username = ""  # reset username for next game
            return True
        return False

    def load_leaderboard(self):
        """load leaderboard from file or create new one if file doesn't exist"""
        try:
            # make sure dir exists
            os.makedirs(os.path.dirname(self.leaderboard_file), exist_ok=True)
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, 'r') as file:
                    return json.load(file)
            else:
                # create default leaderboard
                default_leaderboard = {"scores": []}
                with open(self.leaderboard_file, 'w') as file:
                    json.dump(default_leaderboard, file)
                return default_leaderboard
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            return {"scores": []}

    def save_leaderboard(self, leaderboard):
        """saving leaderboard to file"""
        try:
            with open(self.leaderboard_file, 'w') as file:
                json.dump(leaderboard, file)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def add_score(self, name, score):
        """add a new score to leaderboard"""
        if not name.strip(): name = "Player"

        leaderboard = self.load_leaderboard()  # load current leaderboard

        if "scores" not in leaderboard: # make sure leaderboard has scores property // reason for leaderboard display problem
            leaderboard["scores"] = []

        new_entry = {
            "name": name,
            "score": score
        }

        leaderboard["scores"].append(new_entry)

        # sort by score DESCENDING order -- from highest to lowest
        leaderboard["scores"] = sorted(
            leaderboard["scores"],
            key=lambda x: x["score"],
            reverse=True
        )

        # save only top 7 scores
        if len(leaderboard["scores"]) > 7:
            leaderboard["scores"] = leaderboard["scores"][:7]

        self.save_leaderboard(leaderboard)

    def get_top_scores(self, limit=7):
        """get top scores from leaderboard"""
        leaderboard = self.load_leaderboard()
        
        # handle both structures for compatibility
        if "scores" in leaderboard:
            return leaderboard["scores"][:limit]
        elif "leaderboard" in leaderboard:
            return leaderboard["leaderboard"][:limit]
        return []

    def isTopScore(self, score):
        """check if score qualifies for leaderboard"""
        top_scores = self.get_top_scores()
        return True if len(top_scores) < 7 else (score > min([entry["score"] for entry in top_scores]))

    def update_high_score(self):
        """update max score if current score is greater"""
        if self.score > self.high_score: self.high_score = self.score

        # if qualifies for leaderboard AND its NOT ZERO -- in case leaderboard is empty
        if self.isTopScore(self.score) and self.score > 0:
            self.show_name_input = True
            self.active_input = True

    def reset_score(self):
        """reset score & score messages"""
        self.score = 0
        self.score_messages.clear()
        self.show_name_input = False
        self.username = ""
