import keyboard
import winsound
import argparse
import operator

# https://github.com/boppreh/keyboard

parser = argparse.ArgumentParser(description='Keyboard Sound Args')
parser.add_argument(
    '-bf', type=int, help='base frequenzy (default = 20hz)', default=20)
parser.add_argument(
    '-sl', type=int, help='sound length (default = 50m)', default=50)
parser.add_argument(
    '-bo', type=str, help='beep on (up, down, both - default = up)', default='up')
parser.add_argument(
    '-scm', type=int, help='scan code multiplier', default=1)
parser.add_argument(
    '-bfm', type=str, help='base frequenzy operator (+, -, *, / - default = *)', default='*')

args = parser.parse_args()
ops = {"+": operator.add, "-": operator.sub,
       "*": operator.mul, "/": operator.truediv}


def keyPressed(event):
    if event.event_type == args.bo or args.bo == 'both':
        winsound.Beep(
            int(max(37, min(ops[args.bfm](args.bf, (event.scan_code * args.scm)), 32767))), args.sl)


keyboard.hook(keyPressed)
keyboard.wait()
