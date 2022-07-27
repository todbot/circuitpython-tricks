# robust_keyboard_code.py -- demonstrate how to deal with USB disconnect on startup and while running
# 27 Jul 2022 - @todbot / Tod Kurt

import supervisor
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

def usb_connected(): return supervisor.runtime.usb_connected

if usb_connected():  # only attempt keyboard creation if USB 
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)

# make up some buttons. This is for a FunHouse, but could be any keys
buttons = []
for pin in (board.BUTTON_UP, board.BUTTON_SELECT, board.BUTTON_DOWN):
    switch = digitalio.DigitalInOut(pin)
    switch.pull = digitalio.Pull.DOWN # defaults to input
    buttons.append(switch)

# what keycodes to send for each button
keys = [Keycode.A, Keycode.B, Keycode.C]

while True:
    print("usb:", usb_connected(), "buttons:", [b.value for b in buttons] )
    for i in range(len(buttons)):
        if buttons[i].value:
            if usb_connected():
                try:
                    keyboard.send( keys[i] ) 
                except OSError:  # also if USB disconnected 
                    pass
       
    time.sleep(0.1)
