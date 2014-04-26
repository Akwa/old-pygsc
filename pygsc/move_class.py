#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import constants as c
import move_functions as mf

class Move:
    pass

class Move_Container:

    def __init__(self):
        self.moves = {i: Move() for i in range(c.max_moves)}
        self.tm_data = []
        self.name_map = {}

    def __getitem__(self, item):
        """
        Allows to return self.pokemon items directly by self[item].
        You can get to any Move data by its id or name.
        Eg. self[0] will do the same as self['POUND'].
        """
        if type(item) is int:
            return self.moves[item]
        elif type(item) is str:
            return self.moves[self.name_map[item]]
        return None

    def extract_movenames(self, data, start, end):
        self.movenames_maxsize = end - start
        for i, name in enumerate(mf.read_movenames(data)):
            self.moves[i].name = name
            self.name_map[name] = i

    def extract_moves(self, data):
        for i, moves in enumerate(mf.read_moves(data)):
            self.moves[i].__dict__.update(moves)

    def extract_tms(self, data):
        self.tm_data = list(data)

    def assembly_movenames(self):
        movenames = b'\x50'.join(mf.rev_movenames(self.moves))
        return movenames.ljust(self.movenames_maxsize, b'\x00')

    def assembly_moves(self):
        return b''.join(mf.rev_moves(self.moves))

    def assembly_tms(self):
        return bytes(self.tm_data)