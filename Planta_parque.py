# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:47:39 2022
@author: André
"""
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from pathlib import Path
import yaml
from Display import Display
import datetime
from Gclass import Gclass
from MudarMatricula import Mudar

class Planta(tk.Frame,Gclass):
    colunas = ["A","B","C","D","E"]
    def __init__(self, user, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.root = root
        self.saldo = ""
        self.canvas = tk.Canvas(self, width=270, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.tag_bind("parking-spot", "<1>", self.change_color)
        self.count = 0
        self.draw()
        self.gestao_ocupacao()
        self.matricula = Gclass.buscar_matricula(self.user)
        
        ttk.Label(self.canvas, text="\nA\n\n\n\n\n\n\nB\n\n\n\n\n\n\nC\n\n\n\n\n\n\nD\n\n\n\n\n\n\nE\n\n", font=('Helvetica', 8)).pack(padx=5, pady=20, side=tk.LEFT)
        tk.Label(self, text="\n").pack()
        ttk.Label(self.root, text="                                                           Saldo: "+ str(self.saldo), font=('Helvetica', 8)).pack()
        ttk.Label(self.root, text="              1              2              3              4               5              ", font=('Helvetica', 8)).pack()
        ttk.Label(self, text="A sua matrícula é: "+ str(self.matricula), font=('Helvetica', 12)).pack()
        tk.Label(self, text="\n").pack()
        self.button_matricula = tk.Button(self,text="Reservar",command=self.chamar_display, font=('Helvetica', 13)) #função que vai reservar. Temos de pintar o retângulo de vermelho e temos de escrever no ficheiro yalm
        self.button_reservar = tk.Button(self,text="Reservar",command=self.ocupar, font=('Helvetica', 13)) #função que vai reservar. Temos de pintar o retângulo de vermelho e temos de escrever no ficheiro yalm
        self.button_reservar.pack()
        self.button_precario = tk.Button(self,text="Preçário",command= self.precario_clicked, font=('Helvetica', 13))
        self.button_mudar = tk.Button(self,text="Alterar matrícula",command= self.alterar_matricula, font=('Helvetica', 13))
        
        self.button_mudar.pack()
        self.button_precario.pack()
        tk.Label(self, text="").pack()
        self.posicao = ""
        

    
    def draw(self):
        self.items = {}
        for vertical in range(5):   #ao andares na vertical, vais alterar a linha
            for horizontal in range(5): #vai-me prencheer ao longo das linhas
                x = horizontal*50+20
                y = vertical*100
                item = self.canvas.create_rectangle(x, y, x+50, y+80, fill="green", tags=("parking-spot",))
                self.items[str((Planta.colunas[vertical],horizontal+1))] = item
    
    def gestao_ocupacao(self):
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            user_records = yaml.load(f, Loader=yaml.FullLoader)

        for user_record in user_records:
            if user_record["parking_pass"] != "inactive":
                self.canvas.itemconfigure(self.items[user_record["parking_pass"]], fill="red")
            if user_record["username"] == self.user:
                self.saldo = user_record["saldo"]
                
        f.close()
                
        
    def change_color(self, event):
        item = self.canvas.find_withtag("current")    #tupple que guarda o valor da casa que clicarmos
        current_color = self.canvas.itemcget(item, "fill")
        if current_color == "green" and self.count == 0:
            self.count = 1
            new_color = "yellow"
        
        elif current_color == "yellow":
            self.count = 0
            new_color = "green"
        
        elif current_color == "green" and self.count == 1:
            showinfo(title='Erro na escolha do lugar',
                    message='Só pode escolher um lugar de cada vez')
        
        elif current_color == "red":
            showinfo(title='Lugar ocupado',
                    message='Lugar ocupado, escolha outro lugar')

        self.canvas.itemconfigure(item, fill=new_color)
        for posicao in self.items:
            if self.items[posicao]==item[0]:
                self.posicao=posicao      #guarda a posição da casa que cliquemos
        
    
    def ocupar(self):
        now = datetime.datetime.now()
        entrada = now.hour, now.minute, now.second
        h_entrada = entrada[0]
        m_entrada =  entrada[1]
        for i in self.items:
            if i == self.posicao:
                lugar = i
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            login_records = yaml.load(f, Loader=yaml.FullLoader)
        for login_record in login_records:
            if login_record["username"] == self.user:
                login_record["parking_pass"] = lugar
                login_record["h_entry"] = str(h_entrada) + ':' + str(m_entrada) 
                
        f.close()
        with open(user_records_file, "w+") as f:
            f.write(yaml.dump(login_records))
        f.close()
        Planta.chamar_display(self,self.user)

    

    def alterar_matricula(self):
        root = tk.Tk()
        mudar = Mudar(root,self.user)
        root.focus_force()
        root.mainloop()
   
        
    def precario_clicked(self):      #Creates the pop up that shows the price of the park. It's not really beautiful, but I'll look into it if I have any time left
        showinfo(title='Preçário', message='O preço deste parque é: \n   1ª hora: 1 euro \n   2ªhora: 0.5 euros \n   3ªhora ou mais: 0.25 euros')