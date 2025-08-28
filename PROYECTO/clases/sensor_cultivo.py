# clases/sensor_cultivo.py
# Clase que representa un sensor de cultivo en el sistema de agricultura de precisión

from clases.lista import Lista

class SensorCultivo:
    """
    Clase que representa un sensor de cultivo que evalúa el estado del cultivo
    a través de índices vegetales, estrés hídrico/térmico, cobertura, biomasa
    y detección temprana de enfermedades.
    """
    
    def __init__(self, id, nombre):
        """
        Inicializar sensor de cultivo con ID y nombre
        
        Args:
            id (str): Identificador único del sensor
            nombre (str): Nombre descriptivo del sensor
        """
        self.__id = id
        self.__nombre = nombre
        self.__frecuencias = Lista()  # Lista de frecuencias de transmisión
        self.__tipo = "cultivo"  # Tipo de sensor
        self.__activo = True  # Estado del sensor
        self.__parametros_medidos = Lista()  # Parámetros que puede medir este sensor
        
        # Inicializar parámetros típicos de sensores de cultivo
        self.__inicializar_parametros_cultivo()
    
    def __inicializar_parametros_cultivo(self):
        """Inicializar lista de parámetros que mide un sensor de cultivo"""
        parametros = [
            "indices_vegetales",
            "estres_hidrico",
            "estres_termico", 
            "cobertura_vegetal",
            "biomasa",
            "deteccion_enfermedades",
            "ndvi",  # Índice de vegetación de diferencia normalizada
            "clorofila"
        ]
        for param in parametros:
            self.__parametros_medidos.insertar(param)
    
    def get_id(self):
        """
        Obtener el ID del sensor
        
        Returns:
            str: ID único del sensor
        """
        return self.__id
    
    def get_nombre(self):
        """
        Obtener el nombre del sensor
        
        Returns:
            str: Nombre del sensor
        """
        return self.__nombre
    
    def set_nombre(self, nombre):
        """
        Establecer nuevo nombre para el sensor
        
        Args:
            nombre (str): Nuevo nombre del sensor
        """
        self.__nombre = nombre
    
    def get_tipo(self):
        """
        Obtener el tipo de sensor
        
        Returns:
            str: Tipo de sensor ("cultivo")
        """
        return self.__tipo
    
    def agregar_frecuencia(self, frecuencia):
        """
        Agregar frecuencia de transmisión a una estación
        
        Args:
            frecuencia (Frecuencia): Frecuencia de transmisión a agregar
        """
        # Verificar si ya existe frecuencia para esa estación
        freq_existente = self.buscar_frecuencia_por_estacion(frecuencia.get_id_estacion())
        if freq_existente:
            print(f"Advertencia: Ya existe frecuencia para estación {frecuencia.get_id_estacion()}")
            # Actualizar la frecuencia existente
            freq_existente.set_valor(frecuencia.get_valor())
        else:
            self.__frecuencias.insertar(frecuencia)
    
    def obtener_frecuencias(self):
        """
        Obtener lista de frecuencias del sensor
        
        Returns:
            Lista: Lista de frecuencias de transmisión
        """
        return self.__frecuencias
    
    def buscar_frecuencia_por_estacion(self, id_estacion):
        """
        Buscar frecuencia específica por ID de estación
        
        Args:
            id_estacion (str): ID de la estación a buscar
            
        Returns:
            Frecuencia: La frecuencia encontrada o None si no existe
        """
        def criterio(frecuencia):
            return frecuencia.get_id_estacion() == id_estacion
        
        return self.__frecuencias.buscar(criterio)
    
    def esta_activo(self):
        """
        Verificar si el sensor está activo
        
        Returns:
            bool: True si está activo, False si no
        """
        return self.__activo
    
    def activar(self):
        """Activar el sensor"""
        self.__activo = True
    
    def desactivar(self):
        """Desactivar el sensor"""
        self.__activo = False
    
    def obtener_cantidad_frecuencias(self):
        """
        Obtener número total de frecuencias configuradas
        
        Returns:
            int: Cantidad de frecuencias
        """
        return self.__frecuencias.obtener_tamaño()
    
    def obtener_estaciones_conectadas(self):
        """
        Obtener lista de IDs de estaciones a las que transmite
        
        Returns:
            list: Lista de IDs de estaciones conectadas
        """
        estaciones = []
        frecuencias = self.__frecuencias.recorrer()
        for freq in frecuencias:
            if freq.es_valida():  # Solo estaciones con frecuencia válida
                estaciones.append(freq.get_id_estacion())
        return estaciones
    
    def obtener_frecuencia_total(self):
        """
        Calcular la frecuencia total de transmisión del sensor
        
        Returns:
            int: Suma de todas las frecuencias
        """
        total = 0
        frecuencias = self.__frecuencias.recorrer()
        for freq in frecuencias:
            total += freq.get_valor()
        return total
    
    def obtener_parametros_medidos(self):
        """
        Obtener lista de parámetros que mide este sensor
        
        Returns:
            Lista: Lista de parámetros medidos
        """
        return self.__parametros_medidos
    
    def puede_medir_parametro(self, parametro):
        """
        Verificar si el sensor puede medir un parámetro específico
        
        Args:
            parametro (str): Nombre del parámetro
            
        Returns:
            bool: True si puede medirlo, False si no
        """
        def criterio(param):
            return param == parametro
        
        return self.__parametros_medidos.buscar(criterio) is not None
    
    def eliminar_frecuencia(self, id_estacion):
        """
        Eliminar frecuencia para una estación específica
        
        Args:
            id_estacion (str): ID de la estación
            
        Returns:
            bool: True si se eliminó, False si no se encontró
        """
        freq = self.buscar_frecuencia_por_estacion(id_estacion)
        if freq:
            return self.__frecuencias.eliminar(freq)
        return False
    
    def detectar_problemas_cultivo(self):
        """
        Simular detección de problemas en el cultivo basado en frecuencias
        
        Returns:
            list: Lista de problemas detectados
        """
        problemas = []
        frecuencia_total = self.obtener_frecuencia_total()
        
        # Lógica básica de detección basada en frecuencias de transmisión
        if frecuencia_total < 1000:
            problemas.append("Baja actividad de monitoreo")
        elif frecuencia_total > 10000:
            problemas.append("Alta actividad - posible estrés del cultivo")
        
        if self.obtener_cantidad_frecuencias() < 2:
            problemas.append("Pocas estaciones de monitoreo")
        
        return problemas
    
    def obtener_informacion_completa(self):
        """
        Obtener información completa del sensor
        
        Returns:
            dict: Diccionario con toda la información del sensor
        """
        return {
            'id': self.__id,
            'nombre': self.__nombre,
            'tipo': self.__tipo,
            'activo': self.__activo,
            'cantidad_frecuencias': self.obtener_cantidad_frecuencias(),
            'frecuencia_total': self.obtener_frecuencia_total(),
            'estaciones_conectadas': self.obtener_estaciones_conectadas(),
            'parametros_medidos': self.__parametros_medidos.recorrer(),
            'problemas_detectados': self.detectar_problemas_cultivo()
        }
    
    def clonar(self):
        """
        Crear una copia del sensor
        
        Returns:
            SensorCultivo: Copia del sensor actual
        """
        nuevo_sensor = SensorCultivo(self.__id, self.__nombre)
        nuevo_sensor.__activo = self.__activo
        
        # Copiar frecuencias
        frecuencias = self.__frecuencias.recorrer()
        for freq in frecuencias:
            nuevo_sensor.agregar_frecuencia(freq.clonar())
        
        return nuevo_sensor
    
    def validar_configuracion(self):
        """
        Validar que el sensor esté correctamente configurado
        
        Returns:
            bool: True si la configuración es válida
        """
        if not self.__activo:
            return True  # Sensor inactivo es válido
        
        # Verificar que tenga al menos una frecuencia válida
        frecuencias = self.__frecuencias.recorrer()
        for freq in frecuencias:
            if freq.es_valida():
                return True
        
        return False  # No tiene frecuencias válidas
    
    def obtener_eficiencia_monitoreo(self):
        """
        Calcular eficiencia del monitoreo basado en distribución de frecuencias
        
        Returns:
            float: Porcentaje de eficiencia (0-100)
        """
        cantidad_estaciones = self.obtener_cantidad_frecuencias()
        if cantidad_estaciones == 0:
            return 0.0
        
        # Eficiencia básica: más estaciones = mejor distribución
        eficiencia_base = min(cantidad_estaciones * 20, 80)  # Máximo 80% por cantidad
        
        # Bonus por frecuencias balanceadas
        frecuencias = self.__frecuencias.recorrer()
        if frecuencias:
            valores = [f.get_valor() for f in frecuencias]
            promedio = sum(valores) / len(valores)
            
            # Calcular desviación de balance
            desviaciones = [abs(v - promedio) for v in valores]
            desviacion_promedio = sum(desviaciones) / len(desviaciones)
            
            # Menos desviación = mejor balance = más eficiencia
            balance_bonus = max(0, 20 - (desviacion_promedio / promedio) * 10)
            eficiencia_base += balance_bonus
        
        return min(eficiencia_base, 100.0)
    
    def __str__(self):
        """
        Representación en string del sensor
        
        Returns:
            str: Descripción del sensor
        """
        estado = "Activo" if self.__activo else "Inactivo"
        eficiencia = self.obtener_eficiencia_monitoreo()
        return (f"SensorCultivo({self.__id}: {self.__nombre} - {estado} - "
                f"{self.obtener_cantidad_frecuencias()} frecuencias - "
                f"Eficiencia: {eficiencia:.1f}%)")
    
    def __repr__(self):
        """
        Representación técnica del sensor
        
        Returns:
            str: Representación técnica
        """
        return f"SensorCultivo('{self.__id}', '{self.__nombre}')"
    
    def __eq__(self, other):
        """
        Comparar sensores por ID
        
        Args:
            other (SensorCultivo): Otro sensor para comparar
            
        Returns:
            bool: True si tienen el mismo ID
        """
        if not isinstance(other, SensorCultivo):
            return False
        return self.__id == other.__id
    
    def __hash__(self):
        """
        Hash del sensor basado en su ID
        
        Returns:
            int: Hash del sensor
        """
        return hash(self.__id)