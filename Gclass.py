# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 00:57:14 2022

@author: André
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
from pathlib import Path
import yaml
from Display import Display
# from Planta_parque import Planta

import sys
class Gclass:
    cod = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': "[", 'K': "£", 'L': "§", 'M': "{", 'N': "}", 'O': "", 'P': "A", 'Q': "E", 'R': "F", 'S': "G", 'T': "U", 'U': "D", 'V': "M", 'W': "N", 'X': "B", 'Y': "V", 'Z': "C", 'a': "b", 'b': "d", 'c': "f", 'd': "Y", 'e': "$", 'f': "#", 'g': "?", 'h': "`", 'i': "^", 'j': "+", 'k': "d", 'l': "f", 'm': "d", 'n': "e", 'o': "«", 'p': "ª", 'q': "'", 'r': "-", 's': "_", 't': ".", 'u': ",", 'v': "ç", 'w': "!", "x": "%", 'y': "&", 'z': "@", "1": "a", "2": "z"}   
    def __init__(self):
        pass
    
    @classmethod
    def chamar_display(cls,self2,user):
        # self2.app_end()
        self2.root.destroy()
        root = tk.Tk()        
        display = Display(root,user)
        root.focus_force()
        root.mainloop()
        return None
    
    
    @classmethod 
    def app_end(cls,self2):
        self2.root.destroy()
        return None


    @classmethod 
    def buscar_matricula(cls,user):
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            login_records = yaml.load(f, Loader=yaml.FullLoader)
    
        for login_record in login_records:
            if login_record["username"] == str(user):
                matricula = login_record["matricula"]
        return matricula

    @classmethod 
    def buscar_parking_pass(cls,user):
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            login_records = yaml.load(f, Loader=yaml.FullLoader)
    
        for login_record in login_records:
            if login_record["username"] == str(user):
                parking_pass = login_record["parking_pass"]
        return parking_pass
    
    @classmethod
    def encriptar(cls, password):
        pass_nova = ""
        for letra in password:
            if letra in Gclass.cod:
                pass_nova = pass_nova + str(Gclass.cod[letra])
            else:
                pass_nova = pass_nova + letra
        
        return pass_nova
        