# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:47:39 2022
@author: André
"""

import tkinter as tk
from tkinter.messagebox import showinfo
import yaml
from pathlib import Path

root = tk.Tk()

class Planta(tk.Frame):
    colunas = ["A","B","C","D","E"]
    posicao = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = tk.Canvas(self, width=250, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.tag_bind("parking-spot", "<1>", self.change_color)
        self.count = 0
        self.draw()
        self.gestao_ocupacao()
        
        tk.Label(self, text="\n").pack()
        self.button_reservar = tk.Button(self,text="Reservar",command= None, font=('Helvetica', 13)) #função que vai reservar. Temos de pintar o retângulo de vermelho e temos de escrever no ficheiro yalm
        self.button_reservar.pack()
        self.button_precario = tk.Button(self,text="Preçário",command= None, font=('Helvetica', 13))
        self.button_precario.pack()
        tk.Label(self, text="").pack()
        self.ultimo_item = ""

    # @property 
    # def ultimo_item(self):
    #     return self.ultimo_item
    
    # @ultimo_item.setter
    # def ultimo_item(self,retangulo):
    #     self.ultimo_item=retangulo
        
        
    def draw(self):
        self.items = {}
        for vertical in range(5):
            for horizontal in range(5): #vai-me prencheer ao longo das linhas
                x = horizontal*50
                y = vertical*100
                item = self.canvas.create_rectangle(x, y, x+50, y+80, fill="green", tags=("parking-spot",))
                self.items[str((Planta.colunas[horizontal],vertical+1))] = item
        # self.items[("A",1)] = self.canvas.create_rectangle(0,0, 50, 100, fill="red", tags=("parking-spot",))   
        print(self.items)        
        
    def gestao_ocupacao(self):
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            user_records = yaml.load(f, Loader=yaml.FullLoader)

        for user_record in user_records:
            print(user_record["parking_pass"])
            if user_record["parking_pass"] != "inactive":
                self.canvas.itemconfigure(self.items[user_record["parking_pass"]], fill="red")
                

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
                Planta.posicao=posicao      #guarda a posição da casa que cliquemos
        
    
        
