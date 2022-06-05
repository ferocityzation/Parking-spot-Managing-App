# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:47:39 2022

@author: André
"""

import tkinter as tk
from tkinter.messagebox import showinfo

root = tk.Tk()

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = tk.Canvas(self, width=250, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.tag_bind("parking-spot", "<1>", self.change_color)
        self.count = 0
        self.draw()

    def draw(self):
        self.items = {}
        for row in range(5):
            for column in range(5):
                x = row*50
                y = column*100
                item = self.canvas.create_rectangle(x, y, x+50, y+100, fill="green", tags=("parking-spot",))
                self.items[(row,column)] = item
        self.items[(0,0)] = self.canvas.create_rectangle(0,0, 50, 100, fill="red", tags=("parking-spot",))            

    def change_color(self, event):
        item = self.canvas.find_withtag("current")
        current_color = self.canvas.itemcget(item, "fill")
        
        if current_color == "green" and self.count == 0:
            self.count = 1
            new_color = "yellow"
        
        elif current_color == "yellow":
            self.count =0
            new_color = "green"
        
        elif current_color == "green" and self.count == 1:
            showinfo(title='Erro na escolha do lugar',
                    message='Só pode escolher um lugar de cada vez')
        
        elif current_color == "red":
            showinfo(title='Lugar ocupado',
                    message='Lugar ocupado, escolha outro lugar')
            

            
        self.canvas.itemconfigure(item, fill=new_color)

ex = Example()
ex.pack(fill="both", expand=True)
root.mainloop()