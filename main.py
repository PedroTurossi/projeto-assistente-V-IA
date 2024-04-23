import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
import config_read as conf
import icone as icon
import gemini_ia as gem_ia
import time
import threading

class Assistente:
    def __init__(self):
        global janela_atual
        janela_atual = self

        # cria a janela espiritual e a imagem (que no futuro será uma animação real)
        self.root = tk.Tk()
        self.root.configure(background="gray")
        self.root.geometry('400x300+05-50')
        self.image = tk.PhotoImage(file='imgs/BitBot1.png')
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


    # movimento
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
        if self.imagem_tela:
            self.imagem_tela = False
            self.colocar_imagem_1()
            self.destruir_menu()
        else:
            self.imagem_tela = True
            self.colocar_imagem_tela()
            self.gerar_menu()

    def gerar_menu(self):
        ia_img = Image.open('imgs/IA_API_logo.png')
        self.ia_imagem = ImageTk.PhotoImage(ia_img.resize((50, 50)))
        self.ia_label = tk.Label(self.root, image=self.ia_imagem, bg='black')
        self.ia_label.place(x=50, y=120)
        self.ia_label.bind('<Button-1>', self.ia_interface)

        timer_img = Image.open('imgs/Timer_logo.png')
        self.timer_imagem = ImageTk.PhotoImage(timer_img.resize((50,50)))
        self.timer_label = tk.Label(self.root, image=self.timer_imagem, bg='black')
        self.timer_label.place(x=165, y=120)
        self.timer_label.bind('<Button-1>', self.timer_interface)

        saida_img = Image.open('imgs/saida_logo.png')
        self.image_close = ImageTk.PhotoImage(saida_img.resize((50, 50)))
        self.close_label = tk.Label(self.root, image=self.image_close, bg='black')
        self.close_label.place(x=300, y=120)
        self.close_label.bind('<Button-1>', self.click_fechar)

    def destruir_menu(self):
        self.ia_label.destroy()
        self.close_label.destroy()
        self.timer_label.destroy()

        if hasattr(self, 'ia_input'):
            self.ia_input.destroy()
            self.botao_enviar.destroy()
            self.painel_msg.destroy()
            self.botao_sair.destroy()
        elif hasattr(self, 'timer_bar') or hasattr(self, 'painel_timer'):
            self.botao_sair.destroy()
            self.painel_timer.destroy()
            if hasattr(self, 'botao_timer_off'):
                self.botao_timer_off.destroy()

    # imagens / (futuramente) sprites
    def colocar_imagem_1(self):
        self.image = tk.PhotoImage(file='imgs/BitBot1.png')
        self.label.configure(image=self.image)

    def colocar_imagem_2(self):
        self.image = tk.PhotoImage(file='imgs/BitBot1.png')
        self.label.configure(image=self.image)

    def colocar_imagem_tela(self):
        self.image = tk.PhotoImage(file='imgs/BitBot_rosto.png')
        self.label.configure(image=self.image)

    def click_fechar(self, event):
        self.root.destroy()
        icone = icon.Icone()
        if icone.continuar:
            main()

    def fechar_funcao(self):
        self.destruir_menu()
        self.gerar_menu()

    def ia_interface(self, event):
        self.destruir_menu()
        self.ia_input = tk.Entry(self.root, width=54, bg='black', fg='white')
        self.ia_input.place(x=12, y=248)

        self.botao_enviar = tk.Button(self.root, text='enviar', command=self.ia_responder, bg='black', fg='white')
        self.botao_enviar.place(x=345, y=245)

        self.painel_msg = tk.Frame(self.root, bg='black', width=350, height=190)
        self.painel_msg.place(x=15, y=55)

        self.botao_sair = tk.Button(self.root, text='X', bg='black', fg='white', height=1, command=self.fechar_funcao)
        self.botao_sair.place(x=10, y=30)

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
            self.adicionar_mensagem_painel(msg)
        
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
        self.destruir_menu()
        self.botao_sair = tk.Button(self.root, text='X', bg='black', fg='white', height=1, command=self.fechar_funcao)
        self.botao_sair.place(x=10, y=30)

        self.painel_timer = tk.Frame(self.root, bg='black', width=365, height=190)
        self.painel_timer.place(x=15, y=55)

        style_bar = ttk.Style()
        style_bar.configure('Horizontal.TProgressbar', background="green")
        self.timer_bar = ttk.Progressbar(self.painel_timer, orient='horizontal', length=350, style='Horizontal.TProgressbar')
        self.timer_bar.place(relx=0.5, rely=0.3, anchor="center")

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

    def iniciar_timer_thread(self):
        timer = threading.Thread(target=self.iniciar_timer)
        timer.start()

    def iniciar_timer(self):
        min = self.input_minutos.get()
        min = self.verificar_tempo_soum(min)
        seg = self.input_segundos.get()
        seg = self.verificar_tempo_soum(seg)
        self.input_minutos.delete(0, tk.END)
        self.input_segundos.delete(0, tk.END)
        tempo_em_segundos = ((min * 60) + seg)

        for s in range(tempo_em_segundos):
            time.sleep(1)
            if not hasattr(self, 'timer_bar') or not self.root.winfo_exists():
                return
            self.timer_bar['value']+=100/tempo_em_segundos
            self.root.update_idletasks()

        self.botao_timer_off = tk.Button(self.painel_timer, text='Parar', command=self.parar_alarme_timer, width=10)
        self.botao_timer_off.place(x=145, y=80)

    def parar_alarme_timer(self):
        self.botao_timer_off.destroy()
        self.timer_bar['value'] = 0

    def verificar_tempo_soum(self, string):
        if string == '':
            return 0
        for char in string:
            if not char.isdigit():
                return 0
        return int(string)

def main():
    Assistente()
    

if __name__ == '__main__':
    main()