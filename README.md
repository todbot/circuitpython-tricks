
# circuitpython-tricks


## Common Tasks

* Read a Input as a Button
```py
import board
from digitalio import DigitalInOut, Pull
button = DigitalInOut(pin_switch) # defaults to input
button.pull = Pull.UP # turn on internal pull-up resistor
print(button.value)  # False == pressed
```

* Read a Potentiometer 
```py
import board
import analogio
potknob = analogio.AnalogIn(board.A1)
position = potknob.value  # ranges from 0-65535
pos = potknob.value // 256  # make 0-255 range
```

* Read a Touch Pin / Capsense
```py
import touchio
import board
touch_pin = touchio.TouchIn(board.GP6)
# on Pico / RP2040, need 1M pull-down on each input
```


* Read a Rotary Encoder
```py
import board
import rotaryio
encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1) # must be consecutive on Pico
print(encoder.position)  # starts at zero, goes neg or pos
```

* Print to USB Serial
```py
print("hello there")  # prints a newline
print("waiting...", end='')   # does not print newline
```

* Read user input from USB Serial, non-blocking
```py

```

## More Esoteric Tasks

* Determine which board you're on:
```py
import os
print(os.uname().machine)
'Adafruit ItsyBitsy M4 Express with samd51g19'
```



* Detect if USB is connected or not
```py
def is_usb_connected():
    import storage
    try:
        storage.remount('/', readonly=False)  # attempt to mount readwrite
        storage.remount('/', readonly=True)  # attempt to mount readonly
    except RuntimeError as e:
        return True
    return False

    is_usb = "USB" if is_usb_connected() else "NO USB"
    print("USB:", is_usb)
```
* Read keys from USB Serial


* RasPI boot.py protection.
```
# Copy this as 'boot.py' in your Pico's CIRCUITPY drive
# from https://gist.github.com/Neradoc/8056725be1c209475fd09ffc37c9fad4
# Useful in case Pico locks up (which it's done a few times on me)
#
import board
import time
from digitalio import DigitalInOut,Pull

import time
led = DigitalInOut(board.LED)
led.switch_to_output()

safe = DigitalInOut(board.GP14)
safe.switch_to_input(Pull.UP)

def reset_on_pin():
	if safe.value is False:
		import microcontroller
		microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
		microcontroller.reset()

led.value = False
for x in range(16):
	reset_on_pin()
	led.value = not led.value
	time.sleep(0.1)

```
