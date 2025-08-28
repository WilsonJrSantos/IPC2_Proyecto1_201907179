# clases/lista.py
# Implementación de lista enlazada personalizada
# Esta clase reemplaza las listas nativas de Python según las restricciones del proyecto

from clases.nodo import Nodo

class Lista:
    """
    Implementación de lista enlazada simple personalizada.
    Proporciona todas las funcionalidades necesarias sin usar estructuras nativas de Python.
    """
    
    def __init__(self):
        """Inicializar lista vacía"""
        self.__primero = None  # Referencia al primer nodo
        self.__tamaño = 0  # Contador de elementos en la lista
    
    def insertar(self, dato):
        """
        Insertar elemento al final de la lista
        
        Args:
            dato: Elemento a insertar
        """
        nuevo_nodo = Nodo(dato)
        
        if self.__primero is None:
            # Lista vacía - el nuevo nodo es el primero
            self.__primero = nuevo_nodo
        else:
            # Buscar el último nodo y agregar el nuevo
            actual = self.__primero
            while actual.get_siguiente() is not None:
                actual = actual.get_siguiente()
            actual.set_siguiente(nuevo_nodo)
        
        self.__tamaño += 1
    
    def insertar_al_inicio(self, dato):
        """
        Insertar elemento al inicio de la lista
        
        Args:
            dato: Elemento a insertar
        """
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.set_siguiente(self.__primero)
        self.__primero = nuevo_nodo
        self.__tamaño += 1
    
    def insertar_en_posicion(self, dato, posicion):
        """
        Insertar elemento en posición específica
        
        Args:
            dato: Elemento a insertar
            posicion: Posición donde insertar (0 = inicio)
        """
        if posicion < 0 or posicion > self.__tamaño:
            raise IndexError("Posición fuera de rango")
        
        if posicion == 0:
            self.insertar_al_inicio(dato)
            return
        
        if posicion == self.__tamaño:
            self.insertar(dato)
            return
        
        nuevo_nodo = Nodo(dato)
        actual = self.__primero
        
        # Navegar hasta la posición anterior
        for i in range(posicion - 1):
            actual = actual.get_siguiente()
        
        # Insertar el nuevo nodo
        nuevo_nodo.set_siguiente(actual.get_siguiente())
        actual.set_siguiente(nuevo_nodo)
        self.__tamaño += 1
    
    def buscar(self, criterio):
        """
        Buscar elemento que cumpla un criterio específico
        
        Args:
            criterio: Función que recibe un elemento y retorna bool
            
        Returns:
            El primer elemento que cumpla el criterio o None si no se encuentra
        """
        actual = self.__primero
        
        while actual is not None:
            if criterio(actual.get_dato()):
                return actual.get_dato()
            actual = actual.get_siguiente()
        
        return None
    
    def buscar_por_id(self, id_buscado):
        """
        Buscar elemento por ID (asume que el elemento tiene método get_id())
        
        Args:
            id_buscado: ID del elemento a buscar
            
        Returns:
            El elemento con el ID especificado o None si no se encuentra
        """
        def criterio(elemento):
            try:
                return elemento.get_id() == id_buscado
            except:
                return False
        
        return self.buscar(criterio)
    
    def eliminar(self, dato):
        """
        Eliminar la primera ocurrencia de un elemento
        
        Args:
            dato: Elemento a eliminar
            
        Returns:
            bool: True si se eliminó, False si no se encontró
        """
        if self.__primero is None:
            return False
        
        # Si el elemento a eliminar es el primero
        if self.__primero.get_dato() == dato:
            self.__primero = self.__primero.get_siguiente()
            self.__tamaño -= 1
            return True
        
        # Buscar el elemento en el resto de la lista
        actual = self.__primero
        while actual.get_siguiente() is not None:
            if actual.get_siguiente().get_dato() == dato:
                actual.set_siguiente(actual.get_siguiente().get_siguiente())
                self.__tamaño -= 1
                return True
            actual = actual.get_siguiente()
        
        return False
    
    def eliminar_en_posicion(self, posicion):
        """
        Eliminar elemento en posición específica
        
        Args:
            posicion: Posición del elemento a eliminar (0 = inicio)
            
        Returns:
            El elemento eliminado
        """
        if posicion < 0 or posicion >= self.__tamaño:
            raise IndexError("Posición fuera de rango")
        
        if posicion == 0:
            dato = self.__primero.get_dato()
            self.__primero = self.__primero.get_siguiente()
            self.__tamaño -= 1
            return dato
        
        actual = self.__primero
        
        # Navegar hasta la posición anterior
        for i in range(posicion - 1):
            actual = actual.get_siguiente()
        
        dato = actual.get_siguiente().get_dato()
        actual.set_siguiente(actual.get_siguiente().get_siguiente())
        self.__tamaño -= 1
        
        return dato
    
    def obtener_en_posicion(self, posicion):
        """
        Obtener elemento en posición específica sin eliminarlo
        
        Args:
            posicion: Posición del elemento (0 = inicio)
            
        Returns:
            El elemento en la posición especificada
        """
        if posicion < 0 or posicion >= self.__tamaño:
            raise IndexError("Posición fuera de rango")
        
        actual = self.__primero
        
        # Navegar hasta la posición
        for i in range(posicion):
            actual = actual.get_siguiente()
        
        return actual.get_dato()
    
    def obtener_tamaño(self):
        """
        Obtener el número de elementos en la lista
        
        Returns:
            int: Cantidad de elementos
        """
        return self.__tamaño
    
    def esta_vacia(self):
        """
        Verificar si la lista está vacía
        
        Returns:
            bool: True si está vacía, False si contiene elementos
        """
        return self.__tamaño == 0
    
    def recorrer(self):
        """
        Recorrer la lista y retornar todos los elementos como una nueva lista
        
        Returns:
            Lista: Nueva lista con todos los elementos (para compatibilidad)
        """
        elementos = Lista()
        actual = self.__primero
        
        while actual is not None:
            elementos.insertar(actual.get_dato())
            actual = actual.get_siguiente()
        
        return elementos
    
    def crear_iterador(self):
        """
        Crear un iterador personalizado para recorrer la lista
        
        Returns:
            IteradorLista: Iterador personalizado para la lista
        """
        return IteradorLista(self.__primero)
    
    def limpiar(self):
        """Vaciar completamente la lista"""
        self.__primero = None
        self.__tamaño = 0
    
    def contiene(self, dato):
        """
        Verificar si la lista contiene un elemento específico
        
        Args:
            dato: Elemento a buscar
            
        Returns:
            bool: True si se encuentra, False si no
        """
        actual = self.__primero
        
        while actual is not None:
            if actual.get_dato() == dato:
                return True
            actual = actual.get_siguiente()
        
        return False
    
    def obtener_ultimo(self):
        """
        Obtener el último elemento de la lista
        
        Returns:
            El último elemento o None si la lista está vacía
        """
        if self.__primero is None:
            return None
        
        actual = self.__primero
        while actual.get_siguiente() is not None:
            actual = actual.get_siguiente()
        
        return actual.get_dato()
    
    def filtrar(self, criterio):
        """
        Filtrar elementos que cumplan un criterio
        
        Args:
            criterio: Función que recibe un elemento y retorna bool
            
        Returns:
            Lista: Nueva lista con elementos que cumplen el criterio
        """
        lista_filtrada = Lista()
        actual = self.__primero
        
        while actual is not None:
            if criterio(actual.get_dato()):
                lista_filtrada.insertar(actual.get_dato())
            actual = actual.get_siguiente()
        
        return lista_filtrada
    
    def mapear(self, funcion):
        """
        Aplicar una función a todos los elementos
        
        Args:
            funcion: Función a aplicar a cada elemento
            
        Returns:
            Lista: Nueva lista con elementos transformados
        """
        lista_mapeada = Lista()
        actual = self.__primero
        
        while actual is not None:
            nuevo_elemento = funcion(actual.get_dato())
            lista_mapeada.insertar(nuevo_elemento)
            actual = actual.get_siguiente()
        
        return lista_mapeada
    
    def __str__(self):
        """
        Representación en string de la lista
        
        Returns:
            str: Representación de la lista
        """
        if self.esta_vacia():
            return "Lista vacía"
        
        resultado = "Lista["
        actual = self.__primero
        primera_iteracion = True
        
        while actual is not None:
            if not primera_iteracion:
                resultado += ", "
            resultado += str(actual.get_dato())
            actual = actual.get_siguiente()
            primera_iteracion = False
        
        resultado += "]"
        return resultado
    
    def __len__(self):
        """Soporte para len() de Python"""
        return self.__tamaño
    
    def __iter__(self):
        """Hacer la Lista iterable con bucles for de Python"""
        return IteradorLista(self.__primero)


class IteradorLista:
    """Iterador personalizado para la lista enlazada"""
    
    def __init__(self, primer_nodo):
        self.__actual = primer_nodo
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__actual is None:
            raise StopIteration
        
        dato = self.__actual.get_dato()
        self.__actual = self.__actual.get_siguiente()
        return dato
    
    def siguiente(self):
        """Método personalizado para obtener el siguiente elemento"""
        if self.__actual is None:
            return None
        
        dato = self.__actual.get_dato()
        self.__actual = self.__actual.get_siguiente()
        return dato
    
    def hay_siguiente(self):
        """Verificar si hay más elementos"""
        return self.__actual is not None