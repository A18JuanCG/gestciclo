# Gestión de ciclos de FP [gestciclo]
## Módulo de Odoo para la 2ª evaluación de SXE - IES San Clemente
###### Versión de Odoo: 12

Este módudo pretende implementar la funcionalidad básica para la gestión de un ciclo de FP, incluyendo la creación, modificación y borrado de profesores, alumnos, asignaturas, etc.

Permite la gestión de faltas (de asistencia o puntualidad) y comprueba si se dan las condiciones para la pérdida de la evaluación continua. Por cada cinco faltas de puntualidad, añade una hora al cómputo de faltas general.

Asimismo, permite la creación de contenidos evaluables, tanto tareas como exámenes, calculando las notas de cada evaluación y la nota final de forma automática, teniendo en cuenta cada una de las notas de las tareas y exámenes y el porcentaje que suponen en la evaluación.

El ejercicio incide especialmente en la parte del servidor, estando la interfaz de usuario menos elaborada. Aún así, mediante los menús es posible crear o modificar todos los elementos del módulo.

![Interfaz del módulo](/doc/img/ciclos1.png)
*Interfaz del módulo*

## Guía de uso

1. Crear un **ciclo**
2. En Módulos/Lista de módulos, crear un  **módulo** perteneciente a ese ciclo
3. Crear un **profesor** y añadirlo al módulo anteriormente creado.
4. Crear un **alumno** y añadirle el módulo que vaya a cursar
5. En Módulos/Evaluaciones, crear una o varias **evaluaciones**
6. En Módulos/Tareas, crear las **tareas o exámenes** para el módulo deseado y la evaluación correspondiente, teniendo en cuenta señalar el porcentaje que supondrá en la evaluación
7. Editar el alumno y añadir cada tarea  que haya tenido que realizar y su nota
8. En Alumnos/Gestión de faltas, añadir las faltas que haya tenido cada alumno
