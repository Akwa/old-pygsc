#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pygsc import constants as c
from struct import pack, unpack

def read_name(data_names):
    for i in range(0, c.name_size*c.max_pokemon, c.name_size):
        byte_seq = data_names[i:i + c.name_size]
        name_chars = []
        for j, byte in enumerate(byte_seq):
            if byte == 0x50:
                break
            name_chars.append(c.alph[byte])
        yield ''.join(name_chars)

def read_basestats(data_basestats):
    for i in range(0, c.basestat_size*c.max_pokemon, c.basestat_size):
        byte_seq = data_basestats[i:i + c.basestat_size]
        basestats = {}
        basestats['id'] = byte_seq[0x0]
        basestats['stats'] = list(byte_seq[0x1:0x7])
        basestats['types'] = list(byte_seq[0x7:0x9])
        basestats['catch_rate'] = byte_seq[0x9]
        basestats['exp_yield'] = byte_seq[0xa]
        basestats['wild_held_items'] = list(byte_seq[0xb:0xd])
        basestats['gender_ratio'] = byte_seq[0xd]
        basestats['egg_cycles'] = byte_seq[0xf]
        basestats['dimensions'] = byte_seq[0x11]
        basestats['growth_rate'] = byte_seq[0x16]
        basestats['egg_groups'] = read_egg(byte_seq[0x17])
        basestats['tms'] = read_tms(byte_seq[0x18:0x20])
        yield basestats

def read_egg(byte):
    first_group = byte >> 4
    second_group = byte & 0b00001111
    return [first_group, second_group]

def read_tms(byte_seq):
    tms = []
    for byte in byte_seq:
        byte = format(byte, '#010b')[:1:-1]
        byte = [int(item) for item in byte]
        tms.extend(byte)
    return tms

def read_palettes(data_palettes):
    for i in range(0, c.palette_size*c.max_pokemon, c.palette_size):
        byte_seq = list(data_palettes[i:i + c.palette_size])
        palettes = []
        for j in range(0, c.palette_size, 2):
            a, b = byte_seq[j:j + 2]
            R = a & 0b00011111
            G = (a >> 5) + (b & 0b00000011) * 0b1000
            B = b >> 2
            palettes.append([R, G, B])
        yield palettes

def read_evomoves(data_evomoves, position):
    for i in range(c.max_pokemon):
        j = i * c.pointer_size
        byte_seq = data_evomoves[j:j + c.pointer_size]
        pointer = unpack('<H', byte_seq)[0]
        pointer = pointer - c.bank_size - position
        evos, moves = [], []
        while data_evomoves[pointer] != 0x00:
            evo_len = c.evodata_len[data_evomoves[pointer]]
            evo_data = list(data_evomoves[pointer:pointer + evo_len])
            evo_data[-1] -= 1  # We enumerate Pokémon from 0, not 1
            evos.append(evo_data)
            pointer += evo_len
        pointer += 1
        while data_evomoves[pointer] != 0x00:
            entry = list(data_evomoves[pointer:pointer + c.entry_size])
            moves.append(entry)
            pointer += 2
        yield evos, moves

def read_eggmoves(data_evomoves, position):
    for i in range(c.max_pokemon):
        j = i * c.pointer_size
        byte_seq = data_eggmoves[j:j + c.pointer_size]
        pointer = unpack('<H', byte_seq)[0]
        pointer = pointer - c.bank_size - position
        eggmoves = [], []
        while data_evomoves[pointer] != 0xff:
            entry = list(data_evomoves[pointer:pointer + c.entry_size])
            eggmoves.append(entry)
            pointer += 2
        yield eggmoves

def process_evos(pokemon):
    for i in range(c.max_pokemon):
        for *x, j in pokemon[i].evos:
            pokemon[j].prevolution = i
    dfs_families(pokemon)

