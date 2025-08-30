# clases/estacion_base.py
# Clase que representa una estación base del sistema de agricultura de precisión
from clases.diccionario import Diccionario
class EstacionBase:
    """
    Clase que representa una estación base que recibe datos de sensores
    y los transmite a la plataforma en la nube.
    """
    
    def __init__(self, id, nombre):
        """
        Inicializar estación base con ID y nombre
        
        Args:
            id (str): Identificador único de la estación
            nombre (str): Nombre descriptivo de la estación
        """
        self.__id = id
        self.__nombre = nombre
        self.__activa = True  # Estado de la estación (activa/inactiva)
        self.__ubicacion = None  # Ubicación opcional de la estación
    
    def get_id(self):
        """
        Obtener el ID de la estación
        
        Returns:
            str: ID único de la estación
        """
        return self.__id
    
    def get_nombre(self):
        """
        Obtener el nombre de la estación
        
        Returns:
            str: Nombre de la estación
        """
        return self.__nombre
    
    def set_nombre(self, nombre):
        """
        Establecer nuevo nombre para la estación
        
        Args:
            nombre (str): Nuevo nombre de la estación
        """
        self.__nombre = nombre
    
    def esta_activa(self):
        """
        Verificar si la estación está activa
        
        Returns:
            bool: True si está activa, False si está inactiva
        """
        return self.__activa
    
    def activar(self):
        """Activar la estación base"""
        self.__activa = True
    
    def desactivar(self):
        """Desactivar la estación base"""
        self.__activa = False
    
    def set_ubicacion(self, ubicacion):
        """
        Establecer ubicación de la estación
        
        Args:
            ubicacion (str): Descripción de la ubicación
        """
        self.__ubicacion = ubicacion
    
    def get_ubicacion(self):
        """
        Obtener ubicación de la estación
        
        Returns:
            str: Ubicación de la estación o None si no está establecida
        """
        return self.__ubicacion
    
    def obtener_informacion_completa(self):
        """
        Obtener información completa de la estación usando Diccionario personalizado
        
        Returns:
            Diccionario: Diccionario personalizado con toda la información de la estación
        """
        info = Diccionario()  #  Usar Diccionario personalizado
        info.insertar('id', self.__id)
        info.insertar('nombre', self.__nombre)
        info.insertar('activa', self.__activa)
        info.insertar('ubicacion', self.__ubicacion)
        return info
    
    def es_compatible_con(self, otra_estacion):
        """
        Verificar si esta estación es compatible con otra para agrupación
        
        Args:
            otra_estacion (EstacionBase): Otra estación para comparar
            
        Returns:
            bool: True si son compatibles para agrupación
        """
        # Las estaciones son compatibles si están activas
        return self.__activa and otra_estacion.esta_activa()
    
    def clonar(self):
        """
        Crear una copia de la estación
        
        Returns:
            EstacionBase: Copia de la estación actual
        """
        nueva_estacion = EstacionBase(self.__id, self.__nombre)
        nueva_estacion.__activa = self.__activa
        nueva_estacion.__ubicacion = self.__ubicacion
        return nueva_estacion
    
    def __str__(self):
        """
        Representación en string de la estación
        
        Returns:
            str: Descripción de la estación
        """
        estado = "Activa" if self.__activa else "Inactiva"
        ubicacion_str = f" - {self.__ubicacion}" if self.__ubicacion else ""
        return f"EstacionBase({self.__id}: {self.__nombre} - {estado}{ubicacion_str})"
    
    def __repr__(self):
        """
        Representación técnica de la estación
        
        Returns:
            str: Representación técnica
        """
        return f"EstacionBase('{self.__id}', '{self.__nombre}')"
    
    def __eq__(self, other):
        """
        Comparar estaciones por ID
        
        Args:
            other (EstacionBase): Otra estación para comparar
            
        Returns:
            bool: True si tienen el mismo ID
        """
        if not isinstance(other, EstacionBase):
            return False
        return self.__id == other.__id
    
    def __hash__(self):
        """
        Hash de la estación basado en su ID
        
        Returns:
            int: Hash de la estación
        """
        return hash(self.__id)