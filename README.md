# Neuralbus Logger
## The logging component of the neuralbus project.

This code base handles logging Dublin bus data to a file to be latter processed by the main neuralbus program. This project is hosted on a Raspberry Pi Zero and uses a small LCD screen to display the live bus results to be used as a small Realtime display. This program is also an exercise in writing a standalone Python application with full unittest integration.

## Technologies Used:

#### SmartDublin RTPI API

This project uses the SmartDublin RTPI API to retrieve real time data from the two stops 3 times a minute and logs that data to a date specific file. Each day the data is then sent to a server to be processed using SSH and cron.

#### Pimoroni Display-o-tron Breakout

To display the data IRL the Display-o-tron Breakout by Pimoroni is used. This little LCD screen features 16x3 characters and has room to display up to the next 6 buses at once.

#### Raspberry Pi Zero

The project is hosted on a Raspberry Pi Zero and is set to run constantly and is housed in a custom 3D printed case with the LCD display. Cron and a small bash script keep the program running.

## Future Features:

#### LED Backlight

The LCD breakout includes some LEDs to light up the display. A custom method has been written to handle turning them off and and again but in reality the LEDs are too bright when on but also the screen is too dim when they're off. There is a method to use PWM (Pulse Width Modulation) to keep the lights dim so in a future update this will be implemented. There is no reason for the lights to be on all the time so a small LDR might be used as a light sensor to better control the brightness of the LEDs.