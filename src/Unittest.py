import unittest
from color import ColorBGR
from vector2 import Vector2
import cv2_interface
import numpy as np
import cv2
from unittest.mock import patch, MagicMock, ANY
from text import Text
import time
from image import image
from button import Button
from fps import fps_counter


class TestColorBGR(unittest.TestCase):
    def test_color_to_tuple(self):
        self.assertEqual(ColorBGR(0, 0, 0).to_tuple(), (0, 0, 0))
        self.assertEqual(ColorBGR(255, 255, 255).to_tuple(), (255, 255, 255))
        self.assertEqual(ColorBGR(100, 100, 100).to_tuple(), (100, 100, 100))
        self.assertEqual(ColorBGR(100, 50, 200).to_tuple(), (100, 50, 200))
        self.assertEqual(ColorBGR(50, 50, 200).to_tuple(), (50, 50, 200))

class TestVector2(unittest.TestCase):
    def test_vector2_values(self):
        self.assertEqual(Vector2(1920, 1080).to_tuple(), (1920, 1080))
        self.assertEqual(Vector2(0, 0).to_tuple(), (0, 0))
        self.assertEqual(Vector2(1000, 500).to_tuple(), (1000, 500))
        self.assertEqual(Vector2(700, 200).to_tuple(), (700, 200))
        self.assertEqual(Vector2(900, 100).to_tuple(), (900, 100))

class TestDrawFunctions(unittest.TestCase):
    def setUp(self):
        self.frame = np.zeros((200, 200, 3), dtype=np.uint8)

    def test_draw_rectangle_changes_pixels(self):
        pos = Vector2(10, 10)
        size = Vector2(50, 50)
        kleur = ColorBGR(0, 255, 0)
        line_thickness = 2

        cv2_interface.draw_rectangle(self.frame, pos, size, kleur, line_thickness)

        pixel = self.frame[10, 10]
        self.assertTrue(np.array_equal(pixel, np.array([0, 255, 0])))

    def test_draw_text_changes_pixels(self):
        pos = Vector2(20, 60)
        kleur = ColorBGR(255, 255, 255)
        text = "Hallo!"
        line_thickness = 1

        cv2_interface.draw_text(self.frame, text, pos, kleur, line_thickness)

        self.assertTrue(np.any(self.frame != 0))

class TestTextAnimation(unittest.TestCase):
    def setUp(self):
        self.text = "Hallo wereld"
        self.color = ColorBGR(255, 255, 255)
        self.pos = Vector2(10, 20)
        self.text_instance = Text(self.text, self.color, self.pos, animation_duration=1)

    def test_initial_state(self):
        self.assertIsNone(self.text_instance.start_time)
        self.assertEqual(self.text_instance.animated_text, "")

    @patch("text.time")
    def test_animation_progression(self, mock_time):
        mock_time.time.side_effect = [100.0, 100.5]
        self.text_instance.animation()
        chars_expected = int(0.5 / self.text_instance.seconds_per_word)
        self.assertEqual(len(self.text_instance.animated_text), chars_expected)

    @patch("text.draw_text")
    def test_draw_calls_draw_text(self, mock_draw_text):
        self.text_instance.animated_text = "Hallo\nwereld"
        dummy_frame = MagicMock()

        self.text_instance.draw(dummy_frame)

        calls = [
            ((dummy_frame, "Hallo", ANY, self.color, 2),),
            ((dummy_frame, "wereld", ANY, self.color, 2),)
        ]
        mock_draw_text.assert_has_calls(calls, any_order=False)

    def test_line_wrapping(self):
        long_text = "Dit is een hele lange zin die automatisch moet worden afgebroken op meerdere regels."
        text_instance = Text(long_text, self.color, self.pos)
        self.assertIn("\n", "".join(text_instance.seperated_text))

