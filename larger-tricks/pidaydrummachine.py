# pidaydrummachine.py - Pi Day Drum Machine
# 14 Mar 2021 - @todbot / Tod Kurt
# samples from: https://freesound.org/people/BaDoink/packs/30682/
#
import time
import board
import keypad
import audiocore
import audiomixer
from audiopwmio import PWMAudioOut as AudioOut

time.sleep(3) # wait a bit to reduce noise from CIRCUITPY access

wav_files = (
    "wav/544413_punch_22k16b.wav",
    "wav/544682_snare_22k16b.wav",
    "wav/544684_dubhat1_22k16b.wav",
    "wav/544694_toggle_22k16b.wav",
    "wav/544587_splash1a_22k16b.wav",
)

# what keys to use as our drum machine
keys = keypad.Keys((board.GP16, board.GP17, board.GP18, board.GP19, board.GP20),
                   value_when_pressed=False, pull=True)

audio = AudioOut(board.GP15)
mixer = audiomixer.Mixer(voice_count=len(wav_files), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback, play with mixer.voice[n].play()

while True:
  event = keys.events.get()
  if event and event.pressed:
      n = event.key_number
      mixer.voice[n].play( audiocore.WaveFile(open(wav_files[n],"rb")) )




      
