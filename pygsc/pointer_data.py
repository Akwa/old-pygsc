#! /usr/bin/env python3
# -*- coding: utf-8 -*-

versions = {
            b'POKEMON_GL': 'Gold',
            b'POKEMON_SL': 'Silver',
            b'PM_CRYSTAL': 'Crystal'
            }

pointers = {
            'Gold': {
                     'evomoves': 0x427bd,
                     'basestats': 0x51b0b,
                     'moves': 0x41afe,
                     'palettes': 0xad45,
                     'names': 0x1b0b74,
                     'movenames': 0x1b1574,
                     'tms': 0x11a66,
                     },
            'Silver': {
                       'evomoves': 0x427bd,
                       'basestats': 0x51b0b,
                       'moves': 0x41afe,
                       'palettes': 0xad45,
                       'names': 0x1b0b74,
                       'movenames': 0x1b1574,
                       'tms':0x11a66,
                       },
            'Crystal': {
                        'evomoves': 0x425b1,
                        'basestats': 0x51424,
                        'moves': 0x41afb,
                        'palettes': 0xa8d6,
                        'names': 0x53384,
                        'movenames': 0x1c9f29,
                        'tms': 0x1167a,
                        }
            }

