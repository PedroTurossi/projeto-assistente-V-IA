import tkinter as tk

class Assistente:
    def __init__(self):
        # cria a janela espiritual e a imagem (que no futuro será uma animação real)
        self.root = tk.Tk()
        self.image = tk.PhotoImage(file="rajehfeliz.png")
        self.label = tk.Label(self.root, image=self.image, bg='white')
        self.label.pack()

        # faz a janela ser sem bordas e transparente
        self.root.geometry("+50-50")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

        # adiciona a funcionalidade de arrastar o label
        self.label.bind("<Button-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)

        self.label.bind("<Button-3>", self.teste1arroba)
        self.root.mainloop()

    def on_drag_start(self, event):
        self._start_x = event.x
        self._start_y = event.y

    def on_drag_motion(self, event):
        new_x = self.root.winfo_x() + (event.x - self._start_x)
        new_y = self.root.winfo_y() + (event.y - self._start_y)
        self.root.geometry(f"+{new_x}+{new_y}")

    def teste1arroba(self, event):
        print('teste1@')
        self.label2 = tk.Label(self.root, text="teste1@", bg="#dddddd", fg="#333333")

Assistente()
