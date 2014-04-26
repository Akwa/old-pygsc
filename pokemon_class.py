#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pygsc import constants as c
from pygsc import pokemon_functions as pf

class Pokemon:

    def __init__(self):
        self.prevolution = None
        self.family_len = None

class Pokemon_Container:

    def __init__(self):
        self.pokemon = {i: Pokemon() for i in range(c.max_pokemon)}
        self.name_map = {}

    def __getitem__(self, item):
        """
        Allows to return self.pokemon items directly by self[item].
        You can get to any Pokemon data by its (id - 1) or name.
        Eg. self[0] will do the same as self['BULBASAUR'].
        """
        if type(item) is int:
            return self.pokemon[item]
        elif type(item) is str:
            return self.pokemon[self.name_map[item]]
        return None

    def extract_names(self, data):
        for i, name in enumerate(pf.read_name(data)):
            self.pokemon[i].name = name
            self.name_map[name] = i

    def extract_basestats(self, data):
        for i, basestats in enumerate(pf.read_basestats(data)):
            self.pokemon[i].__dict__.update(basestats)

    def extract_palettes(self, data):
        for i, palettes in enumerate(pf.read_palettes(data)):
            self.pokemon[i].palettes = palettes

    def extract_evomoves(self, data):
        for i, (evos, moves) in enumerate(pf.read_evomoves(data)):
            self.pokemon[i].evos = evos
            self.pokemon[i].moves = moves
        pf.process_evos(self.pokemon)

    def assembly_names(self):
        return b''.join(pf.rev_names(self.pokemon))

    def assembly_basestats(self):
        return b''.join(pf.rev_basestats(self.pokemon))

    def assembly_palettes(self):
        return b''.join(pf.rev_palettes(self.pokemon))

    def assembly_evomoves(self, start, end):
        return pf.rev_evomoves(self.pokemon, start, end)