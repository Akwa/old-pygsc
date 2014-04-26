#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pygsc import constants as c

def read_movenames(data_movenames):
    i, m = 0, 0
    len_data = len(data_movenames)
    while i < c.max_moves and m < len_data:
        name_chars = []
        char = data_movenames[m]
        while char != 0x50:
            name_chars.append(c.alph[char])
            m += 1
            char = data_movenames[m]
        yield ''.join(name_chars)
        i += 1
        m += 1

def read_moves(data_moves):
    for i in range(0, c.move_size*c.max_moves, c.move_size):
        byte_seq = data_moves[i:i + c.move_size]
        moves = {}
        moves['animation'] = byte_seq[0]
        moves['effect'] = byte_seq[1]
        moves['power'] = byte_seq[2]
        moves['type'] = byte_seq[3]
        moves['accuracy'] = byte_seq[4]
        moves['pp'] = byte_seq[5]
        moves['effect_chance'] = byte_seq[6]
        yield moves

def rev_movenames(moves):
    for i in range(c.max_moves):
        name = moves[i].name
        name = [c.rev_alph[char] for char in name]
        name = bytes(name)
        yield name
    yield b''  # for one more 0x50 in b'\x50'.join iteration

def rev_moves(moves):
    for i in range(c.max_moves):
        mv = moves[i]
        move = []
        move.append(mv.animation)
        move.append(mv.effect)
        move.append(mv.power)
        move.append(mv.type)
        move.append(mv.accuracy)
        move.append(mv.pp)
        move.append(mv.effect_chance)
        yield bytes(move)
