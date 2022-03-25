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

print("chikkenplayer ready")

edit_voices = [False] * len(wav_files)
pickup_voices = [False] * len(wav_files)

while True:
  event = keys.events.get()
  if event:
    voice_num = event.key_number
    if event.pressed:
      edit_voices[voice_num] = True
    if event.released:
      edit_voices[voice_num] = False
      pickup_voices[voice_num] = False

  for i in range(len(wav_files)):
    new_val = knob.value
    if edit_voices[i]:  # only edit voices with pressed buttons
      if pickup_voices[i]:  # have we crossed old value?
        mixer.voice[i].level = new_val / 65535 # convert to 0-1.0
      else:
        old_val = int(mixer.voice[i].level * 65535) # convert 0-1 to 0-65535
        if abs(new_val - old_val) < 100: # if we get close to old value,
          pickup_voices[i] = True        # flip the pickup switch until key release
