# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:29:37 2023

test edit

@author: sflab
"""
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import pyvisa as visa
import sys
from time import sleep

sys.path.append('X:\Software\Python')
from instruments.SmartValve import SmartValve

rm = visa.ResourceManager()

valve = SmartValve(rm, 'ASRL12::INSTR')

valve.unlock()
valve.valveangle(90)
sleep(1)
print(valve.getangle())




