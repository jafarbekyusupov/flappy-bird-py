import pygame as pg

class Bird:
    def __init__(self, settings):
        self.settings = settings
        self.velocity = 0

        # original screen size for scaling
        self.original_width = settings.SCREEN_SIZES["medium"][0]
        self.original_height = settings.SCREEN_SIZES["medium"][1]

        # bird frames
        self.load_frames()

        # animation
        self.bird_index = 0
        self.image = self.bird_frames[self.bird_index]
        self.rect = self.image.get_rect(center=(settings.width // 5, settings.height // 2))

    def load_frames(self):
        """load & scale bird animation frames"""
        # bird images -- sprites for 3 states -- UPFLAP | MIDFLAP | DOWNFLAP -- for animation
        bird_downflap_original = pg.transform.scale2x(pg.image.load('assets/img/bird-sprites/bird-downflap.png').convert_alpha())
        bird_midflap_original = pg.transform.scale2x(pg.image.load('assets/img/bird-sprites/bird-midflap.png').convert_alpha())
        bird_upflap_original = pg.transform.scale2x(pg.image.load('assets/img/bird-sprites/bird-upflap.png').convert_alpha())

        # scale based on screen size
        scale_factor = self.settings.width / self.original_width

        # get original dimensions to maintain aspect ratio
        original_width = bird_midflap_original.get_width()
        original_height = bird_midflap_original.get_height()

        # calculate new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # scale each frame
        self.bird_frames = [
            pg.transform.scale(bird_downflap_original, (new_width, new_height)),
            pg.transform.scale(bird_midflap_original, (new_width, new_height)),
            pg.transform.scale(bird_upflap_original, (new_width, new_height))
        ]

    def resize(self, settings):
        """update bird for new screen size"""
        self.settings = settings

        # store relative position before resizing
        rel_y_position = self.rect.centery / self.settings.height

        # reload and rescale frames
        self.load_frames()

        # update bird image
        self.image = self.bird_frames[self.bird_index]

        # update position while keeping relative position on screen
        self.rect = self.image.get_rect(center=(
            settings.width // 5,
            int(rel_y_position * settings.height)
        ))

    def update(self):
        """update bird position & rotation"""
        self.velocity += self.settings.gravity
        self.rect.centery += self.velocity

    def jump(self):
        self.velocity = 0
        self.velocity -= 6

    def flap_animation(self):
        """update bird flap animation frame"""
        self.bird_index = self.bird_index + 1 if self.bird_index<2 else 0

        center = self.rect.center

        self.image = self.bird_frames[self.bird_index] # update the bird image  -- switch between sprites to create animation of movement

        self.rect = self.image.get_rect(center=center) # restore center position

    def rotate_bird(self):
        """bird rotation depending on velocity"""
        rotated_bird = pg.transform.rotozoom(self.image, -self.velocity * 3, 1)
        return rotated_bird

    def draw(self, screen):
        """draw bird on screen"""
        rotated_bird = self.rotate_bird()
        screen.blit(rotated_bird, self.rect)

    def reset(self):
        """reset bird to default position"""
        self.velocity = 0
        self.rect.center = (self.settings.width // 5, self.settings.height // 2)
