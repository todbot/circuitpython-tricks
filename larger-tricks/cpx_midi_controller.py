# quick-n-dirty MIDI controller with Circuit Playground Express
# 30 Apr 2024 - @todbot / Tod Kurt
# Works on Circuit Playground Express in CircuitPython 9, 
#  but will also work on also any board with touchio, like Trinket M0 or QTPy M0
# Uses the minimal number of libraries to save RAM on the tiny M0 in the CPX
#  (e.g. cannot load `adafruit_circuitpython`, `adafruit_midi`, and `adafruit_debouncer` on CPX)

import board
import touchio
import usb_midi
import neopixel

# which MIDI notes to send
midi_notenums = (40, 41, 42, 43)

# which pins for each of the above notes
touch_pins = (board.A1, board.A2, board.A3, board.A4)

# which MIDI channel to transmit on
midi_out_channel = 1

# set up the status byte constants for sending MIDI later
note_on_status = (0x90 | (midi_out_channel-1))
note_off_status = (0x80 | (midi_out_channel-1))

# get a MIDI out port
midi_out = usb_midi.ports[1]
# make ready the neopixels so we can blink when a pad is touched
leds = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)

# set up the touch pins
touchins = []
for i, pin in enumerate(touch_pins):
    touchins.append( touchio.TouchIn(pin) )
last_touch = [False] * len(touchins)

print("Welcome! Touch a pad!")
while True:
    for i, touchin in enumerate(touchins):
        touch = touchin.value          # get current touch value
        if touch != last_touch[i]:     # was there a change in touch?
            last_touch[i] = touch      # save for next time
            notenum = midi_notenums[i] # get MIDI note for this pad
            if touch                 : # pressed!
                print("touch!", i)
                midi_out.write(bytearray([note_on_status, notenum, 127]))
                leds.fill(0x330044)
            else:
                print("release!",i)
                midi_out.write(bytearray([note_off_status, notenum, 0]))
                leds.fill(0)
