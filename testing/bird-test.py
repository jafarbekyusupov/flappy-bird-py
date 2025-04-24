import unittest
import sys
import os

import pygame as pg

# add code dir to path
sys.path.insert(0, os.path.abspath('code'))

from settings import Settings
from bird import Bird
from pipes import PipeManager
from score_system import ScoreSystem

pg.init()

class TestSettings(unittest.TestCase):
    # test settings stuff
    def setUp(self):
        self.settings = Settings()

    def test_default_screen_size(self):
        # check default size
        self.assertEqual(self.settings.current_size, "medium")
        self.assertEqual(self.settings.width, 600)

    def test_update_screen_size(self):
        # switch to small
        result = self.settings.update_screen_size("small")
        self.assertTrue(result)
        self.assertEqual(self.settings.current_size, "small")
        self.assertEqual(self.settings.width, 480)

        # switch to large
        result = self.settings.update_screen_size("large")
        self.assertTrue(result)
        self.assertEqual(self.settings.current_size, "large")
        self.assertEqual(self.settings.width, 720)

        # throw invalid size
        result = self.settings.update_screen_size("invalid_size")
        self.assertFalse(result)


class TestBird(unittest.TestCase):
    # test bird stuff
    def setUp(self):
        self.settings = Settings()
        self.bird = Bird(self.settings)

    def test_bird_jump(self):
        # test jump sets velocity up
        initial_velocity = self.bird.velocity
        self.bird.jump()
        self.assertLess(self.bird.velocity, initial_velocity)
        self.assertEqual(self.bird.velocity, -6)

    def test_bird_update(self):
        # check y and velocity go up after gravity
        initial_y = self.bird.rect.centery
        self.bird.update()
        self.assertGreater(self.bird.rect.centery, initial_y)
        self.assertGreater(self.bird.velocity, 0)

    def test_bird_reset(self):
        # move bird, then reset it
        self.bird.velocity = 10
        self.bird.update()
        self.bird.reset()
        self.assertEqual(self.bird.velocity, 0)
        self.assertEqual(self.bird.rect.center, (self.settings.width // 5, self.settings.height // 2))


class TestPipeManager(unittest.TestCase):
    # test pipes
    def setUp(self):
        self.settings = Settings()
        self.pipe_manager = PipeManager(self.settings)

    def test_create_pipe_pair(self):
        # spawn pipes, check spots
        bottom_pipe, top_pipe = self.pipe_manager.create_pipe_pair()
        self.assertEqual(bottom_pipe.centerx, self.settings.width + 100)
        self.assertEqual(top_pipe.centerx, self.settings.width + 100)
        self.assertLess(top_pipe.bottom, bottom_pipe.top)

    def test_move_pipes(self):
        # add pipe then move it
        self.pipe_manager.spawn_pipe()
        initial_x = self.pipe_manager.pipes[0].centerx
        self.pipe_manager.move_pipes()
        self.assertLess(self.pipe_manager.pipes[0].centerx, initial_x)

    def test_pipes_limit(self):
        # add a bunch, check limit
        for _ in range(10):
            self.pipe_manager.spawn_pipe()
        self.assertLessEqual(len(self.pipe_manager.pipes), 8)

    def test_reset_pipes(self):
        # spawn then reset pipes
        self.pipe_manager.spawn_pipe()
        self.assertTrue(len(self.pipe_manager.pipes) > 0)
        self.pipe_manager.reset()
        self.assertEqual(len(self.pipe_manager.pipes), 0)
        self.assertEqual(len(self.pipe_manager.passed_pipes), 0)


class TestScoreSystem(unittest.TestCase):
    # test score stuff
    def setUp(self):
        self.settings = Settings()
        self.score_system = ScoreSystem(self.settings)
        self.test_leaderboard_file = "test_leaderboard.json"
        self.score_system.leaderboard_file = self.test_leaderboard_file

    def tearDown(self):
        # nuke test file
        if os.path.exists(self.test_leaderboard_file):
            os.remove(self.test_leaderboard_file)

    def test_increase_score(self):
        # score goes up
        initial_score = self.score_system.score
        self.score_system.increase_score()
        self.assertEqual(self.score_system.score, initial_score + 1)

    def test_update_high_score(self):
        # new high score gets set
        self.score_system.high_score = 5
        self.score_system.score = 10
        self.score_system.update_high_score()
        self.assertEqual(self.score_system.high_score, 10)
        self.assertTrue(self.score_system.show_name_input)

    def test_add_score_to_leaderboard(self):
        # save a score -->> check
        self.score_system.add_score("TestPlayer", 42)
        leaderboard = self.score_system.load_leaderboard()
        self.assertTrue("scores" in leaderboard)
        self.assertEqual(len(leaderboard["scores"]), 1)
        self.assertEqual(leaderboard["scores"][0]["name"], "TestPlayer")
        self.assertEqual(leaderboard["scores"][0]["score"], 42)

    def test_leaderboard_sorting(self):
        # add scores in rand order
        self.score_system.add_score("Player3", 30)
        self.score_system.add_score("Player1", 10)
        self.score_system.add_score("Player2", 20)
        top_scores = self.score_system.get_top_scores()
        self.assertEqual(len(top_scores), 3)
        self.assertEqual(top_scores[0]["name"], "Player3")
        self.assertEqual(top_scores[1]["name"], "Player2")
        self.assertEqual(top_scores[2]["name"], "Player1")

    def test_leaderboard_limit(self):
        # add too many ==>> check top 7 kept
        for i in range(10):
            self.score_system.add_score(f"Player{i}", i)
        top_scores = self.score_system.get_top_scores()
        self.assertEqual(len(top_scores), 7)
        self.assertEqual(top_scores[0]["score"], 9)
        self.assertEqual(top_scores[6]["score"], 3)


if __name__ == "__main__":
    unittest.main()
