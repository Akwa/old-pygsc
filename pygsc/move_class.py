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

    def extract_movenames(self, data):
        for i, name in enumerate(mf.read_movenames(data)):
            if i == 251:
                self.name_leftovers = name
                break
            self.moves[i].name = name
            self.name_map[name] = i

    def extract_moves(self, data):
        for i, moves in enumerate(mf.read_moves(data)):
            self.moves[i].__dict__.update(moves)

    def extract_tms(self, data):
        self.tm_data = list(data)

    def assembly_movenames(self):
        movenames = b'\x50'.join(mf.rev_movenames(self.moves))
        return b''.join((movenames, self.name_leftovers))

    def assembly_moves(self):
        return b''.join(mf.rev_moves(self.moves))

    def assembly_tms(self):
        return bytes(self.tm_data)