#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import constants as c
from helping_functions import bank_end
from move_class import Move_Container, Move
from pointer_data import pointers
from pokemon_class import Pokemon_Container, Pokemon

class Rom:

    def __init__(self, path, out_path):
        if out_path is None:
            out_path = 'output.gbc'
        self.out_path = out_path
        self.read_rom(path)
        self.parse_data()

    def read_rom(self, path):
        with open(path, 'rb') as rom:
            self.data = rom.read(c.rom_size)

    def parse_data(self):
        self.read_version()
        self.set_pointers()
        self.load_data()
        self.create_classes()

    def read_version(self):
        version = self.data[c.ver_start:c.ver_end]
        self.version = c.versions.get(version, 'Custom')

    def set_pointers(self):
        """Evolution and moveset data index bounds"""
        evomoves_start = pointers[self.version]['evomoves']
        evomoves_end = bank_end(evomoves_start)
        self.pnt_evomoves = (evomoves_start, evomoves_end)

        """Pokémon base stats index bounds"""
        basestats_start = pointers[self.version]['basestats']
        basestats_end = basestats_start + c.max_pokemon * c.basestat_size
        self.pnt_basestats = (basestats_start, basestats_end)

        """Moves' stats data index bounds"""
        moves_start = pointers[self.version]['moves']
        moves_end = moves_start + c.max_moves * c.move_size
        self.pnt_moves = (moves_start, moves_end)

        """Pokémon palettes data index bounds"""
        palettes_start = pointers[self.version]['palettes']
        palettes_end = palettes_start + c.max_pokemon * c.palette_size
        self.pnt_palettes = (palettes_start, palettes_end)

        """Pokémon names data index bounds"""
        names_start = pointers[self.version]['names']
        names_end = names_start + c.max_pokemon * c.name_size
        self.pnt_names = (names_start, names_end)

        """Moves' names data index bounds"""
        movenames_start = pointers[self.version]['movenames']
        movenames_end = movenames_start + c.max_moves * c.movename_size
        self.pnt_movenames = (movenames_start, movenames_end)

        """TM to move mapping index bounds"""
        tms_start = pointers[self.version]['tms']
        tms_end = tms_start + c.max_tms * c.tm_size
        self.pnt_tms = (tms_start, tms_end)

    def load_data(self):
        data = self.data
        self.data_evomoves = data[slice(*self.pnt_evomoves)]
        self.data_basestats = data[slice(*self.pnt_basestats)]
        self.data_moves = data[slice(*self.pnt_moves)]
        self.data_palettes = data[slice(*self.pnt_palettes)]
        self.data_names = data[slice(*self.pnt_names)]
        self.data_movenames = data[slice(*self.pnt_movenames)]
        self.data_tms = data[slice(*self.pnt_tms)]

    def create_classes(self):
        self.pokemon = Pokemon_Container()
        pokemon = self.pokemon

        pokemon.extract_names(self.data_names)
        pokemon.extract_basestats(self.data_basestats)
        pokemon.extract_palettes(self.data_palettes)
        pokemon.extract_evomoves(self.data_evomoves)
        #self.move = Move_Container()

