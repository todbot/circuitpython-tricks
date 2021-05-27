
# circuitpython-tricks

A small list of tips & tricks I find myself needing when working with CircuitPython

## Table of Contents
* [Inputs](#inputs)
   * [Read an digital input as a Button](#read-an-digital-input-as-a-button)
   * [Read a Potentiometer](#read-a-potentiometer)
   * [Read a Touch Pin / Capsense](#read-a-touch-pin--capsense)
   * [Read a Rotary Encoder](#read-a-rotary-encoder)
   * [Debounce a pin / button](#debounce-a-pin--button)
   * [Set up and debounce a list of pins](#set-up-and-debounce-a-list-of-pins)
* [Outputs](#outputs)
   * [Output HIGH / LOW on a pin (like an LED)](#output-high--low-on-a-pin-like-an-led)
   * [Output Analog value on a DAC pin](#output-analog-value-on-a-dac-pin)
   * [Output a "Analog" value on a PWM pin](#output-a-analog-value-on-a-pwm-pin)
   * [Control Neopixel / WS2812 LEDs](#control-neopixel--ws2812-leds)
* [Neopixels / Dotstars](#neopixels--dotstars)
   * [Make moving rainbow gradient across LED strip](#make-moving-rainbow-gradient-across-led-strip)
   * [Fade all LEDs by amount for chase effects](#fade-all-leds-by-amount-for-chase-effects)
* [USB](#usb)
   * [Detect if USB is connected or not](#detect-if-usb-is-connected-or-not)
   * [Get CIRCUITPY disk size and free space](#get-circuitpy-disk-size-and-free-space)
   * [Programmatically reset to UF2 bootloader](#programmatically-reset-to-uf2-bootloader)
* [USB Serial](#usb-serial)
   * [Print to USB Serial](#print-to-usb-serial)
   * [Read user input from USB Serial, blocking](#read-user-input-from-usb-serial-blocking)
   * [Read user input from USB Serial, non-blocking (mostly)](#read-user-input-from-usb-serial-non-blocking-mostly)
   * [Read keys from USB Serial](#read-keys-from-usb-serial)
* [Computery Tasks](#computery-tasks)
   * [Formatting strings](#formatting-strings)
   * [Formatting strings with f-strings](#formatting-strings-with-f-strings)
   * [Make and Use a config file](#make-and-use-a-config-file)
* [More Esoteric Tasks](#more-esoteric-tasks)
   * [Map an input range to an output range](#map-an-input-range-to-an-output-range)
   * [Time how long something takes](#time-how-long-something-takes)
   * [Preventing Ctrl-C from stopping the program](#preventing-ctrl-c-from-stopping-the-program)
   * [Raspberry Pi Pico boot.py Protection](#raspberry-pi-pico-bootpy-protection)
* [Networking](#networking)
   * [Scan for WiFi Networks, sorted by signal strength (ESP32-S2)](#scan-for-wifi-networks-sorted-by-signal-strength-esp32-s2)
   * [Ping an IP address (ESP32-S2)](#ping-an-ip-address-esp32-s2)
   * [Fetch a JSON file (ESP32-S2)](#fetch-a-json-file-esp32-s2)
   * [What the heck is secrets.py?](#what-the-heck-is-secretspy)
* [I2C](#i2c)
   * [Scan I2C bus for devices](#scan-i2c-bus-for-devices)
* [Board Info](#board-info)
   * [Display amount of free RAM](#display-amount-of-free-ram)
   * [Show microcontroller.pin to board mappings](#show-microcontrollerpin-to-board-mappings)
   * [Determine which board you're on](#determine-which-board-youre-on)
   * [Support multiple boards with one code.py](#support-multiple-boards-with-one-codepy)
* [Hacks](#hacks)
   * [Using the REPL](#using-the-repl)
      * [Display built-in modules / libraries](#display-built-in-modules--libraries)
      * [Use REPL fast with copy-paste multi-one-liners](#use-repl-fast-with-copy-paste-multi-one-liners)
* [Python info](#python-info)
   * [Display which (not built-in) libraries have been imported](#display-which-not-built-in-libraries-have-been-imported)
   * [List names of all global variables](#list-names-of-all-global-variables)

## Inputs

### Read an digital input as a Button
  ```py
  import board
  from digitalio import DigitalInOut, Pull
  button = DigitalInOut(board.D3) # defaults to input
v  button.pull = Pull.UP # turn on internal pull-up resistor
  print(button.value)  # False == pressed
  ```

### Read a Potentiometer 
  ```py
  import board
  import analogio
  potknob = analogio.AnalogIn(board.A1)
  position = potknob.value  # ranges from 0-65535
  pos = potknob.value // 256  # make 0-255 range
  ```

### Read a Touch Pin / Capsense
  ```py
  import touchio
  import board
  touch_pin = touchio.TouchIn(board.GP6)
  # on Pico / RP2040, need 1M pull-down on each input
  if touch_pin.value: 
    print("touched!")
  ```

### Read a Rotary Encoder
  ```py
  import board
  import rotaryio
  encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1) # must be consecutive on Pico
  print(encoder.position)  # starts at zero, goes neg or pos
  ```

### Debounce a pin / button 
  ```py
  import board
  from digitalio import DigitalInOut, Pull
  from adafruit_debouncer import Debouncer
  button_in = DigitalInOut(board.D3) # defaults to input
  button_in.pull = Pull.UP # turn on internal pull-up resistor
  button = Debouncer(button_in)
  while True:
    button.update()
    if button.fell:
      print("press!")
    if button.rose:
      print("release!")
  ```

### Set up and debounce a list of pins
  ```py
  import board
  from digitalio import DigitalInOut, Pull
  from adafruit_debouncer import Debouncer
  pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
  buttons = []   # will hold list of Debouncer objects
  for pin in pins:
    tmp_pin = DigitalInOut(pin) # defaults to input
    tmp_pin.pull = Pull.UP # turn on internal pull-up resistor
    buttons.append( Debouncer(tmp_pin) )
  while True:
    for i in range(len(buttons)):
      buttons[i].update()
      if buttons[i].fell:
        print("button",i,"pressed!")
      if buttons[i].rose:
        print("button",i,"released!")
  ```
        
## Outputs

### Output HIGH / LOW on a pin (like an LED)
  ```py
  import board
  import digitalio
  ledpin = digitalio.DigitalInOut(board.D2)
  ledpin.direction = digitalio.Direction.OUTPUT
  ledpin.value = True
  ```

### Output Analog value on a DAC pin
Different boards have DAC on different pins
  ```py
  import board
  import analogio
  dac = analogio.AnalogOut(board.A0)  # on Trinket M0 & QT Py
  dac.value = 32768   # mid-point of 0-65535
  ```

### Output a "Analog" value on a PWM pin
  ```py
  import board
  import pwmio
  out1 = pwmio.PWMOut(board.MOSI, frequency=25000, duty_cycle=0)
  out1.duty_cycle = 32768  # mid-point 0-65535 = 50 % duty-cycle
  ```

### Control Neopixel / WS2812 LEDs
  ```py
  import neopixel
  led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
  led[0] = 0xff00ff
  led[0] = (255,0,255)  # equivalent

  ```

## Neopixels / Dotstars

### Make moving rainbow gradient across LED strip
The built-in `adafruit_pypixelbuf` library contains a `colorwheel()` function
that returns an `(R,G,B)` tuple given a single 0-255 hue. Here's one way to use
it.  This will also work for `adafruit_dotstar` instead of `neopixel`.
```py
import time, random
import board, neopixel
import adafruit_pypixelbuf
num_leds = 16
leds = neopixel.NeoPixel(board.D2, num_leds, brightness=0.4, auto_write=False )
delta_hue = 256//num_leds
speed = 10  # higher numbers = faster rainbow spinning
i=0
while True:
  for l in range(len(leds)):
    leds[l] = adafruit_pypixelbuf.colorwheel( int(i*speed + l * delta_hue) % 255  )
  leds.show()  # only write to LEDs after updating them all
  i = (i+1) % 255
  time.sleep(0.05)
```
### Fade all LEDs by amount for chase effects
```py
my_color = (55,200,230)
dim_by = 20  # dim amount, higher = shorter tails
pos = 0
while True:
  leds[pos] = my_color
  leds[0:] = [[max(i-dim_by,0) for i in l] for l in leds] # dim all by (y,y,y)
  pos = (pos+1) % num_leds  # move to next position
  leds.show()  # only write to LEDs after updating them all
  time.sleep(0.05)
```


## USB

### Detect if USB is connected or not
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

### Get CIRCUITPY disk size and free space
  ```py
  import os
  fs_stat = os.statvfs('/')
  print("Disk size in MB", fs_stat[0] * fs_stat[2] / 1024 / 1024)
  print("Free space in MB", fs_stat[0] * fs_stat[3] / 1024 / 1024)
  ```

### Programmatically reset to UF2 bootloader 
  ```py
  import micrcocontroller
  microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
  microcontroller.reset()
  ```

## USB Serial

### Print to USB Serial
  ```py
  print("hello there")  # prints a newline
  print("waiting...", end='')   # does not print newline
  ```

### Read user input from USB Serial, blocking
  ```py
  while True:
    print("Type something: ", end='')
    my_str = input()  # type and press ENTER or RETURN
    print("You entered: ", my_str)
  ```

### Read user input from USB Serial, non-blocking (mostly)
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

### Read keys from USB Serial
  ```py
  [tbd]

  ```


## Computery Tasks

### Formatting strings
  ```py
  name = "John"
  fav_color = 0x003366
  body_temp = 98.65
  print("name:%s color:%06x thermometer:%2.1f" % (name,fav_color,body_temp))
  'name:John color:ff3366 thermometer:98.6'
  ```

### Formatting strings with f-strings
(doesn't work on 'small' CircuitPythons like QTPy M0)

```py
  name = "John"
  fav_color = 0x003366
  body_temp = 98.65
  print(f"name:{name} color:{color:06x} thermometer:{body_temp:2.1f}")
  'name:John color:ff3366 thermometer:98.6'
```


### Make and Use a config file
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


## More Esoteric Tasks

### Map an input range to an output range
  ```py
  # simple range mapper, like Arduino map()
  def map_range(s, a, b):
      (a1, a2), (b1, b2) = a, b
      return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
  # map 0-0123 value to 0.0-1.0 value
  out = map_range( in, (0,1023), (0.0,1.0) )
  ```

### Time how long something takes
  ```py
  import time
  start_time = time.monotonic() # fraction seconds uptime
  do_something()
  elapsed_time = time.monotonic() - start_time
  print("do_something took %f seconds" % elapsed_time)
  ```

### Preventing Ctrl-C from stopping the program

Put a `try`/`except KeyboardInterrupt` to catch the Ctrl-C
on the inside of your main loop.

```py
while True:
  try:
    print("Doing something important...")
    time.sleep(0.1)
  except KeyboardInterrupt:
    print("Nice try, human! Not quitting.")
```

Also useful for graceful shutdown (turning off neopixels, say) on Ctrl-C.

```py
import time, random
import board, neopixel, adafruit_pypixelbuf
leds = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.4 )
while True:
  try:
    rgb = adafruit_pypixelbuf.colorwheel(int(time.monotonic()*75) % 255)
    leds.fill(rgb) 
    time.sleep(0.05)
  except KeyboardInterrupt:
    print("shutting down nicely...")
    leds.fill(0)
    break  # gets us out of the while True
```


### Raspberry Pi Pico boot.py Protection

Also works on other RP2040-based boards like QTPy RP2040

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

## Networking

### Scan for WiFi Networks, sorted by signal strength (ESP32-S2)

```py
networks = []
for network in wifi.radio.start_scanning_networks():
  networks.append(network)
wifi.radio.stop_scanning_networks()
networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
for network in networks:
  print("ssid:",network.ssid, "rssi:",network.rssi)
```

### Ping an IP address (ESP32-S2)
```py
import time
import wifi
import ipaddress
from secrets import secrets
ip_to_ping = "1.1.1.1"
wifi.radio.connect(ssid=secrets['ssid'],password=secrets['password'])
print("my IP addr:", wifi.radio.ipv4_address)
print("pinging ",ip_to_ping)
ip1 = ipaddress.ip_address(ip_to_ping)
while True:
    print("ping:", wifi.radio.ping(ip1))
    time.sleep(1)
```

### Fetch a JSON file (ESP32-S2)
```py
import time
import wifi
import socketpool
import ssl
import adafruit_requests
from secrets import secrets
wifi.radio.connect(ssid=secrets['ssid'],password=secrets['password'])
print("my IP addr:", wifi.radio.ipv4_address)
pool = socketpool.SocketPool(wifi.radio)
session = adafruit_requests.Session(pool, ssl.create_default_context())
while True:
    response = session.get("https://todbot.com/tst/randcolor.php")
    data = response.json()
    print("data:",data)
    time.sleep(5)
```

### What the heck is `secrets.py`?
It's a config file that lives next to your `code.py` and is used
(invisibly) by many Adafruit WiFi libraries.
You can use it too (as in the examples above) without those libraries

It looks like this for basic WiFi connectivity:
```py
# secrets.py
secrets = {
  "ssid": "Pretty Fly for a WiFi",
  "password": "donthackme123"
}
# code.py
from secrets import secrets
print("your WiFi password is:", secrets['password'])
```

## I2C

### Scan I2C bus for devices
from: https://learn.adafruit.com/circuitpython-essentials/circuitpython-i2c#find-your-sensor-2985153-11

```py
import board
i2c = board.I2C() # or busio.I2C(pin_scl,pin_sda)
while not i2c.try_lock():  pass
print("I2C addresses found:", [hex(device_address)
    for device_address in i2c.scan()])
i2c.unlock()
```


## Board Info

### Display amount of free RAM

from: https://learn.adafruit.com/welcome-to-circuitpython/frequently-asked-questions
```py
import gc
print( gc.mem_free() )
```

### Show microcontroller.pin to board mappings
from https://gist.github.com/anecdata/1c345cb2d137776d76b97a5d5678dc97
```py

import microcontroller
import board

for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        print("".join(("microcontroller.pin.", pin, "\t")), end=" ")
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                print("".join(("", "board.", alias)), end=" ")
    print()
```
### Determine which board you're on
  ```py
  import os
  print(os.uname().machine)
  'Adafruit ItsyBitsy M4 Express with samd51g19'
  ```

### Support multiple boards with one `code.py`
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


## Hacks

### Using the REPL

#### Display built-in modules / libraries
  ```
  Adafruit CircuitPython 6.2.0-beta.2 on 2021-02-11; Adafruit Trinket M0 with samd21e18
  >>> help("modules")
  __main__          digitalio         pulseio           supervisor
  analogio          gc                pwmio             sys
  array             math              random            time
  board             microcontroller   rotaryio          touchio
  builtins          micropython       rtc               usb_hid
  busio             neopixel_write    storage           usb_midi
  collections       os                struct
  Plus any modules on the filesystem
  ```

#### Use REPL fast with copy-paste multi-one-liners

(yes, semicolons are legal in Python)

```py
# load most common libraries
import time; import board; from digitalio import DigitalInOut,Pull; import analogio; import touchio

# print out board pins and objects (like 'I2C' and 'display')
import board; dir(board)

# print out microcontroller pins (chip pins, not the same as board pins)
import microcontroller; dir(microcontroller.pin)

# release configured / built-in display
import displayio; displayio.release_displays()

# make all neopixels purple
import board; import neopixel; leds = neopixel.NeoPixel(board.D3, 8, brightness=0.2); leds.fill(0xff00ff)

```

## Python info

### Display which (not built-in) libraries have been imported 
```py
import sys
print(sys.modules.keys())
# 'dict_keys([])'
import board
import neopixel
import adafruit_dotstar
print(sys.modules.keys())
prints "dict_keys(['neopixel', 'adafruit_dotstar'])"
```

### List names of all global variables
```py
a = 123
b = 'hello there'
my_globals = sorted(dir)
print(my_globals)
# prints "['__name__', 'a', 'b']"
if 'a' in my_globals:
  print("you have a variable named 'a'!")
if 'c' in my_globals:
  print("you have a variable named 'c'!")
```


