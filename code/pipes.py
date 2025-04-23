import pygame as pg
import random

class PipeManager:
    def __init__(self, settings):
        self.settings = settings

        # pipe lists -- pipes and passed ones
        self.pipes = []
        self.passed_pipes = []

        # load images
        self.load_pipe_image()

        # calc pipe heights based on screen.size
        self.pipe_heights = [
            settings.height * 0.6,
            settings.height * 0.5,
            settings.height * 0.7
        ]

    def load_pipe_image(self):
        """laod & SCALE pipe img"""
        self.pipe_image = pg.image.load("assets/img/pipe.png").convert_alpha()
        self.pipe_image.set_colorkey(self.settings.WHITE)
        self.pipe_image = pg.transform.scale2x(self.pipe_image)

    def resize(self, settings):
        """update pipe manager if new Screen Size selected"""
        self.settings = settings

        self.load_pipe_image() # Reload Pipe Image

        # heights updated
        self.pipe_heights = [
            settings.height * 0.6,
            settings.height * 0.5,
            settings.height * 0.7
        ]

    def spawn_pipe(self): # generate new pair of pipes - later to make em top and bottom
        self.pipes.extend(self.create_pipe_pair())

    def create_pipe_pair(self):
        """create pair of top & bottom pipes"""
        random_pipe_pos = random.choice(self.pipe_heights)
        pipe_gap = self.settings.height // 3  # gap between pipes scales with screen height

        # scale pipe size based on screen size
        pipe_scaled = pg.transform.scale(
            self.pipe_image,
            (
                int(self.pipe_image.get_width() * self.settings.width / self.settings.SCREEN_SIZES["medium"][0]),
                int(self.pipe_image.get_height() * self.settings.height / self.settings.SCREEN_SIZES["medium"][1])
            )
        )

        bottom_pipe = pipe_scaled.get_rect(midtop=(self.settings.width + 100, random_pipe_pos))
        top_pipe = pipe_scaled.get_rect(midbottom=(self.settings.width + 100, random_pipe_pos - pipe_gap))

        return bottom_pipe, top_pipe

    def update(self):
        """update pipe pos & remove off-screen pipes"""
        self.move_pipes(); self.remove_offscreen_pipes()

    def move_pipes(self):
        """moving pipes from right to left -- towards the bird (player)"""
        speed_factor = self.settings.scale_factor
        for pipe in self.pipes: pipe.centerx -= 5 * speed_factor

        # limit the number of pipes for better performance // fixing the bugs
        if len(self.pipes) > 8:
            self.pipes = self.pipes[-8:]

    def remove_offscreen_pipes(self):
        """remove pipes that have moved off screen // fixing the problem of game slowing down due to 'overflow' of pipes in the array"""
        pipes_copy = self.pipes.copy()
        for pipe in pipes_copy:
            if pipe.centerx <= -100: # fixed from <100 to <=
                self.pipes.remove(pipe)
                if pipe in self.passed_pipes: self.passed_pipes.remove(pipe)

    def check_score(self, bird_x):
        """check if bird passed a pipe to score a point"""
        for pipe in self.pipes:
            if pipe.centerx < bird_x and pipe not in self.passed_pipes and pipe.bottom >= self.settings.height:
                self.passed_pipes.append(pipe)
                return True
        return False

    def check_collision(self, bird_rect):
        """check if bird collided with any pipe"""
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe): return True
        return False

    def draw(self, screen):
        """draw all pipes"""
        for pipe in self.pipes:
            if pipe.bottom >= self.settings.height: # bottom pipe
                screen.blit(pg.transform.scale(self.pipe_image, (pipe.width, pipe.height)), pipe)
            else: # top -- flipped image
                flip_pipe = pg.transform.flip(
                    pg.transform.scale(self.pipe_image, (pipe.width, pipe.height)),
                    False, True
                )
                screen.blit(flip_pipe, pipe)

    def reset(self):
        """clear all pipes"""
        self.pipes.clear()
        self.passed_pipes.clear()
