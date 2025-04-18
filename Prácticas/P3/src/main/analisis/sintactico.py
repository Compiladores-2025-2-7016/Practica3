from analisis.lexico import Lexer
from componente.clase_lexica import ClaseLexica

class Parser:

    def __init__(self, lexer: Lexer):
        self.an_lexico = lexer
        self.token_actual = 0

    def eat(self, clase_lexica: int):
        if self.token_actual == clase_lexica:
            try:
                tok = self.an_lexico.lexer.token()
                if not tok: # No hay mas entrada
                    self.token_actual = 0
                else:
                    self.token_actual = ClaseLexica[tok.type].value
            except Exception as e:
                print("No fue posible leer el siguiente token. {excp}".format(excp=str(e)))
        else:
            print("Se esperaba el token: {esperado} pero se encontró {actual}".format(
                esperado=clase_lexica, actual=self.token_actual))
            self.error("Token inesperado")

    def error(self, msg: str):
        print("ERROR DE SINTAXIS: {mensaje}. En la línea {linea}".format(mensaje=msg,
                                                                        linea=self.an_lexico.lexer.lineno))
        exit(1)

    def parse(self):
        try:
            tok = self.an_lexico.lexer.token()
            if not tok:
                print("Entrada vacía")
                return
            self.token_actual = ClaseLexica[tok.type].value
        except Exception as e:
            print("No fue posible obtener el primer token de la entrada: {excepcion}".format(excepcion=str(e)))
            exit(1)

        self.programa()
        if self.token_actual == 0: # llegamos al EOF sin error
            print("La cadena es aceptada")
        else:
            print("La cadena no pertenece al lenguaje generado por la gramática")

    # Implementación de las funciones para cada no terminal

    def programa(self):
        """programa → declaraciones sentencias"""
        print("Analizando programa")
        self.declaraciones()
        self.sentencias()

    def declaraciones(self):
        """declaraciones → declaracion declaraciones_prima"""
        print("Analizando declaraciones")
        self.declaracion()
        self.declaraciones_prima()

    def declaraciones_prima(self):
        """declaraciones_prima → declaracion declaraciones_prima | ε"""
        print("Analizando declaraciones_prima")
        # Verificamos si el token actual puede ser el inicio de una declaración
        if self.token_actual in [ClaseLexica.INT.value, ClaseLexica.FLOAT.value]:
            self.declaracion()
            self.declaraciones_prima()
        # Si no, asumimos que es epsilon (no hacemos nada)

    def declaracion(self):
        """declaracion → tipo lista_var ;"""
        print("Analizando declaracion")
        self.tipo()
        self.lista_var()
        self.eat(ClaseLexica.PUNTOYCOMA.value)

    def tipo(self):
        """tipo → int | float"""
        print("Analizando tipo")
        if self.token_actual == ClaseLexica.INT.value:
            self.eat(ClaseLexica.INT.value)
        elif self.token_actual == ClaseLexica.FLOAT.value:
            self.eat(ClaseLexica.FLOAT.value)
        else:
            self.error("Se esperaba 'int' o 'float'")

    def lista_var(self):
        """lista_var → identificador lista_var_prima"""
        print("Analizando lista_var")
        self.eat(ClaseLexica.IDENTIFICADOR.value)
        self.lista_var_prima()

    def lista_var_prima(self):
        """lista_var_prima → , identificador lista_var_prima | ε"""
        print("Analizando lista_var_prima")
        if self.token_actual == ClaseLexica.COMA.value:
            self.eat(ClaseLexica.COMA.value)
            self.eat(ClaseLexica.IDENTIFICADOR.value)
            self.lista_var_prima()
        # Si no, asumimos que es epsilon (no hacemos nada)

    def sentencias(self):
        """sentencias → sentencia sentencias_prima"""
        print("Analizando sentencias")
        self.sentencia()
        self.sentencias_prima()

    def sentencias_prima(self):
        """sentencias_prima → sentencia sentencias_prima | ε"""
        print("Analizando sentencias_prima")
        # Verificamos si el token actual puede ser el inicio de una sentencia
        if self.token_actual == ClaseLexica.IDENTIFICADOR.value or \
           self.token_actual == ClaseLexica.IF.value or \
           self.token_actual == ClaseLexica.WHILE.value:
            self.sentencia()
            self.sentencias_prima()
        # Si no, asumimos que es epsilon (no hacemos nada)

    def sentencia(self):
        """sentencia → identificador = expresion ; | if ( expresion ) sentencias else sentencias | while ( expresion ) sentencias"""
        print("Analizando sentencia")
        if self.token_actual == ClaseLexica.IDENTIFICADOR.value:
            self.eat(ClaseLexica.IDENTIFICADOR.value)
            self.eat(ClaseLexica.IGUAL.value)
            self.expresion()
            self.eat(ClaseLexica.PUNTOYCOMA.value)
        elif self.token_actual == ClaseLexica.IF.value:
            self.eat(ClaseLexica.IF.value)
            self.eat(ClaseLexica.PARIZQ.value)
            self.expresion()
            self.eat(ClaseLexica.PARDER.value)
            self.sentencias()
            self.eat(ClaseLexica.ELSE.value)
            self.sentencias()
        elif self.token_actual == ClaseLexica.WHILE.value:
            self.eat(ClaseLexica.WHILE.value)
            self.eat(ClaseLexica.PARIZQ.value)
            self.expresion()
            self.eat(ClaseLexica.PARDER.value)
            self.sentencias()
        else:
            self.error("Se esperaba 'identificador', 'if' o 'while'")

    def expresion(self):
        """expresion → expresion_mult expresion_suma_prima"""
        print("Analizando expresion")
        self.expresion_mult()
        self.expresion_suma_prima()

    def expresion_suma_prima(self):
        """expresion_suma_prima → + expresion_mult expresion_suma_prima | - expresion_mult expresion_suma_prima | ε"""
        print("Analizando expresion_suma_prima")
        if self.token_actual == ClaseLexica.MAS.value:
            self.eat(ClaseLexica.MAS.value)
            self.expresion_mult()
            self.expresion_suma_prima()
        elif self.token_actual == ClaseLexica.MENOS.value:
            self.eat(ClaseLexica.MENOS.value)
            self.expresion_mult()
            self.expresion_suma_prima()
        # Si no, asumimos que es epsilon (no hacemos nada)

    def expresion_mult(self):
        """expresion_mult → expresion_unaria expresion_mult_prima"""
        print("Analizando expresion_mult")
        self.expresion_unaria()
        self.expresion_mult_prima()

    def expresion_mult_prima(self):
        """expresion_mult_prima → * expresion_unaria expresion_mult_prima | / expresion_unaria expresion_mult_prima | ε"""
        print("Analizando expresion_mult_prima")
        if self.token_actual == ClaseLexica.POR.value:
            self.eat(ClaseLexica.POR.value)
            self.expresion_unaria()
            self.expresion_mult_prima()
        elif self.token_actual == ClaseLexica.DIVIDIDO.value:
            self.eat(ClaseLexica.DIVIDIDO.value)
            self.expresion_unaria()
            self.expresion_mult_prima()
        # Si no, asumimos que es epsilon (no hacemos nada)

    def expresion_unaria(self):
        """expresion_unaria → identificador | numero | ( expresion )"""
        print("Analizando expresion_unaria")
        if self.token_actual == ClaseLexica.IDENTIFICADOR.value:
            self.eat(ClaseLexica.IDENTIFICADOR.value)
        elif self.token_actual == ClaseLexica.NUMERO.value:
            self.eat(ClaseLexica.NUMERO.value)
        elif self.token_actual == ClaseLexica.PARIZQ.value:
            self.eat(ClaseLexica.PARIZQ.value)
            self.expresion()
            self.eat(ClaseLexica.PARDER.value)
        else:
            self.error("Se esperaba 'identificador', 'numero' o '('")

    def expresion(self):
        """expresion → expresion_mult expresion_suma_prima expresion_rel_prima"""
        print("Analizando expresion")
        self.expresion_mult()
        self.expresion_suma_prima()
        # Añadimos soporte para operadores relacionales
        self.expresion_rel_prima()

    def expresion_rel_prima(self):
        """expresion_rel_prima → operador_relacional expresion_mult expresion_suma_prima | ε"""
        print("Analizando expresion_rel_prima")
        if self.token_actual in [ClaseLexica.MAYOR.value, ClaseLexica.MENOR.value,
                                ClaseLexica.MAYORIGUAL.value, ClaseLexica.MENORIGUAL.value,
                                ClaseLexica.IGUALIGUAL.value, ClaseLexica.DISTINTO.value]:
            self.operador_relacional()
            self.expresion_mult()
            self.expresion_suma_prima()
        # Si no, asumimos que es epsilon (no hacemos nada)

    def operador_relacional(self):
        """operador_relacional → > | < | >= | <= | == | !="""
        print("Analizando operador_relacional")
        if self.token_actual == ClaseLexica.MAYOR.value:
            self.eat(ClaseLexica.MAYOR.value)
        elif self.token_actual == ClaseLexica.MENOR.value:
            self.eat(ClaseLexica.MENOR.value)
        elif self.token_actual == ClaseLexica.MAYORIGUAL.value:
            self.eat(ClaseLexica.MAYORIGUAL.value)
        elif self.token_actual == ClaseLexica.MENORIGUAL.value:
            self.eat(ClaseLexica.MENORIGUAL.value)
        elif self.token_actual == ClaseLexica.IGUALIGUAL.value:
            self.eat(ClaseLexica.IGUALIGUAL.value)
        elif self.token_actual == ClaseLexica.DISTINTO.value:
            self.eat(ClaseLexica.DISTINTO.value)
        else:
            self.error("Se esperaba un operador relacional")