
# circuitpython-tricks

A small list of tips & tricks I find myself needing when working with CircuitPython.
I find these examples useful when picking up a new project and I just want some boilerplate to get started.
Also see the [circuitpython-tricks/larger-tricks](larger-tricks) directory for additional ideas.

An older version of this page is a [Learn Guide on Adafruit](https://learn.adafruit.com/todbot-circuitpython-tricks?view=all) too!

If you're new to CircuitPython overall, there's no single reference, but:
- [The Python Tutorial](https://docs.python.org/3/tutorial/) on Python.org,
   since "CircuitPython is Python" mostly. (approx. Python 3.4)
- [CircuitPython API reference](https://docs.circuitpython.org/en/latest/docs/), particularly the ["Core Modules > Modules" section](https://docs.circuitpython.org/en/latest/shared-bindings/index.html#modules) in the left sidebar
    - for compiled-in libraries like `displayio`, `usb`, `audioio`, `ulab.numpy`
- [Pure-Python libraries in Adafruit Library Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) for [drivers](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/tree/main/libraries/drivers) & [helpers](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/tree/main/libraries/helpers) libraries like `board`, `neopixel` & `ble`
- and [CircuitPython Essentials Learn Guide](https://learn.adafruit.com/circuitpython-essentials) of course


Table of Contents
=================

But it's probably easiest to do a Cmd-F/Ctrl-F find on keyword of idea you want.

* [Inputs](#inputs)
   * [Read a digital input as a Button](#read-a-digital-input-as-a-button)
   * [Read a Potentiometer](#read-a-potentiometer)
   * [Read a Touch Pin / Capsense](#read-a-touch-pin--capsense)
   * [Read a Rotary Encoder](#read-a-rotary-encoder)
   * [Debounce a pin / button](#debounce-a-pin--button)
   * [Detect button double-click](#detect-button-double-click)
   * [Set up and debounce a list of pins](#set-up-and-debounce-a-list-of-pins)
* [Outputs](#outputs)
   * [Output HIGH / LOW on a pin (like an LED)](#output-high--low-on-a-pin-like-an-led)
   * [Output Analog value on a DAC pin](#output-analog-value-on-a-dac-pin)
   * [Output a "Analog" value on a PWM pin](#output-a-analog-value-on-a-pwm-pin)
   * [Control Neopixel / WS2812 LEDs](#control-neopixel--ws2812-leds)
   * [Control a servo, with animation list](#control-a-servo-with-animation-list)
* [Neopixels / Dotstars](#neopixels--dotstars)
   * [Light each LED in order](#light-each-led-in-order)
   * [Moving rainbow on built-in board.NEOPIXEL](#moving-rainbow-on-built-in-boardneopixel)
   * [Make moving rainbow gradient across LED strip](#make-moving-rainbow-gradient-across-led-strip)
   * [Fade all LEDs by amount for chase effects](#fade-all-leds-by-amount-for-chase-effects)
* [Audio](#audio)
   * [Making simple tones](#making-simple-tones)
   * [Play a WAV file](#play-a-wav-file)
   * [Audio out using PWM](#audio-out-using-pwm)
   * [Audio out using DAC](#audio-out-using-dac)
   * [Audio out using I2S](#audio-out-using-i2s)
   * [Use audiomixer to prevent audio crackles](#use-audiomixer-to-prevent-audio-crackles)
   * [Play multiple sounds with audiomixer](#play-multiple-sounds-with-audiomixer)
   * [Playing MP3 files](#playing-mp3-files)
* [USB](#usb)
   * [Rename CIRCUITPY drive to something new](#rename-circuitpy-drive-to-something-new)
   * [Detect if USB is connected or not](#detect-if-usb-is-connected-or-not)
   * [Get CIRCUITPY disk size and free space](#get-circuitpy-disk-size-and-free-space)
   * [Programmatically reset to UF2 bootloader](#programmatically-reset-to-uf2-bootloader)
* [USB Serial](#usb-serial)
   * [Print to USB Serial](#print-to-usb-serial)
   * [Read user input from USB Serial, blocking](#read-user-input-from-usb-serial-blocking)
   * [Read user input from USB Serial, non-blocking (mostly)](#read-user-input-from-usb-serial-non-blocking-mostly)
   * [Read keys from USB Serial](#read-keys-from-usb-serial)
   * [Read user input from USB serial, non-blocking](#read-user-input-from-usb-serial-non-blocking)
* [USB Keyboard & Mouse](#usb-keyboard-mouse)
   * [Sending keystrokes and mouse moves](#sending-keystrokes-and-mouse-moves)
* [USB MIDI](#usb-midi)
   * [Sending MIDI with adafruit_midi](#sending-midi-with-adafruit_midi)
   * [Sending MIDI with bytearray](#sending-midi-with-bytearray)
   * [MIDI over Serial UART](#midi-over-serial-uart)
   * [Receiving MIDI](#receiving-midi)
   * [Receiving MIDI USB and MIDI Serial UART together](#receiving-midi-usb-and-midi-serial-uart-together)
   * [Enable USB MIDI in boot.py (for ESP32-S2 and STM32F4)](#enable-usb-midi-in-bootpy-for-esp32-s2-and-stm32f4)
* [WiFi / Networking](#wifi--networking)
   * [Scan for WiFi Networks, sorted by signal strength](#scan-for-wifi-networks-sorted-by-signal-strength)
   * [Join WiFi network with highest signal strength](#join-wifi-network-with-highest-signal-strength)
   * [Ping an IP address](#ping-an-ip-address)
   * [Get IP address of remote host](#get-ip-address-of-remote-host)
   * [Fetch a JSON file](#fetch-a-json-file)
   * [Serve a webpage via HTTP](#serve-a-webpage-via-http)
   * [Set RTC time from NTP](#set-rtc-time-from-ntp)
   * [Set RTC time from time service](#set-rtc-time-from-time-service)
   * [What the heck is settings.toml?](#what-the-heck-is-settingstoml)
   * [What the heck is secrets.py?](#what-the-heck-is-secretspy)
* [Displays (LCD / OLED / E-Ink) and displayio](#displays-lcd--oled--e-ink-and-displayio)
   * [Get default display and change display rotation](#get-default-display-and-change-display-rotation)
   * [Display an image](#display-an-image)
   * [Display background bitmap](#display-background-bitmap)
   * [Image slideshow](#image-slideshow)
   * [Dealing with E-Ink "Refresh Too Soon" error](#dealing-with-e-ink-refresh-too-soon-error)
   * [Turn off REPL on built-in display](#turn-off-repl-on-built-in-display)
* [I2C](#i2c)
   * [Scan I2C bus for devices](#scan-i2c-bus-for-devices)
   * [Speed up I2C bus](#speed-up-i2c-bus)
* [Timing](#timing)
   * [Measure how long something takes](#measure-how-long-something-takes)
   * [More accurate timing with ticks_ms(), like Arduino millis()](#more-accurate-timing-with-ticks_ms-like-arduino-millis)
   * [Control garbage collection for reliable timing](#control-garbage-collection-for-reliable-timing)
   * [Converting milliseconds to seconds: 0.004 * 1000 != 4, sometimes](#converting-milliseconds-to-seconds-0004--1000--4-sometimes)
* [Board Info](#board-info)
   * [Get CPU speed (and set it!)](#get-cpu-speed-and-set-it)
   * [Display amount of free RAM](#display-amount-of-free-ram)
   * [Show microcontroller.pin to board mappings](#show-microcontrollerpin-to-board-mappings)
   * [Determine which board you're on](#determine-which-board-youre-on)
   * [Support multiple boards with one code.py](#support-multiple-boards-with-one-codepy)
* [Computery Tasks](#computery-tasks)
   * [Formatting strings](#formatting-strings)
   * [Formatting strings with f-strings](#formatting-strings-with-f-strings)
   * [Using regular expressions to "findall" strings](#using-regular-expressions-to-findall-strings)
   * [Make and use a config file](#make-and-use-a-config-file)
   * [Run different code.py on startup](#run-different-codepy-on-startup)
* [Coding Techniques](#coding-techniques)
   * [Map an input range to an output range](#map-an-input-range-to-an-output-range)
   * [Constrain an input to a min/max](#constrain-an-input-to-a-minmax)
   * [Turn a momentary value into a toggle](#turn-a-momentary-value-into-a-toggle)
   * [Do something every N seconds without sleep()](#do-something-every-n-seconds-without-sleep)
* [System error handling](#system-error-handling)
   * [Preventing Ctrl-C from stopping the program](#preventing-ctrl-c-from-stopping-the-program)
   * [Prevent auto-reload when CIRCUITPY is touched](#prevent-auto-reload-when-circuitpy-is-touched)
   * [Raspberry Pi Pico boot.py Protection](#raspberry-pi-pico-bootpy-protection)
* [Using the REPL](#using-the-repl)
   * [Display built-in modules / libraries](#display-built-in-modules--libraries)
   * [Turn off built-in display to speed up REPL printing](#turn-off-built-in-display-to-speed-up-repl-printing)
   * [Useful REPL one-liners](#useful-repl-one-liners)
* [Python tricks](#python-tricks)
   * [Create list with elements all the same value](#create-list-with-elements-all-the-same-value)
   * [Convert RGB tuples to int and back again](#convert-rgb-tuples-to-int-and-back-again)
   * [Storing multiple values per list entry](#storing-multiple-values-per-list-entry)
* [Python info](#python-info)
   * [Display which (not built-in) libraries have been imported](#display-which-not-built-in-libraries-have-been-imported)
   * [List names of all global variables](#list-names-of-all-global-variables)
   * [Display the running CircuitPython release](#display-the-running-circuitpython-release)
* [Host-side tasks](#host-side-tasks)
   * [Installing CircuitPython libraries](#installing-circuitpython-libraries)
      * [Installing libraries with circup](#installing-libraries-with-circup)
      * [Copying libraries by hand with cp](#copying-libraries-by-hand-with-cp)
   * [Preparing images for CircuitPython](#preparing-images-for-circuitpython)
      * [Online](#online)
      * [Command-line: using ImageMagick](#command-line-using-imagemagick)
      * [Command-line: using GraphicsMagick](#command-line-using-graphicsmagick)
      * [Making images smaller or for E-Ink displays](#making-images-smaller-or-for-e-ink-displays)
      * [NodeJs: using gm](#nodejs-using-gm)
      * [Python: using PIL / pillow](#python-using-pil--pillow)
   * [Preparing audio files for CircuitPython](#preparing-audio-files-for-circuitpython)
      * [WAV files](#wav-files)
      * [MP3 files](#mp3-files)
      * [Getting sox](#getting-sox)
   * [Circup hacks](#circup-hacks)
      * [Finding where circup stores its files](#finding-where-circup-stores-its-files)
   * [Building CircuitPython](#building-circuitpython)
* [About this guide](#about-this-guide)


## Inputs

### Read a digital input as a Button

```py
import board
from digitalio import DigitalInOut, Pull
button = DigitalInOut(board.D3) # defaults to input
button.pull = Pull.UP # turn on internal pull-up resistor
print(button.value)  # False == pressed
```

Can also do:

```py
import time, board, digitalio
button = digitalio.DigitalInOut(board.D3)
button.switch_to_input(digitalio.Pull.UP)
while True:
    print("button pressed:", button.value == False) # False == pressed
    time.sleep(0.1)
```

But you probably want to use `keypad` to get debouncing and press/release events.
You can use it for a single button!

```py
import board, keypad
keys = keypad.Keys((board.D3,), value_when_pressed=False, pull=True)
while True:
  if key := keys.events.get():
    if key.pressed: 
      print("pressed key!")

```
Note: be sure to add the comma when using a single button (e.g. `(board.D3,)`)


### Read a Potentiometer

```py
import board
import analogio
potknob = analogio.AnalogIn(board.A1)
position = potknob.value  # ranges from 0-65535
pos = potknob.value // 256  # make 0-255 range
```

Note: While `AnalogIn.value` is 16-bit (0-65535) corresponding to 0 V to 3.3V,
the MCU ADCs can have limitations in resolution and voltage range.
This reduces what CircuitPython sees.
For example, the ESP32 ADCs are 12-bit w/ approx 0.1 V to 2.5 V range
(e.g. `value` goes from around 200 to 50,000, in steps of 16)

### Read a Touch Pin / Capsense

```py
import touchio
import board
touch_pin = touchio.TouchIn(board.GP6)
# on Pico / RP2040, need 1M pull-down on each input
if touch_pin.value:
    print("touched!")
```

You can also get an "analog" touch value with `touch_pin.raw_value` to do
basic proximity detection or even [theremin-like behavior](https://gist.github.com/todbot/bb4ec9c509f8c301e4787e5cb26ec870).

### Read a Rotary Encoder

```py
import board
import rotaryio
encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1) # must be consecutive on Pico
print(encoder.position)  # starts at zero, goes neg or pos
```

### Debounce a pin / button

But you probably want to use `keypad` to get debouncing and press/release events.
You can use it for a single button!

```py
import board, keypad
keys = keypad.Keys((board.D3,), value_when_pressed=False, pull=True)
while True:
  if key := keys.events.get():
    if key.pressed: 
      print("pressed key!", key.key_number)
    if key.released:
      print("released key!", key.key_number)

```
Note: be sure to add the comma when using a single button (e.g. `(board.D3,)`)

If your board doesn't have `keypad`, you can use `adafruit_debouncer` from 
the bundle. 

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

Note: Most boards have the native `keypad` module that can do keypad debouncing in a much more
efficient way.  See [Set up and debounce a list of pins](#set-up-and-debounce-a-list-of-pins)


### Detect button double-click

```py
import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Button
button_in = DigitalInOut(board.D3) # defaults to input
button_in.switch_to_input(Pull.UP) # turn on internal pull-up resistor
button = Button(button_in)
while True:
    button.update()
    if button.pressed:
        print("press!")
    if button.released:
      print("release!")
    if button.short_count > 1:  # detect multi-click
      print("multi-click: click count:", button.short_count)
```

### Set up and debounce a list of pins

If your board's CircuitPython has the `keypad` library (most do),
then I recommend using it. It's not just for key matrixes! And it's more efficient
and, since it's built-in, reduces a library dependency.

```py
import board
import keypad
button_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
buttons = keypad.Keys(button_pins, value_when_pressed=False, pull=True)

while True:
    button = buttons.events.get()  # see if there are any key events
    if button:                      # there are events!
      if button.pressed:
        print("button", button.key_number, "pressed!")
      if button.released:
        print("button", button.key_number, "released!")
```

Otherwise, you can use `adafruit_debouncer`:

```py
import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer
button_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
buttons = []   # will hold list of Debouncer objects
for pin in button_pins:   # set up each pin
    tmp_pin = DigitalInOut(pin) # defaults to input
    tmp_pin.pull = Pull.UP      # turn on internal pull-up resistor
    buttons.append( Debouncer(tmp_pin) )
while True:
    for i in range(len(buttons)):
        buttons[i].update()
        if buttons[i].fell:
            print("button",i,"pressed!")
        if buttons[i].rose:
            print("button",i,"released!")
```

And you can use `adafruit_debouncer` on touch pins too:

```py
import board, touchio, adafruit_debouncer
touchpad = adafruit_debouncer.Debouncer(touchio.TouchIn(board.GP1))
while True:
    touchpad.update()
    if touchpad.rose:  print("touched!")
    if touchpad.fell:  print("released!")
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

Can also do:
```py
ledpin = digitalio.DigitalInOut(board.D2)
ledpin.switch_to_output(value=True)
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
leds = neopixel.NeoPixel(board.NEOPIXEL, 16, brightness=0.2)
leds[0] = 0xff00ff  # first LED of 16 defined
leds[0] = (255,0,255)  # equivalent
leds.fill( 0x00ff00 )  # set all to green
```

### Control a servo, with animation list

```py
# servo_animation_code.py -- show simple servo animation list
import time, random, board
from pwmio import PWMOut
from adafruit_motor import servo

# your servo will likely have different min_pulse & max_pulse settings
servoA = servo.Servo(PWMOut(board.RX, frequency=50), min_pulse=500, max_pulse=2250)

# the animation to play
animation = (
    # (angle, time to stay at that angle)
    (0, 2.0),
    (90, 2.0),
    (120, 2.0),
    (180, 2.0)
)
ani_pos = 0 # where in list to start our animation

while True:
    angle, secs = animation[ ani_pos ]
    print("servo moving to", angle, secs)
    servoA.angle = angle
    time.sleep( secs )
    ani_pos = (ani_pos + 1) % len(animation) # go to next, loop if at end
```


## Neopixels / Dotstars

### Light each LED in order

You can access each LED with Python array methods on the `leds` object.
And you can set the LED color with either an RGB tuple (`(255,0,80)`) or an
RGB hex color as a 24-bit number (`0xff0050`)

```py
import time, board, neopixel

led_pin = board.GP5   # which pin the LED strip is on
num_leds = 10
colors = ( (255,0,0), (0,255,0), (0,0,255), 0xffffff, 0x000000 )

leds = neopixel.NeoPixel(led_pin, num_leds, brightness=0.1)

i = 0
while True:
    print("led:",i)
    for c in colors:
        leds[i] = c
        time.sleep(0.2)
    i = (i+1) % num_leds
```

### Moving rainbow on built-in `board.NEOPIXEL`

In CircuitPython 7, the `rainbowio` module has a `colorwheel()` function.
Unfortunately, the `rainbowio` module is not available in all builds.
In CircuitPython 6, `colorwheel()` is a built-in function part of `_pixelbuf` or `adafruit_pypixelbuf`.

The `colorwheel()` function takes a single value 0-255 hue and returns an `(R,G,B)` tuple
given a single 0-255 hue.  It's not a full HSV_to_RGB() function but often all you need
is "hue to RGB", wher you assume saturation=255 and value=255.
It can be used with `neopixel`, `adafruit_dotstar`, or any place you need a (R,G,B) 3-byte tuple.
Here's one way to use it.

```py
# CircuitPython 7 with or without rainbowio module
import time, board, neopixel
try:
    from rainbowio import colorwheel
except:
    def colorwheel(pos):
        if pos < 0 or pos > 255:  return (0, 0, 0)
        if pos < 85: return (255 - pos * 3, pos * 3, 0)
        if pos < 170: pos -= 85; return (0, 255 - pos * 3, pos * 3)
        pos -= 170; return (pos * 3, 0, 255 - pos * 3)

led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.4)
while True:
    led.fill( colorwheel((time.monotonic()*50)%255) )
    time.sleep(0.05)
```


### Make moving rainbow gradient across LED strip

See [demo of it in this tweet](https://twitter.com/todbot/status/1397992493833097218).

```py
import time, board, neopixel, rainbowio
num_leds = 16
leds = neopixel.NeoPixel(board.D2, num_leds, brightness=0.4, auto_write=False )
delta_hue = 256//num_leds
speed = 10  # higher numbers = faster rainbow spinning
i=0
while True:
  for l in range(len(leds)):
    leds[l] = rainbowio.colorwheel( int(i*speed + l * delta_hue) % 255  )
  leds.show()  # only write to LEDs after updating them all
  i = (i+1) % 255
  time.sleep(0.05)
```

A shorter version using a Python list comprehension. The `leds[:]` trick is a way to assign
a new list of colors to all the LEDs at once.

```py
import supervisor, board, neopixel, rainbowio
num_leds = 16
speed = 10  # lower is faster, higher is slower
leds = neopixel.NeoPixel(board.D2, 16, brightness=0.4)
while True:
  t = supervisor.ticks_ms() / speed
  leds[:] = [rainbowio.colorwheel( t + i*(255/len(leds)) ) for i in range(len(leds))]

```

### Fade all LEDs by amount for chase effects
```py
import time
import board, neopixel
num_leds = 16
leds = neopixel.NeoPixel(board.D2, num_leds, brightness=0.4, auto_write=False )
my_color = (55,200,230)
dim_by = 20  # dim amount, higher = shorter tails
pos = 0
while True:
  leds[pos] = my_color
  leds[:] = [[max(i-dim_by,0) for i in l] for l in leds] # dim all by (dim_by,dim_by,dim_by)
  pos = (pos+1) % num_leds  # move to next position
  leds.show()  # only write to LEDs after updating them all
  time.sleep(0.05)
```

## Audio

If you're used to Arduino, making sound was mostly constrained to simple beeps
using the Arduino `tone()` function. You can do that in CircuitPython too with
`pwmio` and `simpleio`, but CircuitPython can also play WAV and MP3
files and become a [fully-fledged audio synthesizer with `synthio`](https://github.com/todbot/circuitpython-synthio-tricks).

In CircuitPython, there are multiple core module libraries available to output audio:

- `pwmio`  -- use almost any GPIO pin to output simple beeps, no WAV/MP3/synthio
- `audioio` -- uses built-in DAC to output WAV, MP3, synthio
- `audiopwmio` -- like above, but uses PWM like arduino `analogWrite()`, requires RC filter to convert to analog
- `audiobusio` -- outputs high-quality I2S audio data stream, requires external I2S decoder hardware

Different devices will have different audio modules available. Generally, the
pattern is:

- SAMD51 (e.g. "M4" boards) -- `audioio` (DAC) and `audiobusio` (I2S)
- RP2040 (e.g. Pico) -- `audiopwmio` (PWM) and `audiobusio` (I2S)
- ESP32 (e.g. QTPy ESP32) -- `audiobusio` (I2S) only

To play WAV and MP3 files, they usually must be resaved in a format parsable by CircuitPython,
see [Preparing Audio Files for CircuitPython](#preparing-audio-files-for-circuitpython)

### Making simple tones

For devices that only have `pwmio` capability, you can make simple tones.
The [`simpleio`](https://docs.circuitpython.org/projects/simpleio/en/latest/examples.html#id1) library can be used for this:

```py
# a short piezo song using tone()
import time, board, simpleio
while True:
    for f in (262, 294, 330, 349, 392, 440, 494, 523):
        simpleio.tone(board.A0, f, 0.25)
    time.sleep(1)
```

### Play a WAV file

WAV files are easiest for CircuitPython to play.
The shortest code to play a WAV file on Pico RP2040 is:

```py
import time, board, audiocore, audiopwmio
audio = audiopwmio.PWMAudioOut(board.GP0)
wave = audiocore.WaveFile("laser2.wav")
audio.play(wave)
while True:
  pass   # wait for audio to finish playing
```
Details and other ways below.

### Audio out using PWM

This uses the `audiopwmio` library, only available for RP2040 boards like Raspberry Pi Pico and NRF52840-based boards like Adafruit Feather nRF52840 Express.
On RP2040-based boards, any pin can be PWM Audio pin.
See the [audiopwomio Support Matrix](https://circuitpython.readthedocs.io/en/latest/shared-bindings/support_matrix.html?filter=audiopwmio) for which boards support `audiopwmio`.

```py
import time, board
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut
wave = WaveFile("laser2.wav")  # can also be filehandle from open()
audio = AudioOut(board.GP0) # must be PWM-capable pin
while True:
    print("audio is playing:",audio.playing)
    if not audio.playing:
      audio.play(wave)
      wave.sample_rate = int(wave.sample_rate * 0.90) # play 10% slower each time
    time.sleep(0.1)
```

Notes:

- There will be a small *pop* when audio starts playing as the PWM driver
takes the GPIO line from not being driven to being PWM'ed.
There's currently no way around this. If playing multiple WAVs, consider using
[`AudioMixer`](#use-audiomixer-to-prevent-audio-crackles) to keep the audio system
running between WAVs. This way, you'll only have the startup pop.

- If you want *stereo* output on boards that support it
then you can pass in two pins, like:
`audio = audiopwmio.PWMAudioOut(left_channel=board.GP14, right_channel=board.GP15)`

- PWM output must be filtered and converted to line-level to be usable.
Use an RC circuit to accomplish this, see [this simple circuit](https://github.com/todbot/circuitpython-tricks/blob/main/larger-tricks/docs/breakbeat_sampleplayer_wiring.png) or [this twitter thread for details](https://twitter.com/todbot/status/1403451581593374720).

- The `WaveFile()` object can take either a filestream
(the output of `open('filewav','rb')`) or can take a string filename (`wav=WaveFile("laser2.wav")`).


### Audio out using DAC

Some CircuitPython boards (SAMD51 "M4" & SAMD21 "M0") have built-in DACs that are supported.
The code is the same as above, with just the import line changing.
See the [audioio Support Matrix](https://circuitpython.readthedocs.io/en/latest/shared-bindings/support_matrix.html?filter=audioio) for which boards support `audioio`.

```py
import time, board
import audiocore, audioio # DAC
wave_file = open("laser2.wav", "rb")
wave = audiocore.WaveFile(wave_file)
audio = audioio.AudioOut(board.A0)  # must be DAC-capable pin, A0 on QTPy Haxpress
while True:
  print("audio is playing:",audio.playing)
  if not audio.playing:
    audio.play(wave)
    wave.sample_rate = int(wave.sample_rate * 0.90) # play 10% slower each time
  time.sleep(0.1)
```

Note: if you want *stereo* output on boards that support it (SAMD51 "M4" mostly),
then you can pass in two pins, like:
`audio = audioio.AudioOut(left_channel=board.A0, right_channel=board.A1)`


### Audio out using I2S

Unlike PWM or DAC, most CircuitPython boards support driving an external I2S audio board.
This will also give you higher-quality sound output than DAC or PWM.
See the [audiobusio Support Matrix](https://circuitpython.readthedocs.io/en/latest/shared-bindings/support_matrix.html?filter=audiobusio) for which boards support `audiobusio`.

```py
# for e.g. Pico RP2040 pins bit_clock & word_select pins must be adjacent
import board, audiobusio, audiocore
audio = audiobusio.I2SOut(bit_clock=board.GP0, word_select=board.GP1, data=board.GP2)
audio.play( audiocore.WaveFile("laser2.wav") )
```

### Use audiomixer to prevent audio crackles

The default buffer used by the audio system is quite small.
This means you'll hear corrupted audio if CircuitPython is doing anything else
(having CIRCUITPY written to, updating a display). To get around this, you can
use `audiomixer` to make the audio buffer larger. Try `buffer_size=2048` to start.
A larger buffer means a longer lag between when a sound is triggered when its heard.

AudioMixer is also great if you want to play multiple WAV files at the same time.

```py
import time, board
from audiocore import WaveFile
from audioio import AudioOut
import audiomixer
wave = WaveFile("laser2.wav", "rb")
audio = AudioOut(board.A0) # assuming QTPy M0 or Itsy M4
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True, buffer_size=2048)
audio.play(mixer)  # never touch "audio" after this, use "mixer"
while True:
    print("mixer voice is playing:", mixer.voice[0].playing)
    if not mixer.voice[0].playing:
      time.sleep(1)
      print("playing again")
      mixer.voice[0].play(wave)
    time.sleep(0.1)
```

### Play multiple sounds with audiomixer

This example assumes WAVs that are mono 22050 Hz sample rate, w/ signed 16-bit samples.

```py
import time, board, audiocore, audiomixer
from audiopwmio import PWMAudioOut as AudioOut

wav_files = ("loop1.wav", "loop2.wav", "loop3.wav")
wavs = [None] * len(wav_files)  # holds the loaded WAVs

audio = AudioOut(board.GP2)  # RP2040 example
mixer = audiomixer.Mixer(voice_count=len(wav_files), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True, buffer_size=2048)
audio.play(mixer)  # attach mixer to audio playback

for i in range(len(wav_files)):
    print("i:",i)
    wavs[i] = audiocore.WaveFile(open(wav_files[i], "rb"))
    mixer.voice[i].play( wavs[i], loop=True) # start each one playing

while True:
    print("doing something else while all loops play")
    time.sleep(1)
```

Note: M0 boards do not have `audiomixer`

Note: Number of simultaneous sounds is limited sample rate and flash read speed.
Rules of thumb:
- Built-in flash: 10 22kHz sounds simultanously
- SPI SD cards: 2 22kHz sounds simultaneously


Also see the many examples in [larger-tricks](./larger-tricks/).

### Playing MP3 files

Once you have set up audio output (either directly or via AudioMixer), you can play WAVs or
MP3s through it, or play both simultaneously.

For instance, here's an example that uses an I2SOut to a PCM5102 on a Raspberry Pi Pico RP2040
to simultaneously play both a WAV and an MP3:

```py
import board, audiobusio, audiocore, audiomp3
num_voices = 2

i2s_bclk, i2s_wsel, i2s_data = board.GP9, board.GP10, board.GP11 # BCLK, LCLK, DIN on PCM5102

audio = audiobusio.I2SOut(bit_clock=i2s_bclk, word_select=i2s_wsel, data=i2s_data)
mixer = audiomixer.Mixer(voice_count=num_voices, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

wav_file = "/amen1_22k_s16.wav" # in 'circuitpython-tricks/larger-tricks/breakbeat_wavs'
mp3_file = "/vocalchops476663_22k_128k.mp3" # in 'circuitpython-tricks/larger-tricks/wav'
# https://freesound.org/people/f-r-a-g-i-l-e/sounds/476663/

wave = audiocore.WaveFile(open(wav_file, "rb"))
mp3 = audiomp3.MP3Decoder(open(mp3_file, "rb"))
mixer.voice[0].play( wave )
mixer.voice[1].play( mp3 )

while True:
    pass   # both audio files play

```

__Note:__ For MP3 files, be aware that since this is doing software MP3 decoding,
you will likely need to re-encode the MP3s to lower bitrate and sample rate
(max 128 kbps and 22,050 Hz) to be playable the lower-end CircuitPython devices
like the Pico / RP2040.

__Note:__ For MP3 files and setting `loop=True` when playing, there is a small delay
when looping.  WAV files loop seemlessly.



An example of boards with `pwmio` but no audio are ESP32-S2-based boards like
[FunHouse](https://www.adafruit.com/product/4985),
where you cannot play WAV files, but you can make beeps.
A larger example is this gist: https://gist.github.com/todbot/f35bb5ceed013a277688b2ca333244d5


## USB


### Rename CIRCUITPY drive to something new

For instance, if you have multiple of the same device.
The `label` can be up to 11 characters.
This goes in `boot.py` not `code.py` and you must powercycle board.

```py
# this goes in boot.py not code.py!
new_name = "TRINKEYPY0"
import storage
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = new_name
storage.remount("/", readonly=True)
```

### Detect if USB is connected or not

```py
import supervisor
if supervisor.runtime.usb_connected:
  led.value = True   # USB
else:
  led.value = False  # no USB
```

An older way that tries to mount CIRCUITPY read-write and if it fails, USB connected:

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
import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.UF2)
microcontroller.reset()
```

Note: in older CircuitPython use `RunMode.BOOTLOADER` and for boards with multiple
bootloaders (like ESP32-S2):

```py
import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
microcontroller.reset()
```


## USB Serial

### Print to USB Serial

```py
print("hello there")  # prints a newline
print("waiting...", end='')   # does not print newline
for i in range(256):  print(i, end=', ')   # comma-separated numbers
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
import time, sys, supervisor
print("type charactcers")
while True:
    n = supervisor.runtime.serial_bytes_available
    if n > 0:  # we read something!
        s = sys.stdin.read(n)  # actually read it in
        # print both text & hex version of recv'd chars (see control chars!)
        print("got:", " ".join("{:s} {:02x}".format(c,ord(c)) for c in s))
    time.sleep(0.01) # do something else
```

### Read user input from USB serial, non-blocking
```py
class USBSerialReader:
    """ Read a line from USB Serial (up to end_char), non-blocking, with optional echo """
    def __init__(self):
        self.s = ''
    def read(self,end_char='\n', echo=True):
        import sys, supervisor
        n = supervisor.runtime.serial_bytes_available
        if n > 0:                    # we got bytes!
            s = sys.stdin.read(n)    # actually read it in
            if echo: sys.stdout.write(s)  # echo back to human
            self.s = self.s + s      # keep building the string up
            if s.endswith(end_char): # got our end_char!
                rstr = self.s        # save for return
                self.s = ''          # reset str to beginning
                return rstr
        return None                  # no end_char yet

usb_reader = USBSerialReader()
print("type something and press the end_char")
while True:
    mystr = usb_reader.read()  # read until newline, echo back chars
    #mystr = usb_reader.read(end_char='\t', echo=False) # trigger on tab, no echo
    if mystr:
        print("got:",mystr)
    time.sleep(0.01)  # do something time critical
```

## USB Keyboard & Mouse

CircuitPython comes set up to be a USB keyboard and mouse. 
Many more details in [CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse) but the basics are below.  The `adafruit_hid` library needs 
to be installed from the [the bundle](https://circuitpython.org/libraries). 
I do `circup install adafruit_hid` in a terminal.

### Sending keystrokes and mouse moves

```py
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

while True:
    time.sleep(1)
    print("moving right")
    kbd.send(Keycode.A)  # types "a" (sends press() & release_all())
    mouse.move(x=50, y=0)  # moves mouse slightly right
    time.sleep(1)
    print("moving left")
    kbd.send(Keycode.B)  # types "b" (sends press() & release_all())
    mouse.move(x=-50, y=0)  # moves mouse slightly left
    time.sleep(1)
```

## USB MIDI

CircuitPython can be a MIDI controller, or respond to MIDI!
Adafruit provides an [`adafruit_midi`](https://github.com/adafruit/Adafruit_CircuitPython_MIDI)
class to make things easier, but it's rather complex for how simple MIDI actually is.

For outputting MIDI, you can opt to deal with raw `bytearray`s, since most MIDI messages
are just 1,2, or 3 bytes long.  For reading MIDI,
you may find [Winterbloom's SmolMIDI](https://github.com/wntrblm/Winterbloom_SmolMIDI) to be faster
to parse MIDI messages, since by design it does less.

### Sending MIDI with adafruit_midi

```py
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
midi_out_channel = 3 # human version of MIDI out channel (1-16)
midi = adafruit_midi.MIDI( midi_out=usb_midi.ports[1], out_channel=midi_out_channel-1)

def play_note(note,velocity=127):
    midi.send(NoteOn(note, velocity))  # 127 = highest velocity
    time.sleep(0.1)
    midi.send(NoteOff(note, 0))  # 0 = lowest velocity
```

Note: This pattern works for sending serial (5-pin) MIDI too, see below

### Sending MIDI with bytearray

Sending MIDI with a lower-level `bytearray` is also pretty easy and
could gain some speed for timing-sensitive applications.
This code is equivalent to the above, without `adafruit_midi`

```py
import usb_midi
midi_out = usb_midi.ports[1]
midi_out_channel = 3   # MIDI out channel (1-16)
note_on_status = (0x90 | (midi_out_channel-1))
note_off_status = (0x80 | (midi_out_channel-1))

def play_note(note,velocity=127):
    midi_out.write( bytearray([note_on_status, note, velocity]) )
    time.sleep(0.1)
    midi_out.write( bytearray([note_off_status, note, 0]) )
```

### MIDI over Serial UART

Not exactly USB, but it is MIDI!
Both `adafruit_midi` and the bytearray technique works for Serial MIDI (aka "5-pin MIDI") too.
With a [simple MIDI out circuit](https://learn.adafruit.com/qt-py-rp2040-usb-to-serial-midi-friends/circuit-diagram)
you can control old hardware synths.

```py
import busio
midi_out_channel = 3  # MIDI out channel (1-16)
note_on_status = (0x90 | (midi_out_channel-1))
note_off_status = (0x80 | (midi_out_channel-1))
# must pick board pins that are UART TX and RX pins
midi_uart = busio.UART(tx=board.GP16, rx=board.GP17, baudrate=31250)

def play_note(note,velocity=127):
    midi_uart.write( bytearray([note_on_status, note, velocity]) )
    time.sleep(0.1)
    midi_uart.write( bytearray([note_off_status, note, 0]) )
```

### Receiving MIDI

```py
import usb_midi        # built-in library
import adafruit_midi   # install with 'circup install adafruit_midi'
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

midi_usb = adafruit_midi.MIDI(midi_in=usb_midi.ports[0])
while True:
    msg = midi_usb.receive()
    if msg:
        if isinstance(msg, NoteOn):
            print("usb noteOn:",msg.note, msg.velocity)
        elif isinstance(msg, NoteOff):
            print("usb noteOff:",msg.note, msg.velocity)
```
Note with `adafruit_midi` you must `import` each kind of MIDI Message you want to handle.

### Receiving MIDI USB and MIDI Serial UART together

MIDI is MIDI, so you can use either the `midi_uart` or the `usb_midi.ports[]` created above with `adafruit_midi`.
Here's an example receiving MIDI from both USB and Serial on a QTPy RP2040.
Note for receiving serial MIDI, you need an appropriate optoisolator input circuit,
like [this one for QTPys](https://www.denki-oto.com/store/p74/MICROMIDITRS-USB.html#/)
or [this one for MacroPad RP2040](https://www.tindie.com/products/todbot/macropadsynthplug-turn-rp2040-into-a-synth/).

```py
import board, busio
import usb_midi        # built-in library
import adafruit_midi   # install with 'circup install adafruit_midi'
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

uart = busio.UART(tx=board.TX, rx=board.RX, baudrate=31250, timeout=0.001)
midi_usb = adafruit_midi.MIDI( midi_in=usb_midi.ports[0],  midi_out=usb_midi.ports[1] )
midi_serial = adafruit_midi.MIDI( midi_in=uart, midi_out=uart )

while True:
    msg = midi_usb.receive()
    if msg:
        if isinstance(msg, NoteOn):
            print("usb noteOn:",msg.note, msg.velocity)
        elif isinstance(msg, NoteOff):
            print("usb noteOff:",msg.note, msg.velocity)
    msg = midi_serial.receive()
    if msg:
        if isinstance(msg, NoteOn):
            print("serial noteOn:",msg.note, msg.velocity)
        elif isinstance(msg, NoteOff):
            print("serial noteOff:",msg.note, msg.velocity)
```

If you don't care about the source of the MIDI messages, you can combine
the two if blocks using the "walrus operator" (`:=`)

```py
while True:
    while msg := midi_usb.receive() or midi_uart.receive():
        if isinstance(msg, NoteOn) and msg.velocity != 0:
            note_on(msg.note, msg.velocity)
        elif isinstance(msg,NoteOff) or isinstance(msg,NoteOn) and msg.velocity==0:
            note_off(msg.note, msg.velocity)
```


### Enable USB MIDI in boot.py (for ESP32-S2 and STM32F4)

Some CircuitPython devices like ESP32-S2 based ones, do not have enough
[USB endpoints to enable all USB functions](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/how-many-usb-devices-can-i-have), so USB MIDI is disabled by default.
To enable it, the easiest is to disable USB HID (keyboard/mouse) support.
This must be done in `boot.py` and the board power cycled.

```py
# boot.py
import usb_hid
import usb_midi
usb_hid.disable()
usb_midi.enable()
print("enabled USB MIDI, disabled USB HID")
```


## WiFi / Networking

### Scan for WiFi Networks, sorted by signal strength

Note: this is for boards with native WiFi (ESP32)

```py
import wifi
networks = []
for network in wifi.radio.start_scanning_networks():
    networks.append(network)
wifi.radio.stop_scanning_networks()
networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
for network in networks:
    print("ssid:",network.ssid, "rssi:",network.rssi)
```

### Join WiFi network with highest signal strength

```py
import wifi

def join_best_network(good_networks, print_info=False):
    """join best network based on signal strength of scanned nets"""
    networks = []
    for network in wifi.radio.start_scanning_networks():
        networks.append(network)
    wifi.radio.stop_scanning_networks()
    networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
    for network in networks:
        if print_info: print("network:",network.ssid)
        if network.ssid in good_networks:
            if print_info: print("connecting to WiFi:", network.ssid)
            try:
                wifi.radio.connect(network.ssid, good_networks[network.ssid])
                return True
            except ConnectionError as e:
                if print_info: print("connect error:",e)
    return False

good_networks = {"todbot1":"FiOnTheFly",  # ssid, password
                 "todbot2":"WhyFlyWiFi",}
connected = join_best_network(good_networks, print_info=True)
if connected:
    print("connected!")

```

### Ping an IP address

Note: this is for boards with native WiFi (ESP32)

```py
import os
import time
import wifi
import ipaddress

ip_to_ping = "1.1.1.1"

wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("my IP addr:", wifi.radio.ipv4_address)
print("pinging ",ip_to_ping)
ip1 = ipaddress.ip_address(ip_to_ping)
while True:
    print("ping:", wifi.radio.ping(ip1))
    time.sleep(1)
```

### Get IP address of remote host

```py
import os, wifi, socketpool

wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("my IP addr:", wifi.radio.ipv4_address)

hostname = "todbot.com"

pool = socketpool.SocketPool(wifi.radio)
addrinfo = pool.getaddrinfo(host=hostname, port=443) # port is required
print("addrinfo", addrinfo)

ipaddr = addrinfo[0][4][0]

print(f"'{hostname}' ip address is '{ipaddr}'")
```


### Fetch a JSON file

Note: this is for boards with native WiFi (ESP32)

```py
import os
import time
import wifi
import socketpool
import ssl
import adafruit_requests

wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("my IP addr:", wifi.radio.ipv4_address)
pool = socketpool.SocketPool(wifi.radio)
session = adafruit_requests.Session(pool, ssl.create_default_context())
while True:
    response = session.get("https://todbot.com/tst/randcolor.php")
    data = response.json()
    print("data:",data)
    time.sleep(5)
```


### Serve a webpage via HTTP

Note: this is for boards with native WiFi (ESP32)

The [`adafruit_httpserver`](https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer) library
makes this pretty easy, and has good examples. You can tell it to either `server.serve_forver()`
and do all your computation in your `@server.route()` functions, or use `server.poll()` inside a while-loop.
There is also the [Ampule library](https://github.com/deckerego/ampule).

```py
# based on https://docs.circuitpython.org/projects/httpserver/en/latest/starting_methods.html
import socketpool
import wifi
from adafruit_httpserver import Request, Response, Server

WIFI_SSID="..."
WIFI_PASSWORD="..."
MY_PORT=8080

print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
MY_IP_ADDR = str(wifi.radio.ipv4_address)
print(f"Connected to {WIFI_SSID}")
print(f"My ip address: {MY_IP_ADDR}")
pool = socketpool.SocketPool(wifi.radio)

server = Server(pool, root_path="/static", debug=True)

@server.route("/")
def base(request: Request):
    return Response(request, "Hello from the CircuitPython HTTP Server!")

server.serve_forever(host=MY_IP_ADDR, port=MY_PORT)
```


### Set RTC time from NTP

Note: this is for boards with native WiFi (ESP32)

Note: You need to set `my_tz_offset` to match your region

```py
# copied from:
# https://docs.circuitpython.org/projects/ntp/en/latest/examples.html
import time, os, rtc
import socketpool, wifi
import adafruit_ntp

my_tz_offset = -7  # PDT

wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("Connected, getting NTP time")
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=my_tz_offset)

rtc.RTC().datetime = ntp.datetime

while True:
    print("current datetime:", time.localtime())
    time.sleep(5)
```

### Set RTC time from time service

Note: this is for boards with native WiFi (ESP32)

This uses the awesome and free [WorldTimeAPI.org site](http://worldtimeapi.org/pages/examples),
and this example will fetch the current local time (including timezone and UTC offset)
based on the geolocated IP address of your device.

```py
import time, os, rtc
import wifi, ssl, socketpool
import adafruit_requests

wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("Connected, getting WorldTimeAPI time")
pool = socketpool.SocketPool(wifi.radio)
request = adafruit_requests.Session(pool, ssl.create_default_context())

print("Getting current time:")
response = request.get("http://worldtimeapi.org/api/ip")
time_data = response.json()
tz_hour_offset = int(time_data['utc_offset'][0:3])
tz_min_offset = int(time_data['utc_offset'][4:6])
if (tz_hour_offset < 0):
    tz_min_offset *= -1
unixtime = int(time_data['unixtime'] + (tz_hour_offset * 60 * 60)) + (tz_min_offset * 60)

print(time_data)
print("URL time: ", response.headers['date'])

rtc.RTC().datetime = time.localtime( unixtime ) # create time struct and set RTC with it

while True:
  print("current datetime: ", time.localtime()) # time.* now reflects current local time
  time.sleep(5)
```

Also see [this more concise version from @deilers78](https://github.com/todbot/circuitpython-tricks/issues/14#issuecomment-1489181920).


### What the heck is `settings.toml`?

It's a config file that lives next to your `code.py` and is used to store
WiFi credentials and other global settings.  It is also used (invisibly)
by many Adafruit libraries that do WiFi.
You can use it (as in the examples above) without those libraries.
The settings names used by CircuitPython are documented in
[CircuitPython Web Workflow](https://docs.circuitpython.org/en/latest/docs/workflows.html#web).

Note: You can use any variable names for your WiFI credentials
(a common pair is `WIFI_SSID` and `WIFI_PASSWORD`), but if you use the
`CIRCUITPY_WIFI_*` names that will also start up the
[Web Workflow](https://docs.circuitpython.org/en/latest/docs/workflows.html#web)


You use it like this for basic WiFi connectivity:

```py
# settings.toml
CIRCUITPY_WIFI_SSID = "PrettyFlyForAWiFi"
CIRCUITPY_WIFI_PASSWORD = "mysecretpassword"

# code.py
import os, wifi
print("connecting...")
wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("my IP addr:", wifi.radio.ipv4_address)

```


### What the heck is `secrets.py`?
It's an older version of the `settings.toml` idea.
You may see older code that uses it.


## Displays (LCD / OLED / E-Ink) and displayio

[displayio](https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/#)
is the native system-level driver for displays in CircuitPython. Several CircuitPython boards
(FunHouse, MagTag, PyGamer, CLUE) have `displayio`-based displays and a
built-in `board.DISPLAY` object that is preconfigured for that display.
Or, you can add your own [I2C](https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/#displayio.I2CDisplay) or [SPI](https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/#displayio.FourWire) display.

### Get default display and change display rotation

Boards like FunHouse, MagTag, PyGamer, CLUE have built-in displays.
`display.rotation` works with all displays, not just built-in ones.

```py
import board
display = board.DISPLAY
print(display.rotation) # print current rotation
display.rotation = 0    # valid values 0,90,180,270
```

### Display an image

__Using `displayio.OnDiskBitmap`__

CircuitPython has a built-in BMP parser called `displayio.OnDiskBitmap`:
The images should be in non-compressed, paletized BMP3 format.
([how to make BMP3 images](#preparing-images-for-circuitpython))

```py
import board, displayio
display = board.DISPLAY

maingroup = displayio.Group() # everything goes in maingroup
display.root_group = maingroup # show our maingroup (clears the screen)

bitmap = displayio.OnDiskBitmap(open("my_image.bmp", "rb"))
image = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
maingroup.append(image) # shows the image
```

__Using `adafruit_imageload`__

You can also use the `adafruit_imageload` library that supports slightly more kinds of BMP files,
(but should still be [paletized BMP3 format](#preparing-images-for-circuitpython)
as well as paletized PNG and GIF files. Which file format to choose?
* BMP images are larger but faster to load
* PNG images are about 2x smaller than BMP and almost as fast to load
* GIF images are a little bigger than PNG but *much* slower to load


```py
import board, displayio
import adafruit_imageload
display = board.DISPLAY
maingroup = displayio.Group() # everything goes in maingroup
display.root_group = maingroup # set the root group to display
bitmap, palette = adafruit_imageload.load("my_image.png")
image = displayio.TileGrid(bitmap, pixel_shader=palette)
maingroup.append(image) # shows the image
```

__How `displayio` is structured__

CircuitPython's `displayio` library works like:
- an image `Bitmap` (and its `Palette`) goes inside a `TileGrid`
- a `TileGrid` goes inside a `Group`
- a `Group` is shown on a `Display`.



### Display background bitmap

Useful for display a solid background color that can be quickly changed.

```py
import time, board, displayio
display = board.DISPLAY         # get default display (FunHouse,Pygamer,etc)
maingroup = displayio.Group()   # Create a main group to hold everything
display.root_group = maingroup  # put it on the display

# make bitmap that spans entire display, with 3 colors
background = displayio.Bitmap(display.width, display.height, 3)

# make a 3 color palette to match
mypal = displayio.Palette(3)
mypal[0] = 0x000000 # set colors (black)
mypal[1] = 0x999900 # dark yellow
mypal[2] = 0x009999 # dark cyan

# Put background into main group, using palette to map palette ids to colors
maingroup.append(displayio.TileGrid(background, pixel_shader=mypal))

time.sleep(2)
background.fill(2)  # change background to dark cyan (mypal[2])
time.sleep(2)
background.fill(1)  # change background to dark yellow (mypal[1])
```

Another way is to use
[`vectorio`](https://docs.circuitpython.org/en/latest/shared-bindings/vectorio/index.html):

```py
import board, displayio, vectorio

display = board.DISPLAY  # built-in display
maingroup = displayio.Group()   # a main group that holds everything
display.root_group = maingroup  # put maingroup on the display

mypal = displayio.Palette(1)
mypal[0] = 0x999900
background = vectorio.Rectangle(pixel_shader=mypal, width=display.width, height=display.height, x=0, y=0)
maingroup.append(background)
```

Or can also use
[`adafruit_display_shapes`](https://docs.circuitpython.org/projects/display-shapes/en/latest/index.html):

```py
import board, displayio
from adafruit_display_shapes.rect import Rect

display = board.DISPLAY
maingroup = displayio.Group()   # a main group that holds everything
display.root_group = maingroup  # add it to display

background = Rect(0,0, display.width, display.height, fill=0x000000 ) # background color
maingroup.append(background)
```

### Image slideshow

```py
import time, board, displayio
import adafruit_imageload

display = board.DISPLAY      # get display object (built-in on some boards)
screen = displayio.Group()   # main group that holds all on-screen content
display.root_group = screen  # add it to display

file_names = [ '/images/cat1.bmp', '/images/cat2.bmp' ]  # list of filenames

screen.append(displayio.Group())  # placeholder, will be replaced w/ screen[0] below
while True:
    for fname in file_names:
        image, palette = adafruit_imageload.load(fname)
        screen[0] = displayio.TileGrid(image, pixel_shader=palette)
        time.sleep(1)
```

__Note:__ Images must be in palettized BMP3 format.
For more details, see [Preparing images for CircuitPython](#preparing-images-for-circuitpython)


### Dealing with E-Ink "Refresh Too Soon" error

E-Ink displays are damaged if refreshed too frequently.
CircuitPython enforces this, but also provides `display.time_to_refresh`,
the number of seconds you need to wait before the display can be refreshed.
One solution is to sleep a little longer than that and you'll never get the error.
Another would be to wait for `time_to_refresh` to go to zero, as show below.

```py
import time, board, displayio, terminalio
from adafruit_display_text import label
mylabel = label.Label(terminalio.FONT, text="demo", x=20,y=20,
                      background_color=0x000000, color=0xffffff )
display = board.DISPLAY  # e.g. for MagTag
display.root_group = mylabel
while True:
    if display.time_to_refresh == 0:
        display.refresh()
    mylabel.text = str(time.monotonic())
    time.sleep(0.1)
```

### Turn off REPL on built-in display 

If you have a board with a built-in display (like Feather TFT, Cardputer, FunHouse, etc),
CircuitPython will set up the display for you and print the REPL to it.
But if you want a more polished look for your project, you can turn off the REPL
from printing on the built-in display by putting this at at the top of both
your `boot.py` and `code.py`

```py
# put at top of both boot.py & code.py 
import board
board.DISPLAY.root_group = None
```


## I2C

### Scan I2C bus for devices
from:
[CircuitPython I2C Guide: Find Your Sensor](https://learn.adafruit.com/circuitpython-essentials/circuitpython-i2c#find-your-sensor-2985153-11)

```py
import board
i2c = board.I2C() # or busio.I2C(pin_scl,pin_sda)
while not i2c.try_lock():  pass
print("I2C addresses found:", [hex(device_address)
    for device_address in i2c.scan()])
i2c.unlock()
```

One liner to copy-n-paste into REPL for quicky I2C scan:

```py
import board; i2c=board.I2C(); i2c.try_lock(); [hex(a) for a in i2c.scan()]; i2c.unlock()
```

### Speed up I2C bus

CircuitPython defaults to 100 kHz I2C bus speed. This will work for all devices,
but some devices can go faster. Common faster speeds are 200 kHz and 400 kHz.

```py
import board
import busio
# instead of doing
# i2c = board.I2C()
i2c = busio.I2C( board.SCL, board.SDA, frequency=200_000)
# then do something with 'i2c' object as before, like:
oled = adafruit_ssd1306.SSD1306_I2C(width=128, height=32, i2c=i2c)
```

## Timing

### Measure how long something takes

Generally use `time.monotonic()` to get the current "uptime" of a board in fractional seconds.
So to measure the duration it takes CircuitPython to do something like:

```py
import time
start_time = time.monotonic()
# put thing you want to measure here, like:
import neopixel
stop_time = time.monotonic()
print("elapsed time = ", stop_time - start_time)
```

Note that on the "small" versions of CircuitPython in the QT Py M0, Trinket M0, etc.,
the floating point value of seconds will become less accurate as uptime increases.

### More accurate timing with `ticks_ms()`, like Arduino `millis()`

If you want something more like Arduino's `millis()` function, the `supervisor.ticks_ms()`
function returns an integer, not a floating point value. It is more useful for sub-second
timing tasks and you can still convert it to floating-point seconds for human consumption.

```py
import supervisor
start_msecs = supervisor.ticks_ms()
import neopixel
stop_msecs = supervisor.ticks_ms()
print("elapsed time = ", (stop_msecs - start_msecs)/1000)
```

### Control garbage collection for reliable timing

The CircuitPython garbage collector makes it so you don't have to deal with
memory allocations like you do in languages like C/C++. But when it runs, it can pause your
program for tens of milliseconds in some cases. For timing-sensitive applications,
you can exhibit some control over the garbage collector so it only runs when
you want it (like in the "shadow" after a timing-critical event)

Here's one way to do this.
```py
import gc
from adafruit_ticks import ticks_ms, ticks_add, ticks_less
gc.collect()  # collect any garbage before we...
gc.disable()  # disable automatic garbage collection
dmillis = 10  # how many millis between explicit gc
deadline = ticks_add(ticks_ms(), dmillis)
while True:
    now = ticks_ms()
    if ticks_diff(now, deadline) >= 0:
        deadline = ticks_add(now, dmillis)
        gc.collect()  # explicitly run a garbage collection cycle
    # do timing-sensitive thing here
```

### Converting milliseconds to seconds: 0.004 * 1000 != 4, sometimes

When doing timing-sensitive tasks in CircuitPython, you may have code that looks like this (say from the above):
```py
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

check_secs = 0.004  # check_secs is seconds between checks
check_millis = check_secs * 1000  # convert to millis
deadline = ticks_add(ticks_ms(), check_millis)
while True:
  now = ticks_ms()
  if ticks_less(now,deadline) >= 0:
    deadline = ticks_add(now, check_millis)
    do_periodic_task()  # do timing-critical thing every 'check_secs'
```
This seems more accurate than using `time.monotonic()` since it's using the millisecond-accurate `supervisor.ticks_ms` property, the timing resolution of CircuitPython.
This seems to work, until you pass in `check_secs = 0.004`, because the `ticks_*()` functions expect an integer and `int(0.004*1000) = 3`. If you were
using the above code to output an accurate timing signal, it's now going to be 25% off from what you expect. This is ultimately because [CircuitPython has reduced floating point precision (30-bit instead of 32-bit)](https://learn.adafruit.com/welcome-to-circuitpython/frequently-asked-questions#faq-3129274) ([further discusion here](https://github.com/adafruit/circuitpython/issues/9237)).
In short: stick to integer milliseconds.


## Board Info

### Get CPU speed (and set it!)

CircuitPython provides a way to get the microcontroller's CPU frequency with
[`microcontroller.cpu.frequency`](https://docs.circuitpython.org/en/latest/shared-bindings/microcontroller/index.html#microcontroller.Processor.frequency).

```py
import microcontroller
print("CPU speed:", microcontroller.cpu.frequency)
```

On some chips (most notably Pico P2040), you can also **set** this value. Overclock your Pico!
It's safe to double the RP2040 speed, Raspberry Pi officially supports up to 200 MHz.
CircuitPython will adjust its internal timings, but you should
do this change before creating any peripheral objects like UARTs or displays.

```py
import microcontroller
microcontroller.cpu.frequency = 250_000_000  # run at 250 MHz instead of 125 MHz
```


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

Another way is the `board.board_id`.  This is the "port" name used when 
compiling CircuitPython. To find a list of valid board IDs,
you can look in the circuitpython core repo inside of: "ports/[some_port]/boards/".
i.e. for espressif boards find the list of directories in: 
[ports/espressif/boards/](https://github.com/adafruit/circuitpython/tree/main/ports/espressif/boards).
The "board_id is used as the argument for 
`circuitpython_setboard` in [`circuitpython-stubs`](https://pypi.org/project/circuitpython-stubs/)

```py
import board
print(board.board_id)
'raspberry_pi_pico'
```

To get the chip family:

```py
import os
print(os.uname().sysname)
'ESP32S2'
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
    print("unsupported board", board_type)
  ```


## Computery Tasks

### Formatting strings
```py
name = "John"
fav_color = 0x003366
body_temp = 98.65
fav_number = 123
print("name:%s color:%06x temp:%2.1f num:%d" % (name,fav_color,body_temp,fav_number))
# 'name:John color:ff3366 temp:98.6 num:123'
```

### Formatting strings with f-strings
(doesn't work on 'small' CircuitPythons like QTPy M0)

```py
name = "John"
fav_color = 0xff3366
body_temp = 98.65
fav_number = 123
print(f"name:{name} color:{fav_color:06x} temp:{body_temp:2.1f} num:{fav_number}")
# 'name:John color:ff3366 temp:98.6 num:123'
```

### Using regular expressions to "findall" strings

Regular expressions are a really powerful way to match information in and parse data
from strings.  While CircuitPython has a version of the `re` regex module you may know
from desktop Python, it is very limited. Specifcally it doesn't have the very useful
`re.findall()` function.  Below is a semi-replacement for `findall()`.

```py
import re
def find_all(regex, some_str):
    matches = []
    while m := regex.search(some_str):
        matches.append( m.groups() )
        some_str = some_str[ m.end(): ] # get past match
    return matches

my_str = "<thing>thing1 I want</thing> <thing>thing2 I want</thing>  <thing>thing3 I want</thing>"
regex1 = re.compile('<thing.*?>(.*?)<\/thing>')
my_matches = find_all( regex1, my_str )
print("matches:", my_matches)

```


### Make and use a config file

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
# 'secret: 3a3d9bfaf05835df69713c470427fe35'
```

### Run different `code.py` on startup

Use `microcontroller.nvm` to store persistent state across
resets or between `boot.py` and `code.py`, and declare that
the first byte of `nvm` will be the `startup_mode`.
Now if you create multiple code.py files (say) `code1.py`, `code2.py`, etc.
you can switch between them based on `startup_mode`.

```py
import time
import microcontroller
startup_mode = microcontroller.nvm[0]
if startup_mode == 1:
    import code1      # runs code in `code1.py`
if startup_mode == 2:
    import code2      # runs code in `code2.py`
# otherwise runs 'code.py`
while True:
    print("main code.py")
    time.sleep(1)

```

**Note:** in CircuitPyton 7+ you can use [`supervisor.set_next_code_file()`](https://circuitpython.readthedocs.io/en/latest/shared-bindings/supervisor/index.html#supervisor.set_next_code_file)
to change which .py file is run on startup.
This changes only what happens on reload, not hardware reset or powerup.
Using it would look like:
```py
import supervisor
supervisor.set_next_code_file('code_awesome.py')
# and then if you want to run it now, trigger a reload
supervisor.reload()
```

## Coding Techniques

### Map an input range to an output range

```py
# simple range mapper, like Arduino map()
def map_range(s, a1, a2, b1, b2):
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

# example: map 0-0123 value to 0.0-1.0 value
val = 768
outval = map_range( val, 0,1023, 0.0,1.0 )
# outval = 0.75
```

### Constrain an input to a min/max
The Python built-in `min()` and `max()` functions can be used together
to make something like Arduino's `constrain()` to clamp an input between two values.

```py
# constrain a value to be 0-255
outval = min(max(val, 0), 255)
# constrain a value to be 0-255 integer
outval = int(min(max(val, 0), 255))
# constrain a value to be -1 to +1
outval = min(max(val, -1), 1)
```

### Turn a momentary value into a toggle

```py
import touchio
import board

touch_pin = touchio.TouchIn(board.GP6)
last_touch_val = False  # holds last measurement
toggle_value = False  # holds state of toggle switch

while True:
  touch_val = touch_pin.value
  if touch_val != last_touch_val:
    if touch_val:
      toggle_value = not toggle_value   # flip toggle
      print("toggle!", toggle_value)
  last_touch_val = touch_val
  ```

### Do something every N seconds without `sleep()`

Also known as "blink-without-delay"

```py
import time
last_time1 = time.monotonic()  # holds when we did something #1
last_time2 = time.monotonic()  # holds when we did something #2
while True:
  if time.monotonic() - last_time1 > 2.0:  # every 2 seconds
    last_time1 = time.monotonic() # save when we do the thing
    print("hello!")  # do thing #1
  if time.monotonic() - last_time2 > 5.0:  # every 5 seconds
    last_time2 = time.monotonic() # save when we do the thing
    print("world!")  # do thing #2

```

Note: a more accurate of this [uses `ticks_ms()`](#more-accurate-timing-with-ticks_ms-like-arduino-millis)
and maybe turning off gc / garbage collection.


## System error handling

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
import board, neopixel, rainbowio
leds = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.4 )
while True:
  try:
    rgb = rainbowio.colorwheel(int(time.monotonic()*75) % 255)
    leds.fill(rgb)
    time.sleep(0.05)
  except KeyboardInterrupt:
    print("shutting down nicely...")
    leds.fill(0)
    break  # gets us out of the while True
```

### Prevent auto-reload when CIRCUITPY is touched

Normally, CircuitPython restarts anytime the CIRCUITPY drive is written to.
This is great normally, but is frustrating if you want your code to keep running,
and you want to control exactly when a restart happens.

```py
import supervisor
supervisor.runtime.autoreload = False  # CirPy 8 and above
#supervisor.disable_autoreload()  # CirPy 7 and below
```

To trigger a reload, do a Ctrl-C + Ctrl-D in the REPL or reset your board.

### Raspberry Pi Pico boot.py Protection

Also works on other RP2040-based boards like QTPy RP2040.
From https://gist.github.com/Neradoc/8056725be1c209475fd09ffc37c9fad4

Also see [getting into Safe Mode with a REPL one-liner](#useful-repl-one-liners).

```py
# Copy this as 'boot.py' in your Pico's CIRCUITPY drive
# Useful in case Pico locks up (which it's done a few times on me)
import board
import time
from digitalio import DigitalInOut,Pull

led = DigitalInOut(board.LED)
led.switch_to_output()

safe = DigitalInOut(board.GP14)  # <-- choose your button pin
safe.switch_to_input(Pull.UP)

def reset_on_pin():
    if safe.value is False:
        import microcontroller
        microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
        microcontroller.reset()

led.value = False
for x in range(16):
	reset_on_pin()
	led.value = not led.value  # toggle LED on/off as notice
	time.sleep(0.1)

```


## Using the REPL

The "serial" REPL is the most useful diagnostic tools in CircuitPython.
Always have it open when saving your code to see any errors.
If you use a separate terminal program instead of an IDE, I recommend [`tio`](https://github.com/tio/tio).

### Display built-in modules / libraries
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

### Turn off built-in display to speed up REPL printing

By default CircuitPython will echo the REPL to the display of those boards with built-in displays.
This can slow down the REPL. So one way to speed the REPL up is to hide the `displayio.Group` that
contains all the REPL output.

```py
import board, displayio
board.DISPLAY.root_group = None  # turn off REPL printing
board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL  # turn back on REPL printing
```

In CircuitPython 8.x, you could do the below. In 9.x, the `root_group` is read-only
after it's been assigned. 

```py
import board
board.DISPLAY.root_group.hidden = True
board.DISPLAY.root_group.hidden = False  # to turn it back on
```

### Useful REPL one-liners

(yes, semicolons are legal in Python)

```py
# get into Safe Mode if you have REPL access
import microcontroller; microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE); microcontroller.reset()

# load common libraries (for later REPL experiments)
import time, board, analogio, touchio; from digitalio import DigitalInOut,Pull

# create a pin and set a pin LOW (if you've done the above)
pin = DigitalInOut(board.GP0); pin.switch_to_output(value=False)

# print out board pins and objects (like `I2C`, `STEMMA_I2C`, `DISPLAY`, if present)
import board; dir(board)

# print out microcontroller pins (chip pins, not the same as board pins)
import microcontroller; dir(microcontroller.pin)

# release configured / built-in display
import displayio; displayio.release_displays()

# turn off auto-reload when CIRCUITPY drive is touched
import supervisor; supervisor.runtime.autoreload = False

# test neopixel strip, make them all purple
import board, neopixel; leds = neopixel.NeoPixel(board.GP3, 8, brightness=0.2); leds.fill(0xff00ff)
leds.deinit()  # releases pin

# scan I2C bus
import board; i2c=board.I2C(); i2c.try_lock(); [hex(a) for a in i2c.scan()]; i2c.unlock()

```


## Python tricks

These are general Python tips that may be useful in CircuitPython.

### Create list with elements all the same value

```py
blank_array = [0] * 50   # creats 50-element list of zeros
```

### Convert RGB tuples to int and back again

Thanks to @Neradoc for this tip:

```py
rgb_tuple = (255, 0, 128)
rgb_int = int.from_bytes(rgb_tuple, byteorder='big')

rgb_int = 0xFF0080
rgb_tuple2 = tuple((rgb_int).to_bytes(3,"big"))

rgb_tuple2 == rgb_tuple
```

### Storing multiple values per list entry

Create simple data structures as config to control your program.
Unlike Arduino, you can store multiple values per list/array entry.

```py
mycolors = (
    # color val, name
    (0x0000FF, "blue"),
    (0x00FFFF, "cyan"),
    (0xFF00FF, "purple"),
)
for i in range(len(mycolors)):
    (val, name) = mycolors[i]
    print("my color ", name, "has the value", val)
```


## Python info

How to get information about Python inside of CircuitPython.

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

### Display the running CircuitPython release

With an established serial connection, press `Ctrl+c`:

```sh
Adafruit CircuitPython 7.1.1 on 2022-01-14; S2Pico with ESP32S2-S2FN4R2
>>>
```

Without connection or code running, check the `boot_out.txt` file in your CIRCUITPY drive.

```py
import os
print(os.uname().release)
'7.1.1'
print(os.uname().version)
'7.1.1 on 2022-01-14'
```

## Host-side tasks

Things you might need to do on your computer when using CircuitPython.

### Installing CircuitPython libraries

The below examples are for MacOS / Linux.  Similar commands are used for Windows

#### Installing libraries with `circup`

`circup` can be used to easily install and update modules

```sh
$ pip3 install --user circup
$ circup install adafruit_midi
$ circup update   # updates all modules
```

Freshly update all modules to latest version (e.g. when going from CP 6 -> CP 7)
(This is needed because `circup update` doesn't actually seem to work reliably)

```sh
circup freeze > mymodules.txt
rm -rf /Volumes/CIRCUITPY/lib/*
circup install -r mymodules.txt
```


And updating circup when a new version of CircuitPython comes out:
```sh
$ pip3 install --upgrade circup
```


#### Copying libraries by hand with `cp`

To install libraries by hand from the
[CircuitPython Library Bundle](https://circuitpython.org/libraries)
or from the [CircuitPython Community Bundle](https://github.com/adafruit/CircuitPython_Community_Bundle/releases) (which circup doesn't support), get the bundle, unzip it and then use `cp -rX`.

```sh
cp -rX bundle_folder/lib/adafruit_midi /Volumes/CIRCUITPY/lib
```

**Note:** on limited-memory boards like Trinkey, Trinket, QTPy, you must use the `-X` option on MacOS
to save space. You may also need to omit unused parts of some libraries (e.g. `adafruit_midi/system_exclusive` is not needed if just sending MIDI notes)


### Preparing images for CircuitPython

There's two ways to load images for use with `displayio`:
* The built-in [`displayio.OnDiskBitmap()`](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.OnDiskBitmap)
* The library [`adafruit_imageload`](https://docs.circuitpython.org/projects/imageload/en/latest/index.html)

`displayio.OnDisBitmap()`:
* can load "indexed" (aka "palette") non-compressed BMP3 images
* doesn't load image into RAM (great for TileGrids)

`adafruit_imageload`
* can load BMP3 images with RLE compression
* loads entire image into RAM (thus you may run out of memory)
* an load palette PNG images and GIF images
* PNG image loading is almost as fast as BMP and uses 1/2 the disk space
* GIF loading is very slow

To make images load faster generally, you can reduce the number of colors in the image.
The maximum number of colors is 256, but try reducing colors to 64 or even 2 if
it's a black-n-white image.

Some existing Learn Guides:
- https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics
- https://learn.adafruit.com/preparing-graphics-for-e-ink-displays

And here's some ways to do the conversions.


#### Online

Most online image converters do not create BMPs in the proper format:
BMP3, non-compressed, up to 256 colors in an 8-bit palette.

However @Neradoc found the site [convert2bmp](https://online-converting.com/image/convert2bmp/)
will work when you set "Color:" mode to "8 (Indexed)". Some initial tests show this works!
I'd recommend also trying out one of the following techniques too to have finer control.

The site https://cancerberosgx.github.io/magic/playground/ lets you
use any of the ImageMagick commands below to convert images. It's really handy if you can't
install ImageMagick locally.


#### Command-line: using ImageMagick

[ImageMagick](https://imagemagick.org/) is a command-line image manipulation tool. With it,
you can convert any image format to BMP3 format. The main ImageMagick CLI command is `convert`.

```sh
convert myimage.jpg -resize 240x240 -type palette -colors 64 -compress None BMP3:myimage_for_cirpy.bmp
```

You can also use this technique to create reduced-color palette PNGs:

```sh
convert myimage.jpg -resize 240x240 -type palette -colors 64 myimage.png
```

#### Command-line: using GraphicsMagick

[GraphicsMagick](http://www.graphicsmagick.org/) is a slimmer, lower-requirement
clone of ImageMagick. All GraphicsMagick commands are accessed via the `gm` CLI command.

```sh
gm convert myimage.jpg -resize 240x240 -colors 64 -type palette -compress None BMP3:myimage_for_cirpy.bmp
```

#### Making images smaller or for E-Ink displays

To make images smaller (and load faster), reduce number of colors from 256.
If your image is a monochrome (or for use with E-Ink displays like MagTag), use 2 colors.
The ["-dither" options](https://legacy.imagemagick.org/Usage/quantize/#colors)
are really helpful for monochrome:
```
convert cat.jpg -dither FloydSteinberg -colors 2 -type palette BMP3:cat.bmp
```


#### NodeJs: using gm

There is a nice wrapper around GraphicsMagick / Imagemagick with the [`gm library`](https://github.com/aheckmann/gm).
A small NodeJs program to convert images could look like this:

```js
var gm = require('gm');
gm('myimage.jpg')
    .resize(240, 240)
    .colors(64)
    .type("palette")
    .compress("None")
    .write('BMP3:myimage_for_cirpy.bmp', function (err) {
        if (!err) console.log('done1');
    });
```

#### Python: using PIL / pillow

The [Python Image Library (PIL) fork `pillow`](https://pillow.readthedocs.io/en/stable/index.html)
seems to work the best.  It's unclear how to toggle compression.

```py
from PIL import Image
size = (240, 240)
num_colors = 64
img = Image.open('myimage.jpg')
img = img.resize(size)
newimg = img.convert(mode='P', colors=num_colors)
newimg.save('myimage_for_cirpy.bmp')
```

### Preparing audio files for CircuitPython

CircuitPython can play both WAV files and MP3 files, but there are specific
variants of these files that will work better, as some options require much more
processor demand. WAV files are much easier to play but take up more disk space.

#### WAV files

For WAV files, I've found the best trade-off in quality / flash-space / compatibility to be:

- PCM 16-bit signed PCM
- Mono (but stereo will work if using I2S or SAMD51)
- 22050 Hz sample rate

And remember that these settings must match how you're setting up the `audiomixer` object.
So for the above settings, you'd create an `audiomixer.Mixer` like:

```py
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
```

To convert WAVs for CircuitPython, I like to use Audacity or the `sox` command-line tool.
Sox can convert just about any audio to the correct WAV format:

```sh
sox loop.mp3 -b 16 -c 1 -r 22050 loop.wav
```

#### MP3 files

MP3 files require a lot more CPU to decode so in general you will want to
re-encode MP3s to be a lower bit-rate and lower sample-rate.  These settings
seem to work okay on an lower-end chip like the Pico  /RP2040:

* 128 kbps data rate CBR or lower
* 22050 Hz sample rate or lower
* Mono

In `sox`, you can do this conversion with:

```sh
sox loop.mp3 -c 1 -r 22050 -C 128 loop_22k_128kbps.mp3
```


#### Getting sox

To get `sox` on various platforms:
- Linux: `sudo apt install sox libsox-fmt-mp3`
- macOS: `brew install sox`
- Windows: Use installer at http://sox.sourceforge.net/

Some audio Learn Guide links:
- https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out#play-a-wave-file-2994862-6
- https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/convert-files


### Circup hacks

[`circup`](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup?view=all)
is a great tool to help you install CircuitPython libraries. Think of it like `pip` or `npm` for CircuitPython.

#### Finding where `circup` stores its files

Instead of downloading the bundles by hand, `circup` has it already downloaded an unzipped.
Here's how to find that directory:

```sh
circup_dir=`python3 -c 'import appdirs; print(appdirs.user_data_dir(appname="circup", appauthor="adafruit"))'`
ls $circup_dir
```

### Building CircuitPython

If you want to build CircuitPython yourself, you can! It's not too bad.
There's a very good ["Building CircuitPython" Learn Guide](https://learn.adafruit.com/building-circuitpython/build-circuitpython) that I refer to all the time, since it goes through the main reasons
why you might want to build your own version of CircuitPython, including:
- Adding "Frozen" Modules (libraries built-in to the firmware)
- Setting different SPI flash chips (if your custom board uses a different kind of flash)
- Adding a new board to CircuitPython

But if you just want a quick list of the commands to use to build, here's what I use
(as of Jun 2024) to build CircuitPython for rp2040.

```sh
git clone https://github.com/todbot/circuitpython circuitpython-todbot
cd circuitpython-todbot
pip3 install --upgrade -r requirements-dev.txt  # do occasionally, after 'git pull'
pip3 install --upgrade -r requirements-doc.txt  # do occasionally, after 'git pull'
cd ports/raspberrypi
make fetch-port-submodules     # takes a long time the first time ran, do after 'git pull' too
make BOARD=raspberry_pi_pico   # or other board name listed in ports/raspberrypi/boards/
# make -C ../../mpy-cross  # if you need mpy-cross
```

And for Espressif / ESP32 builds:

```sh
git clone https://github.com/todbot/circuitpython circuitpython-todbot
cd circuitpython-todbot
pip3 install --upgrade -r requirements-dev.txt  # do occasionally, after 'git pull'
pip3 install --upgrade -r requirements-doc.txt  # do occasionally, after 'git pull'
cd ports/espressif
make fetch-port-submodules     # takes a long time the first time ran, do after 'git pull' too
./esp-idf/install.sh
. ./esp-idf/export.sh
pip3 install --upgrade -r requirements-dev.txt  # because now we're using a new python
pip3 install --upgrade -r requirements-doc.txt  # because now we're using a new python
make BOARD=adafruit_qtpy_esp32s3
```

Note, this assumes you've [already installed the system-level prerequisites](https://learn.adafruit.com/building-circuitpython/introduction).
On MacOS, this is what I do to get those:

```sh
brew install git git-lfs python3 gettext uncrustify cmake
brew install gcc-arm-embedded   # (the cask, not 'arm-none-eabi-gcc')
```

## About this guide

* Many of the code snippets are not considered "well-formatted"
by Python linters. This guide favors brevity over strict style adherence.

* The precursor to this guide is [QTPy Tricks](https://github.com/todbot/qtpy-tricks),
which has similar but different (and still valid) fun things to do in CircuitPython.

* This guide is the result of trying to learn Python via CircuitPython and
from very enlightening discussions with John Edgar Park.  I have a good background in
other languages, but mostly C/C++, and have
[taught classes in Arduino](https://todbot.com/blog/bionicarduino/) for several years.
This informs how I've been thinking about things in this guide.
