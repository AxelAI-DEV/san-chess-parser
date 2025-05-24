# Parser SAN - Árbol de Turnos de Partidas de Ajedrez 

## Descripción

Este proyecto es la solución a la práctica III del Lenguajes de Programación, impartido en la Universidad EAFIT, mayo 2025.

Consiste en un programa que recibe una partida de ajedrez escrita en notación algebraica estándar (SAN), valida sintácticamente cada movimiento según una gramática BNF, y si la partida es válida, la representa mediante un árbol binario visual por turnos.

## Funcionalidades

- Validación sintáctica de movimientos individuales y turnos completos.
- Detección y notificación de errores en movimientos inválidos.
- Visualización gráfica en árbol binario donde cada nodo representa un turno, con movimientos de blancas y negras.
- Interfaz gráfica amigable desarrollada con PyQt5.

## Tecnologías

- Lenguaje: Python 3.10+
- Biblioteca gráfica: PyQt5
- Expresiones regulares para validación según gramática BNF

## Estructura del repositorio

- `main.py`: Código principal con la implementación del parser y la interfaz.
- `README.md`: Este archivo con la descripción y guía.
- Otros archivos: (si aplican)

## Instrucciones para ejecutar

1. Clonar el repositorio:
git clone https://github.com/AxelAI-DEV/san-chess-parser.git
cd repositorio_parser_san

2. Instalar dependencias:
pip install PyQt5

3. Ejecutar el programa:
python main.py


4. En la interfaz, ingresar la partida en SAN en el campo de texto y presionar "Parsear y Mostrar Árbol" para visualizar la estructura.

## Integrantes

- Axel Cardona Vasquez

## Entorno de desarrollo

- Lenguaje: Python 3.10
- IDE: Visual Studio Code
- Sistema operativo: Windows 10

## Observaciones

La práctica cumple con la especificación entregada, realizando validación sintáctica y mostrando el árbol binario intercalado por turnos.

---

### Referencia

- Profesor: Alexander Narváez Berrío  
- Curso: ST0244 - Lenguajes de Programación  
- Universidad EAFIT, Mayo 2025
