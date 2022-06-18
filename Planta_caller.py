# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 00:57:14 2022

@author: André
"""
from Planta_parque import Planta
import tkinter as tk
from tkinter import ttk
from tkinter import *
import yaml

import sys
class Planta_caller:
    # Constructor: Called when an object is instantiated
    def __init__(self):
        pass
    
    
    @classmethod 
    def app_end(cls,self2):
        self2.root.destroy()
        return None
    
    
    @classmethod
    def chamar_planta (cls, self2, user):      
        self2.root.destroy()

        root = tk.Tk()
        ex = Planta(user, root)
        ex.pack(fill="both", expand=True)
        root.mainloop()  
  
