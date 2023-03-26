#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:53:51 2023

@author: filip
"""

import numpy as np
import pyvisa as visa
from time import sleep

from .Instrument import Instrument

class SmartValve (Instrument):
    
    def __init__(self,rm,address):
        super().__init__(rm, address)
        #self.dev.write('echo 1')
        
    def valveopen(self):
        command = 'open'
        self.dev.write(command)
        
    def valveclose(self):
        command = 'close'
        self.dev.write(command)
        
    def vlaveangle(self, angle):
        command = 'ang {}'.format(angle)
        self.dev.write(command)
        
    def getangle(self):
        command = 'pos'
        ang = self.dev.query(command)
        return ang
        
    def angleplus(self):
        command = '+'
        self.dev.write(command)
        
    def angleminus(self):
        command = '-'
        self.dev.write(command)
    
