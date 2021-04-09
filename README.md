
# circuitpython-tricks


## Common Tasks

### Inputs

* Read an digital input as a Button
  ```py
  import board
  from digitalio import DigitalInOut, Pull
  button = DigitalInOut(board.D3) # defaults to input
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

### Outputs

* Output HIGH / LOW on a pin (like an LED)
  ```py
  import board
  import digitalio
  ledpin = digitalio.DigitalInOut(board.D2)
  ledpin.direction = digitalio.Direction.OUTPUT
  ledpin.value = True
  ```

* Output Analog value on a DAC pin
  ```py
  import board
  import analogio
  dac = analogio.AnalogOut(board.D1)
  dac.value = 32768   # mid-point of 0-65535
  ```

* Output a "Analog" value on a PWM pin
  ```py
  import board
  import pwmio
  out1 = pwmio.PWMOut(board.MOSI, frequency=25000, duty_cycle=0)
  out1.out1.duty_cycle = 32768  # mid-point 0-65535 = 50 % duty-cycle
  ```
    
### USB

* Print to USB Serial
  ```py
  print("hello there")  # prints a newline
  print("waiting...", end='')   # does not print newline
  ```

* Read user input from USB Serial, non-blocking
  ```py

  ```

## More Esoteric Tasks

* Time how long something takes:
  ```py
  import time
  start_time = time.monotonic() # fraction seconds uptime
  do_something()
  elapsed_time = time.monotonic() - start_time
  print("do_something took %f seconds" % elapsed_time)
  ```

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
  ```py
  ```

* RasPI boot.py protection.
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

