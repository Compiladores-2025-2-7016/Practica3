# Analizador Sintáctico de Descenso Recursivo

## Análisis de la Gramática

### 1. Conjuntos N, Σ y símbolo inicial S

**N (No terminales):**
- programa
- declaraciones
- declaracion
- tipo
- lista_var
- sentencias
- sentencia
- expresion

**Σ (Terminales):**
- int
- float
- identificador
- numero
- ;
- ,
- =
- if
- else
- while
- (
- )
- +
- -
- *
- /

**S (Símbolo inicial):** programa

### 2. Eliminación de ambigüedad

La gramática presenta ambigüedad en las expresiones aritméticas, ya que no define la precedencia entre operadores. Por ejemplo, en una expresión como "a + b * c", no está claro si debe interpretarse como "(a + b) * c" o "a + (b * c)".

Para eliminar esta ambigüedad, redefino las expresiones con diferentes niveles de precedencia:
expresion → expresion_suma
expresion_suma → expresion_suma + expresion_mult | expresion_suma - expresion_mult | expresion_mult
expresion_mult → expresion_mult * expresion_unaria | expresion_mult / expresion_unaria | expresion_unaria
expresion_unaria → identificador | numero | ( expresion )


Esto establece que la multiplicación y división tienen mayor precedencia que la suma y resta, lo cual es el comportamiento esperado en la mayoría de los lenguajes de programación.

### 3. Eliminación de recursividad izquierda

La gramática tiene recursividad izquierda en varias producciones:

1. `declaraciones → declaraciones declaracion | declaracion`
2. `lista_var → lista_var , identificador | identificador`
3. `sentencias → sentencias sentencia | sentencia`
4. Las expresiones que acabamos de redefinir

Para eliminar la recursividad izquierda, aplico la siguiente transformación:

Para una producción de la forma A → Aα | β, la transformación es:
A → βA'
A' → αA' | ε

Aplicando esto a nuestras producciones:

1. Para `declaraciones`:
declaraciones → declaracion declaraciones_prima
declaraciones_prima → declaracion declaraciones_prima | ε


2. Para `lista_var`:
lista_var → identificador lista_var_prima
lista_var_prima → , identificador lista_var_prima | ε


3. Para `sentencias`:
sentencias → sentencia sentencias_prima
sentencias_prima → sentencia sentencias_prima | ε


4. Para las expresiones:
expresion → expresion_mult expresion_suma_prima
expresion_suma_prima → + expresion_mult expresion_suma_prima | - expresion_mult expresion_suma_prima | ε
expresion_mult → expresion_unaria expresion_mult_prima
expresion_mult_prima → * expresion_unaria expresion_mult_prima | / expresion_unaria expresion_mult_prima | ε
expresion_unaria → identificador | numero | ( expresion )


### 4. Factorización izquierda

Después de analizar la gramática resultante de las transformaciones anteriores, no encuentro producciones que requieran factorización izquierda, ya que no hay producciones con prefijos comunes.

La factorización izquierda se aplica cuando tenemos producciones de la forma:
A → αβ₁ | αβ₂

Que se transforman en:
A → αA'
A' → β₁ | β₂

En nuestra gramática transformada, no hay producciones que tengan esta forma, por lo que no es necesario aplicar factorización izquierda.

### 5. Gramática resultante

Después de aplicar las transformaciones para eliminar la ambigüedad y la recursividad izquierda, la gramática queda así:

**N (No terminales):**
- programa
- declaraciones
- declaraciones_prima
- declaracion
- tipo
- lista_var
- lista_var_prima
- sentencias
- sentencias_prima
- sentencia
- expresion
- expresion_suma_prima
- expresion_mult
- expresion_mult_prima
- expresion_unaria

**P (Producciones):**
programa → declaraciones sentencias
declaraciones → declaracion declaraciones_prima
declaraciones_prima → declaracion declaraciones_prima | ε
declaracion → tipo lista_var ;
tipo → int | float
lista_var → identificador lista_var_prima
lista_var_prima → , identificador lista_var_prima | ε
sentencias → sentencia sentencias_prima
sentencias_prima → sentencia sentencias_prima | ε
sentencia → identificador = expresion ; | if ( expresion ) sentencias else sentencias | while ( expresion ) sentencias
expresion → expresion_mult expresion_suma_prima
expresion_suma_prima → + expresion_mult expresion_suma_prima | - expresion_mult expresion_suma_prima | ε
expresion_mult → expresion_unaria expresion_mult_prima
expresion_mult_prima → * expresion_unaria expresion_mult_prima | / expresion_unaria expresion_mult_prima | ε
expresion_unaria → identificador | numero | ( expresion )


Esta gramática ya no tiene ambigüedad ni recursividad izquierda, y está lista para ser implementada en un analizador sintáctico de descenso recursivo.
Este README.md contiene el análisis completo de la gramática, incluyendo:

Los conjuntos N, Σ y el símbolo inicial S
El proceso de eliminación de ambigüedad
El proceso de eliminación de recursividad izquierda
La justificación de por qué no es necesaria la factorización izquierda
Los nuevos conjuntos N y P resultantes