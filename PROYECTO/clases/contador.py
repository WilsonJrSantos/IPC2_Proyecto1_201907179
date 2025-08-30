#clases/contador.py
class Contador:
    def __init__(self, inicio, fin):
        self.valor = inicio
        self.limite = fin

    def hay_siguiente(self):
        return self.valor < self.limite

    def siguiente(self):
        temp = self.valor
        self.valor += 1
        return temp