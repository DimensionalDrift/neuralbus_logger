import dot3k.lcd as lcd
import RPi.GPIO as GPIO
import time


class screenwriter(object):
    """
    Wrapper for the Pimironi screen library used to write text to the LCD screen

    The screen should be wired to the pi as such:
        VCC -> 5V
        GND -> GND
        RST -> BCM 12
        RS -> BCM 25
        CS -> BCM 8
        SCLK -> BCM 11
        MOSI -> BCM 10
        R -> BCM 5
        G -> BCM 6
        B -> BCM 13
    """

    def __init__(self):

        # Clear the screen and set the contrast
        lcd.clear()
        lcd.set_contrast(20)  # Tested a bunch of contrasts 20 seems the best

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        # GPIO.cleanup()
        # It is good practice to clean up the GPIO after use to protect
        # the pins but since they are used later in the code cleaning up
        # now causes issues. Look into ways to clean up the gpio when
        # closing or ending the final script

    def write(self, text=None, line=1, cursor=0, truncate=True, center=False):
        """
        Function to write text to the LCD Screen.

        Parameters
        ----------
        text : str
            String to be written to the screen.
        line : int, optional
            Line number to write to (default: 1)
        cursor : int, optional
            The cursor position to start at (default: 0)
        truncate : bool, optional
            Boolean flag to indicate whether to truncate the line or not
            (default: True)
        center : bool, optional
            Boolean flag to indicate whether to center the line or not
            (default: False)
        """
        # Force the text to be a string
        # [X] I couldn't find a way to test this variable without making it
        # a variable of the class, look into a way to not have to do
        # this as it's not necessary
        self.text = str(text)

        # If the truncate flag is set and the length of the text is
        # longer than 16 characters then cut it down to size
        if len(self.text) > 16 and truncate:
            self.text = self.text[:16]

        if center:
            self.text = self.text.center(16)

        lcd.set_cursor_position(cursor, line)
        lcd.write(self.text)

    def lights(self, state):
        """
        Function to set the light state.

        Parameters
        ----------
        state : bool
            The state of the light, true for on false for off.
        """
        if state:
            GPIO.setmode(GPIO.BCM)
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(6, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(6, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
        # GPIO.cleanup()
