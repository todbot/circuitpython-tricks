#!/bin/zsh

# make a bunch of test waves
NOTE_START=32
NOTE_END=60
WAVE_TYPE=sin

for n in $(seq $NOTE_START $NOTE_END) ; do
    freq=$(( (440.0/32.0) * (2**(($n-9.0)/12.0)) ))  # midi to hz
    fn=`printf "%03d.wav" ${n}`
    printf "note:%2d freq:%4.1f fn:%s\n" $n $freq $fn
    sox -V -r 22050 -n -b 16 -c 1 $fn synth 1 $WAVE_TYPE $freq vol -10dB
done
