from .lista import Lista

class Contador:
    """Clase auxiliar para reemplazar range()"""
    def __init__(self, inicio, fin, paso=1):
        self.actual = inicio
        self.fin = fin
        self.paso = paso
    
    def siguiente(self):
        if self.actual < self.fin:
            valor = self.actual
            self.actual += self.paso
            return valor
        return None
    
    def hay_siguiente(self):
        return self.actual < self.fin

class Matriz:
    def __init__(self, filas, columnas):
        """Inicializar matriz con dimensiones específicas usando listas propias"""
        self.filas = filas
        self.columnas = columnas
        # Crear matriz usando Lista personalizada de listas
        self.datos = Lista()
        
        # Reemplazar range() con contador personalizado
        contador_filas = Contador(0, filas)
        while contador_filas.hay_siguiente():
            i = contador_filas.siguiente()
            fila = Lista()
            
            contador_columnas = Contador(0, columnas)
            while contador_columnas.hay_siguiente():
                j = contador_columnas.siguiente()
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
            
            contador = Contador(0, self.columnas)
            while contador.hay_siguiente():
                i = contador.siguiente()
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
        """Obtener fila completa como Lista personalizada"""
        if 0 <= numero_fila < self.filas:
            fila_actual = self.datos.obtener_en_posicion(numero_fila)
            # Crear nueva lista con los mismos elementos
            nueva_fila = Lista()
            
            contador = Contador(0, self.columnas)
            while contador.hay_siguiente():
                i = contador.siguiente()
                valor = fila_actual.obtener_en_posicion(i)
                nueva_fila.insertar(valor)
            
            return nueva_fila
        else:
            raise IndexError("Número de fila fuera de rango")

    def obtener_columna(self, numero_columna):
        """Obtener columna completa como Lista personalizada"""
        if 0 <= numero_columna < self.columnas:
            columna = Lista()
            
            contador = Contador(0, self.filas)
            while contador.hay_siguiente():
                i = contador.siguiente()
                fila_actual = self.datos.obtener_en_posicion(i)
                valor = fila_actual.obtener_en_posicion(numero_columna)
                columna.insertar(valor)
            
            return columna
        else:
            raise IndexError("Número de columna fuera de rango")

    def convertir_a_patron(self):
        """Convertir matriz de frecuencias a matriz de patrones (0/1)"""
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
        """Método auxiliar para comparar dos listas personalizadas"""
        if lista1.obtener_tamaño() != lista2.obtener_tamaño():
            return False
        
        contador = Contador(0, lista1.obtener_tamaño())
        while contador.hay_siguiente():
            i = contador.siguiente()
            if lista1.obtener_en_posicion(i) != lista2.obtener_en_posicion(i):
                return False
        
        return True

    def comparar_fila(self, fila1, fila2):
        """Comparar si dos filas son idénticas"""
        if fila1 >= self.filas or fila2 >= self.filas:
            return False
        
        lista_fila1 = self.obtener_fila(fila1)
        lista_fila2 = self.obtener_fila(fila2)
        
        return self._comparar_listas(lista_fila1, lista_fila2)

    def obtener_filas_identicas(self):
        """Identificar grupos de filas con patrones idénticos"""
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
            
            # Buscar filas idénticas
            contador_secundario = Contador(i + 1, self.filas)
            while contador_secundario.hay_siguiente():
                j = contador_secundario.siguiente()
                if self.comparar_fila(i, j):
                    grupo_actual.insertar(j)
                    filas_procesadas.insertar(j)
            
            grupos.insertar(grupo_actual)
        
        return grupos

    def _fila_ya_procesada(self, fila, filas_procesadas):
        """Verificar si una fila ya fue procesada"""
        def criterio(fila_procesada):
            return fila_procesada == fila
        
        return filas_procesadas.buscar(criterio) is not None

    def sumar_filas(self, indices_filas):
        """Sumar valores de filas específicas"""
        if indices_filas.esta_vacia():
            return None
            
        fila_suma = Lista()
        contador_init = Contador(0, self.columnas)
        while contador_init.hay_siguiente():
            j = contador_init.siguiente()
            fila_suma.insertar(0)
        
        # Iterar sobre los índices usando acceso directo a nodos
        actual = indices_filas._Lista__primero
        while actual is not None:
            indice = actual.get_dato()
            
            contador_columnas = Contador(0, self.columnas)
            while contador_columnas.hay_siguiente():
                j = contador_columnas.siguiente()
                valor_actual = fila_suma.obtener_en_posicion(j)
                valor_fila = self.get_valor(indice, j)
                nuevo_valor = valor_actual + valor_fila
                
                # Actualizar valor en la lista suma
                nueva_suma = Lista()
                contador_update = Contador(0, self.columnas)
                while contador_update.hay_siguiente():
                    k = contador_update.siguiente()
                    if k == j:
                        nueva_suma.insertar(nuevo_valor)
                    else:
                        nueva_suma.insertar(fila_suma.obtener_en_posicion(k))
                fila_suma = nueva_suma
            
            actual = actual.get_siguiente()
        
        return fila_suma

    def _lista_a_string(self, lista):
        """Convertir Lista personalizada a string"""
        if lista.esta_vacia():
            return ""
        
        resultado = ""
        primera_iteracion = True
        
        contador = Contador(0, lista.obtener_tamaño())
        while contador.hay_siguiente():
            i = contador.siguiente()
            if not primera_iteracion:
                resultado += " "
            resultado += str(lista.obtener_en_posicion(i))
            primera_iteracion = False
        
        return resultado

    def imprimir_matriz(self):
        """Mostrar matriz en consola"""
        print("Matriz [{}x{}]:".format(self.filas, self.columnas))
        
        contador = Contador(0, self.filas)
        while contador.hay_siguiente():
            i = contador.siguiente()
            fila = self.obtener_fila(i)
            fila_str = self._lista_a_string(fila)
            print("[{}] {}".format(i, fila_str))
        print()

    def __str__(self):
        """Representación en string de la matriz"""
        resultado = "Matriz [{}x{}]:\n".format(self.filas, self.columnas)
        
        contador = Contador(0, self.filas)
        while contador.hay_siguiente():
            i = contador.siguiente()
            fila = self.obtener_fila(i)
            fila_str = self._lista_a_string(fila)
            resultado += "{}\n".format(fila_str)
        
        return resultado