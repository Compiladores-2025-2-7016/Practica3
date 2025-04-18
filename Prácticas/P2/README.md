<p  align="center">
  <img  width="200"  src="https://www.fciencias.unam.mx/sites/default/files/logoFC_2.png"  alt="">  <br>Compiladores  2025-2 <br>
  Práctica 2: Analizadores léxicos con Lex (PLY) <br> Profesora: Ariel Adara Mercado Martínez
</p>

## Analizador léxico para el lenguaje C_1
### Objetivo:
Que el alumno conozca y utilice los principios para generar analizadores léxicos utilizando Lex.

### Introducción
Lex es una herramienta para generar analizadores léxicos, que se deben describir mediante las expresiones regulares de los tokens que serán reconocidas por el analizador léxico (scanner o lexer). Originalmente fue desarrollado para el sistema operativo Unix, pero con la popularidad de Linux se han creado diversas versiones de este generador para varios lenguajes de programación.

### Estructura del directorio
```c++
P2
├── README.md
└── src
    ├── main
    │   ├── __init__.py
    │   ├── componente
    │   │   ├── __init__.py
    │   │   ├── clase_lexica.py // Enum que contiene todas las clases léxicas del lenguaje a reconocer
    │   │   └── componente_lexico.py // Estructura de datos que conforma un token. Una clase léxica y su lexema asociado.
    │   ├── lexer
    │   │   ├── __init__.py
    │   │   └── scanner.py // Definición de PLY del Analizador Léxico a generar. 
    │   └── main.py // Script o clase principal que se ejecutará para manejar la entrada del usuario del lenguaje, 
    └── tst
        └── input.txt // archivo ejemplo de código fuente en nuestro lenguaje de programación de a mentis. 
```

### Uso

#### Ejecución ejemplo

Con el código sin cambio alguno, ya pueden realizar una ejecución como sigue: 

```bash
$ cd src/
$ python main.py
```

Producirá la siguiente salida:
```
Encontré un número: 3
LexToken(NUMERO,'3',1,0)
LexToken(PALABRA,'y',1,2)
Encontré un número: 4
LexToken(NUMERO,'4',1,4)
```

#### Ejecución esperada

```bash
$ cd src/
$ python main.py tst/input.txt 
```


#### Salida esperada
```
<INT, int>
<FLOAT, float>
<IF, if>
<ELSE, else>
<WHILE, while>
<INT, int>
<NUMERO, 12345>
<NUMERO, 1.2e6>
<ID, a1>
<ID, a_23>
<ID, ___>
<ID, id2>
<ID, if3>
<ID, while4>
<ID, _b>
<PYC, ;>
<COMA, ,>
<LPAR, (>
<RPAR, )>
<INT, int>
<RPAR, )>
<ID, a>
<ID, _qbcaaa>
```


#### Ejercicios
1. Crear la lógica necesaria para recibir nuestro archivo de entrada _tst/input.txt_. **(2 pts)**
2. Describir el conjunto de terminales en _clase_lexica.py_. **(4 pts)**
3. Generar acciones léxicas para cada terminal de nuestro lenguaje en _scanner.py_, de modo que se muestre en pantalla la salida esperada con el archivo _prueba.txt_. **(4 pts)**
*Hint: Crear primero un objeto de tipo ComponenteLexico y después imprimirlo al momento de identificar un patrón o al finalizar el análisis léxico.* 

---
#### Extras

4. Modificar lo necesario para producir una salida que considere no guardar lexemas que son los únicos miembros de su clase léxica. (0.5 pts.)
5. Documentar el código con las convenciones de Python. (0.25 pts.)
6. Proponer 4 archivos de prueba nuevos, 2 válidos y 2 inválidos. (0.25 pts.)



