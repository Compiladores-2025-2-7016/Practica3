import sys
from analisis.sintactico import Parser
from analisis.lexico import Lexer

def main():
    # Verificar si se proporcionó un archivo como argumento
    if len(sys.argv) > 1:
        try:
            # Intentamos abrir el archivo especificado
            with open(sys.argv[1], 'r') as file:
                data = file.read()
            print(f"Leyendo archivo: {sys.argv[1]}")
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{sys.argv[1]}'")
            return
        except Exception as e:
            print(f"Error al leer el archivo: {str(e)}")
            return
    else:
        # Si no se proporcionó un archivo, usamos una cadena de prueba
        data = """int a, b;
        float c;
        a = 5;
        b = a + 10;
        if (b > 10)
            c = 1.5;
        else
            c = 2.5;
        while (a > 0)
            a = a - 1;
        """
        print("Usando cadena de prueba predeterminada.")
        print("Para usar un archivo, ejecute: python main.py <archivo>")

    # Creamos el analizador léxico
    scanner = Lexer()
    scanner.build()

    # Configuramos la entrada para el analizador léxico
    scanner.lexer.input(data)

    # Creamos el analizador sintáctico y ejecutamos el análisis
    parser = Parser(scanner)
    parser.parse()

if __name__ == "__main__":
    main()