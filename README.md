# schedule_generator
Este repositorio contiene un programa para generar guías de horarios universitarios, con base en las necesidades de la Facultad de Farmacia de la Universidad de Costa Rica. Responde a la asignación final del curso: Proyecto Eléctrico - IE0499 de la Escuela de Ingeniería Eléctrica.

## Requisitos
* Python 3.x

## Dependencias
El programa requiere las siguientes bibliotecas de Python:
* tkinter: para la interfaz gráfica de usuario.
* csv: para la lectura y escritura de archivos CSV.
* random: para generar números aleatorios.
* math: para realizar cálculos matemáticos.
* sys: para acceder a algunas variables utilizadas o mantenidas por el intérprete y para funciones que interactúan fuertemente con el intérprete.
* time: para acceder a funciones que nos permiten manejar operaciones relacionadas con el tiempo.
* subprocess: para ejecutar procesos.
* threading: para ejecutar hilos.

La mayoría de estas bibliotecas son parte de la biblioteca estándar de Python y no deberían requerir instalación adicional. Sin enmbargo, es posible que algunas de estas sí lo requieran.

## Guía de usuario
El programa toma archivos 2 archivos `csv` de entrada. Uno con las diferentes posibilidades y otro con las restricciones de los cursos de servicio. Genera `n` soluciones se le pidan, cada una de estas es una guía de horarios distinta, y cada una se genera su respectivo archivo `csv` de salida.

#### Clone el repositorio
* HTTPS: `git clone https://github.com/Jams1001/schedule_generator.git`
* SSH: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`git clone git@github.com:Jams1001/schedule_generator.git`
#### Cambie a la rama develop
`git switch develop`
#### Ejecute el programa
`python3 generador.py`  
![Main del programa](/images/1.png)
#### Cargue los archivos de entrada
Toque los botones "Cargar csv de disponibilidad" y "Cargar csv de cursos de servicio". Una vez cargados, aparecerá la ruta de estos archivos para confirmar que se cargaron. En este punto puede reemplazar los archivos cargados volviendo a tocar los botones.  
![Main del programa](/images/2.png)
#### Elija un nombre base para los archivos de salida
Escriba en el espacio "Nombre de las soluciones a generar:" el nombre base de los archivos. Es posible generar más de una solución, por lo tanto, el nombre para la solución _n_ será `nombre-base_n`.  
![Main del programa](/images/3.png)
#### Indique el número de soluciones
Escriba en el espacio "Número de soluciones a generar:" el número de soluciones que desee generar. Se generán tantas soluciones indique, siempre y cuando el parámetro esté dentro del rango posible para la disponibilidad de la entrada utilizada.
#### Ejecute el programa
1. Toque el botón "Ejecutar", el cual abrirá una ventana para seleccionar un directorio en donde guardar las soluciones generadas.
2. Espere a que se actualice el estado a "Listo".
3. Utilice las soluciones generadas en el directorio seleccionado.  
![Main del programa](/images/4.png)

## Sobre los archivos de entrada

### Archivo de disponibilidad
Debe ser necesariamente un archivo `.csv` respetando la primera fila del ejemplo proporciado. 
Ejemplo:  
| bloque | sigla      | horas_semanales | dias_semana | profesor   | disponibilidad |  |
|--------|------------|-----------------|-------------|------------|----------------|-------------------|
| 3      | lineales1  | 4               | 2           | JDR        | M:T            | 2                 |
| 4      | lineales2  | 4               | 2           | Gonzalo    | N              | 3:2               |
| 4      | electro1   | 4               | 2           | Carlos     | T              | 1                 |
| 6      | maquinas1  | 4               | 2           | Fausto     | M              | 2                 |
| 6      | LabMaquinas| 3               | 1           | LuisDiego  | N              | 2                 |
| 6      | Compus1    | 5               | 2           | Ericka     | T              | 5                 |
| 5      | Campo2     | 3               | 2           | LuisDiego  | M              | 6                 |
| 6      | Labelectro2| 4               | 1           | Rosses     | T:N            | 1                 |
| 4      | Analisis   | 4               | 2           | Joaquin    | M              | 4                 |
| 5      | electro2   | 5               | 2           | Rosses     | M              | 2                 |
| 8      | Redes      | 5               | 2           | Isaac      | T:N            | 6                 |
| 7      | Control    | 4               | 2           | Helber     | M              | 2                 |
| 8      | Diseño     | 4               | 2           | Fernando   | N              | 4                 |
| 6      | Respo      | 3               | 1           | Yandell    | N              | 1                 |
| 8      | Micros     | 4               | 1           | Villalta   | M              | 5                 |
| 3      | plataformas| 6               | 2           | Benavides  | N              | 12                |

