import unittest
import pygame as pg
import sys
import time
from unittest.mock import Mock, patch, MagicMock
import random


# game modules
sys.path.insert(0, 'code')  # src directory name
from settings import Settings
from bird import Bird
from pipes import PipeManager
from interface import UI, Button
from score_system import ScoreSystem, ScoreMessage
from game import Game


class TestBirdClass(unittest.TestCase):
    """test for the Bird class"""

    def setUp(self):
        """setup resources before each test"""
        pg.init()
        self.settings = Settings()
        self.bird = Bird(self.settings)

    def tearDown(self): pg.quit() # clean up rsrc after each test

    def test_bird_initialization(self):
        """test bird is properly initialized"""
        self.assertEqual(self.bird.velocity, 0)
        self.assertTrue(hasattr(self.bird, 'rect'))
        self.assertTrue(hasattr(self.bird, 'image'))
        self.assertTrue(hasattr(self.bird, 'bird_frames'))
        self.assertEqual(len(self.bird.bird_frames), 3)  # Should have 3 animation frames

    def test_bird_jump(self):
        """test bird jump mechanics"""
        initial_velocity = self.bird.velocity
        self.bird.jump()
        self.assertTrue(self.bird.velocity < initial_velocity)  # Velocity should decrease (negative is up)
        self.assertEqual(self.bird.velocity, -6)  # Check exact jump value

    def test_bird_gravity(self):
        """test gravity affects bird"""
        initial_y = self.bird.rect.centery
        self.bird.update()
        self.assertTrue(self.bird.rect.centery > initial_y)  # Bird should fall

    def test_flap_animation(self):
        """test bird animation frame changes"""
        initial_index = self.bird.bird_index
        self.bird.flap_animation()

        if initial_index < 2:
            self.assertEqual(self.bird.bird_index, initial_index + 1)
        else:
            self.assertEqual(self.bird.bird_index, 0)  # Should wrap around to 0

    def test_bird_reset(self):
        """test bird reset functionality"""
        # Change bird position and velocity
        self.bird.velocity = 10
        original_pos = (self.settings.width // 5, self.settings.height // 2)
        self.bird.rect.center = (100, 100)  # Move bird away from starting position

        # Reset bird
        self.bird.reset()

        # Verify reset worked
        self.assertEqual(self.bird.velocity, 0)
        self.assertEqual(self.bird.rect.center[0], original_pos[0])
        self.assertEqual(self.bird.rect.center[1], original_pos[1])

    def test_resize(self):
        """test bird correctly resizes with screen size change"""
        original_rect = self.bird.rect.copy()

        # Change settings size
        self.settings.width = 720
        self.settings.height = 1200
        self.settings.scale_factor = 1.2

        # Call resize
        self.bird.resize(self.settings)

        # Check if resized properly
        self.assertNotEqual(self.bird.rect.width, original_rect.width)
        self.assertNotEqual(self.bird.rect.height, original_rect.height)


class TestPipeManager(unittest.TestCase):
    """test suite for the PipeManager class"""

    def setUp(self):
        """Setup resources before each test"""
        pg.init()
        self.settings = Settings()
        self.pipe_manager = PipeManager(self.settings)

    def tearDown(self):
        """Clean up resources after each test"""
        pg.quit()

    def test_pipe_initialization(self):
        """test pipe manager initialization"""
        self.assertEqual(len(self.pipe_manager.pipes), 0)
        self.assertEqual(len(self.pipe_manager.passed_pipes), 0)
        self.assertTrue(hasattr(self.pipe_manager, 'pipe_image'))
        self.assertEqual(len(self.pipe_manager.pipe_heights), 3)

    def test_create_pipe_pair(self):
        """test creation of pipe pairs"""
        pipe_pair = self.pipe_manager.create_pipe_pair()
        self.assertEqual(len(pipe_pair), 2)

        bottom_pipe, top_pipe = pipe_pair
        self.assertGreater(bottom_pipe.top, top_pipe.bottom)  # Verify gap exists
        self.assertEqual(bottom_pipe.centerx, top_pipe.centerx)  # Same x position

    def test_spawn_pipe(self):
        """test spawning pipes"""
        initial_pipe_count = len(self.pipe_manager.pipes)
        self.pipe_manager.spawn_pipe()
        self.assertEqual(len(self.pipe_manager.pipes), initial_pipe_count + 2)  # Should add 2 pipes

    def test_move_pipes(self):
        """test pipes movement"""
        self.pipe_manager.spawn_pipe()

        # Get initial positions
        initial_positions = [pipe.centerx for pipe in self.pipe_manager.pipes]

        # Move pipes
        self.pipe_manager.move_pipes()

        # Check positions have decreased (moved left)
        for i, pipe in enumerate(self.pipe_manager.pipes):
            self.assertLess(pipe.centerx, initial_positions[i])

    def test_remove_offscreen_pipes(self):
        """test removal of off-screen pipes"""
        # Create pipes and manually position one off-screen
        self.pipe_manager.spawn_pipe()
        self.pipe_manager.pipes[0].centerx = -200

        # Should have 2 pipes before removal
        initial_count = len(self.pipe_manager.pipes)

        # Remove off-screen pipes
        self.pipe_manager.remove_offscreen_pipes()

        # Should have removed 1 pipe
        self.assertEqual(len(self.pipe_manager.pipes), initial_count - 1)

    def test_check_collision(self):
        """test collision detection with pipes"""
        self.pipe_manager.spawn_pipe()

        # Create a mock bird rect far from pipes (no collision)
        bird_rect = pg.Rect(0, 0, 30, 30)
        self.assertFalse(self.pipe_manager.check_collision(bird_rect))

        # Move mock bird to collide with a pipe
        for pipe in self.pipe_manager.pipes:
            bird_rect.center = pipe.center
            self.assertTrue(self.pipe_manager.check_collision(bird_rect))
            break

    def test_reset(self):
        """test resetting pipes"""
        self.pipe_manager.spawn_pipe()
        self.assertGreater(len(self.pipe_manager.pipes), 0)

        self.pipe_manager.reset()
        self.assertEqual(len(self.pipe_manager.pipes), 0)
        self.assertEqual(len(self.pipe_manager.passed_pipes), 0)


class TestScoreSystem(unittest.TestCase):
    """test suite for the ScoreSystem class"""

    def setUp(self):
        """setup resources before each test"""
        pg.init()
        self.settings = Settings()
        self.score_system = ScoreSystem(self.settings)

    def tearDown(self):
        """clean up resources after each test"""
        pg.quit()

    def test_score_initialization(self):
        """test score system initialization"""
        self.assertEqual(self.score_system.score, 0)
        self.assertEqual(self.score_system.high_score, 0)
        self.assertEqual(len(self.score_system.score_messages), 0)

    def test_increase_score(self):
        """test increasing the score"""
        initial_score = self.score_system.score
        self.score_system.increase_score()
        self.assertEqual(self.score_system.score, initial_score + 1)

    def test_add_score_message(self):
        """test adding score messages"""
        self.score_system.add_score_message(100, 100)
        self.assertEqual(len(self.score_system.score_messages), 1)
        self.assertEqual(self.score_system.score_messages[0].x, 100)
        self.assertEqual(self.score_system.score_messages[0].y, 100)

    def test_update_score_messages(self):
        """test updating score messages"""
        # add a message with low lifetime to test expiration
        self.score_system.score_messages.append(ScoreMessage(100, 100, 1))

        # update messages
        self.score_system.update_score_messages()

        # msg should have moved up (y decreased)
        self.assertEqual(self.score_system.score_messages[0].y, 99)

        # upd again should remove expired message
        self.score_system.update_score_messages()
        self.assertEqual(len(self.score_system.score_messages), 0)

    def test_update_high_score(self):
        """test updating high score"""
        self.score_system.score = 10
        self.score_system.high_score = 5
        self.score_system.update_high_score()
        self.assertEqual(self.score_system.high_score, 10)

        # test not updating if current score is lower
        self.score_system.score = 3
        self.score_system.update_high_score()
        self.assertEqual(self.score_system.high_score, 10)  # Should remain 10

    def test_reset_score(self):
        """test resetting score"""
        self.score_system.score = 10
        self.score_system.add_score_message(100, 100)

        self.score_system.reset_score()
        self.assertEqual(self.score_system.score, 0)
        self.assertEqual(len(self.score_system.score_messages), 0)


class TestInterface(unittest.TestCase):
    """test suite for the UI class"""

    def setUp(self):
        """setup rsrc before each test"""
        pg.init()
        self.settings = Settings()
        self.ui = UI(self.settings)
        # Create a test surface for rendering
        self.test_surface = pg.Surface((self.settings.width, self.settings.height))

    def tearDown(self):
        """clean up resources after each test"""
        pg.quit()

    def test_ui_initialization(self):
        """test UI initialization"""
        self.assertTrue(hasattr(self.ui, 'start_button'))
        self.assertTrue(hasattr(self.ui, 'again_button'))
        self.assertTrue(hasattr(self.ui, 'quit_button'))
        self.assertTrue(hasattr(self.ui, 'menu_button'))
        self.assertTrue(hasattr(self.ui, 'size_button'))

    def test_button_creation(self):
        """test button creation"""
        test_button = Button(100, 100, "Test", 200, 50)
        self.assertEqual(test_button.x, 100)
        self.assertEqual(test_button.y, 100)
        self.assertEqual(test_button.text, "Test")
        self.assertEqual(test_button.width, 200)
        self.assertEqual(test_button.height, 50)

    def test_resize(self):
        """test UI resizing"""
        original_start_pos = (self.ui.start_button.x, self.ui.start_button.y)
        original_again_pos = (self.ui.again_button.x, self.ui.again_button.y)

        # Change settings size
        self.settings.width = 720
        self.settings.height = 1200
        self.settings.scale_factor = 1.2

        # Resize UI
        self.ui.resize(self.settings)

        # Check buttons have been repositioned
        self.assertNotEqual(original_start_pos, (self.ui.start_button.x, self.ui.start_button.y))
        self.assertNotEqual(original_again_pos, (self.ui.again_button.x, self.ui.again_button.y))

    @patch('pygame.mouse.get_pos')
    @patch('pygame.mouse.get_pressed')
    def test_button_draw(self, mock_pressed, mock_pos):
        """test button drawing and interaction"""
        # create a test button
        test_button = Button(100, 100, "Test", 200, 50)

        # test not hovering, not clicking
        mock_pos.return_value = (0, 0)  # Mouse far from button
        mock_pressed.return_value = (0, 0, 0)  # Not clicking
        result = test_button.draw_button(self.test_surface)
        self.assertFalse(result)
        self.assertFalse(test_button.clicked)

        # test hovering, not clicking
        mock_pos.return_value = (150, 125)  # Mouse over button
        mock_pressed.return_value = (0, 0, 0)  # Not clicking
        result = test_button.draw_button(self.test_surface)
        self.assertFalse(result)
        self.assertFalse(test_button.clicked)

        # test hovering, clicking
        mock_pos.return_value = (150, 125)  # Mouse over button
        mock_pressed.return_value = (1, 0, 0)  # Left clicking
        result = test_button.draw_button(self.test_surface)
        self.assertFalse(result)
        self.assertTrue(test_button.clicked)

        # test hovering, releasing click (action triggered)
        mock_pos.return_value = (150, 125)  # Mouse over button
        mock_pressed.return_value = (0, 0, 0)  # Not clicking anymore
        result = test_button.draw_button(self.test_surface)
        self.assertTrue(result)  # Should return True (action)
        self.assertFalse(test_button.clicked)


class TestGame(unittest.TestCase):
    """test suite for the Game class"""

    def setUp(self):
        """setup resources before each test"""
        pg.init()
        self.settings = Settings()

        # Patch display.set_mode to avoid creating actual window
        self.patcher = patch('pygame.display.set_mode')
        self.mock_display = self.patcher.start()
        self.mock_display.return_value = pg.Surface((self.settings.width, self.settings.height))

        self.game = Game(self.settings)

    def tearDown(self):
        """clean up resources after each test"""
        self.patcher.stop()
        pg.quit()

    def test_game_initialization(self):
        """test game initialization"""
        self.assertFalse(self.game.game_active)
        self.assertFalse(self.game.game_paused)
        self.assertTrue(self.game.in_start_menu)
        self.assertFalse(self.game.countdown_active)

        self.assertTrue(hasattr(self.game, 'bird'))
        self.assertTrue(hasattr(self.game, 'pipe_manager'))
        self.assertTrue(hasattr(self.game, 'ui'))
        self.assertTrue(hasattr(self.game, 'score_system'))

    def test_start_countdown(self):
        """test countdown starting"""
        self.assertFalse(self.game.countdown_active)
        self.game.start_countdown()
        self.assertTrue(self.game.countdown_active)
        self.assertGreater(self.game.countdown_start_time, 0)

    def test_update_countdown(self):
        """test countdown logic"""
        # mock time.time to control countdown
        with patch('time.time') as mock_time:
            # set initial time
            start_time = 1000.0
            mock_time.return_value = start_time

            # start countdown
            self.game.start_countdown()
            self.assertTrue(self.game.countdown_active)
            self.assertEqual(self.game.countdown_start_time, start_time)

            # upd with time still in countdown
            mock_time.return_value = start_time + 1.0  # 1 second passed
            self.game.update_countdown()
            self.assertTrue(self.game.countdown_active)
            self.assertFalse(self.game.game_active)

            # upd with time after countdown finished
            mock_time.return_value = start_time + 4.0  # 4 seconds passed (> countdown_duration)
            self.game.update_countdown()
            self.assertFalse(self.game.countdown_active)
            self.assertFalse(self.game.in_start_menu)
            self.assertTrue(self.game.game_active)

    def test_check_collisions(self):
        """test collision detection in game"""
        # No collision initially
        self.assertTrue(self.game.check_collisions())

        # test floor collision
        self.game.bird.rect.bottom = self.settings.height  # Move bird to floor
        self.assertFalse(self.game.check_collisions())

        # reset bird position
        self.game.bird.reset()
        self.assertTrue(self.game.check_collisions())

        # test ceiling collision
        self.game.bird.rect.top = -150  # Move bird above ceiling
        self.assertFalse(self.game.check_collisions())

        # reset bird position
        self.game.bird.reset()

        # test pipe collision
        with patch.object(self.game.pipe_manager, 'check_collision', return_value=True):
            self.assertFalse(self.game.check_collisions())

    def test_restart_game(self):
        """test game restart functionality"""
        # set up game state
        self.game.game_active = False
        self.game.game_paused = True
        self.game.score_system.score = 10

        # call restart
        self.game.restart_game()

        # vrify game state reset
        self.assertTrue(self.game.game_active)
        self.assertFalse(self.game.game_paused)
        self.assertEqual(self.game.score_system.score, 0)

    def test_return_to_menu(self):
        """test returning to menu"""
        # set up game state
        self.game.in_start_menu = False
        self.game.game_active = True
        self.game.game_paused = True
        self.game.score_system.score = 10

        # call return to menu
        self.game.return_to_menu()

        # vrfy game state reset
        self.assertTrue(self.game.in_start_menu)
        self.assertFalse(self.game.game_active)
        self.assertFalse(self.game.game_paused)
        self.assertEqual(self.game.score_system.score, 0)

    @patch('pygame.event.get')
    def test_handle_events_pause(self, mock_event_get):
        """test handling pause event"""
        # setup game state
        self.game.game_active = True
        self.game.game_paused = False

        # simulate pressing P key
        mock_event_get.return_value = [pg.event.Event(pg.KEYDOWN, {'key': pg.K_p})]

        # handle events
        self.game.handle_events()

        # game SHOULD be paused
        self.assertTrue(self.game.game_paused)

        # simulate pressing P key again
        self.game.handle_events()

        # game should be UNPAUSED
        self.assertFalse(self.game.game_paused)

    @patch('pygame.event.get')
    def test_handle_events_space(self, mock_event_get):
        """test handling space key for jump"""
        # Setup game state
        self.game.game_active = True
        self.game.game_paused = False

        # track initial velocity
        initial_velocity = self.game.bird.velocity

        # simulate no keys pressed
        mock_event_get.return_value = []

        # mock key.get_pressed to simulate space bar
        with patch('pygame.key.get_pressed', return_value={pg.K_SPACE: True}):
            self.game.handle_events()

        # bird should have jumped (negative velocity)
        self.assertLess(self.game.bird.velocity, initial_velocity)

    def test_resize_game(self):
        """test game resizing"""
        # get init sizes
        initial_width = self.game.settings.width
        initial_height = self.game.settings.height

        # resize game
        self.game.resize_game("large")

        # check settings were updated
        self.assertNotEqual(self.game.settings.width, initial_width)
        self.assertNotEqual(self.game.settings.height, initial_height)
        self.assertEqual(self.game.settings.current_size, "large")


class TestIntegration(unittest.TestCase):
    """integration tests for game components working together"""

    def setUp(self):
        """setup resources before each test"""
        pg.init()
        self.settings = Settings()

        # Patch display.set_mode to avoid creating actual window
        self.patcher = patch('pygame.display.set_mode')
        self.mock_display = self.patcher.start()
        self.mock_display.return_value = pg.Surface((self.settings.width, self.settings.height))

        self.game = Game(self.settings)

    def tearDown(self):
        """clean up resources after each test"""
        self.patcher.stop()
        pg.quit()

    def test_scoring_mechanism(self):
        """test full scoring mechanism"""
        # prepare game state
        self.game.game_active = True
        self.game.in_start_menu = False
        self.game.pipe_manager.spawn_pipe()

        # position bird past a pipe to trigger scoring
        pipe = self.game.pipe_manager.pipes[0]  # Get first pipe (bottom pipe)
        bird_x = pipe.centerx + 10  # Position bird just past pipe

        # mock bird position for scoring
        with patch.object(self.game.bird, 'rect') as mock_rect:
            mock_rect.centerx = bird_x
            mock_rect.centery = self.settings.height // 2

            # check if score increases when bird passes pipe
            initial_score = self.game.score_system.score

            # upd game to check for scoring
            self.game.update()

            # score should have increased
            self.assertEqual(self.game.score_system.score, initial_score + 1)

            # shold have added a score message
            self.assertGreater(len(self.game.score_system.score_messages), 0)

    def test_game_over_sequence(self):
        """test game over when collision occurs"""
        # prepare game state
        self.game.game_active = True
        self.game.in_start_menu = False
        original_score = 5
        self.game.score_system.score = original_score

        # mock collision detection to force game over
        with patch.object(self.game, 'check_collisions', return_value=False):
            # upd game which should trigger game over
            self.game.update()

            # game should no longer be active
            self.assertFalse(self.game.game_active)

            # high score should be updated
            self.assertEqual(self.game.score_system.high_score, original_score)

    def test_countdown_to_game_sequence(self):
        """test full sequence from countdown to active game"""
        # start in menu
        self.assertTrue(self.game.in_start_menu)
        self.assertFalse(self.game.game_active)

        # start countdown
        self.game.start_countdown()
        self.assertTrue(self.game.countdown_active)

        # mock time passing for countdown
        with patch('time.time') as mock_time:
            # set time to after countdown finished
            mock_time.return_value = self.game.countdown_start_time + self.game.countdown_duration + 1

            # upd countdown
            self.game.update_countdown()

            # game should now be active
            self.assertFalse(self.game.in_start_menu)
            self.assertFalse(self.game.countdown_active)
            self.assertTrue(self.game.game_active)


class TestPerformance(unittest.TestCase):
    """performance tests for the game"""

    def setUp(self):
        """setup resources before each test"""
        pg.init()
        self.settings = Settings()

        # patch display.set_mode to avoid creating actual window
        self.patcher = patch('pygame.display.set_mode')
        self.mock_display = self.patcher.start()
        self.mock_display.return_value = pg.Surface((self.settings.width, self.settings.height))

        self.game = Game(self.settings)

    def tearDown(self):
        """clean up resources after each test"""
        self.patcher.stop()
        pg.quit()

    def test_fps_stability(self):
        """test frame rate stability with many pipes"""
        # setup game state
        self.game.game_active = True
        self.game.in_start_menu = False

        # add several pipes to stress test
        for _ in range(5):
            self.game.pipe_manager.spawn_pipe()

        # run multiple game updates and measure time
        frame_times = []
        for _ in range(30):  # Simulate 30 frames
            start_time = time.time()

            # update game state
            self.game.update()

            # draw (without actually rendering to screen)
            self.game.draw()

            end_time = time.time()
            frame_time = end_time - start_time
            frame_times.append(frame_time)

        # calc statistics
        avg_frame_time = sum(frame_times) / len(frame_times)
        max_frame_time = max(frame_times)

        # check if performance is acceptable
        self.assertLess(avg_frame_time, 0.1)  # avg frame should take less than 100ms
        self.assertLess(max_frame_time, 0.2)  # NOT A SINGLE FRAME should take more than 200ms

    def test_pipe_limit_enforcement(self):
        """test that pipe count is limited for performance reasons"""
        # setup game state
        self.game.game_active = True

        # add buncha pipes MORE than the limit I SAID MOOOOOOOOOOOOREEEEEEEEEEEE
        for _ in range(15): self.game.pipe_manager.spawn_pipe()

        self.assertLessEqual(len(self.game.pipe_manager.pipes), 8) # now check if pipe limit is enforced

    def test_memory_usage_stability(self):
        """test memory usage remains stable during gameplay"""
        import psutil
        import os

        process = psutil.Process(os.getpid())

        initial_memory = process.memory_info().rss # measure init memory usage

        self.game.game_active = True # run game for multiple frames with many objects
        for _ in range(10): self.game.pipe_manager.spawn_pipe()

        for _ in range(100):  # run for 100 frames
            self.game.update()
            self.game.draw()

        # measure final memory usage
        final_memory = process.memory_info().rss

        # check memory growth isn't excessive | allow for some memory growth but not unbounded
        memory_growth = final_memory - initial_memory
        max_acceptable_growth = 20 * 1024 * 1024  # 20 MB | this one is adjustable depending on sys

        self.assertLess(memory_growth, max_acceptable_growth)


# # automated Fuzz Testing
# class TestFuzz(unittest.TestCase):
#     """Fuzz testing with random inputs"""
#
#     def setUp(self):
#         """Setup resources before each test"""
#         pg.init()
#         self.settings = Settings()
#
#         # Patch display.set_mode to avoid creating actual window
#         self.patcher = patch('pygame.display.set_mode')
#         self.mock_display = self.patcher.start()
#         self.mock_display.return_value = pg.Surface((self.settings.width, self.settings.height))
#
#         self.game = Game(self.settings)
#
#     def tearDown(self):
#         """Clean up resources after each test"""
#         self.patcher.stop()
#         pg.quit()
#
#     def test_random_input_sequences(self):
#         """Test game stability with random input sequences"""
#         # Prepare game state
#         self.game.game_active = True
#         self.game.in_start_menu = False
#
#         # Run multiple frames with random inputs
#         for _ in range(100):
#             # Random space bar presses
#             with patch('pygame.key.get_pressed', return_value={pg.K_SPACE: random.choice([True, False])}):
#                 with patch('pygame.event.get', return_value=[]):
#                     try:
#                         self.game.handle_events()
#                         self.game.update()
#                         self.game.draw()
#                     except Exception as e:
#                         self.fail(f"Game crashed with random input: {e}")
#
#     def test_random_screen_resizing(self):
#         """Test game stability with random screen resizing"""
#         sizes = ["small", "medium", "large"]
#
#         # Resize screen multiple times randomly
#         for _ in range(10):
#             random_size = random.choice(sizes)
#             try:
#                 self.game.resize_game(random_size)
#                 self.game.update()
#                 self.game.draw()
#             except Exception as e:
#                 self.fail(f"Game crashed when resizing to {random_size}: {e}")