Parser SAN - Árbol de Turnos de Partidas de Ajedrez

Descripción

Este proyecto es la solución a la Práctica III del curso Lenguajes de Programación de la Universidad EAFIT (mayo de 2025).

Se trata de una aplicación que recibe como entrada una partida de ajedrez escrita en notación SAN (notación algebraica estándar), verifica que cada jugada sea válida y, si todo está correcto, genera una visualización gráfica en forma de árbol binario, mostrando los turnos de la partida jugada por jugada.

¿Qué hace el programa?

* Revisa que cada movimiento siga las reglas sintácticas de SAN.
* Indica si alguna jugada está mal escrita o fuera de lugar.
* Si todo está bien, dibuja un árbol binario donde se muestran las jugadas de las blancas y las negras en cada turno.
* Usa una interfaz gráfica sencilla para facilitar su uso.

Herramientas utilizadas

* Python 3.10 o superior
* PyQt5 para la parte gráfica
* Expresiones regulares para validar la notación SAN

Archivos del proyecto

* main.py: contiene todo el código de la aplicación.
* README.md: este archivo con la explicación del proyecto.
* (Otros archivos si son necesarios para correr el programa)

¿Cómo se usa?

1. Clona este repositorio:
git clone https://github.com/AxelAI-DEV/san-chess-parser.git
cd san-chess-parser


2. Instala las dependencias necesarias:
pip install PyQt5


3. Ejecuta el archivo principal:
python main.py


4. Cuando se abra la ventana, escribe la partida en el recuadro (en notación SAN) y haz clic en **“Parsear y Mostrar Árbol”**. Si todo está bien, verás el árbol gráfico en la parte inferior.

Autor

* Axel Cardona Vásquez

Entorno de desarrollo

* Python 3.10
* Visual Studio Code
* Windows 10

Nota final

Este proyecto sigue las especificaciones dadas por el profesor, y cumple con lo solicitado en cuanto a validación y representación gráfica del árbol binario por turnos.

Profesor y curso

* Profesor: Alexander Narváez Berrío
* Curso: ST0244 - Lenguajes de Programación
* Universidad EAFIT – Mayo 2025
