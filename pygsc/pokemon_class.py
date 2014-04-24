#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import constants as c
import pokemon_functions as pf

class Pokemon:

    def __init__(self):
        self.prevolution = None
        self.family_len = None

class Pokemon_Container:

    def __init__(self):
        self.pokemon = {i: Pokemon() for i in range(c.max_pokemon)}
        self.name_map = {}

    def extract_names(self, data):
        for i, name in enumerate(pf.read_name(data)):
            self.pokemon[i].name = name
            self.name_map[name] = i

    def extract_basestats(self, data):
        for i, basestats in enumerate(pf.read_basestats(data)):
            self.pokemon[i].basestats = basestats

    def extract_palettes(self, data):
        for i, palettes in enumerate(pf.read_palettes(data)):
            self.pokemon[i].palettes = palettes

    def extract_evomoves(self, data):
        pos = c.bank_size - len(data)
        for i, (evos, moves) in enumerate(pf.read_evomoves(data, pos)):
            self.pokemon[i].evos = evos
            self.pokemon[i].moves = moves
        pf.process_evos(self.pokemon)