def dfs_families(pokemon):
    dfs_stack = []
    backtrack_stack = []
    for i in range(c.max_pokemon):
        if pokemon[i].prevolution is None:
            dfs_stack.append((i, 0))
    while dfs_stack:
        i, stage = dfs_stack.pop()
        stage += 1
        pokemon[i].stage = stage
        evos = pokemon[i].evos
        if evos:
            for *x, j in evos:
                dfs_stack.append((j, stage))
        else:
            backtrack_stack.append((i, stage))
    while backtrack_stack:
        i, stage = backtrack_stack.pop()
        pokemon[i].family_len = stage
        prevolution = pokemon[i].prevolution
        if prevolution is not None:
             backtrack_stack.append((prevolution, stage))

def rev_names(pokemon):
    for i in range(c.max_pokemon):
        name = pokemon[i].name
        name = [c.rev_alph[char] for char in name]
        name = bytes(name)
        name = name.ljust(c.name_size, b'\x50')
        yield name

def rev_basestats(pokemon):
    for i in range(c.max_pokemon):
        pk = pokemon[i]
        basestats = []
        basestats.append(pk.id)
        basestats.extend(pk.stats)
        basestats.extend(pk.types)
        basestats.append(pk.catch_rate)
        basestats.append(pk.exp_yield)
        basestats.extend(pk.wild_held_items)
        basestats.append(pk.gender_ratio)
        basestats.append(0x64)  # unknown
        basestats.append(pk.egg_cycles)
        basestats.append(0x5)  # unknown
        basestats.append(pk.dimensions)
        basestats.extend([0x0, 0x0, 0x0, 0x0])  # unknown
        basestats.append(pk.growth_rate)
        basestats.append(rev_egg_groups(*pk.egg_groups))
        basestats.extend(rev_tms(pk.tms))
        yield bytes(basestats)

def rev_egg_groups(group1, group2):
    return (group1 << 4) + group2

def rev_tms(tms):
    data = []
    for i in range(0, len(tms), c.bits_in_byte):
        byte = ''.join(str(i) for i in reversed(tms[i:i + 8]))
        byte = int(byte, 2)
        data.append(byte)
    return data


def rev_palettes(pokemon):
    for i in range(c.max_pokemon):
        pk = pokemon[i]
        palettes = []
        for R, G, B in pk.palettes:
            a = R + (G & 0b00111) * 0b100000
            b = (G >> 3) + B * 0b100
            palettes.append(bytes((a, b)))
        yield b''.join(palettes)

def rev_evomoves(pokemon, start, end):
    total_length = end - start
    data, evomoves = [], []
    i_data = start % c.bank_size + c.max_pokemon * c.pointer_size
    for i in range(c.max_pokemon):
        pk = pokemon[i]

        pointer = pack('<H', i_data + c.bank_size)
        data.append(pointer)

        packed_evomoves, len_evomoves = pack_evomoves(pk.evos, pk.moves)
        i_data += len_evomoves
        evomoves.append(packed_evomoves)
    data.extend(evomoves)
    data = b''.join(data)
    data = data.ljust(total_length, b'\x00')
    return data

def rev_eggmoves(pokemon, start, end):
    total_length = end - start
    data, eggmoves = [], []
    i_data = start % c.bank_size + c.max_pokemon * c.pointer_size
    for i in range(c.max_pokemon):
        pk = pokemon[i]

        pointer = pack('<H', i_data + c.bank_size)
        data.append(pointer)

        packed_eggmoves, len_eggmoves = pack_eggmoves(pk.eggmoves)
        i_data += len_eggmoves
        eggmoves.append(packed_eggmoves)
    data.extend(eggmoves)
    data = b''.join(data)
    data = data.ljust(total_length, b'\x00')
    return data

def pack_eggmoves(eggmoves):
    data = []
    len_data = 0
    for eggmove in eggmoves:
        data.append(bytes(eggmove))
        len_data += c.entry_size
    data.append(b'\xff')
    len_data += c.entry_size
    return b''.join(data), len_data
