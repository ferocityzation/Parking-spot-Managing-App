import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from pathlib import Path
import yaml
import datetime

class Display:
    def __init__(self, root, user):  
        self.root=root
        self.user = user
        self.place,self.hora,self.saldo = self.dados()
        
        self.root.geometry('270x120')
        self.create_labels_display()
        
    
        
    def create_labels_display(self): 
        paragrafo = tk.Label(self.root, text="")


        texto = tk.Label(self.root, text="O seu lugar é:")
        texto2 = ttk.Label(self.root, text="Feche a app ou clique no botão para sair do parque", style='Heading.TLabel', font=('Helvetica', 8))
        lugar = ttk.Label(self.root, text=self.place, style='Heading.TLabel', font=('Helvetica', 13))
        button_sair = tk.Button(self.root,text="Vou sair do parque",  command= self.sair)     #button that runs the login verification
        texto.pack()
        lugar.pack()
        
        texto2.pack()
        
        paragrafo.pack()
        button_sair.pack()
        
    
        
    def dados(self):  #retorna o lugar onde o utilzador está
    
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            user_records = yaml.load(f, Loader=yaml.FullLoader)

        for user_record in user_records:
            if user_record["username"] == self.user:
                lugar = user_record["parking_pass"]
                hora = user_record["h_entry"]
                saldo = user_record["saldo"]
                break
        f.close()
        return lugar,hora,saldo
    
    def preco(self):
        
        now = datetime.datetime.now()
        saida = now.hour, now.minute, now.second
        h_saida = int(saida[0])
        m_saida=  int(saida[1])
        hh = self.hora.split(':')
        h_entrada = int(hh[0])
        m_entrada = int(hh[1])
        self.saldo = float(self.saldo)
        
        
     
        #h_entrada nao vai existir, fazer split
        #separar a funcao preco da de saida
        #calculo da estadia
        
        if h_entrada > h_saida:
            self.hora_final = (h_saida + 24) - h_entrada
        else:
            self.hora_final = h_saida - h_entrada
            
        if m_entrada > m_saida:
            self.minuto_final = (m_saida + 60) - m_entrada
        else:
            self.minuto_final = m_saida - m_entrada
        
        # print(f'A permanência foi de {hora_final} horas e {minuto_final} minutos.')
        
        #calculo do valor monetario
        
        tempo_minutos = self.hora_final * 60 + self.minuto_final
        

        if tempo_minutos == 0:
            preco = 0.00
        if 1 <= tempo_minutos <= 60:
            precario = 1
            preco = round(precario * (1/60)*tempo_minutos,2)
            
        elif 60 < tempo_minutos <= 120:
            precario =  0.5
            preco = round(1 + precario*(1/60)*tempo_minutos,2)
            
        elif 120 < tempo_minutos:
            precario = 0.25
            preco = round(1 + 1 + precario*(1/60)*tempo_minutos,2)
        
        if self.saldo >= preco:
            self.saldo = round(self.saldo - preco,2)
        else:
            showinfo(title='Saldo insuficiente',
                    message='Foram adicionados 5.00 €')
            self.saldo = round(self.saldo + float(5) - preco,2)
        
        self.preco = round(float(preco),2)
            
    def sair(self):  #volta a reescrever "inativo" no ficheiro yalm
        
        self.preco()
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            login_records = yaml.load(f, Loader=yaml.FullLoader)
    
        for login_record in login_records:
            if login_record["username"] == self.user:
                login_record["parking_pass"] = "inactive"
                login_record["h_entry"] = "ND"
                login_record["saldo"] = self.saldo
        with open(user_records_file, "w+") as f:
            f.write(yaml.dump(login_records))
        f.close()
        
        showinfo(title='Obrigado',
                message='A sua permanência foi de: ' + str(self.hora_final) + " horas e " + str(self.minuto_final) + " minutos.\nO valor a ser pago será de " + str(self.preco) + "€." + "\nNuma próxima utilização terá: " + str(self.saldo) + "€.\nCaso não tenha saldo, este será reposto automaticamente.")
        self.root.destroy()