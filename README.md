
# circuitpython-tricks



* Determine which board you're on:
```
import os
print(os.uname().machine)
'Adafruit ItsyBitsy M4 Express with samd51g19'
```


* Hook a pot to pin A1, use as a knob:
```
import board
import analogio
potknob = analogio.AnalogIn(board.A1)
position = potknob.value  # ranges from 0-65535

pos = potknob.value // 256  # make 0-255 range

```

* Read a touch pin
```
import touchio
import board
touch_pin = touchio.TouchIn(board.GP6)
# on Pico / RP2040, need 1M pull-down on each input
```
