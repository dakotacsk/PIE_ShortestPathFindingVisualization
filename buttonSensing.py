import RPi.GPIO as GPIO
import time

# Set up the GPIO mode to BCM (Broadcom pin numbering)
GPIO.setmode(GPIO.BCM)

# List of GPIO pins to which the buttons are connected
button_pins = [17, 27, 22, 5, 6, 13, 23]

# Set up each GPIO pin as an input with pull-up resistor enabled
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        for pin in button_pins:
            button_state = GPIO.input(pin)
            if button_state == GPIO.HIGH:
                print(f"Button on GPIO {pin} is pressed!")
            else:
                print(f"Button on GPIO {pin} is not pressed.")
        
        time.sleep(0.5)  # Check every 0.5 seconds

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Clean up the GPIO settings when the program exits
