import pygame as pg
import sys
import os
from settings import Settings
from game import Game


def main():
    pg.init()     # initialize pygame

    settings = Settings() # create game settings

    os.makedirs("data", exist_ok=True) #make sure data dir exists
    
    game = Game(settings)  # create obj game and run it
    game.run()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
