#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import constants as c
from helping_functions import bank_end
from move_class import Move_Container, Move
from pointer_data import versions, pointers
from pokemon_class import Pokemon_Container, Pokemon
from re import match

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

    def save_data(self):
        self.update_data()
        self.assembly_data()
        self.write_rom()

    def read_version(self):
        version = self.data[c.ver_start:c.ver_end]
        self.version = versions.get(version, 'Custom')

    def set_pointers(self):
        pnt = pointers[self.version]

        """Pokémon names data index bounds"""
        names_start = pnt['names']
        names_end = names_start + c.max_pokemon * c.name_size
        self.pnt_names = (names_start, names_end)

        """Pokémon base stats index bounds"""
        basestats_start = pnt['basestats']
        basestats_end = basestats_start + c.max_pokemon * c.basestat_size
        self.pnt_basestats = (basestats_start, basestats_end)

        """Pokémon palettes data index bounds"""
        palettes_start = pnt['palettes']
        palettes_end = palettes_start + c.max_pokemon * c.palette_size
        self.pnt_palettes = (palettes_start, palettes_end)

        """Evolution and moveset data index bounds"""
        evomoves_start = pnt['evomoves']
        evomoves_end = pnt.get('evomoves_end', bank_end(evomoves_start))
        self.pnt_evomoves = (evomoves_start, evomoves_end)

        """Moves' names data index bounds"""
        movenames_start = pnt['movenames']
        movenames_end = movenames_start + c.max_moves * c.movename_size
        self.pnt_movenames = (movenames_start, movenames_end)

        """Moves' stats data index bounds"""
        moves_start = pnt['moves']
        moves_end = moves_start + c.max_moves * c.move_size
        self.pnt_moves = (moves_start, moves_end)

        """TM to move mapping index bounds"""
        tms_start = pnt['tms']
        tms_end = tms_start + c.max_tms * c.tm_size
        self.pnt_tms = (tms_start, tms_end)

    def load_data(self):
        data = self.data
        self.data_names = data[slice(*self.pnt_names)]
        self.data_basestats = data[slice(*self.pnt_basestats)]
        self.data_palettes = data[slice(*self.pnt_palettes)]
        self.data_evomoves = data[slice(*self.pnt_evomoves)]
        self.data_movenames = data[slice(*self.pnt_movenames)]
        self.data_moves = data[slice(*self.pnt_moves)]
        self.data_tms = data[slice(*self.pnt_tms)]

    def create_classes(self):
        self.pokemon = Pokemon_Container()
        pk = self.pokemon
        pk.extract_names(self.data_names)
        pk.extract_basestats(self.data_basestats)
        pk.extract_palettes(self.data_palettes)
        pk.extract_evomoves(self.data_evomoves)

        self.moves = Move_Container()
        mv = self.moves
        mv.extract_movenames(self.data_movenames)
        mv.extract_moves(self.data_moves)
        mv.extract_tms(self.data_tms)

    def update_data(self):
        pk, mv = self.pokemon, self.moves
        self.data_names = pk.assembly_names()
        self.data_basestats = pk.assembly_basestats()
        self.data_palettes = pk.assembly_palettes()
        self.data_evomoves = pk.assembly_evomoves(*self.pnt_evomoves)

        self.data_movenames = mv.assembly_movenames()
        self.data_moves = mv.assembly_moves()
        self.data_tms = mv.assembly_tms()

    def assembly_data(self):
        pnt_pat = "pnt_[a-z]+"
        data_pat = "data_[a-z]+"
        items = sorted(self.__dict__.items())

        all_pnts = [v for k, v in items if match(pnt_pat, k)]
        all_datas = [v for k, v in items if match(data_pat, k)]
        all_zipped = sorted(zip(all_pnts, all_datas))

        new_data = []
        k = 0
        for (i, j), block in all_zipped:
            new_data.append(self.data[k:i])
            new_data.append(block)
            k = j
        new_data.append(self.data[j:])
        self.data = b''.join(new_data)

    def write_rom(self):
        with open(self.out_path, 'wb') as rom:
            rom.write(self.data)