class TestImage(unittest.TestCase):

    @patch("image.cv2.imread")
    @patch("image.cv2.resize")
    def test_image_loading_and_resizing(self, mock_resize, mock_imread):
        dummy_img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        mock_imread.return_value = dummy_img
        mock_resize.return_value = dummy_img

        pos = Vector2(0, 0)
        size = Vector2(50, 50)
        img_instance = image("fake_path.png", pos, size)

        mock_imread.assert_called_once_with("fake_path.png")
        mock_resize.assert_called_once_with(dummy_img, (50, 50))
        self.assertTrue((img_instance.image == dummy_img).all())

    @patch("image.cv2.imread", return_value=None)
    def test_image_load_fail(self, mock_imread):
        pos = Vector2(0, 0)
        size = Vector2(50, 50)
        img_instance = image("nonexistent.png", pos, size)
        self.assertIsNone(img_instance.image)

    def test_draw_applies_image_to_frame(self):
        dummy_img = np.full((10, 10, 3), [0, 0, 255], dtype=np.uint8)
        pos = Vector2(5, 5)
        size = Vector2(10, 10)

        img_instance = image.__new__(image)
        img_instance.pos = pos
        img_instance.size = size
        img_instance.image = dummy_img

        frame = np.zeros((20, 20, 3), dtype=np.uint8)
        img_instance.draw(frame)

        region = frame[5:15, 5:15]
        self.assertTrue((region == [0, 0, 255]).all())

class TestButton(unittest.TestCase):

    @patch("button.time.time")
    @patch("button.draw_rectangle")
    @patch("button.draw_text")
    def test_button_hover_and_click(self, mock_draw_text, mock_draw_rectangle, mock_time):
        mock_time.side_effect = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0]
        
        pos = Vector2(10, 10)
        size = Vector2(100, 50)
        text_color = ColorBGR(255, 255, 255)
        color = ColorBGR(0, 255, 0)
        hover_color = ColorBGR(255, 0, 0)
        action = MagicMock()
        button = Button("Click me!", text_color, pos, size, color, hover_color, action)

        button.button_handler(MagicMock(), 200, 200)
        button.hover_time_handler()

        button.button_handler(MagicMock(), 200, 200)
        button.button_cooldown_handler()
        button.button_handler(MagicMock(), 200, 200)

        action.assert_called_once()

        self.assertEqual(button.display_text, "Click me!")

        button.button_handler(MagicMock(), 200, 200)
        button.hover_time_handler()
        self.assertEqual(button.display_text, "Click me!")

    @patch("button.time.time")
    def test_button_no_hover(self, mock_time):
        mock_time.side_effect = [100.0, 100.5, 101.0]
        
        pos = Vector2(10, 10)
        size = Vector2(100, 50)
        text_color = ColorBGR(255, 255, 255)
        color = ColorBGR(0, 255, 0)
        hover_color = ColorBGR(255, 0, 0)
        button = Button("Click me!", text_color, pos, size, color, hover_color)

        button.button_handler(MagicMock(), 200, 200)
        self.assertEqual(button.color.to_tuple(), color.to_tuple())
        self.assertEqual(button.display_text, "Click me!")

class TestFpsCounter(unittest.TestCase):

    def setUp(self):
        self.fps_counter = fps_counter(offset=0)
        self.mock_frame = np.zeros((200, 200, 3), dtype=np.uint8)
        time.sleep(1)

    def test_initial_fps(self):
        self.fps_counter.calculate_fps()
        self.assertGreater(self.fps_counter.fps_display, 0)

    def test_rolling_average_fps(self):
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        self.assertGreater(self.fps_counter.fps_display, 0)
        self.assertLess(abs(self.fps_counter.fps_display - 4), 1)

    def test_window_size_behavior(self):
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        time.sleep(0.2)
        self.fps_counter.calculate_fps()
        self.assertEqual(len(self.fps_counter.fps_dict) - 1, 5)
        self.fps_counter.calculate_fps()
        self.assertEqual(len(self.fps_counter.fps_dict) - 1, 5)

    def test_draw_fps(self):
        self.fps_counter.calculate_fps()
        self.fps_counter.draw_fps(self.mock_frame, "Test")
        self.assertTrue(np.any(self.mock_frame != 0))

    @patch("time.time", return_value=100.0)
    def test_fps_zero_division(self, mock_time):
        self.fps_counter.calculate_fps()
        self.fps_counter.calculate_fps()
        self.assertAlmostEqual(self.fps_counter.fps_display, 0, delta=1e-5)

unittest.main(verbosity=2)