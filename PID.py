#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:45:41 2023

@author: filip
"""

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import pyvisa as visa
import sys
from time import sleep

sys.path.append('X:\Software\Python')
from instruments.LakeShore336 import LakeShore336
from instruments.Keithley2200 import Keithley2200

rm = visa.ResourceManager()

lakeshore = LakeShore336(rm,'ASRL9::INSTR')
keithley = Keithley2200(rm,'USB0::0x05E6::0x2200::1358242::INSTR')
lakeshore.unlock()
keithley.unlock()

print(lakeshore.dev.query('*IDN?'))
print(keithley.dev.query('*IDN?'))


win = tk.Tk()
win.title('PID')
win.geometry('550x200')
win.resizable(width=False,height=False)

global dt
dt = 100
dTint = 0

run = False
def PIDloop():
    global t,T,dT,dTint,Q,setV
    if run == True:

        T = float(lakeshore.read('B','S'))         #read Temp from lakeshore
        ent_T.delete(0,tk.END)
        ent_T.insert(0, '{}'.format(round(T,4)))
        
        dT = T - float(Tset)
        
        ent_dT.delete(0, tk.END)
        ent_dT.insert(0,'{}'.format(round(dT,4)))
        dTint += dT

        Q = -P*dT - I*dTint*dt*1e-3
        #print(Q)
        
        if Q >= 0:
            Vcal = np.sqrt(Q)
        else:
            Vcal = 0
    
        #A vycist z pristorje
        A = float(keithley.getcurrent())
        
        if 0 <= Vcal <= Vmax:
            ent_V.delete(0,tk.END)
            Vset = Vcal
            keithley.setvoltage(Vset)                   #setting to power source
            ent_V.insert(0, '{}'.format(round(Vset,3)))

            Power = A*Vcal
            ent_cP.delete(0,tk.END)
            ent_cP.insert(0, '{}'.format(round(Power,3)))

        ent_A.delete(0,tk.END)
        ent_A.insert(0, '{}'.format(round(A,3)))
        
    win.after(dt,PIDloop)

def start(event):
    global run 
    run = True
    keithley.output(True)

def stop(event):
    global run
    run = False
    keithley.output(False)
    
def setTemp(event):
    global Tset
    Tset = ent_setT.get()  
    
def resetI(event):
    global dTint
    dTint = 0
    
def setPID(event):
    global P,I
    P = float(ent_P.get())
    I = float(ent_I.get())
    
def setR(event):
    global R
    R = float(ent_R.get())   
    print(R)
    
def setVm(event):
    global Vmax
    Vmax = float(ent_mV.get())

def setAm(event):
    global Amax
    Amax = float(ent_mA.get())
    keithley.setcurrent(Amax)

'Start Stop buttons'
btn_start = tk.Button(master = win, text = 'Start', fg = 'Green')
btn_stop = tk.Button(master = win, text = 'Stop', fg = 'red')
btn_start.bind('<Button-1>',start)
btn_stop.bind('<Button-1>',stop)
btn_start.grid(row=0,column=0,padx=10)
btn_stop.grid(row=0,column=1,padx=10)

'Temperature readout'
frm_T = tk.Frame(master = win)
frm_T.grid(row = 0, column = 2, padx = 20)

lbl_T0 = tk.Label(master = frm_T, text = 'T:')
lbl_T = tk.Label(master = frm_T, text = 'K')
ent_T = tk.Entry(master = frm_T,width = 10)
lbl_T0.grid(row=0,column=0, sticky = 'w')
ent_T.grid(row=0,column=1, sticky ='e')
lbl_T.grid(row=0,column=2, sticky ='w')

'SetTemp'
btn_setT = tk.Button(master = win, text = 'Set', fg = 'Blue')
btn_setT.grid(row = 1, column = 1, pady = 20)
btn_setT.bind('<Button-1>',setTemp)

frm_setT = tk.Frame(master = win)
frm_setT.grid(row=1,column=0,pady=20)

ent_setT = tk.Entry(master = frm_setT, width = 6)
lbl_setT = tk.Label(master = frm_setT, text = 'K')
ent_setT.grid(row=0,column=0, sticky ='e')
lbl_setT.grid(row=0,column=1, sticky ='w')
Tset = 1.65   #Default value
ent_setT.insert(0,'1.65')

'set PID'
frm_P = tk.Frame(master = win)
frm_I = tk.Frame(master = win)
frm_D = tk.Frame(master = win)
frm_P.grid(row = 0, column = 3, padx = 10)
frm_I.grid(row = 0, column = 4, padx = 10)
frm_D.grid(row = 0, column = 5, padx = 10)

lbl_P = tk.Label(master = frm_P, text = 'P')
lbl_I = tk.Label(master = frm_I, text = 'I')
lbl_D = tk.Label(master = frm_D, text = 'D')

ent_P = tk.Entry(master = frm_P,width = 5)
ent_I = tk.Entry(master = frm_I,width = 5)
ent_D = tk.Entry(master = frm_D, width = 5)

lbl_P.grid(row = 0,column=0,sticky = 'e')
ent_P.grid(row = 0,column=1,sticky = 'w')
lbl_I.grid(row = 0,column=0,sticky = 'e')
ent_I.grid(row = 0,column=1,sticky = 'w')
lbl_D.grid(row = 0,column=0,sticky = 'e')
ent_D.grid(row = 0,column=1,sticky = 'w')

P = 10
I = 1
ent_P.insert(0, str(P))
ent_I.insert(0, str(I))
ent_D.insert(0,'OUT')

btn_PID = tk.Button(master = win, text = 'Set PID', fg = 'Blue')
btn_PID.grid(row = 1, column=4)
btn_PID.bind('<Button-1>', setPID)

'zero intergral'
btn_rI = tk.Button(master = win, text = 'Reset Int', fg = 'Blue')
btn_rI.grid(row = 2, column = 4)
btn_rI.bind('<Button-1>',resetI)

'read resistance'
frm_R = tk.Frame(master = win)
frm_R.grid(row = 2, column = 0)
btn_R = tk.Button(master = win, text = 'Set', fg = 'Blue')
lbl_R = tk.Label(master = frm_R, text = u'\u03a9')
ent_R = tk.Entry(master = frm_R, width = 6)
ent_R.grid(row=0,column=0, sticky ='e')
lbl_R.grid(row=0,column=1, sticky ='w')

btn_R.grid(row = 2, column = 1)
#R = 100
ent_R.insert(0, 'OUT')
btn_R.bind('<Button-1>', setR)

'current V and I'
frm_V = tk.Frame(master = win)
frm_A = tk.Frame(master = win)
frm_V.grid(row = 2, column = 2)
frm_A.grid(row = 3, column = 2,pady = 20)

ent_A = tk.Entry(master = frm_A, width = 6)
ent_V = tk.Entry(master = frm_V, width = 6)
lbl_A = tk.Label(master = frm_A, text = 'A')
lbl_V = tk.Label(master = frm_V, text = 'V')
lbl_V0 = tk.Label(master = frm_V, text = 'Voltage:')
ent_A.grid(row=0,column=0, sticky ='e')
lbl_A.grid(row=0,column=1, sticky ='w')

lbl_V0.grid(row = 0, column = 0, sticky = 'e')
ent_V.grid(row=0,column=1, sticky ='e')
lbl_V.grid(row=0,column=2, sticky ='w')

'dT indicator'
frm_dT = tk.Frame(master = win)
frm_dT.grid(row = 1, column = 2)
ent_dT = tk.Entry(master = frm_dT, width = 8)
lbl_dT1 = tk.Label(master = frm_dT, text = u'\u0394T:')
lbl_dT2 = tk.Label(master = frm_dT, text = 'K')

lbl_dT1.grid(row=0,column=0, sticky ='e')
ent_dT.grid(row=0,column=1, sticky ='w')
lbl_dT2.grid(row=0,column=2, sticky ='e')

'constrains for A and V'

frm_mV = tk.Frame(master = win)
frm_mV.grid(row = 3, column = 0)
ent_mV = tk.Entry(master = frm_mV, width = 6)
lbl_mV = tk.Label(master = frm_mV, text= 'V')
ent_mV.grid(row=0,column=0, sticky ='e')
lbl_mV.grid(row=0,column=1, sticky ='w')

btn_mV = tk.Button(master = win, text = 'Set', fg = 'Blue')
btn_mV.grid(row = 3, column = 1)
btn_mV.bind('<Button-1>',setVm)

Vmax = 0
ent_mV.insert(0, str(Vmax))
keithley.setvoltage(Vmax)

frm_mA = tk.Frame(master = win)
ent_mA = tk.Entry(master = frm_mA, width = 6)
lbl_mA = tk.Label(master = frm_mA, text= 'A')
ent_mA.grid(row=0,column=0, sticky ='e')
lbl_mA.grid(row=0,column=1, sticky ='w')
frm_mA.grid(row = 4, column = 0)
btn_mA = tk.Button(master = win, text = 'Set', fg = 'Blue')
btn_mA.grid(row = 4, column = 1)
btn_mA.bind('<Button-1>',setAm)

Amax = 0
ent_mA.insert(0, str(Amax))
keithley.setcurrent(Amax)

'current power'  #ROW = 3 col = 2
frm_cP = tk.Frame(master = win)

lbl_P1 = tk.Label(master = frm_cP, text = 'Power:')
ent_cP = tk.Entry(master = frm_cP, width = 6)
lbl_P2 = tk.Label(master = frm_cP, text = 'W')

frm_cP.grid(row= 3, column = 2)
lbl_P1.grid(row=0,column=0, sticky ='e')
ent_cP.grid(row=0,column=1, sticky ='w')
lbl_P2.grid(row=0,column=2, sticky ='e')


win.after(dt,PIDloop)

win.mainloop()