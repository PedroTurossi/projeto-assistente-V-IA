import pystray
from PIL import Image
import main as Janela

Janela.janela_atual = None


class Icone():
    def __init__(self):
        # Escolha uma imagem pra representar seu ícone
        image = Image.open("imgs/BitBot_ico.ico")

        # Crie um ícone
        self.icon = pystray.Icon("BitBot", image, "BitBot AV")
        self.icon.run(self.mostrar_na_bandeja)

    # Função pra mostrar a aplicação na bandeja do sistema
    def mostrar_na_bandeja(self, icon):
        self.icon.visible = True
        menu = pystray.Menu(pystray.MenuItem("Abrir", self.abrir_janela),
                            pystray.MenuItem("Fechar", self.fechar_icone))
        self.icon.menu = menu

    def abrir_janela(self):
        self.icon.stop()
        self.continuar = True

    def fechar_icone(self):
        self.icon.stop()
        self.continuar = False