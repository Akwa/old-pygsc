#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from constants import *

def bank_end(offset):
    return offset + bank_size - offset % bank_size

