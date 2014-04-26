#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


def differences(path1, path2, show_differences=False):
    """
    Pass two .gbc files as arguments. Function will check, byte by byte,
    if two roms have the same data in same offsets. In case of difference,
    print out the offset (decimal) and values of bytes. In the end, print
    out total amount of differences.
    """
    total = 0

    with open(path1, 'rb') as rom:
        data1 = rom.read()
    with open(path2, 'rb') as rom:
        data2 = rom.read()

    for n, (i, j) in enumerate(zip(data1, data2)):
        if i != j:
            if show_differences:
                print('n %s,   %s != %s' % (n, i, j))
            total += 1
    print('Total differences: %s' % (total))

if __name__ == '__main__':
    """
    Usage:
    $ python3 diff_roms.py ***.gbc ***.gbc
    """
    if len(sys.argv) > 2:
        differences(sys.argv[1], sys.argv[2])