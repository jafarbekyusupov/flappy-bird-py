import pygame as pg

class Settings:
    def __init__(self):

        # dynamic sizing
        display_info = pg.display.Info()
        self.width = 600
        self.height = display_info.current_h - 85
        
        # screen sizes configurations / options
        self.SCREEN_SIZES = {
            "small": (480, 720),
            "medium": (600, display_info.current_h - 85),
            "large": (720, 1200)
        }

        # initial default screen size -- medium
        self.current_size = "medium"

        # game constants / settings
        self.FPS = 80
        self.speed = 5
        self.gravity = 0.25
        self.pipe_spawn_time = 1300  # ms
        self.bird_flap_time = 200  # ms
        self.double_click_interval = 0.4  # seconds

        # colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.ORANGE = (255, 165, 0)

        # events
        self.SPAWNPIPE = pg.USEREVENT
        self.BIRDFLAP = pg.USEREVENT + 1

        # scale factor
        self.scale_factor = self.width / self.SCREEN_SIZES["medium"][0]

    def update_screen_size(self, size):
        """update settings when Screen Size changes"""
        if size in self.SCREEN_SIZES:
            self.current_size = size
            self.width, self.height = self.SCREEN_SIZES[size]
            self.scale_factor = self.width / self.SCREEN_SIZES["medium"][0]
            return True
        return False
