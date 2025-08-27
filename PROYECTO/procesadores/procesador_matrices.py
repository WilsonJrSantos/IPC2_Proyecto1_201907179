from clases.matriz import Matriz
from clases.lista import Lista
from clases.diccionario import Diccionario

class ProcesadorMatrices:
    def __init__(self):
        """Inicializar procesador de matrices"""
        pass

    def crear_rango(self, inicio, fin):
        """Crear rango de números sin usar range() nativo"""
        numeros = Lista()
        i = inicio
        while i < fin:
            numeros.insertar(i)
            i += 1
        return numeros

    def crear_matriz_frecuencias_suelo(self, campo):
        """Crear matriz F[n,s] para sensores de suelo"""
        try:
            # Obtener dimensiones usando métodos de Lista
            estaciones = campo.obtener_estaciones().recorrer()
            sensores_suelo = campo.obtener_sensores_suelo().recorrer()
            
            n_estaciones = campo.obtener_estaciones().obtener_tamaño()
            s_sensores = campo.obtener_sensores_suelo().obtener_tamaño()
            
            if n_estaciones == 0 or s_sensores == 0:
                return None
            
            # Crear matriz F[n,s]
            matriz_freq = Matriz(n_estaciones, s_sensores)
            
            # Llenar matriz con frecuencias usando contadores manuales
            i = 0
            for estacion in estaciones:
                j = 0
                for sensor in sensores_suelo:
                    # Buscar frecuencia para esta estación en este sensor
                    frecuencia = sensor.buscar_frecuencia_por_estacion(estacion.get_id())
                    valor = frecuencia.get_valor() if frecuencia else 0
                    matriz_freq.set_valor(i, j, valor)
                    j += 1
                i += 1
            
            return matriz_freq
            
        except Exception as e:
            print("Error creando matriz de frecuencias de suelo: {}".format(str(e)))
            return None

    def crear_matriz_frecuencias_cultivo(self, campo):
        """Crear matriz F[n,t] para sensores de cultivo"""
        try:
            # Obtener dimensiones usando métodos de Lista
            estaciones = campo.obtener_estaciones().recorrer()
            sensores_cultivo = campo.obtener_sensores_cultivo().recorrer()
            
            n_estaciones = campo.obtener_estaciones().obtener_tamaño()
            t_sensores = campo.obtener_sensores_cultivo().obtener_tamaño()
            
            if n_estaciones == 0 or t_sensores == 0:
                return None
            
            # Crear matriz F[n,t]
            matriz_freq = Matriz(n_estaciones, t_sensores)
            
            # Llenar matriz con frecuencias usando contadores manuales
            i = 0
            for estacion in estaciones:
                j = 0
                for sensor in sensores_cultivo:
                    # Buscar frecuencia para esta estación en este sensor
                    frecuencia = sensor.buscar_frecuencia_por_estacion(estacion.get_id())
                    valor = frecuencia.get_valor() if frecuencia else 0
                    matriz_freq.set_valor(i, j, valor)
                    j += 1
                i += 1
            
            return matriz_freq
            
        except Exception as e:
            print("Error creando matriz de frecuencias de cultivo: {}".format(str(e)))
            return None

    def convertir_a_patrones(self, matriz_frecuencias):
        """Convertir matriz de frecuencias a matriz de patrones"""
        if not matriz_frecuencias:
            return None
        
        try:
            return matriz_frecuencias.convertir_a_patron()
        except Exception as e:
            print("Error convirtiendo a patrones: {}".format(str(e)))
            return None

    def obtener_indice_estacion(self, lista_estaciones, id_estacion):
        """Obtener índice de estación en la lista"""
        estaciones = lista_estaciones.recorrer()
        i = 0
        for estacion in estaciones:
            if estacion.get_id() == id_estacion:
                return i
            i += 1
        return -1

    def obtener_indice_sensor(self, lista_sensores, id_sensor):
        """Obtener índice de sensor en la lista"""
        sensores = lista_sensores.recorrer()
        i = 0
        for sensor in sensores:
            if sensor.get_id() == id_sensor:
                return i
            i += 1
        return -1

    def mostrar_matriz_consola(self, matriz, titulo, etiquetas_filas, etiquetas_columnas):
        """Mostrar matriz formateada en consola"""
        if not matriz:
            print("Matriz no disponible")
            return
        
        print("\n" + "="*50)
        print(titulo)
        print("="*50)
        
        # Mostrar encabezados de columnas
        if etiquetas_columnas:
            print("       ", end="")
            for etiqueta in etiquetas_columnas:
                print("{:>8}".format(etiqueta[:7]), end="")
            print()
        
        # Mostrar filas con etiquetas
        indices_filas = self.crear_rango(0, matriz.get_filas())
        for i in indices_filas.recorrer():
            if etiquetas_filas and i < etiquetas_filas.obtener_tamaño():
                etiqueta = etiquetas_filas.obtener_en_posicion(i)
                print("{:>6} ".format(etiqueta[:6]), end="")
            else:
                print("{:>6} ".format("F{}".format(i)), end="")
            
            fila = matriz.obtener_fila(i)
            for valor in fila:
                print("{:>8}".format(str(valor)), end="")
            print()
        
        print("="*50 + "\n")

    def validar_dimensiones_matriz(self, matriz):
        """Validar que la matriz tenga dimensiones correctas"""
        if not matriz:
            return False, "Matriz no existe"
        
        if matriz.get_filas() <= 0:
            return False, "Número de filas debe ser mayor a 0"
        
        if matriz.get_columnas() <= 0:
            return False, "Número de columnas debe ser mayor a 0"
        
        return True, "Dimensiones válidas"

    def crear_matriz_reducida(self, matriz_original, grupos_estaciones):
        """Crear matriz reducida basada en grupos de estaciones"""
        if not matriz_original or grupos_estaciones.esta_vacia():
            return None
        
        try:
            grupos = grupos_estaciones.recorrer()
            filas_reducidas = grupos_estaciones.obtener_tamaño()
            columnas = matriz_original.get_columnas()
            
            matriz_reducida = Matriz(filas_reducidas, columnas)
            
            # Para cada grupo, sumar las frecuencias de sus estaciones
            i = 0
            for grupo in grupos:
                fila_sumada = matriz_original.sumar_filas(grupo)
                if fila_sumada:
                    j = 0
                    for valor in fila_sumada:
                        matriz_reducida.set_valor(i, j, valor)
                        j += 1
                i += 1
            
            return matriz_reducida
            
        except Exception as e:
            print("Error creando matriz reducida: {}".format(str(e)))
            return None

    def identificar_patrones_combinados(self, matriz_patron_suelo, matriz_patron_cultivo):
        """Identificar patrones combinados de suelo y cultivo"""
        if not matriz_patron_suelo or not matriz_patron_cultivo:
            return None
        
        try:
            # Combinar patrones de suelo y cultivo para cada estación
            filas = matriz_patron_suelo.get_filas()
            grupos = Lista()
            estaciones_procesadas = Lista()
            
            indices_i = self.crear_rango(0, filas)
            for i in indices_i.recorrer():
                if self._estacion_procesada(i, estaciones_procesadas):
                    continue
                
                grupo_actual = Lista()
                grupo_actual.insertar(i)
                estaciones_procesadas.insertar(i)
                
                # Buscar estaciones con patrones idénticos
                indices_j = self.crear_rango(i + 1, filas)
                for j in indices_j.recorrer():
                    if self._patrones_identicos(matriz_patron_suelo, matriz_patron_cultivo, i, j):
                        grupo_actual.insertar(j)
                        estaciones_procesadas.insertar(j)
                
                grupos.insertar(grupo_actual)
            
            return grupos
            
        except Exception as e:
            print("Error identificando patrones combinados: {}".format(str(e)))
            return None

    def _estacion_procesada(self, estacion, estaciones_procesadas):
        """Verificar si una estación ya fue procesada"""
        def criterio(elemento):
            return elemento == estacion
        return estaciones_procesadas.buscar(criterio) is not None

    def _patrones_identicos(self, matriz_suelo, matriz_cultivo, fila1, fila2):
        """Verificar si dos estaciones tienen patrones idénticos en suelo y cultivo"""
        # Comparar patrones de suelo
        patron_suelo_identico = matriz_suelo.comparar_fila(fila1, fila2)
        
        # Comparar patrones de cultivo
        patron_cultivo_identico = matriz_cultivo.comparar_fila(fila1, fila2)
        
        return patron_suelo_identico and patron_cultivo_identico

    def obtener_estadisticas_matriz(self, matriz):
        """Obtener estadísticas de la matriz"""
        if not matriz:
            return None
        
        try:
            estadisticas = Diccionario()
            estadisticas.insertar('filas', matriz.get_filas())
            estadisticas.insertar('columnas', matriz.get_columnas())
            estadisticas.insertar('total_elementos', matriz.get_filas() * matriz.get_columnas())
            estadisticas.insertar('suma_total', 0)
            estadisticas.insertar('valores_cero', 0)
            estadisticas.insertar('valores_positivos', 0)
            
            # Calcular estadísticas usando rangos personalizados
            indices_i = self.crear_rango(0, matriz.get_filas())
            for i in indices_i.recorrer():
                indices_j = self.crear_rango(0, matriz.get_columnas())
                for j in indices_j.recorrer():
                    valor = matriz.get_valor(i, j)
                    
                    # Actualizar suma total
                    suma_actual = estadisticas.obtener('suma_total')
                    estadisticas.insertar('suma_total', suma_actual + valor)
                    
                    # Contar valores cero y positivos
                    if valor == 0:
                        ceros_actual = estadisticas.obtener('valores_cero')
                        estadisticas.insertar('valores_cero', ceros_actual + 1)
                    elif valor > 0:
                        positivos_actual = estadisticas.obtener('valores_positivos')
                        estadisticas.insertar('valores_positivos', positivos_actual + 1)
            
            return estadisticas
            
        except Exception as e:
            print("Error calculando estadísticas: {}".format(str(e)))
            return None