from .lista import Lista

class Matriz:
    def __init__(self, filas, columnas):
        """Inicializar matriz con dimensiones específicas usando listas propias"""
        self.filas = filas
        self.columnas = columnas
        # Crear matriz usando Lista personalizada de listas
        self.datos = Lista()
        for i in range(filas):
            fila = Lista()
            for j in range(columnas):
                fila.insertar(0)  # Inicializar con ceros
            self.datos.insertar(fila)

    def get_filas(self):
        """Retornar número de filas"""
        return self.filas

    def get_columnas(self):
        """Retornar número de columnas"""
        return self.columnas

    def set_valor(self, fila, columna, valor):
        """Establecer valor en posición específica"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            fila_actual = self.datos.obtener_en_posicion(fila)
            # Reconstruir la fila con el nuevo valor
            nueva_fila = Lista()
            for i in range(self.columnas):
                if i == columna:
                    nueva_fila.insertar(valor)
                else:
                    valor_actual = fila_actual.obtener_en_posicion(i)
                    nueva_fila.insertar(valor_actual)
            # Reemplazar la fila en la matriz
            self.datos.eliminar_en_posicion(fila)
            self.datos.insertar_en_posicion(nueva_fila, fila)
        else:
            raise IndexError("Índices fuera de rango")

    def get_valor(self, fila, columna):
        """Obtener valor de posición específica"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            fila_actual = self.datos.obtener_en_posicion(fila)
            return fila_actual.obtener_en_posicion(columna)
        else:
            raise IndexError("Índices fuera de rango")

    def obtener_fila(self, numero_fila):
        """Obtener fila completa como lista"""
        if 0 <= numero_fila < self.filas:
            fila_actual = self.datos.obtener_en_posicion(numero_fila)
            return fila_actual.recorrer()
        else:
            raise IndexError("Número de fila fuera de rango")

    def obtener_columna(self, numero_columna):
        """Obtener columna completa como lista"""
        if 0 <= numero_columna < self.columnas:
            columna = Lista()
            for i in range(self.filas):
                fila_actual = self.datos.obtener_en_posicion(i)
                valor = fila_actual.obtener_en_posicion(numero_columna)
                columna.insertar(valor)
            return columna.recorrer()
        else:
            raise IndexError("Número de columna fuera de rango")

    def convertir_a_patron(self):
        """Convertir matriz de frecuencias a matriz de patrones (0/1)"""
        matriz_patron = Matriz(self.filas, self.columnas)
        for i in range(self.filas):
            for j in range(self.columnas):
                valor_actual = self.get_valor(i, j)
                patron = 1 if valor_actual > 0 else 0
                matriz_patron.set_valor(i, j, patron)
        return matriz_patron

    def comparar_fila(self, fila1, fila2):
        """Comparar si dos filas son idénticas"""
        if fila1 >= self.filas or fila2 >= self.filas:
            return False
        
        lista_fila1 = self.obtener_fila(fila1)
        lista_fila2 = self.obtener_fila(fila2)
        
        if len(lista_fila1) != len(lista_fila2):
            return False
            
        for i in range(len(lista_fila1)):
            if lista_fila1[i] != lista_fila2[i]:
                return False
        return True

    def obtener_filas_identicas(self):
        """Identificar grupos de filas con patrones idénticos"""
        grupos = Lista()
        filas_procesadas = Lista()
        
        for i in range(self.filas):
            if self._fila_ya_procesada(i, filas_procesadas):
                continue
                
            grupo_actual = Lista()
            grupo_actual.insertar(i)
            filas_procesadas.insertar(i)
            
            # Buscar filas idénticas
            for j in range(i + 1, self.filas):
                if self.comparar_fila(i, j):
                    grupo_actual.insertar(j)
                    filas_procesadas.insertar(j)
            
            grupos.insertar(grupo_actual)
        
        return grupos

    def _fila_ya_procesada(self, fila, filas_procesadas):
        """Verificar si una fila ya fue procesada"""
        lista_procesadas = filas_procesadas.recorrer()
        return fila in lista_procesadas

    def sumar_filas(self, indices_filas):
        """Sumar valores de filas específicas"""
        if indices_filas.esta_vacia():
            return None
            
        fila_suma = Lista()
        for j in range(self.columnas):
            fila_suma.insertar(0)
        
        lista_indices = indices_filas.recorrer()
        for indice in lista_indices:
            for j in range(self.columnas):
                valor_actual = fila_suma.obtener_en_posicion(j)
                valor_fila = self.get_valor(indice, j)
                nuevo_valor = valor_actual + valor_fila
                
                # Actualizar valor en la lista suma
                nueva_suma = Lista()
                for k in range(self.columnas):
                    if k == j:
                        nueva_suma.insertar(nuevo_valor)
                    else:
                        nueva_suma.insertar(fila_suma.obtener_en_posicion(k))
                fila_suma = nueva_suma
        
        return fila_suma.recorrer()

    def imprimir_matriz(self):
        """Mostrar matriz en consola"""
        print("Matriz [{}x{}]:".format(self.filas, self.columnas))
        for i in range(self.filas):
            fila = self.obtener_fila(i)
            fila_str = " ".join([str(valor) for valor in fila])
            print("[{}] {}".format(i, fila_str))
        print()

    def __str__(self):
        """Representación en string de la matriz"""
        resultado = "Matriz [{}x{}]:\n".format(self.filas, self.columnas)
        for i in range(self.filas):
            fila = self.obtener_fila(i)
            fila_str = " ".join([str(valor) for valor in fila])
            resultado += "{}\n".format(fila_str)
        return resultado