import os

class Configuracoes():
    def __init__(self):
        self.path = 'config.txt'
        if not os.path.exists(self.path):
            with open(self.path, 'w') as config:

                # as configurações ficam aqui
                config.write('formal: off\n')
        
        with open(self.path, 'r') as config:
            self.config = config.readlines()
        self.config = [linha.strip() for linha in self.config]
    
    
    def formal_on(self):
        if self.config[0] == 'formal: on':
            return True
        else:
            return False
