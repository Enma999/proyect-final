# 🎓 Sistema de Gestion de Estudiantes

## 📌 Descripción

Sistema académico completo desarrollado en Python que permite gestionar estudiantes, profesores, materias, inscripciones, tareas y calificaciones dentro de una plataforma tipo universidad real.

El sistema incluye operaciones CRUD, cálculo automático de promedios y visualización de datos en un dashboard.

---

## 🚀 Características principales

* 👨‍🎓 Gestión de estudiantes (nombre, matrícula, edad, rol, descripción)
* 👨‍🏫 Gestión de profesores (nombre y especialidad)
* 📚 Gestión de materias con horas asignadas
* 🧾 Inscripciones (estudiante + materia + profesor + tanda + horas)
* 📝 Asignación de tareas por materia
* 📊 Registro de calificaciones:

  * Asignación
  * Práctica
  * Prueba
  * Examen
* 📈 Dashboard con:

  * Promedio automático
  * Ranking de estudiantes

---

## 🧱 Tecnologías utilizadas

* Python 3
* Tkinter (Interfaz gráfica)
* SQLite (Base de datos local)
* unittest (Pruebas automatizadas)

---

## 📁 Estructura del proyecto

```
/sistema-universitario
│
├── main.py                # Sistema principal
├── sistema_pro.db       # Base de datos
├── test_sistema.py       # Pruebas automatizadas
├── README.md             # Documentación
```

---

## ▶️ Ejecución

### 3. Ejecutar el sistema

```
python main.py
```

## 🧪 Pruebas automatizadas

El sistema incluye pruebas automatizadas utilizando `unittest`.

### Ejecutar pruebas:

```
python test_sistema.py
```

### Resultado esperado:

```
........
----------------------------------------------------------------------
Ran 7 tests

OK
```

---

## 📊 Funcionalidades detalladas

### 👨‍🎓 Estudiantes

* Registro completo
* Actualización y eliminación
* Visualización en tabla

### 👨‍🏫 Profesores

* Registro con especialidad
* Gestión completa (CRUD)

### 📚 Materias

* Creación con horas académicas
* Edición y eliminación

### 🧾 Inscripciones

* Relación entre estudiante, materia y profesor
* Selección de tanda (mañana, tarde, noche)
* Gestión completa

### 📝 Tareas

* Asignación por materia
* Actualización y eliminación
* Visualización en lista

### 📊 Calificaciones

* Registro de notas
* Cálculo automático del promedio
* Edición y eliminación

---

## 📈 Dashboard

El sistema incluye un panel donde se visualiza:

* Promedio por estudiante
* Ranking automático
* Orden descendente por rendimiento

---

## 🎯 Objetivo del proyecto

Desarrollar un sistema académico funcional aplicando:

* Programación en Python
* Bases de datos SQLite
* Diseño de interfaces gráficas
* Metodologías ágiles (Scrum)
* Pruebas automatizadas

---

## 📌 Estado del proyecto

* ✅ Funcional
* ✅ Completo
* ✅ Nivel académico avanzado
* 🚀 Listo para presentación

---

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura **Programación III**
Instituto Tecnológico de Las Américas (ITLA)

---

## 🏆 Conclusión

Este sistema simula una plataforma universitaria real, integrando múltiples módulos académicos con persistencia de datos y pruebas automatizadas, garantizando calidad y funcionalidad.

---
