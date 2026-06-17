#!/usr/bin/env python3
import subprocess
import curses
import time
import sys



def sec2hms(sec):
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return [h, m, s]



def sec2hhmmss(sec):
    h, m, s = sec2hms(sec)
    hh = str(h).rjust(2, '0')
    mm = str(m).rjust(2, '0')
    ss = str(s).rjust(2, '0')
    return [hh, mm, ss]



def char2bit(char):
    CHAR = {
        '0': '111101101101111',
        '1': '110010010010111',
        '2': '111001111100111',
        '3': '111001111001111',
        '4': '101101111001001',
        '5': '111100111001111',
        '6': '111100111101111',
        '7': '111101101001001',
        '8': '111101111101111',
        '9': '111101111001111',
        ':': '000010000010000',
    }
    return CHAR[char]



def main(stdscr):
    # args
    if len(sys.argv) == 2:
        try: seconds = abs(int(sys.argv[1]))
        except: return 'ERROR: it is not int arg for seconds'
    else:
        return 'ERROR: enter int arg for seconds'

    # setup
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)
    DELAY = 1
    

    while True:
        # clear
        stdscr.clear()

        # state update
        height, width = stdscr.getmaxyx()
        width //= 2 # for react pixel
        mid_y, mid_x = height // 2, width // 2
        end_y, end_x = height - 1, width - 1
        hh, mm, ss = sec2hhmmss(seconds)
        hhmmss = ':'.join([hh, mm, ss])
        lenght = 4 * (len(hh) + 6) - 1
        i_x = -lenght // 2
        i_y = -2

        # render
        try: stdscr.addstr(end_y, 0, '[q - exit]')
        except: pass

        for i, char in enumerate(hhmmss):
            char_bit = char2bit(char)
            for d_y in range(5):
                for d_x in range(3):
                    y = mid_y + i_y + d_y
                    x = 2 * (mid_x + i_x + d_x + i * 4 + 1)
                    
                    l = d_y * 3 + d_x
                    if char_bit[l] == '1':
                        try:
                            stdscr.addstr(y, x, '[')
                            stdscr.addstr(y, x+1, ']')
                        except: pass

        # keypad event
        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]: return

        # update
        stdscr.refresh()
        time.sleep(1)

        # alarm
        if seconds <= 0: subprocess.run(["paplay", "alarm.wav"])
        else: seconds -= 1



if __name__ == '__main__':
    exit_msg = curses.wrapper(main)
    if exit_msg: print(exit_msg)