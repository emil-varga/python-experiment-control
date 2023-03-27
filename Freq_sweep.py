#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:02:58 2023

@author: filip
"""

import matplotlib.pyplot as plt
import pyvisa as visa
import numpy as np
import os
import time

from tqdm import tqdm

import sys
sys.path.append('X:\Software\Python')

from instruments.SR830 import SR830
from instruments.KS33210A import KS33210A
from instruments.MKS670B import MKS670B

rm = visa.ResourceManager()

lockinA = SR830(rm,'address')
lockinB = SR830(rm,'address')
lockinC = SR830(rm,'address')
lockinD = SR830(rm,'address')
bara = MKS670B(rm, 'address')
genA = KS33210A(rm,'address')
genB = KS33210A(rm,'address')
genC = KS33210A(rm,'address')
genD = KS33210A(rm,'address')

lockins = [lockinA,lockinB,lockinC,lockinD]
gens = [genA,genB,genC,genD]

frequencies = np.linspace(160e3,210e3,1000)
amplitudes = np.linspace(0.02,2,25)

for num in enumerate(lockins):
    print(lockins[num].dev.query('*IDN?'))
    print(gens[num].dev.query('*IDN?'))
    gens[num].amlitude(amplitudes[0],unit = 'VRMS')
    gens[num].output(True)

print(bara.dev.query('*IDN?'))

try:
    while True:
        for amp in amplitudes:
            for num in enumerate(gens):
                gens[num].amplitude(amp,unit='VRMS')
            time.sleep(1.0)
            for f in tqdm(frequencies):
                for num,lockin in enumerate(lockins):
                    lockin.frequency(f)
                    time.sleep(0.1)
                    x,y = lockin.get_xy()
                
                bara.lock()
                P = bara.readP()
                bara.unlock()
                
                
                
finally:
            
                
        
        



