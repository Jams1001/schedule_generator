import csv
import random
import math
import sys
import time

MORNING_BEGIN = 7
MORNING_END = 12
AFTERNOON_BEGIN = 13
AFTERNOON_END = 17
EVENING_BEGIN = 17
EVENING_END = 21
DEFAULT_NUMBER_SOL = 8


class Curso:
    def __init__(
        self,
        bloque,
        sigla,
        horas_semanales,
        dias_semana,
        profesor,
        disponibilidad,
        aulas,
    ):
        self.bloque = int(bloque)
        self.sigla = sigla
        self.horas_semanales = int(horas_semanales)
        self.dias_por_semana = int(dias_semana)
        self.profesor = profesor
        self.disponibilidad = disponibilidad
        self.aulas = aulas


class CursoServicio:
    def __init__(self, bloque, sigla, horario):
        self.bloque = int(bloque)
        self.sigla = sigla
        self.horarios = self.parse_horarios(horario)

    def parse_horarios(self, horario):
        horarios_separados = horario.split(" y ")
        horarios_procesados = []
        for horario in horarios_separados:
            dia, horas = horario.split(":")
            hora_inicio, hora_fin = map(int, horas.split("-"))
            horarios_procesados.append((dia, hora_inicio, hora_fin))
        return horarios_procesados


class Horario:
    def __init__(
        self,
        bloque,
        curso,
        dia1,
        dia2,
        hora_entrada1,
        hora_entrada2,
        hora_salida1,
        hora_salida2,
        profesor,
        aula,
    ):
        self.bloque = bloque
        self.curso = curso
        self.dia1 = dia1
        self.dia2 = dia2
        self.hora_entrada1 = hora_entrada1
        self.hora_entrada2 = hora_entrada2
        self.hora_salida1 = hora_salida1
        self.hora_salida2 = hora_salida2
        self.profesor = profesor
        self.aula = aula


