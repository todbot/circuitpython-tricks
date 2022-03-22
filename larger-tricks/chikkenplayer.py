# chikkenplayer.py - StreetChicken Remixer by todbot
# 21 Mar 2021 - @todbot / Tod Kurt, from @jedgarpark idea
#
import time
import board
import analogio
import keypad
import audiocore
import audiomixer
from audiopwmio import PWMAudioOut as AudioOut

time.sleep(5) # wait a bit to reduce noise from CIRCUITPY access

wav_files = (
    "wav/chikken1_161_22k16b.wav", # slowed down & hacked StreetChicken
    "wav/chikken2_161_22k16b.wav", # fat distorty bassline
    "wav/chikken3_161_22k16b.wav", # reversed & slowed & warped StreetChicken
    "wav/chikken4_161_22k16b.wav", # 808 drum pattern (kick + snare only)
    "wav/chikken5_161_22k16b.wav", # chunky guitar power chords
    "wav/chikken6_161_22k16b.wav", # ethereal space arpeggios
)

# knob to adjust loop levels
knob = analogio.AnalogIn(board.A3)
# what keys to use 
keys = keypad.Keys((board.RX, board.SCK, board.MISO, board.MOSI, board.SCL, board.SDA),
                   value_when_pressed=False, pull=True)
# audio output
audio = AudioOut(board.TX) # board.A0 for SAMD chips, any for rp2040 pico
mixer = audiomixer.Mixer(voice_count=len(wav_files), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback, play with mixer.voice[n].play()

# start loops playing, but silently
for i in range(len(wav_files)):
  wave = audiocore.WaveFile(open(wav_files[i],"rb"))
  mixer.voice[i].play(wave, loop=True)
  mixer.voice[i].level = 0.0

print("chikenplayer ready")
voice_num = None  # which loop level to change if any
while True:
  event = keys.events.get()
  if event:
    if event.pressed:  voice_num = event.key_number
    if event.released: voice_num = None
  if voice_num is not None:  # while voice key is pressed, adjust level
    val = knob.value
    mixer.voice[voice_num].level = val / 65535 # convert to 0-1.0

