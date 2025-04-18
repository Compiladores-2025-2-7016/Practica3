import ply.lex as lex
from ply.lex import TOKEN, LexToken
from componente.clase_lexica import ClaseLexica
from componente.componente_lexico import ComponenteLexico


class Lexer(object):
    # Definiciones de expresiones regulares auxiliares
    digito = r'[0-9]'
    numero = r'(' + digito + r')+'
    letra = r'[a-zA-Z_]'  # Incluimos _ para identificadores
    identificador = r'(' + letra + r')(' + letra + r'|' + digito + r')*'

    # Lista de tokens. Siempre REQUERIDO
    tokens = list(ClaseLexica._member_names_)

    # Palabras reservadas
    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE'
    }

    # Definición de reglas en una sóla línea sin acción léxica
    t_PARIZQ = r'\('
    t_PARDER = r'\)'
    t_PUNTOYCOMA = r';'
    t_COMA = r','
    t_IGUAL = r'='
    t_MAS = r'\+'
    t_MENOS = r'-'
    t_POR = r'\*'
    t_DIVIDIDO = r'/'
    t_MAYOR = r'>'
    t_MENOR = r'<'
    t_MAYORIGUAL = r'>='
    t_MENORIGUAL = r'<='
    t_IGUALIGUAL = r'=='
    t_DISTINTO = r'!='
    t_ESPACIO = r'\ +'

    # Definición de reglas con acción léxica
    @TOKEN(numero)
    def t_NUMERO(self, t):
        print("Encontré un número:", t.value)
        return t

    @TOKEN(identificador)
    def t_IDENTIFICADOR(self, t):
        # Revisar si es una palabra reservada
        t.type = self.reserved.get(t.value, 'IDENTIFICADOR')
        print("Encontré un token:", t.type, "con valor:", t.value)
        return t

    # Definimos una regla para el manejo de número de líneas
    def t_newline(self, t):
        r'\n+' # docstring contiene la regex que maneja el salto de línea
        t.lexer.lineno += len(t.value) # Aumentamos la variable de número de línea del Analizador

    # Una cadena que contiene todos los caracteres que deben ignorarse
    # ej. Espacios y tabuladores
    t_ignore  = " \t"

    # Esta función nos permite manejar el estado de error a nuestra conveniencia
    def t_error(self, t):
        print("Error léxico. Caracter no reconocido: '%s'" % t.value[0])
        t.lexer.skip(1)

    # Función que nos permite construir el analizador léxico
    # NO TOCAR
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Función que nos permite efectuar un análisis léxico
    # sobre una entrada
    def scan(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)