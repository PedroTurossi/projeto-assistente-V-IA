import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
import config_read as conf
import icone as icon
import gemini_ia as gem_ia

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
        balao_img = Image.open('imgs/saida_logo.png')
        self.image_close = ImageTk.PhotoImage(balao_img.resize((50, 50)))
        self.close_label = tk.Label(self.root, image=self.image_close, bg="black")
        self.close_label.place(x=300, y=120)
        self.close_label.bind('<Button-1>', self.click_fechar)

        ia_img = Image.open('imgs/IA_API_logo.png')
        self.ia_imagem = ImageTk.PhotoImage(ia_img.resize((50, 50)))
        self.ia_label = tk.Label(self.root, image=self.ia_imagem, bg="black")
        self.ia_label.place(x=50, y=120)
        self.ia_label.bind('<Button-1>', self.ia_interface)

    def destruir_menu(self):
        self.ia_label.destroy()
        self.close_label.destroy()
        if hasattr(self, 'ia_input'):
            self.ia_input.destroy()
            self.botao_enviar.destroy()
            self.painel_msg.destroy()
            self.botao_sair.destroy()

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
        ia_api = gem_ia.IA()
        comando = self.ia_input.get()
        self.ia_input.delete(0,tk.END)
        self.adicionar_mensagem_painel(comando)
        self.adicionar_mensagem_txt(comando)
        resposta = ia_api.responder(comando)
        self.adicionar_mensagem_painel(resposta)
        self.adicionar_mensagem_txt(resposta)


def main():
    Assistente()
    

if __name__ == '__main__':
    main()