#
# midi_forward.py -- forward MIDI between MIDI USB and MIDI serial
#
# 8 Jan 2022 - @todbot / Tod Kurt
#

import time
import board
import busio
import usb_midi
import adafruit_midi

print("Hello World!")

midi_usb = adafruit_midi.MIDI( midi_in=usb_midi.ports[0],
                               midi_out=usb_midi.ports[1] )

class MIDI_Forward:
    def __init__(self, serial_tx_pin=board.TX, serial_rx_pin=board.RX, timeout=0.01):
        uart = busio.UART(tx=serial_tx_pin, rx=serial_rx_pin,
                          baudrate=31250, timeout=timeout)
        self.midiusb_in = usb_midi.ports[0]
        self.midiusb_out = usb_midi.ports[1]
        self.midiser_in  = uart
        self.midiser_out = uart

    def forward(self):
        bytes_usb = self.midiusb_in.read(30)  # 30 from adafruit_midi
        if bytes_usb:
            self.midiser_out.write(bytes_usb, len(bytes_usb))
        bytes_ser = self.midiser_in.read(30)
        if bytes_ser:
            selfmidiusb_out.write(bytes_ser, len(bytes_ser))

# can specify 'serial_tx_pin=' and 'serial_rx_pin=', or accept defaults
midi_forward = MIDI_Forward()

while True:
    midi_forward.forward()
