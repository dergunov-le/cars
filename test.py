import os
import time
import random
import msvcrt

os.system("")

orange, red, green, blue, yellow, reset, reset_all = \
    '\033[38;2;255;128;0m', '\033[31m', '\033[32m', '\033[34m', '\033[33m', '\033[39m', '\033[0m'
code = [31, 32, 33, 34, 35, 36, 37, 91, 92, 93, 94, 95, 97]

print()
a = ord('А')
for i in range(a, a + 32):
    print(f'{chr(155)}{random.choice(code)};1m{chr(i)}', flush=True, end=" ")
    time.sleep(.1)

print(f'\n{orange}Для выхода нажмите любую клавишу{reset_all}')

_key_ = ord(msvcrt.getch())
if _key_:
    print('[ВЫХОД]')
