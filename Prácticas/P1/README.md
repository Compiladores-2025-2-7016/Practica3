<p  align="center">
  <img  width="200"  src="https://www.fciencias.unam.mx/sites/default/files/logoFC_2.png"  alt="">  <br>Compiladores  2025-2 <br>
  Práctica 1: Analizadores léxicos con Lex (PLY) <br> Profesora: Ariel Adara Mercado Martínez
</p>

## Análisis léxico con Flex
### Objetivo:
Que el alumno conozca y utilice los principios para generar analizadores léxicos utilizando Lex.

### Introducción
Lex es una herramienta para generar analizadores léxicos, que se deben describir mediante las expresiones regulares de los tokens que serán reconocidas por el analizador léxico (scanner o lexer). Originalmente fue desarrollado para el sistema operativo Unix, pero con la popularidad de Linux se han creado diversas versiones de este generador para varios lenguajes de programación.

#### Estructura de un archivo Lex
Un programa en LEX hecho con PLY consta de al menos estos tres elementos:
- La lista de tokens (o componentes léxicos).
- Especificación de tokens mediante expresiones regulares.
- Código en Python auxiliar o de construcción.


#### Lista de tokens
Todos los analizadores léxicos hechos con PLY, deben proporcionar una lista de tokens. Esta lista siempre es requerida y se utiliza para declarar los tokens realizar una variedad de comprobaciones de validación. La lista de tokens es utilizada por el módulo yacc.py para identificar los terminales.

Debe ser una lista de Python cuyo nombre de variable sea ```tokens``` y cuyos valores sean cadenas en mayúsculas con el nombre de cada componente léxico.

Por ejemplo:
```python
tokens = ['LPAREN', 'RPAREN', ... , 'PLUS', 'INTEGER']
```


#### Especifcación de tokens mediante expresiones regulares
La forma en que PLY nos ayudará a reconocer cada lexema perteneciente a una clase léxica en nuestra entrada, es mediante una expresión regular escrita al estilo del modulo ```re``` de Python. Cada una de estas reglas se define haciendo declaraciones con un prefijo especial **t\_** para indicar que define un token. 

- Para tokens simples, la expresión regular puede especificarse en asignaciones como esta:
    ```python
    t_PLUS = r'+'   # reconocemos el lexema '+'
    ````
    En este caso, el nombre que sigue al prefijo **t\_** debe coincidir exactamente con uno de los nombres proporcionados en tokens. 
    
- Si se necesita realizar alguna acción léxica, una regla de token puede especificarse como una función. Por ejemplo, esta regla encuentra incidencias de números enteros positivos y convierte la cadena en un entero de Python, que después podemos acceder y utilizar:
    ```python
    def t_INTEGER(t):
        r'[0-9]+' # docstring debe contener la regex 
        t.value = int(t.value)
        return t
    ```



#### Sección de código de usuario 
A lo largo de la definición de PLY podemos hacer uso de nuestras propias variables, funciones u objetos que nos auxilien en el Análisis Léxico o su integración con el proceso de compilación en general. 

Un ejemplo de lo que requerimos hacer con código de usuario es la construcción del objeto de lex, así como la "tokenización" de la entrada.

Por lo general es la forma en que podemos agregar la función main.

Por ejemplo:
```python
# Construimos el An. Léxico previa definción
scanner = ply.lex.lex()

# Una cadena de entrada ejemplo
codigo_fuente = '''
hola mundo
'''

# Asignamos la cadena como entrada
scanner.input(codigo_fuente)

# Descomposición de la entrada en componentes léxicos
while True:
    token = scanner.token()
    if not token: 
        break      # No hay nada más que tokenizar
    print(token)

