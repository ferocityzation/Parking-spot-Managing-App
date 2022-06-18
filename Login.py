# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:03:16 2022

@author: andre
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from pathlib import Path
import yaml
from Registar import Registar
from Gclass import Gclass
from Planta_caller import Planta_caller


class Login(Gclass, Planta_caller):
    def __init__(self, root):
        super().__init__()

        self.root = root

        self.root.geometry('300x150')
        
    
        self.root.resizable(0, 0)
        self.root.title('Login')
        self.create_menu()
        self.create_buttons()
        self.create_entries()
        self.create_headings()
        
        # configura a grelha
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)    
        
    

    def create_headings (self):
        heading = ttk.Label(self.root, text='Bem-vindo', style='Heading.TLabel', font=('Helvetica', 11))
        heading.grid(column=0, row=0, columnspan=2, pady=5, sticky=tk.N)

        
    def create_entries(self):
                    
        #acrescenta uma linha vazia para poder puxar conteúdos para baixo
        paddings2 = {'padx': 1, 'pady': 1}
        espaco = ttk.Label(self.root, text="")
        espaco.grid(column=1, row=3, sticky=tk.E, **paddings2)
        espaco2 = ttk.Label(self.root, text="")
        espaco.grid(column=1, row=5, sticky=tk.E, **paddings2)
        
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 10)}
        
        username = tk.StringVar()
        password = tk.StringVar()
        # username
        username_label = ttk.Label(self.root, text="Username:")
        username_label.grid(column=0, row=1, sticky=tk.W, **paddings)

        # Never create instance variables outside of the init method
        self.username_entry = ttk.Entry(self.root, textvariable=username, **entry_font)
        self.username_entry.grid(column=1, row=1, sticky=tk.E, **paddings)

        # password
        password_label = ttk.Label(self.root, text="Password:")
        password_label.grid(column=0, row=2, sticky=tk.W, **paddings)

        # Never create instance variables outside of the init method
        self.password_entry = ttk.Entry(self.root, textvariable=password, show="*", **entry_font)
        self.password_entry.grid(column=1, row=2, sticky=tk.E, **paddings)

                
    def create_buttons(self):
        
        #Frame onde os butões ficarão alocados
        frame_buttons = Frame(self.root)
        frame_buttons.grid(row=4,column=1)
        
        # Frame para editar os butões em conjunto
        frame_edit_button = Frame(frame_buttons)
        frame_edit_button.grid(row=0,column=0, padx=20,pady=10)
        
        # criação butões 
        button_login = Button(frame_edit_button,text="Login",  command= self.verificar_login, font=('Helvetica', 9))     #button that runs the login verification
        button_registar = Button(frame_edit_button,text="Registar",  command = self.chamar_registo, font=('Helvetica', 9))              #button that will take you the registration window
        button_precario = Button(frame_edit_button,text="Preçário",command= self.precario_clicked, font=('Helvetica', 9)) #button that "precario" pop up
        
        # grid dos butões
        button_login.grid(row=0,column=0, sticky=tk.E)
        button_registar.grid(row=0,column=1, sticky=tk.E)
        button_precario.grid(row=0,column=3, sticky=tk.E)
        

        
    def create_menu(self):  #Cria o menu no canto superior esquero. Não é necessário ter
        # cria o menu "Sair"
        my_menu = Menu(self.root)
        self.root.config(menu = my_menu)
        menu = Menu(my_menu)
        my_menu.add_cascade(label='Sair', menu=menu)                            
        menu.add_command(label='quit', command = self.app_end)
        
    def app_end(self):
        # fecha a app
        self.root.destroy()
    
    def precario_clicked(self):      #Cria pop up que mostra o preço do parque
        showinfo(title='Preçário', message='O preço deste parque é: \n   1ª hora: 1 euro \n   2ªhora: 0.5 euros \n   3ªhora ou mais: 0.25 euros')
            
        
    def verificar_login(self):
        # Don't forget to call .get to actually get the text
        username1 = self.username_entry.get()
        password1 = self.password_entry.get()
        password_encriptada = Gclass.encriptar(password1)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
    
        user_records_file = Path(__file__).parent / "user_records.yaml"

        if not user_records_file.exists():                #cria o ficheiro yalm onde ficarão guardados os logins
            with open(user_records_file, "w+") as f:
                # cria um ficheiro em branco
                pass

        # Get all user records from the file
        with open(user_records_file, "r") as f:
            user_records = yaml.load(f, Loader=yaml.FullLoader)

        for user_record in user_records:
            if user_record["username"] == username1:
                if user_record["password"] == password_encriptada:
                    self.avancar(username1)
                    f.close()
                    break
    
                else:
                    showinfo(
                        title='Incorrect password!',
                        message='Incorrect password! Try again'
                    )
                    f.close()
                    break
    
        else:
            showinfo(title='Erro no login',
                    message='Utlizador não encontrado')
    
    def avancar(self,user):
        parking_status = str(Gclass.buscar_parking_pass(user))
        
        if parking_status == "inactive":
            Login.chamar_planta(self,user)  
        else:
            Login.chamar_display(self,user)
 
        
    def chamar_registo (self):      
        Gclass.app_end(self)

        if __name__ == "__main__":
    
            root = tk.Tk()
            registar = Registar(root)
            root.focus_force()
            root.mainloop()
    
if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    root.focus_force()
    root.mainloop()