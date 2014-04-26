#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pygsc import rom_class
from pygsc.test import diff_roms

"""
We want to check if the tool is stable.
In order to do so, we will load the .gbc file we want, and change some data.
Then, we will save changes and check differences between base and changed rom.
The differences between roms should happen in exact spots and their amount
should be small.
"""

def test_1(path1, path2):
    Data = rom_class.Rom(path1, path2)

    """
    No getter/setter functions yet, so basic assignment operators are used.
    """

    """Change some data"""
    # Change Bulbasaur name to Bulbosour
    Data.pokemon['BULBASAUR'].name = 'BULBASOUR'
    # Change Celebi type to Normal
    Data.pokemon['CELEBI'].types = [0, 0]
    # Make Ditto evolve into Bulbasaur at level 10
    bulbasaur = Data.pokemon.name_map['BULBASAUR']
    Data.pokemon['DITTO'].evos.append([1, 10, bulbasaur])
    # Make Magikarp learn Hyper Beam at level 5
    hyper_beam = Data.moves.name_map['HYPER BEAM']
    Data.pokemon['MAGIKARP'].moves.append([5, hyper_beam])
    # Change Pound power to 100
    Data.moves['POUND'].power = 100
    # Change Pound name to Pwned
    Data.moves['POUND'].name = 'PWNED'

    """Save our data """
    Data.save_data()

    """
    Amount of differences should be:
    2621 for G/S
    2632 for C
    """
    diff_roms.differences(path1, path2)
    print('Proper amount for original silver/gold: %s' % (2621))
    print('Proper amount for original crystal: %s' % (2632))

if __name__ == '__main__':

    """ Initialize our Rom class """
    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            sys.argv.append('test1.gbc')
        test_1(sys.argv[1], sys.argv[2])
