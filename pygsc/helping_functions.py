#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pygsc import constants as c

def bank_end(offset):
    return offset + c.bank_size - offset % c.bank_size

