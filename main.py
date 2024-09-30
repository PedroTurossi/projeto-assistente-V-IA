import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
import time
import threading
import pygame
from dateutil.parser import isoparse

import config_read as conf
import icone as icon
import gemini_ia as gem_ia
import agenda as agenda_api


class Assistente:
    def __init__(self):
        global janela_atual
        janela_atual = self

        # cria a janela espiritual e a imagem (que no futuro será uma animação real)
        self.root = tk.Tk()
        self.root.configure(background="gray")
        self.root.geometry('400x300+05-50')
        self.image = tk.PhotoImage(file='midia/BitBot2.png')
        self.label = tk.Label(self.root,
                              image=self.image,
                              bg='gray')
        self.label.pack(side="bottom")

        # faz a janela ser sem bordas e transparente
        self.root.overrideredirect(True)
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "gray")
        self.label.bind("<Button-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)

        self.label.bind("<Button-3>", self.on_right_click)

        #isso é uma ferramenta secreta que utilizaremos mais tarde
        self.configuracoes = conf.Configuracoes()
        self.imagem_tela = False

        self.root.title('BitBot')

        self.root.mainloop()

    def on_drag_start(self, event):
        self._start_x = event.x
        self._start_y = event.y
        if not self.configuracoes.formal_on() and not self.imagem_tela:
            self.colocar_imagem_2()
        self.label.bind("<ButtonRelease-1>", self.on_drag_stop)

    def on_drag_motion(self, event):
        new_x = self.root.winfo_x() + (event.x - self._start_x)
        new_y = self.root.winfo_y() + (event.y - self._start_y)
        self.root.geometry(f"+{new_x}+{new_y}")

    def on_drag_stop(self, event):
        self.label.bind("<Button-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)
        if not self.configuracoes.formal_on() and not self.imagem_tela:
            self.colocar_imagem_1()

    def on_right_click(self, event):
        if not self.imagem_tela:
            self.imagem_tela = True
            self.colocar_imagem_tela()
            self.gerar_menu()

    def gerar_menu(self):
        self.menu_painel = tk.Frame(self.root, bg='black', width=365, height=190)
        self.menu_painel.place(x=15, y=55)

        self.botao_sair = tk.Button(self.menu_painel, text='X', bg='black', fg='white', height=1, command=self.call_destruir_menu)
        self.botao_sair.place(x=0, y=0)

        ia_img = Image.open('midia/IA_API_logo.png')
        self.ia_imagem = ImageTk.PhotoImage(ia_img.resize((50, 50)))
        self.ia_label = tk.Label(self.menu_painel, image=self.ia_imagem, bg='black')
        self.ia_label.place(x=20, y=65)
        self.ia_label.bind('<Button-1>', self.ia_interface)

        timer_img = Image.open('midia/Timer_logo.png')
        self.timer_imagem = ImageTk.PhotoImage(timer_img.resize((50,50)))
        self.timer_label = tk.Label(self.menu_painel, image=self.timer_imagem, bg='black')
        self.timer_label.place(x=110, y=65)
        self.timer_label.bind('<Button-1>', self.timer_interface)

        windows_img = Image.open('midia/calendario.png')
        self.win_img = ImageTk.PhotoImage(windows_img.resize((50,50)))
        self.win_label = tk.Label(self.menu_painel, image=self.win_img, bg='black')
        self.win_label.place(x=190, y=65)
        self.win_label.bind('<Button-1>', self.calendario_interface)

        saida_img = Image.open('midia/saida_logo.png')
        self.image_close = ImageTk.PhotoImage(saida_img.resize((50, 50)))
        self.close_label = tk.Label(self.menu_painel, image=self.image_close, bg='black')
        self.close_label.place(x=285, y=65)
        self.close_label.bind('<Button-1>', self.click_fechar)
    
    def call_destruir_menu(self):
        self.destruir_menu(self.menu_painel)
        self.imagem_tela = False
        self.colocar_imagem_1()

    def call_destruir_timer(self):
        if pygame.mixer.music.get_busy() == True:
            pygame.mixer.music.stop()
        self.destruir_menu(self.painel_timer)
        self.gerar_menu()

    def call_destruir_ia(self):
        self.destruir_menu(self.painel_ia)
        self.gerar_menu()

    def call_destruir_calendario(self):
        self.destruir_menu(self.painel_calendario)
        self.gerar_menu()

    def destruir_menu(self, janela):
        for elemento in janela.winfo_children():
            elemento.destroy()
        janela.destroy()

    # imagens / (futuramente) sprites
    def colocar_imagem_1(self):
        self.image = tk.PhotoImage(file='midia/BitBot2.png')
        self.label.configure(image=self.image)

    def colocar_imagem_2(self):
        self.image = tk.PhotoImage(file='midia/BitBot2.png')
        self.label.configure(image=self.image)

    def colocar_imagem_tela(self):
        self.image = tk.PhotoImage(file='midia/BitBot_rosto.png')
        self.label.configure(image=self.image)

    def click_fechar(self, event):
        self.root.destroy()
        icone = icon.Icone()
        if icone.continuar:
            main()

    def ia_interface(self, event):
        self.destruir_menu(self.menu_painel)

        self.painel_ia = tk.Frame(self.root, bg='black', width=380, height=240)
        self.painel_ia.place(x=10, y=31)
        
        self.ia_input = tk.Entry(self.painel_ia, width=54, bg='black', fg='white')
        self.ia_input.place(x=3, y=216)

        self.botao_enviar = tk.Button(self.painel_ia, text='enviar', command=self.ia_responder, bg='black', fg='white')
        self.botao_enviar.place(x=333, y=213)

        self.painel_msg = tk.Frame(self.painel_ia, bg='black', width=350, height=200)
        self.painel_msg.place(x=5, y=17)

        self.botao_sair = tk.Button(self.painel_ia, text='X', bg='black', fg='white', height=1, command=self.call_destruir_ia)
        self.botao_sair.place(x=0, y=0)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('Vertical.TScrollbar', background='darkgray', troughcolor='black', borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.painel_msg, orient=tk.VERTICAL, style='Vertical.TScrollbar')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.painel_msg, yscrollcommand=self.scrollbar.set, bg='black', width=350, height=190, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas, bg='black')
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        self.carregar_mensagens()
        
    def carregar_mensagens(self):
        path = 'mensagens.txt'
        if not os.path.exists(path):
            with open(path, 'w') as texto:
                texto.write('')
        with open(path, 'r') as msg:
            mensagem = msg.readlines()
        for msg in mensagem:
            self.adicionar_mensagem_painel(('    ' + msg))
        
    def adicionar_mensagem_painel(self, texto):
        label = tk.Label(self.inner_frame, text=texto, wraplength=350, justify='left', bg='black', fg='white')
        label.pack(anchor='w')
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def adicionar_mensagem_txt(self, msg):
        path = 'mensagens.txt'
        with open(path, 'a') as texto:
            texto.write(msg + '\n')

    def ia_responder(self):
        ia_responder = threading.Thread(target=self.ia_responder_thread)
        ia_responder.start()

    def ia_responder_thread(self):
        ia_api = gem_ia.IA()
        comando = self.ia_input.get()
        self.ia_input.delete(0,tk.END)
        self.adicionar_mensagem_painel(comando)
        self.adicionar_mensagem_txt(comando)
        resposta = ia_api.responder(comando)
        self.adicionar_mensagem_painel(resposta)
        self.adicionar_mensagem_txt(resposta)

    def timer_interface(self, event):
        self.destruir_menu(self.menu_painel)

        self.painel_timer = tk.Frame(self.root, bg='black', width=365, height=190)
        self.painel_timer.place(x=15, y=55)

        self.botao_sair = tk.Button(self.painel_timer, text='X', bg='black', fg='white', height=1, command=self.call_destruir_timer)
        self.botao_sair.place(x=0, y=0)

        style_bar = ttk.Style()
        style_bar.configure('Horizontal.TProgressbar', background="green")
        self.timer_bar = ttk.Progressbar(self.painel_timer, orient='horizontal', length=350, style='Horizontal.TProgressbar')
        self.timer_bar.place(relx=0.5, rely=0.4, anchor="center")

        input_frame = tk.Frame(self.painel_timer)
        input_frame.place(relx=0.5, rely=0.6, anchor="center")

        self.input_minutos = tk.Entry(input_frame, width=3)
        self.input_minutos.pack(side="left")

        self.label_tempo = tk.Label(input_frame, text=':', fg='white', bg='black')
        self.label_tempo.pack(side="left", padx=5)

        self.input_segundos = tk.Entry(input_frame, width=3)
        self.input_segundos.pack(side="left")

        self.input_enviar = tk.Button(self.painel_timer, text='Iniciar', command=self.iniciar_timer_thread)
        self.input_enviar.place(relx=0.5, rely=0.8, anchor="center")
        
        pygame.mixer.init()

    def iniciar_timer_thread(self):
        timer = threading.Thread(target=self.iniciar_timer)
        timer.start()

    def iniciar_timer(self):
        min = self.input_minutos.get()
        seg = self.input_segundos.get()
        min = self.verificar_tempo_soum(min)
        seg = self.verificar_tempo_soum(seg)

        self.input_minutos.delete(0, tk.END)
        self.input_segundos.delete(0, tk.END)
        self.tempo_total = ((min * 60) + seg)
        self.tempo_restante = self.tempo_total

        self.label_tempo_restante = tk.Label(self.painel_timer, text=f'{min:02d}:{seg:02d}',fg="#ffffff",bg="black",font=('arial', 30, 'bold'))
        self.label_tempo_restante.place(relx=0.5, rely=0.2, anchor="center")

        self.atualizar_timer()
        
    def atualizar_timer(self):
        min = self.tempo_restante // 60
        seg = self.tempo_restante % 60
        self.timer_bar['value'] += 100 / (self.tempo_total + 1)
        self.root.update_idletasks()
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.label_tempo_restante.configure(text=f'{min:02d}:{seg:02d}')
            self.root.after(1000, self.atualizar_timer)
            return self.label_tempo_restante
        else: 
            self.label_tempo_restante.configure(text=f'{min:02d}:{seg:02d}')
            self.tocar_alarme()
            return self.label_tempo_restante

    def tocar_alarme(self):
        if hasattr(self, 'painel_timer'):
            pygame.mixer.music.load('midia/somAlert.wav')
            pygame.mixer.music.play(-1)  # Loop infinito
            self.botao_timer_off = tk.Button(self.painel_timer, text='Parar', command=self.parar_alarme_timer, width=10)
            self.botao_timer_off.place(x=145, y=80)
            
    def parar_alarme_timer(self):
        pygame.mixer.music.stop()
        self.botao_timer_off.destroy()
        self.timer_bar['value'] = 0
        self.label_tempo_restante.destroy()

    def verificar_tempo_soum(self, string):
        if string == '':
            return 0
        for char in string:
            if not char.isdigit():
                return 0
        return int(string)

    def calendario_interface(self, event):
        self.destruir_menu(self.menu_painel)

        self.painel_calendario = tk.Frame(self.root, bg='black', width=380, height=230)
        self.painel_calendario.place(x=10, y=40)

        self.botao_sair = tk.Button(self.painel_calendario, text='X', bg='black', fg='white', height=1, command=self.call_destruir_calendario)
        self.botao_sair.place(x=0, y=0)

        self.painel_eventos = tk.Frame(self.painel_calendario, bg='black', width=370, height=190)
        self.painel_eventos.place(x=5, y=25)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('Horizontal.TScrollbar', background='darkgray', troughcolor='black', borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.painel_eventos, orient=tk.HORIZONTAL, style='Horizontal.TScrollbar')

        self.canvas = tk.Canvas(self.painel_eventos, xscrollcommand=self.scrollbar.set, bg='black', width=370, height=190, highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.inner_frame = tk.Frame(self.canvas, bg='black', width=370, height=190)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar.config(command=self.canvas.xview)

        agenda_thread = threading.Thread(target=self.carregar_calendario)
        agenda_thread.start()

        botao_inserir_compromisso = tk.Button(self.painel_calendario, text='Novo', bg='black', fg='white', height=1, command=agenda_api.tela_adicionar_evento)
        botao_inserir_compromisso.place(x=170, y=183)
        
    def carregar_calendario(self):
        eventos = agenda_api.return_calendario()
        if eventos == []:
            label_erro = tk.Label(self.inner_frame, text='Você não tem nenhum evento no calendário', justify='left', bg='black', fg='white')
            label_erro.pack()
        else:
            for event in eventos:
                start = event["start"].get("dateTime", event["start"].get("date"))
                event_id = event['id']  # Pegando o ID do evento para excluir
                if "dateTime" in event["start"]:
                    start_datetime = isoparse(start)
                    day = start_datetime.strftime("%d-%m-%Y")
                    time = start_datetime.strftime("%H:%M")
                else:
                    day = start
                    time = ""

                event_summary = event["summary"]

                painel_evento = tk.Frame(self.inner_frame, bg='black', highlightthickness=1, width=200, height=200)
                painel_evento.pack(side='left', padx=5, pady=15)

                label_data = tk.Label(painel_evento, text=day, justify='left', bg='black', fg='white', font=("Arial", 8))
                label_data.pack(padx=5, pady=5)

                label_evento = tk.Label(painel_evento, text=event_summary, bg='black', fg='white', font=("Arial", 16))
                label_evento.pack(padx=5, pady=5)

                label_horario = tk.Label(painel_evento, text=time, bg='black', fg='white', font=("Arial", 12))
                label_horario.pack(padx=5, pady=5)

                botao_excluir = tk.Button(painel_evento, text="Excluir", bg="red", fg="white", command=lambda e_id=event_id: agenda_api.deletar_evento(e_id, painel_evento))
                botao_excluir.pack(padx=5, pady=5)

                self.canvas.update_idletasks()
                self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    

def main():
    Assistente()
 
if __name__ == '__main__':
    main()