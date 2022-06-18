import tkinter as tk
from tkinter.messagebox import showinfo
import yaml
from pathlib import Path
from tkinter import ttk
from Gclass import Gclass

class Mudar(Gclass):
    def __init__(self, root, user):  
        super().__init__()
        self.root=root
        self.user = user
        
        self.root.geometry('300x130')
        self.create_labels_display()
        
        
    def create_labels_display(self): 
        paddings_entrada = {'padx': 5, 'pady': 1}
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 10)}
        paddings_butao = {'padx': 5, 'pady': 3}
        matricula = tk.StringVar()

        matricula_label = ttk.Label(self.root, text="Digite a nova matrícula:")
        matricula_label.grid(column=0, row=1, sticky=tk.W, **paddings)
        
        paragrafo2 = ttk.Label(self.root, text="")
        paragrafo2.grid(column=0, row=0, sticky=tk.W, **paddings_entrada)
        
        self.matricula_entry = ttk.Entry(self.root, textvariable=matricula, **entry_font)
        self.matricula_entry.grid(column=1, row=1, sticky=tk.E, **paddings)
        
        paragrafo = ttk.Label(self.root, text="")
        paragrafo.grid(column=0, row=2, sticky=tk.W, **paddings_butao)
        
        button_mudar = tk.Button(self.root,text="Mudar",  command= self.mudar_matricula, font=('Helvetica', 9))     
        button_mudar.grid(column=0, row=3, columnspan=2, pady=5, sticky=tk.N)
        
    def mudar_matricula(self):
        
        matricula = self.matricula_entry.get()
        
        user_records_file = Path(__file__).parent / "user_records.yaml"
        with open(user_records_file, "r") as f:
            login_records = yaml.load(f, Loader=yaml.FullLoader)  
        for login_record in login_records:
            if str(login_record["username"]) == self.user:
                login_record["matricula"] = str(matricula) 
        f.close()
        with open(user_records_file, "w+") as f:
            f.write(yaml.dump(login_records))
        f.close()
        
        
        showinfo(title='Matrícula mudada com sucesso!',
                    message='Proceda agora para a escolha do seu lugar com a sua nova matrícula, a qual será atualizada na próxima utilização.')  
  
        Gclass.app_end(self)        
