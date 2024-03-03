import tkinter as tk
from PIL import Image, ImageTk
import config_read as conf
import icone as icon

class Assistente:
    def __init__(self):
        global janela_atual
        janela_atual = self

        # cria a janela espiritual e a imagem (que no futuro será uma animação real)
        self.root = tk.Tk()
        self.root.configure(background="orange")
        self.root.geometry('300x300+50-50')
        self.image = tk.PhotoImage(file='rajehfeliz.png')
        self.label = tk.Label(self.root,
                              image=self.image,
                              bg='orange')
        self.label.pack(side="bottom")

        # faz a janela ser sem bordas e transparente
        self.root.overrideredirect(True)
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "orange")

        # adiciona a funcionalidade de arrastar o label
        self.label.bind("<Button-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)

        # criar baloeszinhos
        self.label.bind("<Button-3>", self.on_right_click)

        #isso é uma ferramenta secreta que utilizaremos mais tarde
        self.configuracoes = conf.Configuracoes()

        self.root.title('BitBot') ### vamos mudar o nome dps

        self.root.mainloop()


    # movimento
    def on_drag_start(self, event):
        self._start_x = event.x
        self._start_y = event.y
        if not self.configuracoes.formal_on():
            self.colocar_imagem_2()
        self.label.bind("<ButtonRelease-1>", self.on_drag_stop)

    # movimento
    def on_drag_motion(self, event):
        new_x = self.root.winfo_x() + (event.x - self._start_x)
        new_y = self.root.winfo_y() + (event.y - self._start_y)
        self.root.geometry(f"+{new_x}+{new_y}")

    # movimento
    def on_drag_stop(self, event):
        self.label.bind("<Button-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)
        self.colocar_imagem_1()

    # ve se aperto botao direito
    def on_right_click(self, event):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        balao_img = Image.open('balao_rosa.png')
        self.image_balao1 = ImageTk.PhotoImage(balao_img.resize((50, 50)))

        self.balloon_label = tk.Label(self.root, image=self.image_balao1, bg="orange")
        self.balloon_label.place(x=0, y=0)

        self.balloon_label.bind('<Button-1>', self.click_fechar)


    # imagens / sprites
    def colocar_imagem_1(self):
        self.image = tk.PhotoImage(file='rajehfeliz.png')
        self.label.configure(image=self.image)


    def colocar_imagem_2(self):
        self.image = tk.PhotoImage(file='rajehshy.png')
        self.label.configure(image=self.image)

    def click_fechar(self, event):
        self.root.destroy()
        icone = icon.Icone()
        if icone.continuar:
            main()
        


def main():
    Assistente()
    

if __name__ == '__main__':
    main()