* **bloque:** Bloque al que pertenece el curso.
* **sigla:** Nombre Identificador del curso.
* **horas_semanales:** Cantidad total de horas semanales del curso.
* **dias_semana:** Días a la semana en los que se debe repartir el curso (1 o 2 únicamente).
* **profesor:** Nombre identificador del docente del curso.
* **disponibilidad:** Disponibilidad del docente para impartir el curso. No requiere un orden específico. El único requisito es separar la disponibilidad con ":" para cada letra. Es posible elegir entre:
    * M: 7:00 a 12:00
    * T: 13:00 a 17:00
    * N: 17:00 a 21:00  
* **aulas_disponibles:** Aulas disponibles en las que se puede dar ese curso. Puede ser texto o número, el único requisito es separar las aulas disponibles con ":".

### Archivo de cursos de servicio
Debe ser necesariamente un archivo `.csv` respetando la primera fila del ejemplo proporciado. 
Ejemplo: 
| bloque | sigla    | horario            |
|--------|----------|--------------------|
| 3      | quimica1 | Lunes:7-21 y Jueves:7-21 |
| 2      | quimica2 | Jueves:7-21 y Miércoles:7-21 y Martes:7-21 |
| 4      | fisica | Jueves:7-21 |

* **bloque:** Bloque al que pertenece el curso.
* **sigla:** Nombre Identificador del curso.
* **horario:** Horario del curso. Debe seguir específicamente el ejemplo proporcionado 
    * Formato Genérico: `Día:HoraInicio-HoraFin y Día:HoraInicio-HoraFin`
    * Día: Solo Lunes, Martes, Miércoles, Jueves, Viernes.
    * Formato de Hora: Rango en formato 24.
    * Separación de Días: Uso de "y" para separar diferentes combinaciones.

### Archivo de salida
A continuación se presenta a modo de ejemplo una solución generada para determinadas entradas.  
| Bloque | Sigla      | Horario                 | Profesor  | Aula | Grupo | Cupo | Observaciones |
|--------|------------|-------------------------|-----------|------|-------|------|---------------|
| 3      | lineales1  | Martes:7-9 y Viernes:7-9| JDR       | 2    |       |      |               |
| 3      | plataformas| Martes:17-20 y Viernes:17-20 | Benavides | 12   |       |      |               |
| 4      | lineales2  | Lunes:17-19 y Jueves:17-19 | Gonzalo   | 3    |       |      |               |
| 4      | electro1   | Lunes:13-15 y Jueves:13-15 | Carlos    | 1    |       |      |               |
| 4      | Analisis   | Lunes:7-9 y Jueves:7-9  | Joaquin   | 4    |       |      |               |
| 5      | Campo2     | Lunes:7-9 y Jueves:7-8  | LuisDiego | 6    |       |      |               |
| 5      | electro2   | Lunes:9-12 y Jueves:9-11| Rosses    | 2    |       |      |               |
| 6      | Respo      | Martes:17-20            | Yandell   | 1    |       |      |               |
| 6      | maquinas1  | Lunes:7-9 y Jueves:7-9  | Fausto    | 2    |       |      |               |
| 6      | LabMaquinas| Lunes:17-20             | LuisDiego | 2    |       |      |               |
| 6      | Compus1    | Lunes:13-16 y Jueves:13-15 | Ericka  | 5    |       |      |               |
| 6      | Labelectro2| Martes:13-17            | Rosses    | 1    |       |      |               |
| 7      | Control    | Martes:9-11 y Viernes:9-11 | Helber  | 2    |       |      |               |
| 8      | Redes      | Lunes:13-16 y Jueves:13-15 | Isaac   | 6    |       |      |               |
| 8      | Diseño     | Lunes:17-19 y Jueves:17-19 | Fernando | 4   |       |      |               |
| 8      | Micros     | Lunes:7-11              | Villalta  | 5    |       |      |               |

### Notas adicionales

* Las tres columnas adicionales en el archivo generado se deben llenar manualmente si así se desea.
* Si se desea más de un grupo para determinado curso se debe agregar en el archivo de entrada como si fuera otro curso, simplemente con un identificador para el nombre que lo distinga.  