import unittest
import time
from neuralbus import screenwriter


class TestScreenWriter(unittest.TestCase):
    """
    Test methods to test that both the hardware and software are working
    to operate the LCD screen
    """

    def setUp(self):
        self.scr = screenwriter.screenwriter()

    def test_trunc_message_length(self):
        """
        Method to test that a message is truncated by default before
        being written to the screen.
        """

        # make a string over 16 characters long
        message = "test" * 5

        # Write a message to the screen
        # [X] I think this might be the wrong way to import a class... It
        # shouldn't have to actually write to the screen
        self.scr.write(message)

        # Assert that the message text is less than 16 characters when
        # truncated
        self.assertEqual(len(self.scr.text), 16)
        time.sleep(3)

    def test_message_length(self):
        """
        Method to test that a message is not truncated when the flag is
        set to false.
        """

        # make a string over 16 characters long
        message = "test" * 5

        # Write a message to the screen
        self.scr.write(message, truncate=False)

        # Assert that the message text is less than 16 characters when
        self.assertNotEqual(len(self.scr.text), 16)
        time.sleep(3)

    def test_lights(self):
        """
        Method to check that the light are working by blinking them off
        and on.
        """

        # Initialize the screen and blink the lights on and off

        for i in range(3):
            self.scr.lights(True)
            time.sleep(0.5)
            self.scr.lights(False)
            time.sleep(0.5)

    def test_screen(self):
        """
        Method to check that the screen actually works and prints a message.
        """

        # Initialize the screen and write some lines
        # Included in these lines are some characters that should not be
        # displayed
        self.scr.write("Check Check.....Nope", line=0)
        self.scr.write("1,2... 1,2......Nope", line=1)
        self.scr.write("Lines are clear.Nope", line=2)

        time.sleep(3)
