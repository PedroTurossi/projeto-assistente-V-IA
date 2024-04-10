import tkinter as tk
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
        balao_img = Image.open('balao_rosa.png')
        self.image_balao1 = ImageTk.PhotoImage(balao_img.resize((50, 50)))
        self.balloon_label = tk.Label(self.root, image=self.image_balao1, bg="black")
        self.balloon_label.place(x=10, y=30)
        self.balloon_label.bind('<Button-1>', self.click_fechar)

        ia_img = Image.open('rajehfeliz.png')
        self.ia_imagem = ImageTk.PhotoImage(ia_img.resize((50, 50)))
        self.ia_label = tk.Label(self.root, image=self.ia_imagem, bg="black")
        self.ia_label.place(x=50, y=100)
        self.ia_label.bind('<Button-1>', self.ia_comando)

    def destruir_menu(self):
        self.ia_label.destroy()
        self.balloon_label.destroy()
        if hasattr(self, 'ia_input'):
            self.ia_input.destroy()

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

    def ia_comando(self, event):
        self.destruir_menu()
        self.ia_input = tk.Entry(self.root, width=54)
        self.ia_input.place(x=12, y=248)

        self.botao_enviar = tk.Button(self.root, text='enviar', command=self.ia_responder)
        self.botao_enviar.place(x=345, y=245)

        self.painel_msg = tk.Frame(self.root, bg='white', width=350, height=200)
        self.painel_msg.place(x=15, y=35)

        self.scrollbar = tk.Scrollbar(self.painel_msg, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.painel_msg, yscrollcommand=self.scrollbar.set, bg='white', width=350, height=200)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        
    def ia_responder(self):
        ia_api = gem_ia.IA()
        comando = self.ia_input.get()
        self.label_pergunta = tk.Label(self.painel_msg, text=comando)
        self.label_pergunta.place(x=0, y=0)
        self.ia_input.delete(0,tk.END)
        resposta = ia_api.responder(comando)
        self.label_resposta = tk.Label(self.painel_msg, text=resposta)
        self.label_resposta.place(x=0, y=30)


def main():
    Assistente()
    

if __name__ == '__main__':
    main()