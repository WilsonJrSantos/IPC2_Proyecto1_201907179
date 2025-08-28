# clases/sensor_suelo.py
# Clase que representa un sensor de suelo en el sistema de agricultura de precisión

from clases.lista import Lista

class SensorSuelo:
    """
    Clase que representa un sensor de suelo que mide parámetros como
    humedad, temperatura, salinidad, conductividad, nutrientes y pH del suelo.
    """
    
    def __init__(self, id, nombre):
        """
        Inicializar sensor de suelo con ID y nombre
        
        Args:
            id (str): Identificador único del sensor
            nombre (str): Nombre descriptivo del sensor
        """
        self.__id = id
        self.__nombre = nombre
        self.__frecuencias = Lista()  # Lista de frecuencias de transmisión
        self.__tipo = "suelo"  # Tipo de sensor
        self.__activo = True  # Estado del sensor
        self.__parametros_medidos = Lista()  # Parámetros que puede medir este sensor
        
        # Inicializar parámetros típicos de sensores de suelo
        self.__inicializar_parametros_suelo()
    
    def __inicializar_parametros_suelo(self):
        """Inicializar lista de parámetros que mide un sensor de suelo"""
        self.__parametros_medidos.insertar("humedad_suelo")
        self.__parametros_medidos.insertar("temperatura_suelo")
        self.__parametros_medidos.insertar("salinidad")
        self.__parametros_medidos.insertar("conductividad_electrica")
        self.__parametros_medidos.insertar("nutrientes_clave")
        self.__parametros_medidos.insertar("ph_suelo")
    
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
            str: Tipo de sensor ("suelo")
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
            Lista: Lista personalizada de IDs de estaciones conectadas
        """
        estaciones = Lista()  # Usar Lista personalizada
        actual = self.__frecuencias._Lista__primero  # Acceso directo al primer nodo
        
        while actual is not None:
            freq = actual.get_dato()
            if freq.es_valida():
                estaciones.insertar(freq.get_id_estacion())
            actual = actual.get_siguiente()
        
        return estaciones
    
    def obtener_frecuencia_total(self):
        """
        Calcular la frecuencia total de transmisión del sensor
        
        Returns:
            int: Suma de todas las frecuencias
        """
        total = 0
        actual = self.__frecuencias._Lista__primero  # Acceso directo
        
        while actual is not None:
            freq = actual.get_dato()
            total += freq.get_valor()
            actual = actual.get_siguiente()
        
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
    
    def obtener_informacion_completa(self):
        """
        Obtener información completa del sensor usando Diccionario personalizado
        
        Returns:
            Diccionario: Diccionario personalizado con toda la información del sensor
        """
        from clases.diccionario import Diccionario
        
        info = Diccionario()
        info.insertar('id', self.__id)
        info.insertar('nombre', self.__nombre)
        info.insertar('tipo', self.__tipo)
        info.insertar('activo', self.__activo)
        info.insertar('cantidad_frecuencias', self.obtener_cantidad_frecuencias())
        info.insertar('frecuencia_total', self.obtener_frecuencia_total())
        info.insertar('estaciones_conectadas', self.obtener_estaciones_conectadas())
        info.insertar('parametros_medidos', self.__parametros_medidos)
        
        return info
    
    def clonar(self):
        """
        Crear una copia del sensor
        
        Returns:
            SensorSuelo: Copia del sensor actual
        """
        nuevo_sensor = SensorSuelo(self.__id, self.__nombre)
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
    
    def __str__(self):
        """
        Representación en string del sensor
        
        Returns:
            str: Descripción del sensor
        """
        estado = "Activo" if self.__activo else "Inactivo"
        return (f"SensorSuelo({self.__id}: {self.__nombre} - {estado} - "
                f"{self.obtener_cantidad_frecuencias()} frecuencias)")
    
    def __repr__(self):
        """
        Representación técnica del sensor
        
        Returns:
            str: Representación técnica
        """
        return f"SensorSuelo('{self.__id}', '{self.__nombre}')"
    
    def __eq__(self, other):
        """
        Comparar sensores por ID
        
        Args:
            other (SensorSuelo): Otro sensor para comparar
            
        Returns:
            bool: True si tienen el mismo ID
        """
        if not isinstance(other, SensorSuelo):
            return False
        return self.__id == other.__id
    
    def __hash__(self):
        """
        Hash del sensor basado en su ID
        
        Returns:
            int: Hash del sensor
        """
        return hash(self.__id)