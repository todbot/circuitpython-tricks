
# circuitpython-tricks

This is a small list of tips and tricks I find myself
needing when working with CircuitPython


## Common Tasks

### Inputs

#### Read an digital input as a Button
  ```py
  import board
  from digitalio import DigitalInOut, Pull
  button = DigitalInOut(board.D3) # defaults to input
  button.pull = Pull.UP # turn on internal pull-up resistor
  print(button.value)  # False == pressed
  ```

#### Read a Potentiometer 
  ```py
  import board
  import analogio
  potknob = analogio.AnalogIn(board.A1)
  position = potknob.value  # ranges from 0-65535
  pos = potknob.value // 256  # make 0-255 range
  ```

#### Read a Touch Pin / Capsense
  ```py
  import touchio
  import board
  touch_pin = touchio.TouchIn(board.GP6)
  # on Pico / RP2040, need 1M pull-down on each input
  if touch_pin.value: 
    print("touched!")
  ```

#### Read a Rotary Encoder
  ```py
  import board
  import rotaryio
  encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1) # must be consecutive on Pico
  print(encoder.position)  # starts at zero, goes neg or pos
  ```

#### Debounce a pin / button 
(using `adafruit_debouncer` library)
  ```py
  import board
  from digitalio import DigitalInOut, Pull
  from adafruit_debouncer import Debouncer
  button_pin = DigitalInOut(board.D3) # defaults to input
  button_pin.pull = Pull.UP # turn on internal pull-up resistor
  button = Debouncer(button_pin)
  while True:
    button.update()
    if button.fell:
      print("press!")
    if button.rose:
      print("release!")
  ```

### Outputs

#### Output HIGH / LOW on a pin (like an LED)
  ```py
  import board
  import digitalio
  ledpin = digitalio.DigitalInOut(board.D2)
  ledpin.direction = digitalio.Direction.OUTPUT
  ledpin.value = True
  ```

#### Output Analog value on a DAC pin
  ```py
  import board
  import analogio
  dac = analogio.AnalogOut(board.D1)
  dac.value = 32768   # mid-point of 0-65535
  ```

#### Output a "Analog" value on a PWM pin
  ```py
  import board
  import pwmio
  out1 = pwmio.PWMOut(board.MOSI, frequency=25000, duty_cycle=0)
  out1.out1.duty_cycle = 32768  # mid-point 0-65535 = 50 % duty-cycle
  ```

#### Drive Neopixel / WS2812 LEDs
  ```py
  import neopixel
  led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
  led[0] = 0xff00ff
  led[0] = (255,0,255)  # equivalent

  ```

----

### USB

#### Print to USB Serial
  ```py
  print("hello there")  # prints a newline
  print("waiting...", end='')   # does not print newline
  ```

#### Read user input from USB Serial, blocking
  ```py
  while True:
    print("Type something: ", end='')
    my_str = input()  # type and press ENTER or RETURN
    print("You entered: ", my_str)
  ```

#### Read user input from USB Serial, non-blocking (mostly)
  ```py
  import time
  import supervisor
  print("Type something when you're ready")
  last_time = time.monotonic()
  while True:
    if supervisor.runtime.serial_bytes_available:
      my_str = input()
      print("You entered:", my_str)
    if time.monotonic() - last_time > 1:  # every second, print
      last_time = time.monotonic()
      print(int(last_time),"waiting...")
  ```

----

### Computery Tasks

#### Formatting strings
  ```py
  name = "John"
  fav_color = 0xff3366
  body_temp = 98.65
  print("name:%s color:%6x thermometer:%2.1f" % (name,fav_color,body_temp))
  'name:John color:ff3366 thermometer:98.6'
  ```

#### Make and Use a config file
  ```py
  # my_config.py
  config = {
    "username": "Grogu Djarin",
    "password": "ig88rules",
    "secret_key": "3a3d9bfaf05835df69713c470427fe35"
  }
  # code.py
  from my_config import config
  print("secret:", config['secret_key'])
  'secret: 3a3d9bfaf05835df69713c470427fe35'
  ```
----

### More Esoteric Tasks

#### Map an input range to an output range:
  ```py
  # simple range mapper, like Arduino map()
  def map_range(s, a, b):
      (a1, a2), (b1, b2) = a, b
      return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
  # map 0-0123 value to 0.0-1.0 value
  out = map_range( in, (0,1023), (0.0,1.0) )
  ```

#### Time how long something takes:
  ```py
  import time
  start_time = time.monotonic() # fraction seconds uptime
  do_something()
  elapsed_time = time.monotonic() - start_time
  print("do_something took %f seconds" % elapsed_time)
  ```

#### Determine which board you're on:
  ```py
  import os
  print(os.uname().machine)
  'Adafruit ItsyBitsy M4 Express with samd51g19'
  ```

#### Support multiple boards with one `code.py`:
  ```py
  import os
  board_type = os.uname().machine
  if 'QT Py M0' in board_type:
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
  elif 'ItsyBitsy M4' in board_type:
    tft_clk  = board.SCK
    tft_mosi = board.MOSI
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
  elif 'Pico' in board_type:
    tft_clk = board.GP10 # must be a SPI CLK
    tft_mosi= board.GP11 # must be a SPI TX
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
  else:
    print("supported board", board_type)
  ```

#### Detect if USB is connected or not
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
    
#### Read keys from USB Serial
  ```py

  ```

#### RasPI boot.py Protection
  ```py
  # Copy this as 'boot.py' in your Pico's CIRCUITPY drive
  # from https://gist.github.com/Neradoc/8056725be1c209475fd09ffc37c9fad4
  # Useful in case Pico locks up (which it's done a few times on me)
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

----

### Hacks

#### Use REPL fast with copy-paste multi-one-liners:

(yes, semicolons are legal in Python)

```py
# load most common libraries
import time; import board; from digitalio import DigitalInOut,Pull; import analogio; import touchio

# print out board pins and objects (like 'I2C' and 'display'
import board; dir(board)

# print out microcontroller pins (chip pins, not the same as board pins)
import microcontroller; dir(microcontroller.pin)

# release configured / built-in display
import displayio; displayio.release_displays()

```
