# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:03:36 2022

@author: andre
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from pathlib import Path
import yaml
from Planta_parque import Planta
from Gclass import Gclass
from Planta_caller import Planta_caller


class Registar(Gclass, Planta_caller):
    def __init__(self, root):
        super().__init__()

    
        self.root = root
        self.username_entry = ""
        self.password_entry = ""
        self.confirmar_pass = ""
        self.matricula = ""

        self.root.geometry('280x310')
        self.root.resizable(0, 0)
        self.root.title('Registar')
        self.create_entries_Registar()
        self.create_buttons()
        
        

    def create_entries_Registar(self):   
        
        username_registo = tk.StringVar()
        password_registo = tk.StringVar()
        confirmar_pass__registo = tk.StringVar()
        matricula = tk.StringVar()
 
        titulo = ttk.Label(self.root, text="Por favor, digita as suas credenciais")
        titulo.config(background = "#dad2d0")   #dá cor
        titulo.pack()
        espaco = ttk.Label(self.root, text="")
        espaco.pack()
        username_lable = ttk.Label(self.root, text="Username * ")
        username_lable.pack()
        self.username_entry = ttk.Entry(self.root, textvariable=username_registo)
        self.username_entry.pack()
        password_lable = ttk.Label(self.root, text="Password * ")
        password_lable.pack()
        self.password_entry = ttk.Entry(self.root, textvariable=password_registo, show='*')
        self.password_entry.pack()
        confirmar_pass = ttk.Label(self.root, text="Confirme a Password * ")
        confirmar_pass.pack()
        self.confirmar_pass = ttk.Entry(self.root, textvariable=confirmar_pass__registo, show='*')
        self.confirmar_pass.pack()
        matricula = ttk.Label(self.root, text="Digite a sua matrícula * ")
        matricula.pack()
        self.matricula = ttk.Entry(self.root, textvariable=matricula)
        self.matricula.pack()
        espaco = ttk.Label(self.root, text="")
        espaco.pack()


    def create_buttons(self):
        # criação butões 
        button_regist = Button(self.root,text="Registar",  command= self.registo, font=('Helvetica', 9))
        button_precario = Button(self.root,text="Preçário",command= self.precario_clicked, font=('Helvetica', 9))
        button_regist.pack()
        button_precario.pack()       
    
    def precario_clicked(self):      #Creates the pop up that shows the price of the park. It's not really beautiful, but I'll look into it if I have any time left
        showinfo(title='Preçário', message='O preço deste parque é: \n   1ª hora: 1 euro \n   2ªhora: 0.5 euros \n   3ªhora ou mais: 0.25 euros')
            
    def registo(self):  
        username1 = self.username_entry.get()
        password1 = self.password_entry.get()
        password2 = self.confirmar_pass.get()
        matricula = self.matricula.get()
        
        utilizador = "não existe"
        
        if (username1 == "") or( password1 == "") or (password2 =="") or (matricula==""):
            showinfo(title='Problema com a daqos',
                    message='Não pode deixar elementos em branco')            
        elif password1 != password2:
            showinfo(title='Problema com a password',
                    message='As palavras-chaves têm de coincidir')
        elif len(matricula)!=8:
            showinfo(title='Problema com a matrícula',
                    message='Digite uma matrícula com o formato XX-XX-XX')            
        elif (matricula[0].isalpha() == False and matricula[0].isnumeric() == False) or (matricula[1].isalpha() == False and matricula[1].isnumeric() == False) or (matricula[2] != "-") or (matricula[3].isalpha() == False and matricula[3].isnumeric() == False) or (matricula[4].isalpha() == False and matricula[4].isnumeric() == False) or (matricula[5] != "-") or (matricula[6].isalpha() == False and matricula[6].isnumeric() == False)  or (matricula[7].isalpha() == False and matricula[7].isnumeric() == False) :
            showinfo(title='Problema com a matrícula',
                    message='Digite uma matrícula com o formato XX-XX-XX')
        else:    
            user_records_file = Path(__file__).parent / "user_records.yaml"
            with open(user_records_file, "r") as f:
                user_records = yaml.load(f, Loader=yaml.FullLoader)

            for user_record in user_records:
                if user_record["username"] == username1:
                    showinfo(title='Utilizador já existente',
                            message='O seu nome de utilizador já existe, por favor escolha outro')
                    utilizador = "existe"
                    break
            f.close()
            if utilizador == "não existe":
                password_encriptada = Gclass.encriptar(password1)
                user_records_file = Path(__file__).parent / "user_records.yaml"
                with open(user_records_file, "r") as f:
                    login_records = yaml.load(f, Loader=yaml.FullLoader)
                
                login_records.append({
                    "username": username1,
                    "password": password_encriptada,
                    "matricula": matricula,
                    "parking_pass": "inactive",
                    "h_entry": "ND",
                    "saldo": "5.00",
                })
                f.close()
                with open(user_records_file, "w+") as f:
                    f.write(yaml.dump(login_records))
                f.close()
                Planta_caller.chamar_planta(self,username1)
                