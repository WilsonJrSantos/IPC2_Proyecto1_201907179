# clases/matriz.py (corregido)
from .lista import Lista
from .contador import Contador

class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = Lista()
        
        contador_filas = Contador(0, filas)
        while contador_filas.hay_siguiente():
            i = contador_filas.siguiente()
            fila = Lista()
            
            contador_columnas = Contador(0, columnas)
            while contador_columnas.hay_siguiente():
                j = contador_columnas.siguiente()
                fila.insertar(0)
            
            self.datos.insertar(fila)

    def get_filas(self):
        return self.filas

    def get_columnas(self):
        return self.columnas

    def set_valor(self, fila, columna, valor):
        """
        Establece un valor en una posición específica de manera eficiente.
        """
        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            raise IndexError("Índices fuera de rango")
        
        # Obtener la fila (Lista) en la posición 'fila'
        fila_actual = self.datos.obtener_en_posicion(fila)
        
        # Usar el nuevo método para actualizar el valor en la columna deseada
        fila_actual.set_dato_en_posicion(columna, valor)

    def get_valor(self, fila, columna):
        """Obtener valor de posición específica"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            fila_actual = self.datos.obtener_en_posicion(fila)
            return fila_actual.obtener_en_posicion(columna)
        else:
            raise IndexError("Índices fuera de rango")

    def obtener_fila(self, numero_fila):
        """Obtener fila completa como Lista personalizada"""
        if 0 <= numero_fila < self.filas:
            fila_actual = self.datos.obtener_en_posicion(numero_fila)
            nueva_fila = Lista()
            
            iterador = fila_actual.crear_iterador()
            while iterador.hay_siguiente():
                nueva_fila.insertar(iterador.siguiente())
            
            return nueva_fila
        else:
            raise IndexError("Número de fila fuera de rango")

    def obtener_columna(self, numero_columna):
        """Obtener columna completa como Lista personalizada"""
        if 0 <= numero_columna < self.columnas:
            columna = Lista()
            
            iterador_filas = self.datos.crear_iterador()
            while iterador_filas.hay_siguiente():
                fila_actual = iterador_filas.siguiente()
                valor = fila_actual.obtener_en_posicion(numero_columna)
                columna.insertar(valor)
            
            return columna
        else:
            raise IndexError("Número de columna fuera de rango")

    def convertir_a_patron(self):
        matriz_patron = Matriz(self.filas, self.columnas)
        
        contador_filas = Contador(0, self.filas)
        while contador_filas.hay_siguiente():
            i = contador_filas.siguiente()
            
            contador_columnas = Contador(0, self.columnas)
            while contador_columnas.hay_siguiente():
                j = contador_columnas.siguiente()
                valor_actual = self.get_valor(i, j)
                patron = 1 if valor_actual > 0 else 0
                matriz_patron.set_valor(i, j, patron)
        
        return matriz_patron

    def _comparar_listas(self, lista1, lista2):
        if lista1.obtener_tamaño() != lista2.obtener_tamaño():
            return False
        
        iterador1 = lista1.crear_iterador()
        iterador2 = lista2.crear_iterador()
        
        while iterador1.hay_siguiente():
            if iterador1.siguiente() != iterador2.siguiente():
                return False
        
        return True

    def comparar_fila(self, fila1, fila2):
        if not (0 <= fila1 < self.filas and 0 <= fila2 < self.filas):
            return False
        
        lista_fila1 = self.obtener_fila(fila1)
        lista_fila2 = self.obtener_fila(fila2)
        
        return self._comparar_listas(lista_fila1, lista_fila2)
        
    def obtener_filas_identicas(self):
        grupos = Lista()
        filas_procesadas = Lista()
        
        contador_principal = Contador(0, self.filas)
        while contador_principal.hay_siguiente():
            i = contador_principal.siguiente()
            
            if self._fila_ya_procesada(i, filas_procesadas):
                continue
                
            grupo_actual = Lista()
            grupo_actual.insertar(i)
            filas_procesadas.insertar(i)
            
            contador_secundario = Contador(i + 1, self.filas)
            while contador_secundario.hay_siguiente():
                j = contador_secundario.siguiente()
                if self.comparar_fila(i, j):
                    grupo_actual.insertar(j)
                    filas_procesadas.insertar(j)
            
            grupos.insertar(grupo_actual)
        
        return grupos

    def _fila_ya_procesada(self, fila, filas_procesadas):
        iterador = filas_procesadas.crear_iterador()
        while iterador.hay_siguiente():
            if iterador.siguiente() == fila:
                return True
        return False

    def sumar_filas(self, indices_filas):
        if indices_filas.esta_vacia():
            return None
            
        fila_suma = Lista()
        contador_init = Contador(0, self.columnas)
        while contador_init.hay_siguiente():
            fila_suma.insertar(0)
            contador_init.siguiente()
        
        iterador_indices = indices_filas.crear_iterador()
        while iterador_indices.hay_siguiente():
            indice = iterador_indices.siguiente()
            
            fila_a_sumar = self.obtener_fila(indice)
            
            iterador_suma = fila_suma.crear_iterador()
            iterador_fila = fila_a_sumar.crear_iterador()
            
            nueva_suma = Lista()
            contador_columnas = Contador(0, self.columnas)
            while contador_columnas.hay_siguiente():
                valor_actual = iterador_suma.siguiente()
                valor_fila = iterador_fila.siguiente()
                nueva_suma.insertar(valor_actual + valor_fila)
                contador_columnas.siguiente()
                
            fila_suma = nueva_suma
            
        return fila_suma

    def _lista_a_string(self, lista):
        if lista.esta_vacia():
            return ""
        
        resultado = ""
        primera_iteracion = True
        iterador = lista.crear_iterador()
        while iterador.hay_siguiente():
            if not primera_iteracion:
                resultado += " "
            resultado += str(iterador.siguiente())
            primera_iteracion = False
        
        return resultado
        
    def imprimir_matriz(self):
        print("Matriz [{}x{}]:".format(self.filas, self.columnas))
        
        iterador_filas = self.datos.crear_iterador()
        contador = Contador(0, self.filas)
        while contador.hay_siguiente():
            i = contador.siguiente()
            fila = iterador_filas.siguiente()
            fila_str = self._lista_a_string(fila)
            print("[{}] {}".format(i, fila_str))
        print()

    def __str__(self):
        resultado = "Matriz [{}x{}]:\n".format(self.filas, self.columnas)
        
        iterador_filas = self.datos.crear_iterador()
        while iterador_filas.hay_siguiente():
            fila = iterador_filas.siguiente()
            fila_str = self._lista_a_string(fila)
            resultado += "{}\n".format(fila_str)
        
        return resultado