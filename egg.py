# -*-coding: utf-8 -*-

import time
import subprocess

from winsound import Beep


def a():
    egg = input('Thanks for using this software!\nPress Enter to exit...\n')

    x1 = '''
    00        00  
  0000        0000
  000000    000000
  0000000000000000
  00    0000    00
  0000  0000  0000
    000000000000  
    000000000000  
        0000      
'''
    #     x2 = '''
    # \033[34m    00        00
    #   0000        0000\n");
    #   0000\033[31m00    00\033[34m0000
    #   00\033[31m0000\033[34m0000\033[31m0000\033[34m00
    #   00    0000    00
    #   00\033[31m00\033[34m  0000  \033[31m00\033[34m00
    #     00\033[31m00\033[34m0000\033[31m00\033[34m00
    #     00\033[31m00\033[34m0000\033[31m00\033[34m00
    #         0000
    # \033[0m'''
    x3 = '''
  00000000  00        00  00000000
  00                            00
  00          00000000          00
  00      0000  0000  0000      00
        0000            0000
  00    00    00    00    00    00
      00    000000000000    00
      0000      0000      0000
      0000  00  0000  00  0000
      00      00000000      00
  00    00  00  0000  00  00    00
        0000            0000
  00      0000  0000  0000      00
  00          00000000          00
  00                            00
  00000000  00        00  00000000

  0  0  00  000  00   00  000  000
  0  0 0  0 0 0 0  0 0  0 0  0 0
  0  0 0  0 00  0    0  0 0  0 00
   0 0 0000 0 0 0  0 0000 0  0 0
    0  0  0 0 0  00  0  0 000  000
'''
    x4 = '''
\033[34m  00000000  \033[31m00        00\033[34m  00000000
  00                            00
  00          00000000          00
  00      \033[31m0000\033[34m  0000  \033[31m0000\033[34m      00
\033[31m        0000            0000
  00    00    00    00    00    00
\033[34m      00    \033[31m0000\033[34m0000\033[31m0000\033[34m    00
      0000      0000      0000
      0000  \033[31m00\033[34m  0000  \033[31m00\033[34m  0000
      00      \033[31m00\033[34m0000\033[31m00\033[34m      00
\033[31m  00    00\033[34m  00  0000  00  \033[31m00    00
        0000            0000
\033[34m  00      \033[31m0000\033[34m  0000  \033[31m0000\033[34m      00
  00          00000000          00
  00                            00
  00000000  \033[31m00        00\033[34m  00000000

  0  0 \033[31m 00  000  00 \033[34m  00  000  000
  0  0 \033[31m0  0 0 0 0  0\033[34m 0  0 0  0 0
  0  0 \033[31m0  0 00  0   \033[34m 0  0 0  0 00
   0 0 \033[31m0000 0 0 0  0\033[34m 0000 0  0 0
    0  \033[31m0  0 0 0  00 \033[34m 0  0 000  000
\033[0m'''

    egg = str.lower(egg)
    if 'voxel' and 'arcade' in egg:
        time.sleep(0.5)
        subprocess.Popen('cls', shell=True)
        time.sleep(0.5)
        print("It seems that you've pressed the name of a studio.")
        time.sleep(2)
        print('"Voxel Arcade"... Nice.')
        time.sleep(1.5)
        print("Well, It's time to show you something.")
        time.sleep(2)
        print('Please wait...')
        b(x3, x4)
    elif '726' in egg or 'voxel' in egg or 'arcade' in egg:
        time.sleep(1)
        subprocess.Popen('cls', shell=True)
        time.sleep(1)
        print('WARNING - SPECIAL CODE DETECTED!!!')
        time.sleep(1.5)
        print(x1)
        time.sleep(0.5)
        print('Preparing to exit...')
        time.sleep(1.5)
        return None


def b(x, y):
    time.sleep(2.5)
    subprocess.Popen('cls', shell=True)

    Beep(523, 500)
    print("I think you've heard it many times.\n")
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    print('We all have dreams, though there are tons of difficulties.\n')
    Beep(784, 1000)
    Beep(784, 500)
    Beep(698, 500)
    Beep(880, 1000)
    Beep(784, 500)

    Beep(523, 500)
    print("As we're chasing them...\n")
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    print('WE')
    Beep(784, 1000)
    print('ARE')
    Beep(784, 500)

    print('ALL')
    Beep(698, 500)
    print('BECOMING')
    Beep(932, 500)
    print('STRONGER')
    Beep(1046, 500)
    print('AS WELL AS')
    Beep(880, 500)
    print('GROWING')
    Beep(784, 500)
    print('UP...\n')
    Beep(698, 3000)
    print('Yeah, something will never change.\n')
    Beep(659, 1000)
    Beep(784, 1000)
    Beep(784, 1000)
    Beep(698, 1000)

    print('Our hearts to...\n')
    Beep(932, 1500)
    Beep(880, 500)
    Beep(784, 1500)
    print('...CRAFT.\n')
    Beep(698, 500)
    Beep(698, 3000)

    subprocess.Popen('cls', shell=True)
    time.sleep(1.5)
    print(x)
    time.sleep(0.75)
    subprocess.Popen('cls', shell=True)
    print(y)
    time.sleep(0.75)
    subprocess.Popen('cls', shell=True)
    print(x)
    time.sleep(0.75)
    subprocess.Popen('cls', shell=True)
    print(y)
    time.sleep(0.75)
