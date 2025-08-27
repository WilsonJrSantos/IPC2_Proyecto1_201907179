# clases/diccionario.py
# Implementación de diccionario personalizado sin usar estructuras nativas de Python

from clases.lista import Lista

class ParClave:
    """
    Clase que representa un par clave-valor para el diccionario
    """
    
    def __init__(self, clave, valor):
        """
        Inicializar par clave-valor
        
        Args:
            clave: La clave del par
            valor: El valor asociado a la clave
        """
        self.__clave = clave
        self.__valor = valor
    
    def get_clave(self):
        """
        Obtener la clave del par
        
        Returns:
            La clave del par
        """
        return self.__clave
    
    def get_valor(self):
        """
        Obtener el valor del par
        
        Returns:
            El valor del par
        """
        return self.__valor
    
    def set_valor(self, valor):
        """
        Establecer nuevo valor para el par
        
        Args:
            valor: Nuevo valor a asignar
        """
        self.__valor = valor
    
    def __str__(self):
        """
        Representación en string del par
        
        Returns:
            str: Representación del par clave-valor
        """
        return f"{self.__clave}: {self.__valor}"
    
    def __eq__(self, other):
        """
        Comparar pares por clave
        
        Args:
            other (ParClave): Otro par para comparar
            
        Returns:
            bool: True si tienen la misma clave
        """
        if not isinstance(other, ParClave):
            return False
        return self.__clave == other.__clave


