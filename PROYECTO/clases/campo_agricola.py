# clases/campo_agricola.py
# Clase que representa un campo agrícola con todas sus estaciones y sensores

from clases.lista import Lista

class CampoAgricola:
    """
    Clase que representa un campo agrícola completo con estaciones base,
    sensores de suelo y sensores de cultivo.
    """
    
    def __init__(self, id, nombre):
        """
        Inicializar campo agrícola con ID y nombre
        
        Args:
            id (str): Identificador único del campo
            nombre (str): Nombre descriptivo del campo
        """
        self.__id = id
        self.__nombre = nombre
        self.__estaciones_base = Lista()  # Lista de estaciones base
        self.__sensores_suelo = Lista()   # Lista de sensores de suelo
        self.__sensores_cultivo = Lista() # Lista de sensores de cultivo
    
    def get_id(self):
        """
        Obtener el ID del campo
        
        Returns:
            str: ID del campo
        """
        return self.__id
    
    def get_nombre(self):
        """
        Obtener el nombre del campo
        
        Returns:
            str: Nombre del campo
        """
        return self.__nombre
    
    def set_nombre(self, nombre):
        """
        Establecer nuevo nombre para el campo
        
        Args:
            nombre (str): Nuevo nombre del campo
        """
        self.__nombre = nombre
    
    def agregar_estacion(self, estacion):
        """
        Agregar estación base al campo
        
        Args:
            estacion (EstacionBase): Estación a agregar
        """
        # Verificar que no exista una estación con el mismo ID
        if not self.__estaciones_base.buscar_por_id(estacion.get_id()):
            self.__estaciones_base.insertar(estacion)
        else:
            print(f"Advertencia: Estación {estacion.get_id()} ya existe en el campo")
    
    def agregar_sensor_suelo(self, sensor):
        """
        Agregar sensor de suelo al campo
        
        Args:
            sensor (SensorSuelo): Sensor de suelo a agregar
        """
        # Verificar que no exista un sensor con el mismo ID
        if not self.__sensores_suelo.buscar_por_id(sensor.get_id()):
            self.__sensores_suelo.insertar(sensor)
        else:
            print(f"Advertencia: Sensor de suelo {sensor.get_id()} ya existe en el campo")
    
    def agregar_sensor_cultivo(self, sensor):
        """
        Agregar sensor de cultivo al campo
        
        Args:
            sensor (SensorCultivo): Sensor de cultivo a agregar
        """
        # Verificar que no exista un sensor con el mismo ID
        if not self.__sensores_cultivo.buscar_por_id(sensor.get_id()):
            self.__sensores_cultivo.insertar(sensor)
        else:
            print(f"Advertencia: Sensor de cultivo {sensor.get_id()} ya existe en el campo")
    
    def obtener_estaciones(self):
        """
        Obtener lista de estaciones base
        
        Returns:
            Lista: Lista de estaciones base del campo
        """
        return self.__estaciones_base
    
    def obtener_sensores_suelo(self):
        """
        Obtener lista de sensores de suelo
        
        Returns:
            Lista: Lista de sensores de suelo del campo
        """
        return self.__sensores_suelo
    
    def obtener_sensores_cultivo(self):
        """
        Obtener lista de sensores de cultivo
        
        Returns:
            Lista: Lista de sensores de cultivo del campo
        """
        return self.__sensores_cultivo
    
    def buscar_estacion_por_id(self, id_estacion):
        """
        Buscar estación específica por ID
        
        Args:
            id_estacion (str): ID de la estación a buscar
            
        Returns:
            EstacionBase: La estación encontrada o None si no existe
        """
        return self.__estaciones_base.buscar_por_id(id_estacion)
    
    def buscar_sensor_suelo_por_id(self, id_sensor):
        """
        Buscar sensor de suelo específico por ID
        
        Args:
            id_sensor (str): ID del sensor a buscar
            
        Returns:
            SensorSuelo: El sensor encontrado o None si no existe
        """
        return self.__sensores_suelo.buscar_por_id(id_sensor)
    
    def buscar_sensor_cultivo_por_id(self, id_sensor):
        """
        Buscar sensor de cultivo específico por ID
        
        Args:
            id_sensor (str): ID del sensor a buscar
            
        Returns:
            SensorCultivo: El sensor encontrado o None si no existe
        """
        return self.__sensores_cultivo.buscar_por_id(id_sensor)
    
    def obtener_cantidad_estaciones(self):
        """
        Obtener número total de estaciones base
        
        Returns:
            int: Cantidad de estaciones base
        """
        return self.__estaciones_base.obtener_tamaño()
    
    def obtener_cantidad_sensores_suelo(self):
        """
        Obtener número total de sensores de suelo
        
        Returns:
            int: Cantidad de sensores de suelo
        """
        return self.__sensores_suelo.obtener_tamaño()
    
    def obtener_cantidad_sensores_cultivo(self):
        """
        Obtener número total de sensores de cultivo
        
        Returns:
            int: Cantidad de sensores de cultivo
        """
        return self.__sensores_cultivo.obtener_tamaño()
    
    def eliminar_estacion(self, id_estacion):
        """
        Eliminar estación del campo
        
        Args:
            id_estacion (str): ID de la estación a eliminar
            
        Returns:
            bool: True si se eliminó, False si no se encontró
        """
        estacion = self.buscar_estacion_por_id(id_estacion)
        if estacion:
            return self.__estaciones_base.eliminar(estacion)
        return False
    
    def obtener_resumen(self):
        """
        Obtener resumen estadístico del campo
        
        Returns:
            dict: Diccionario con estadísticas del campo
        """
        resumen = {
            'id': self.__id,
            'nombre': self.__nombre,
            'total_estaciones': self.obtener_cantidad_estaciones(),
            'total_sensores_suelo': self.obtener_cantidad_sensores_suelo(),
            'total_sensores_cultivo': self.obtener_cantidad_sensores_cultivo()
        }
        
        # Calcular total de frecuencias por tipo de sensor
        total_freq_suelo = 0
        sensores_suelo = self.__sensores_suelo.recorrer()
        for sensor in sensores_suelo:
            total_freq_suelo += sensor.obtener_frecuencias().obtener_tamaño()
        
        total_freq_cultivo = 0
        sensores_cultivo = self.__sensores_cultivo.recorrer()
        for sensor in sensores_cultivo:
            total_freq_cultivo += sensor.obtener_frecuencias().obtener_tamaño()
        
        resumen['total_frecuencias_suelo'] = total_freq_suelo
        resumen['total_frecuencias_cultivo'] = total_freq_cultivo
        
        return resumen
    
    def validar_integridad(self):
        """
        Validar la integridad del campo (verificar referencias)
        
        Returns:
            bool: True si el campo es íntegro, False si hay inconsistencias
        """
        try:
            # Verificar que todas las frecuencias referencien estaciones existentes
            estaciones_ids = [est.get_id() for est in self.__estaciones_base.recorrer()]
            
            # Verificar sensores de suelo
            for sensor in self.__sensores_suelo.recorrer():
                for freq in sensor.obtener_frecuencias().recorrer():
                    if freq.get_id_estacion() not in estaciones_ids:
                        print(f"Error: Sensor {sensor.get_id()} referencia estación inexistente {freq.get_id_estacion()}")
                        return False
            
            # Verificar sensores de cultivo
            for sensor in self.__sensores_cultivo.recorrer():
                for freq in sensor.obtener_frecuencias().recorrer():
                    if freq.get_id_estacion() not in estaciones_ids:
                        print(f"Error: Sensor {sensor.get_id()} referencia estación inexistente {freq.get_id_estacion()}")
                        return False
            
            return True
            
        except Exception as e:
            print(f"Error durante validación: {e}")
            return False
    
    def clonar(self):
        """
        Crear una copia completa del campo agrícola
        
        Returns:
            CampoAgricola: Copia del campo actual
        """
        nuevo_campo = CampoAgricola(self.__id, self.__nombre)
        
        # Copiar estaciones
        for estacion in self.__estaciones_base.recorrer():
            nuevo_campo.agregar_estacion(estacion)
        
        # Copiar sensores de suelo
        for sensor in self.__sensores_suelo.recorrer():
            nuevo_campo.agregar_sensor_suelo(sensor)
        
        # Copiar sensores de cultivo  
        for sensor in self.__sensores_cultivo.recorrer():
            nuevo_campo.agregar_sensor_cultivo(sensor)
        
        return nuevo_campo
    
    def __str__(self):
        """
        Representación en string del campo
        
        Returns:
            str: Descripción del campo
        """
        return (f"CampoAgricola(ID: {self.__id}, Nombre: {self.__nombre}, "
                f"Estaciones: {self.obtener_cantidad_estaciones()}, "
                f"Sensores Suelo: {self.obtener_cantidad_sensores_suelo()}, "
                f"Sensores Cultivo: {self.obtener_cantidad_sensores_cultivo()})")
    
    def __repr__(self):
        """
        Representación técnica del campo
        
        Returns:
            str: Representación técnica
        """
        return f"CampoAgricola('{self.__id}', '{self.__nombre}')"