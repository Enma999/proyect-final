import unittest
import sqlite3

# ===== FUNCIÓN IGUAL QUE EN EL SISTEMA =====
def estado_nota(nota):
    if nota >= 90:
        return "A"
    elif nota >= 80:
        return "B"
    elif nota >= 70:
        return "C"
    elif nota >= 60:
        return "D"
    else:
        return "F"

class TestSistemaUniversitario(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        self.cursor.executescript("""
        CREATE TABLE estudiantes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            matricula TEXT,
            edad INTEGER,
            rol TEXT,
            descripcion TEXT
        );

        CREATE TABLE materias(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            horas INTEGER
        );

        CREATE TABLE calificaciones(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            materia_id INTEGER,
            asignacion REAL,
            practica REAL,
            prueba REAL,
            examen REAL
        );
        """)

    def tearDown(self):
        self.conn.close()

    # ======================================
    # TEST PROMEDIO PONDERADO
    # ======================================
    def test_promedio_ponderado(self):
        self.cursor.execute("INSERT INTO estudiantes(nombre) VALUES('Juan')")
        self.cursor.execute("INSERT INTO materias(nombre,horas) VALUES('Prog',4)")

        self.cursor.execute("""
        INSERT INTO calificaciones(estudiante_id,materia_id,asignacion,practica,prueba,examen)
        VALUES(1,1,80,90,85,95)
        """)
        self.conn.commit()

        self.cursor.execute("""
        SELECT (asignacion*0.2 + practica*0.2 + prueba*0.2 + examen*0.4)
        FROM calificaciones
        """)
        promedio = self.cursor.fetchone()[0]

        self.assertAlmostEqual(promedio, 89.0)

    # ======================================
    # TEST LETRA
    # ======================================
    def test_estado_nota_A(self):
        self.assertEqual(estado_nota(95), "A")

    def test_estado_nota_B(self):
        self.assertEqual(estado_nota(85), "B")

    def test_estado_nota_C(self):
        self.assertEqual(estado_nota(75), "C")

    def test_estado_nota_D(self):
        self.assertEqual(estado_nota(65), "D")

    def test_estado_nota_F(self):
        self.assertEqual(estado_nota(50), "F")

    # ======================================
    # TEST INTEGRADO (PROMEDIO + LETRA)
    # ======================================
    def test_promedio_y_letra(self):
        self.cursor.execute("INSERT INTO estudiantes(nombre) VALUES('Ana')")
        self.cursor.execute("INSERT INTO materias(nombre,horas) VALUES('BD',4)")

        self.cursor.execute("""
        INSERT INTO calificaciones(estudiante_id,materia_id,asignacion,practica,prueba,examen)
        VALUES(1,1,90,90,90,90)
        """)
        self.conn.commit()

        self.cursor.execute("""
        SELECT (asignacion*0.2 + practica*0.2 + prueba*0.2 + examen*0.4)
        FROM calificaciones
        """)
        promedio = self.cursor.fetchone()[0]

        letra = estado_nota(promedio)

        self.assertEqual(promedio, 90)
        self.assertEqual(letra, "A")


if __name__ == "__main__":
    unittest.main()