```

#### Metacaracteres

| Caracter | Descripción |
|----------|-------------|
|c         |Cualquier carácter representado por c que no sea un operador|
|\c        |El carácter c literalmente|
|"S"       |La cadena s, literalmente|
|.         |Cualquier carácter excepto el salto de lı́nea|
|∧         |Inicio de línea|
|$         |Fin de lı́nea|
|[s]       |Cualquier carácter incluido dentro de la cadena s|
|[^s]      |Cualquier carácter que no esté dentro de s|
|\n        |Salto de lı́nea|
|*         |Cerradura de Kleene|
|+         |Cerradura positiva|
|\|        |Disyunción|
|?         |Cero o una instancia|
|{m, n}    |Entre m y n instancias de una expresión que le antecede

 

## Primer programa en PLY

### Instalación de PLY
#### Prerrequisitos
- Python 3.X

Puedes verificar tu instalación desde la terminal ejecutando:
```bash
python --version
```

#### Creación de un entorno virtual

1. Dentro de la carpeta de la práctica _P1/_ crear un entorno virtual ejecutando lo siguiente:
    ```bash
    python -m venv <NOMBRE_DE_ENTORNO_VIRTUAL>
    ```

2. Activar el entorno virtual mediante:
    ```bash
    source <NOMBRE_DE_ENTORNO_VIRTUAL>/bin/activate 
    ```

    Que debe agregar un prefijo al prompt de su terminal parecido a lo siguiente:
    ```bash
    (<NOMBRE_DE_ENTORNO_VIRTUAL>)[user@host P1/]$ ▯
    ```

3. Una vez activado instalamos las dependencias definidas en **requirements.txt** de la siguiente manera:
    ```bash
    (<NOMBRE_DE_ENTORNO_VIRTUAL>)[user@host P1/]$ pip install -r requirements.txt
    ```

    O si lo preferimos, instalamos manualmente PLY o cualquier otra dependencia que necesitemos como sigue:
    ```bash
    (<NOMBRE_DE_ENTORNO_VIRTUAL>)[user@host P1/]$ pip install ply
    ```

4. Confirmamos que tenemos instalado el paquete importandolo en alguna ejecución de nuestro interprete. Pueden hacerlo con una validación sencilla como se muestra a continuación:
    ```bash
    (<NOMBRE_DE_ENTORNO_VIRTUAL>)[user@host P1/]$ echo "import ply.lex; print(ply.lex)" | python
    ```

    Si tuvimos éxito, debe imprimirse algo como:

    ```python
    <module 'ply.lex' from '/.../<NOMBRE_ENTORNO_VIRTUAL>/lib/python3.X/site-packages/ply/lex.py'>
    ```

    De lo contrario obtendremos un error similar a este:
    ```python
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ModuleNotFoundError: No module named 'ply'
    ```
    En cuyo caso será necesario repetir cuidadosamente los pasos anteriores. 


### Primer programa en PLY


```python
import sys
import ply.lex as lex
from ply.lex import TOKEN

# Definiciones de expresiones regulares auxiliares
digito = r'[0-9]'
numero = r'(' + digito + r')+'
letra = r'[a-zA-Z]'


# Lista de tokens. Siempre REQUERIDO
tokens = (
    "PALABRA",
    "NUMERO",
    "PARIZQ",
    "PARDER",
)


# Definición de reglas en una sóla línea sin acción léxica
t_PALABRA = r'(' + letra + r'+)'
t_PARIZQ = r'\('
t_PARDER = r'\)'


# Definición de reglas con acción léxica
#@TOKEN(numero)
@TOKEN(r'(' + digito + r')+')
def t_NUMERO(t):
    print("Encontré un número:", t.value)
    return t


# Definimos una regla para el manejo de número de líneas
def t_newline(t):
    r'\n+' # docstring contiene la regex que maneja el salto de línea
    t.lexer.lineno += len(t.value) # Aumentamos la variable de número de línea del Analizador


# Una cadena que contiene todos los caracteres que deben ignorarse
# ej. Espacios y tabuladores
t_ignore  = " \t"

# Esta función nos permite manejar el estado de error a nuestra conveniencia
def t_error(t):
    print("Error léxico. Caracter no reconocido: '%s'" % t.value[0])
    t.lexer.skip(1)




###### Instanciación y uso del Analizador Léxico ######

# Construcción del Scanner
lexer = lex.lex()


# Código fuente
data = '''
Hola mundo 
La respuesta es 42
'''

# En caso de que estemos leyendo un archivo señalado desde la línea de argumentos
if (len(sys.argv) > 1):
    with open(sys.argv[1], 'r') as file:
        data = file.read()

lexer.input(data)

# Tokenización
while True:
    tok = lexer.token()
    if not tok: 
        break      # Termina el análisis
    print(tok)

```

#### Pasos
a. Transcribir el código anterior a un archivo con extensión .py dentro de la carpeta *src/__primer_lex__/* <br>
b. Ejecutar mediante la instrucción: ```python archivo.py``` <br>
c. Crear un archivo de texto que será la entrada: ```echo "Hay 100 nubes en el cielo hoy" > input.txt``` <br>
d. Ejecutar mediante: ```python main.py input.txt```
(5 pts)

#### Ejercicios 
1. ¿Qué ocurre si agregamos una regla simple como ```t_espacio = r'\ +'``` y nada más? (0.5 pts)
2. ¿Qué ocurre si quitamos algún elemento de la lista de tokens? (0.5 pts)
3. ¿Cómo podemos calcular la posición en columna en caso de un error léxico? (0.5 pts)
4. ¿Qué significa el valor que se aloja en ```t.value```? (0.5 pts)
5. ¿Qué pasa al ejecutar el programa e introducir cadenas de caracteres y de dígitos sin espacios en el archivo de entrada? (0.5 pts)
6. ¿Qué ocurre si introducimos caracteres como "\*" en el archivo de entrada? (0.5 pts)
7. Modificar al código anterior en un archivo nuevo, de tal manera que ejecute una acción léxica al detectar lo siguiente: (2 pts)
    1. La expresión regular para los hexadecimales en lenguaje C.
    2. 5 palabras reservadas del lenguaje Python.
    3. Los identificadores válidos del lenguaje Java, con longitud máxima de 32 caracteres (**Sugerencia**: use el operador {m,n}).
    4. Los espacios en blanco.