def leer_archivo(archivo):
    with open(archivo, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # Salta la cabecera del archivo
        return [Curso(*row) for row in reader]


def leer_servicio(archivo):
    with open(archivo, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # Salta la cabecera del archivo
        return [CursoServicio(*row) for row in reader]


"""
    revisar_choques
    Check if there are any clashes between the selected courses and any
    new courses.
    Args:
        lista_horarios: list with selected courses for the solution.
        nuevo_horario: course to be added to the solution.
        cursos_servicio: services course schedules.
    Return:
        boolean with the result if there is a course clash or not.
"""


def revisar_choques(horarios, nuevo_horario, cursos_servicio):
    # Ensures that only one schedule is generated for that course.
    for horario in horarios:
        if horario.curso == nuevo_horario.curso:
            return True

    # Courses from the same block cannot overlap.
    for horario in horarios:
        if horario.bloque == nuevo_horario.bloque:
            if horario.dia1 == nuevo_horario.dia1 and not (
                horario.hora_salida1 <= nuevo_horario.hora_entrada1
                or horario.hora_entrada1 >= nuevo_horario.hora_salida1
            ):
                return True

            if nuevo_horario.dia2 and horario.dia2 == nuevo_horario.dia2:
                if not (
                    horario.hora_salida2 <= nuevo_horario.hora_entrada2
                    or horario.hora_entrada2 >= nuevo_horario.hora_salida2
                ):
                    return True

    # No two courses can be held at the same time in the same classroom.
    for horario in horarios:
        if horario.aula == nuevo_horario.aula:
            if horario.dia1 == nuevo_horario.dia1 and not (
                horario.hora_salida1 <= nuevo_horario.hora_entrada1
                or horario.hora_entrada1 >= nuevo_horario.hora_salida1
            ):
                return True

            if nuevo_horario.dia2 and horario.dia2 == nuevo_horario.dia2:
                if not (
                    horario.hora_salida2 <= nuevo_horario.hora_entrada2
                    or horario.hora_entrada2 >= nuevo_horario.hora_salida2
                ):
                    return True

    # A teacher cannot teach two courses at the same time.
    for horario in horarios:
        if horario.profesor == nuevo_horario.profesor:
            if horario.dia1 == nuevo_horario.dia1 and not (
                horario.hora_salida1 <= nuevo_horario.hora_entrada1
                or horario.hora_entrada1 >= nuevo_horario.hora_salida1
            ):
                return True

            if nuevo_horario.dia2 and horario.dia2 == nuevo_horario.dia2:
                if not (
                    horario.hora_salida2 <= nuevo_horario.hora_entrada2
                    or horario.hora_entrada2 >= nuevo_horario.hora_salida2
                ):
                    return True

    # Service courses
    for curso_servicio in cursos_servicio:
        if curso_servicio.bloque != nuevo_horario.bloque:
            continue

        for (
            dia_servicio,
            hora_inicio_servicio,
            hora_fin_servicio,
        ) in curso_servicio.horarios:
            if nuevo_horario.dia1 == dia_servicio:
                if not (
                    nuevo_horario.hora_salida1 <= hora_inicio_servicio
                    or nuevo_horario.hora_entrada1 >= hora_fin_servicio
                ):
                    return True

            if nuevo_horario.dia2 and nuevo_horario.dia2 == dia_servicio:
                if not (
                    nuevo_horario.hora_salida2 <= hora_inicio_servicio
                    or nuevo_horario.hora_entrada2 >= hora_fin_servicio
                ):
                    return True

    # If no clashes were found, the course can be added
    return False


"""
    generar_horarios
    Generates all possible scheduling options for each course
    Args:
        cursos: the list of courses read from the csv file
    Return:
        all course options
"""


def generar_horarios(cursos):
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horas_manana = list(range(MORNING_BEGIN, MORNING_END))
    horas_tarde = list(range(AFTERNOON_BEGIN, AFTERNOON_END))
    horas_noche = list(range(EVENING_BEGIN, EVENING_END))

    horarios_disponibles = []

    for curso in cursos:
        disponibilidad_profesor = curso.disponibilidad.split(":")
        aulas_disponibles = curso.aulas.split(":")

        if curso.dias_por_semana == 2:
            horas_dia1 = math.ceil(curso.horas_semanales / 2)
            horas_dia2 = math.floor(curso.horas_semanales / 2)

            # Combinations are Monday and Thursday or Tuesday and Friday only.
            combinaciones_dias = [("Lunes", "Jueves"), ("Martes", "Viernes")]

            for dia1, dia2 in combinaciones_dias:
                if "M" in disponibilidad_profesor:
                    for hora in horas_manana:
                        if ((hora + horas_dia1) <= MORNING_END and
                                (hora + horas_dia2) <= MORNING_END):
                            for aula in aulas_disponibles:
                                horarios_disponibles.append(
                                    Horario(
                                        curso.bloque,
                                        curso.sigla,
                                        dia1,
                                        dia2,
                                        hora,
                                        hora,
                                        hora + horas_dia1,
                                        hora + horas_dia2,
                                        curso.profesor,
                                        aula,
                                    )
                                )
                if "T" in disponibilidad_profesor:
                    for hora in horas_tarde:
                        if ((hora + horas_dia1) <= AFTERNOON_END and
                                (hora + horas_dia2) <= AFTERNOON_END):
                            for aula in aulas_disponibles:
                                horarios_disponibles.append(
                                    Horario(
                                        curso.bloque,
                                        curso.sigla,
                                        dia1,
                                        dia2,
                                        hora,
                                        hora,
                                        hora + horas_dia1,
                                        hora + horas_dia2,
                                        curso.profesor,
                                        aula,
                                    )
                                )
                if "N" in disponibilidad_profesor:
                    for hora in horas_noche:
                        if ((hora + horas_dia1) <= EVENING_END and
                                (hora + horas_dia2) <= EVENING_END):
                            for aula in aulas_disponibles:
                                horarios_disponibles.append(
                                    Horario(
                                        curso.bloque,
                                        curso.sigla,
                                        dia1,
                                        dia2,
                                        hora,
                                        hora,
                                        hora + horas_dia1,
                                        hora + horas_dia2,
                                        curso.profesor,
                                        aula,
                                    )
                                )
        elif curso.dias_por_semana == 1:
            for dia in dias_semana:
                if "M" in disponibilidad_profesor:
                    for hora in horas_manana:
                        if (hora + curso.horas_semanales) <= MORNING_END:
                            for aula in aulas_disponibles:
                                horarios_disponibles.append(
                                    Horario(
                                        curso.bloque,
                                        curso.sigla,
                                        dia,
                                        "",
                                        hora,
                                        -1,
                                        hora + curso.horas_semanales,
                                        -1,
                                        curso.profesor,
                                        aula,
                                    )
                                )
                if "T" in disponibilidad_profesor:
                    for hora in horas_tarde:
                        if (hora + curso.horas_semanales) <= AFTERNOON_END:
                            for aula in aulas_disponibles:
                                horarios_disponibles.append(
                                    Horario(
                                        curso.bloque,
                                        curso.sigla,
                                        dia,
                                        "",
                                        hora,
                                        -1,
                                        hora + curso.horas_semanales,
                                        -1,
                                        curso.profesor,
                                        aula,
                                    )
                                )
                if "N" in disponibilidad_profesor:
                    for hora in horas_noche:
                        if (hora + curso.horas_semanales) <= EVENING_END:
                            for aula in aulas_disponibles:
                                horarios_disponibles.append(
                                    Horario(
                                        curso.bloque,
                                        curso.sigla,
                                        dia,
                                        "",
                                        hora,
                                        -1,
                                        hora + curso.horas_semanales,
                                        -1,
                                        curso.profesor,
                                        aula,
                                    )
                                )
    # Sort the available schedules
    horarios_disponibles_ordenados = sorted(
        horarios_disponibles, key=lambda h: h.bloque
    )
    return horarios_disponibles_ordenados


"""
    generar_soluciones
    Generate timetable solutions from all possibilities
    Args:
        horarios_disponibles: list with all the possibilities of the courses
    Return:
       List of courses and schedules selected for the solution
"""


def generar_soluciones(horarios_disponibles, cursos_servicio):
    horarios = []
    cursos_disponibles = set(horario.curso for horario in horarios_disponibles)

    # Try to find a first schedule that does not clash.
    while len(horarios) == 0 and horarios_disponibles:
        eleccion = random.choice(horarios_disponibles)
        if not revisar_choques(horarios, eleccion, cursos_servicio):
            horarios.append(eleccion)
            cursos_disponibles.remove(eleccion.curso)

    # All options are explored to generate the solution.
    for horario in horarios_disponibles:
        if horario.curso in cursos_disponibles and not revisar_choques(
            horarios, horario, cursos_servicio
        ):
            horarios.append(horario)
            cursos_disponibles.remove(horario.curso)

    # Identify courses not included (because of clashes) and print message
    for curso in cursos_disponibles:
        print(f"El curso {curso} no se incluyó por choques")

    horarios_ordenados = sorted(horarios, key=lambda h: h.bloque)
    return horarios_ordenados


def main(archivo, archivo_servicio, num_soluciones=None):
    cursos = leer_archivo(archivo)
    cursos_servicio = leer_servicio(archivo_servicio)
    horarios_posibles = generar_horarios(cursos)
    soluciones = []

    if num_soluciones is None:
        num_soluciones = DEFAULT_NUMBER_SOL

    for _ in range(num_soluciones):
        solucion_actual = generar_soluciones(horarios_posibles,
                                             cursos_servicio)
        soluciones.append(solucion_actual)

    return soluciones


# Developer function
def crear_archivo_dev(soluciones):
    data = ["Bloque", "Sigla", "Horario", "Profesor", "Aula"]

    with open("Soluciones.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)
        contador = 1
        for solucion in soluciones:
            writer.writerow([f"Solucion {contador}"])
            for horario in solucion:
                if horario.hora_entrada2 != -1:
                    sol = [
                        str(horario.bloque),
                        horario.curso,
                        f"{horario.dia1}:{horario.hora_entrada1}"
                        f"-{horario.hora_salida1} y "
                        f"{horario.dia2}:{horario.hora_entrada2}-"
                        f"{horario.hora_salida2}",
                        horario.profesor,
                        horario.aula,
                    ]
                else:
                    sol = [
                        str(horario.bloque),
                        horario.curso,
                        f"{horario.dia1}:{horario.hora_entrada1}-"
                        f"{horario.hora_salida1}",
                        horario.profesor,
                        horario.aula,
                    ]
                writer.writerow(sol)
            writer.writerow("\n")
            contador += 1
    f.close()


def crear_archivo_user(solucion, numero_solucion, nombre_base):
    columnas = [
        "Bloque",
        "Sigla",
        "Horario",
        "Profesor",
        "Aula",
        "Grupo",
        "Cupo",
        "Observaciones",
    ]

    # Create a CSV file for each solutions
    nombre_archivo = f"{nombre_base}_{numero_solucion}.csv"
    with open(nombre_archivo, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)

        for horario in solucion:
            fila = [
                str(horario.bloque),
                horario.curso,
                f"{horario.dia1}:{horario.hora_entrada1}-"
                f"{horario.hora_salida1}"
                + (
                    f" y {horario.dia2}:{horario.hora_entrada2}-"
                    f"{horario.hora_salida2}"
                    if horario.hora_entrada2 != -1
                    else ""
                ),
                horario.profesor,
                horario.aula,
                "",  # Grupo
                "",  # Cupo
                "",  # Observaciones
            ]
            writer.writerow(fila)


def print_dev(soluciones, archivo):
    print("Horarios Posibles:")
    for horario in generar_horarios(leer_archivo(archivo)):
        if horario.hora_entrada2 != -1:
            print(
                f"Bloque {horario.bloque}, {horario.curso}:{horario.dia1} "
                f"{horario.hora_entrada1} - {horario.hora_salida1} y "
                f"{horario.dia2} {horario.hora_entrada2} - "
                f"{horario.hora_salida2}, {horario.profesor}, {horario.aula}"
            )
        else:
            print(
                f"Bloque {horario.bloque}, {horario.curso}: "
                f"{horario.dia1} {horario.hora_entrada1} - "
                f" {horario.hora_salida1}, {horario.profesor}, {horario.aula}"
            )

    print("\n" + "=" * 80 + "\n")

    for i, solucion_actual in enumerate(soluciones, start=1):
        print(f"Solucion {i}:")
        for horario in solucion_actual:
            if horario.hora_entrada2 != -1:
                linea = (
                    f"Bloque {horario.bloque}, {horario.curso}: "
                    f"{horario.dia1} {horario.hora_entrada1} - "
                    f"{horario.hora_salida1} y {horario.dia2} "
                    f"{horario.hora_entrada2} - {horario.hora_salida2}, "
                    f"{horario.profesor}, {horario.aula}"
                )
            else:
                linea = (
                    f"Bloque {horario.bloque}, {horario.curso}: "
                    f"{horario.dia1} {horario.hora_entrada1} - "
                    f"{horario.hora_salida1}, {horario.profesor}, "
                    f"{horario.aula}"
                )
            print(linea)
        print()
    crear_archivo_dev(soluciones)


def print_user(soluciones, nombre_base):
    time.sleep(5)
    for i, solucion_actual in enumerate(soluciones, start=1):
        crear_archivo_user(solucion_actual, i, nombre_base)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Uso: python3 horarios.py entry_file.csv entry_service_file.csv "
            "[num_soluciones] [output_file_name]"
        )
        sys.exit(1)

    archivo_csv = sys.argv[1]
    archivo_servicio = sys.argv[2]

    try:
        if len(sys.argv) >= 5:
            num_soluciones = int(sys.argv[3])
            nombre_base = sys.argv[4]
            soluciones = main(archivo_csv, archivo_servicio, num_soluciones)
            print_user(soluciones, nombre_base)
        elif len(sys.argv) == 4:
            num_soluciones = int(sys.argv[3])
            soluciones = main(archivo_csv, archivo_servicio, num_soluciones)
            print_dev(soluciones, archivo_csv)
        else:
            soluciones = main(archivo_csv, archivo_servicio)
            print_dev(soluciones, archivo_csv)

    except FileNotFoundError:
        print("Archivo invalido.")
        sys.exit(1)
