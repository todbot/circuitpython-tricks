# pin_state.py -- look at state of all pins in `board`
# 6 Jul 2022 - @todbot / Tod Kurt
#
import time, board, microcontroller, digitalio

def get_pin_states():
    pin_states = {}
    for name in sorted(dir(board)):
        maybe_pin = getattr(board, name)
        if isinstance(maybe_pin, microcontroller.Pin):
            try:
                test_pin = digitalio.DigitalInOut( maybe_pin )
                test_pin.direction = digitalio.Direction.INPUT
                pin_states[ name ] = test_pin.value
            except:
                pin_states[ name ] = None  # in use
            
    return pin_states

while True:
    pin_states = get_pin_states()
    for name,value in pin_states.items():
        print(f"{name:<15} = {value}")
    time.sleep(1)