class Diccionario:
    """
    Implementación de diccionario personalizado usando Lista
    """
    
    def __init__(self):
        """
        Inicializar diccionario vacío
        """
        self.__pares = Lista()  # Lista de objetos ParClave
    
    def insertar(self, clave, valor):
        """
        Insertar o actualizar un par clave-valor
        
        Args:
            clave: La clave a insertar/actualizar
            valor: El valor a asociar con la clave
        """
        # Buscar si ya existe la clave
        par_existente = self.__buscar_par(clave)
        
        if par_existente:
            # Actualizar valor existente
            par_existente.set_valor(valor)
        else:
            # Crear nuevo par y agregarlo
            nuevo_par = ParClave(clave, valor)
            self.__pares.insertar(nuevo_par)
    
    def obtener(self, clave):
        """
        Obtener valor asociado a una clave
        
        Args:
            clave: La clave a buscar
            
        Returns:
            El valor asociado a la clave o None si no existe
        """
        par = self.__buscar_par(clave)
        return par.get_valor() if par else None
    
    def contiene_clave(self, clave):
        """
        Verificar si existe una clave en el diccionario
        
        Args:
            clave: La clave a verificar
            
        Returns:
            bool: True si la clave existe, False si no
        """
        return self.__buscar_par(clave) is not None
    
    def eliminar(self, clave):
        """
        Eliminar un par clave-valor del diccionario
        
        Args:
            clave: La clave a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        par = self.__buscar_par(clave)
        if par:
            return self.__pares.eliminar(par)
        return False
    
    def obtener_claves(self):
        """
        Obtener todas las claves del diccionario
        
        Returns:
            Lista: Lista con todas las claves
        """
        claves = Lista()
        actual = self.__pares._Lista__primero  # Acceso directo al primer nodo
        
        while actual is not None:
            par = actual.get_dato()
            claves.insertar(par.get_clave())
            actual = actual.get_siguiente()
        
        return claves
    
    def obtener_valores(self):
        """
        Obtener todos los valores del diccionario
        
        Returns:
            Lista: Lista con todos los valores
        """
        valores = Lista()
        pares = self.__pares.recorrer()
        for par in pares:
            valores.insertar(par.get_valor())
        return valores
    
    def obtener_pares(self):
        """
        Obtener todos los pares clave-valor
        
        Returns:
            Lista: Lista con todos los pares ParClave
        """
        return self.__pares
    
    def esta_vacio(self):
        """
        Verificar si el diccionario está vacío
        
        Returns:
            bool: True si está vacío, False si no
        """
        return self.__pares.esta_vacia()
    
    def obtener_tamaño(self):
        """
        Obtener el número de pares clave-valor
        
        Returns:
            int: Cantidad de pares en el diccionario
        """
        return self.__pares.obtener_tamaño()
    
    def limpiar(self):
        """
        Eliminar todos los pares del diccionario
        """
        self.__pares = Lista()
    
    def actualizar(self, otro_diccionario):
        """
        Actualizar este diccionario con pares de otro diccionario
        
        Args:
            otro_diccionario (Diccionario): Diccionario con pares a agregar
        """
        if not isinstance(otro_diccionario, Diccionario):
            return
        
        pares_otros = otro_diccionario.obtener_pares().recorrer()
        for par in pares_otros:
            self.insertar(par.get_clave(), par.get_valor())
    
    def clonar(self):
        """
        Crear una copia del diccionario
        
        Returns:
            Diccionario: Copia del diccionario actual
        """
        nuevo_diccionario = Diccionario()
        pares = self.__pares.recorrer()
        for par in pares:
            nuevo_diccionario.insertar(par.get_clave(), par.get_valor())
        return nuevo_diccionario
    
    def obtener_clave_por_valor(self, valor):
        """
        Buscar la primera clave que tenga el valor especificado
        
        Args:
            valor: El valor a buscar
            
        Returns:
            La clave asociada al valor o None si no se encuentra
        """
        pares = self.__pares.recorrer()
        for par in pares:
            if par.get_valor() == valor:
                return par.get_clave()
        return None
    
    def filtrar_por_criterio(self, criterio):
        """
        Filtrar pares que cumplan con un criterio específico
        
        Args:
            criterio (function): Función que recibe ParClave y retorna bool
            
        Returns:
            Diccionario: Nuevo diccionario con pares que cumplen el criterio
        """
        diccionario_filtrado = Diccionario()
        pares = self.__pares.recorrer()
        for par in pares:
            if criterio(par):
                diccionario_filtrado.insertar(par.get_clave(), par.get_valor())
        return diccionario_filtrado
    
    def aplicar_a_valores(self, funcion):
        """
        Aplicar una función a todos los valores del diccionario
        
        Args:
            funcion (function): Función a aplicar a cada valor
        """
        pares = self.__pares.recorrer()
        for par in pares:
            nuevo_valor = funcion(par.get_valor())
            par.set_valor(nuevo_valor)
    
    def __buscar_par(self, clave):
        """
        Método privado para buscar un par por clave
        
        Args:
            clave: La clave a buscar
            
        Returns:
            ParClave: El par encontrado o None si no existe
        """
        def criterio(par):
            return par.get_clave() == clave
        
        return self.__pares.buscar(criterio)
    
    def __str__(self):
        """
        Representación en string del diccionario
        
        Returns:
            str: Representación del diccionario
        """
        if self.esta_vacio():
            return "Diccionario{}"
        
        resultado = "Diccionario{"
        pares = self.__pares.recorrer()
        primera_iteracion = True
        
        for par in pares:
            if not primera_iteracion:
                resultado += ", "
            resultado += str(par)
            primera_iteracion = False
        
        resultado += "}"
        return resultado
    
    def __repr__(self):
        """
        Representación técnica del diccionario
        
        Returns:
            str: Representación técnica
        """
        return f"Diccionario(tamaño={self.obtener_tamaño()})"
    
    def __eq__(self, other):
        """
        Comparar diccionarios
        
        Args:
            other (Diccionario): Otro diccionario para comparar
            
        Returns:
            bool: True si son iguales
        """
        if not isinstance(other, Diccionario):
            return False
        
        if self.obtener_tamaño() != other.obtener_tamaño():
            return False
        
        # Verificar que todas las claves y valores coincidan
        claves = self.obtener_claves().recorrer()
        for clave in claves:
            if not other.contiene_clave(clave):
                return False
            if self.obtener(clave) != other.obtener(clave):
                return False
        
        return True