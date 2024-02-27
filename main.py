import tkinter as tk

root = tk.Tk()

# Carrega a imagem
image = tk.PhotoImage(file="rajehfeliz.png")

# Cria um widget Label e define a imagem como seu conteúdo
label = tk.Label(root, image=image, bg='white')
label.pack()

# Configura a janela para ser sem bordas e transparente
root.overrideredirect(True)
root.geometry("-200+250")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")

root.mainloop()
