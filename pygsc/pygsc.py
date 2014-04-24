#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from rom_class import Rom
import sys

if __name__ == "__main__":
    len_argv = len(sys.argv)
    if len_argv > 1:
        path = sys.argv[1]
        if len_argv > 2:
            out_path = sys.argv[2]
        else:
            out_path = None
        Data = Rom(path, out_path)
