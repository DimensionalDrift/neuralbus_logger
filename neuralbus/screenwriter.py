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


    def write(self, text=None, line=1, cursor=0, truncate=True):
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
        """
        # Force the text to be a string
        text = str(text)

        # If the truncate flag is set and the length of the text is
        # longer than 16 characters then cut it down to size
        if len(text) > 16 and truncate:
            text = text[:16]

        lcd.set_cursor_position(cursor, line)
        lcd.write(text)

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
