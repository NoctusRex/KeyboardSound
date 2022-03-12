import keyboard
import winsound
import argparse
import operator
import random
import math

# https://github.com/boppreh/keyboard

parser = argparse.ArgumentParser(description='Keyboard Sound Args')
parser.add_argument(
    '-bf', type=int, help='base frequency in hz (min 37, max 32767 - default = 65hz)', default=65)
parser.add_argument(
    '-sd', type=int, help='sound duration in ms (default = 50ms)', default=50)
parser.add_argument(
    '-bo', type=str, help='beep on (up, down, both - default = up)', default='up')
parser.add_argument(
    '-scm', type=float, help='scan code multiplier (default = 1)', default=1)
parser.add_argument(
    '-bfo', type=str, help='base frequency operator (+, -, *, / - default = *)', default='*')
parser.add_argument(
    '-r', type=bool, help='use random parameters (default = false)', default=False)
args = parser.parse_args()

ops = {'+': operator.add, '-': operator.sub,
       '*': operator.mul, '/': operator.truediv}
beepModes = ['up', 'down', 'both']
baseFrequency = args.bf
soundDuration = args.sd
beepOn = args.bo
scanCodeMultiplier = args.scm
baseFrequencyOperator = args.bfo
randomParameters = args.r

if randomParameters:
    baseFrequency = random.randrange(37, 32768)
    soundDuration = random.randrange(20, 100)
    beepOn = random.choice(beepModes)
    scanCodeMultiplier = random.randrange(1, 100)
    baseFrequencyOperator = random.choice(list(ops))

print('---------PARAMETERS-----------')
print('base frequency:', baseFrequency)
print('sound duration:', soundDuration)
print('beep on:', beepOn)
print('scan code multiplier:', scanCodeMultiplier)
print('base frequenzy operator:', baseFrequencyOperator)
print('use random parameters:', randomParameters)
print('---------LAST BEEP-----------')


def keyPressed(event):
    if event.event_type == beepOn or beepOn == beepModes[2]:
        frequency = int(max(37, min(ops[baseFrequencyOperator](
            baseFrequency, (event.scan_code * scanCodeMultiplier)), 32767)))
        winsound.Beep(frequency, soundDuration)

        print('key:', str.ljust(event.name + ' - (' + str(event.scan_code) + ')', 20, ' '), 'freqency:', str.ljust(str(frequency) +
              ' hz', 8, ' '), 'note:', str.ljust(str(frequency_to_note(frequency)), 10, ' '), end='\r')


def frequency_to_note(frequency):
    # https://stackoverflow.com/questions/64505024/turning-a-frequency-into-a-note-in-python
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    OCTAVE_MULTIPLIER = 2
    KNOWN_NOTE_NAME, KNOWN_NOTE_OCTAVE, KNOWN_NOTE_FREQUENCY = ('A', 4, 440)

    note_multiplier = OCTAVE_MULTIPLIER**(1/len(NOTES))
    frequency_relative_to_known_note = frequency / KNOWN_NOTE_FREQUENCY
    distance_from_known_note = round(
        math.log(frequency_relative_to_known_note, note_multiplier))

    known_note_index_in_octave = NOTES.index(KNOWN_NOTE_NAME)
    known_note_absolute_index = KNOWN_NOTE_OCTAVE * \
        len(NOTES) + known_note_index_in_octave
    note_absolute_index = known_note_absolute_index + distance_from_known_note
    note_octave, note_index_in_octave = note_absolute_index // len(
        NOTES), note_absolute_index % len(NOTES)
    note_name = NOTES[note_index_in_octave]
    return (note_name, note_octave)


keyboard.hook(keyPressed)
keyboard.wait()
