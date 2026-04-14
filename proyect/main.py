import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ================= BASE DE DATOS =================
conn = sqlite3.connect("sistema_pro.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS estudiantes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    matricula TEXT,
    edad INTEGER,
    rol TEXT,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS profesores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    especialidad TEXT
);

CREATE TABLE IF NOT EXISTS materias(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    horas INTEGER
);

CREATE TABLE IF NOT EXISTS inscripciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER,
    materia_id INTEGER,
    profesor_id INTEGER,
    tanda TEXT,
    horas INTEGER
);

CREATE TABLE IF NOT EXISTS tareas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER,
    materia_id INTEGER,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS calificaciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER,
    materia_id INTEGER,
    asignacion REAL,
    practica REAL,
    prueba REAL,
    examen REAL
);
""")

conn.commit()

# ================= UI =================
root = tk.Tk()
root.title("Sistema de Gestion de Estudiantes")
root.geometry("1200x700")

BG="#0f172a"; TEXT="#ffffff"; CARD="#1e293b"
PRIMARY="#6366f1"; SUCCESS="#22c55e"; DANGER="#ef4444"

root.configure(bg=BG)

def limpiar():
    for w in content.winfo_children():
        w.destroy()

def btn(p,t,c,cmd):
    return tk.Button(p,text=t,bg=c,fg="white",bd=0,command=cmd,pady=6,cursor="hand2")

def inp(p):
    return tk.Entry(p,bg=CARD,fg="white",insertbackground="white",bd=0)

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

# ================= LAYOUT =================
sidebar=tk.Frame(root,bg="#020617",width=220)
sidebar.pack(side="left",fill="y")

content=tk.Frame(root,bg=BG)
content.pack(side="right",expand=True,fill="both")

tk.Label(sidebar,text="🎓 Gestion de Estudiantes",bg="#020617",
         fg="white",font=("Segoe UI",14,"bold")).pack(pady=20)

# ================= DASHBOARD =================
def dashboard():
    limpiar()

    tk.Label(content, text="📊 Dashboard Ejecutivo",
             bg=BG, fg="white",
             font=("Segoe UI", 22, "bold")).pack(pady=10)

    # ================= KPIs =================
    kpi_frame = tk.Frame(content, bg=BG)
    kpi_frame.pack(pady=10)

    def card(titulo, valor, color):
        f = tk.Frame(kpi_frame, bg=CARD, padx=20, pady=15)
        f.pack(side="left", padx=10)

        tk.Label(f, text=titulo, bg=CARD, fg="gray",
                 font=("Segoe UI", 10)).pack()

        tk.Label(f, text=str(valor), bg=CARD, fg=color,
                 font=("Segoe UI", 18, "bold")).pack()

    # CONSULTAS KPI
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    total_est = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM materias")
    total_mat = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM profesores")
    total_prof = cursor.fetchone()[0]

    cursor.execute("""
    SELECT ROUND(AVG((asignacion+practica+prueba+examen)/4),2)
    FROM calificaciones
    """)
    prom = cursor.fetchone()[0] or 0

    card("👨‍🎓 Estudiantes", total_est, "#38bdf8")
    card("📚 Materias", total_mat, "#22c55e")
    card("👨‍🏫 Profesores", total_prof, "#f59e0b")
    card("📊 Promedio Global", prom, "#6366f1")

    # ================= TABLA + GRAFICO =================
    frame = tk.Frame(content, bg=BG)
    frame.pack(fill="both", expand=True)

    # ===== TABLA RANKING =====
    tabla = ttk.Treeview(frame, columns=("Estudiante","Promedio"), show="headings", height=10)
    tabla.heading("Estudiante", text="Estudiante")
    tabla.heading("Promedio", text="Promedio")
    tabla.pack(side="left", fill="both", expand=True, padx=10)

    # ===== CANVAS =====
    canvas = tk.Canvas(frame, bg=CARD, width=500, height=400, highlightthickness=0)
    canvas.pack(side="right", padx=10, pady=10)

    # CONSULTA
    cursor.execute("""
SELECT e.nombre,
       ROUND(AVG((c.asignacion*0.2 + c.practica*0.2 + c.prueba*0.2 + c.examen*0.4)),2)
FROM calificaciones c
JOIN estudiantes e ON c.estudiante_id=e.id
GROUP BY e.id
ORDER BY 2 DESC
""")

    datos = cursor.fetchall()

    # ===== LLENAR TABLA =====
    for i in tabla.get_children():
        tabla.delete(i)

    for r in datos:
        tabla.insert("", "end", values=r)

    # ===== GRAFICO BARRAS PREMIUM =====
    canvas.delete("all")

    if datos:
        max_val = max([x[1] for x in datos])

        x = 60
        for i, (nombre, valor) in enumerate(datos[:6]):  # top 6

            altura = (valor / max_val) * 250

            # COLOR DINÁMICO
            color = "#22c55e" if valor >= 70 else "#ef4444"

            # Sombra
            canvas.create_rectangle(x+3, 300-altura+3, x+43, 300+3, fill="#020617", outline="")

            # Barra
            canvas.create_rectangle(x, 300-altura, x+40, 300, fill=color, outline="")

            # Valor
            canvas.create_text(x+20, 300-altura-10,
                               text=str(valor),
                               fill="white",
                               font=("Segoe UI", 10, "bold"))

            # Nombre
            canvas.create_text(x+20, 320,
                               text=nombre[:6],
                               fill="white",
                               font=("Segoe UI", 9))

            x += 70

    else:
        canvas.create_text(250, 200,
                           text="Sin datos",
                           fill="white",
                           font=("Segoe UI", 14))

    # ================= TOP 3 =================
    top_frame = tk.Frame(content, bg=BG)
    top_frame.pack(pady=10)

    tk.Label(top_frame, text="🏆 Top 3 Estudiantes",
             bg=BG, fg="white",
             font=("Segoe UI", 14, "bold")).pack()

    for i, (nombre, valor) in enumerate(datos[:3]):
        tk.Label(top_frame,
                 text=f"{i+1}. {nombre} - {valor}",
                 bg=BG,
                 fg="#22c55e" if i == 0 else "white",
                 font=("Segoe UI", 11)).pack()

# ================= ESTUDIANTES =================
def estudiantes():
    limpiar()

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=10)

    tk.Label(frame, text="👨‍🎓 Registro de Estudiantes", bg=BG, fg="white",
             font=("Segoe UI", 16, "bold")).grid(row=0, columnspan=4)

    tk.Label(frame, text="Nombre completo:", bg=BG, fg="white").grid(row=1, column=0)
    e1 = inp(frame); e1.grid(row=1, column=1); e1.insert(0,"Ej: Juan Pérez")

    tk.Label(frame, text="Matrícula:", bg=BG, fg="white").grid(row=1, column=2)
    e2 = inp(frame); e2.grid(row=1, column=3); e2.insert(0,"Ej: 2025-001")

    tk.Label(frame, text="Edad:", bg=BG, fg="white").grid(row=2, column=0)
    e3 = inp(frame); e3.grid(row=2, column=1); e3.insert(0,"Ej: 20")

    tk.Label(frame, text="Rol:", bg=BG, fg="white").grid(row=2, column=2)
    rol = ttk.Combobox(frame, values=["Estudiante","Admin"]); rol.grid(row=2, column=3)

    tk.Label(frame, text="Descripción:", bg=BG, fg="white").grid(row=3, column=0)
    e4 = inp(frame); e4.grid(row=3, column=1, columnspan=3)
    e4.insert(0,"Ej: Estudiante de Ingeniería")

    sel={"id":None}

    tabla = ttk.Treeview(content, columns=("Nombre","Matrícula","Edad","Rol","Descripción"), show="headings")
    for c in ("Nombre","Matrícula","Edad","Rol","Descripción"):
        tabla.heading(c,text=c)
    tabla.pack(fill="both", expand=True)

    def cargar():
        for i in tabla.get_children(): tabla.delete(i)
        for r in cursor.execute("SELECT * FROM estudiantes"):
            tabla.insert("", "end", text=r[0], values=r[1:])

    def guardar():
        cursor.execute("INSERT INTO estudiantes(nombre,matricula,edad,rol,descripcion) VALUES(?,?,?,?,?)",
                       (e1.get(),e2.get(),e3.get(),rol.get(),e4.get()))
        conn.commit(); cargar()

    def actualizar():
        if sel["id"]:
            cursor.execute("UPDATE estudiantes SET nombre=?,matricula=?,edad=?,rol=?,descripcion=? WHERE id=?",
                           (e1.get(),e2.get(),e3.get(),rol.get(),e4.get(),sel["id"]))
            conn.commit(); cargar()

    def eliminar():
        if sel["id"]:
            cursor.execute("DELETE FROM estudiantes WHERE id=?",(sel["id"],))
            conn.commit(); cargar()

    def select(e):
        item=tabla.selection()
        if item:
            sel["id"]=tabla.item(item)["text"]
            d=tabla.item(item)["values"]
            e1.delete(0,tk.END); e1.insert(0,d[0])
            e2.delete(0,tk.END); e2.insert(0,d[1])
            e3.delete(0,tk.END); e3.insert(0,d[2])
            rol.set(d[3])
            e4.delete(0,tk.END); e4.insert(0,d[4])

    tabla.bind("<<TreeviewSelect>>",select)

    btn(frame,"💾 Guardar",SUCCESS,guardar).grid(row=4,column=0)
    btn(frame,"✏️ Actualizar",PRIMARY,actualizar).grid(row=4,column=1)
    btn(frame,"🗑 Eliminar",DANGER,eliminar).grid(row=4,column=2)

    cargar()

# ================= PROFESORES =================
def profesores():
    limpiar()

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=10)

    tk.Label(frame, text="👨‍🏫 Gestión de Profesores",
             bg=BG, fg="white", font=("Segoe UI", 16, "bold")).grid(row=0, columnspan=4, pady=10)

    # ===== FORMULARIO =====
    tk.Label(frame, text="Nombre del profesor:", bg=BG, fg="white").grid(row=1, column=0, sticky="w")
    nombre = inp(frame)
    nombre.grid(row=1, column=1)
    nombre.insert(0, "Ej: Prof. Juan Pérez")

    tk.Label(frame, text="Especialidad:", bg=BG, fg="white").grid(row=1, column=2, sticky="w")
    esp = inp(frame)
    esp.grid(row=1, column=3)
    esp.insert(0, "Ej: Matemáticas")

    sel = {"id": None}

    # ===== TABLA =====
    tabla = ttk.Treeview(content, columns=("Nombre", "Especialidad"), show="headings")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Especialidad", text="Especialidad")
    tabla.pack(fill="both", expand=True)

    # ===== FUNCIONES =====
    def cargar():
        for i in tabla.get_children():
            tabla.delete(i)
        for r in cursor.execute("SELECT * FROM profesores"):
            tabla.insert("", "end", text=r[0], values=r[1:])

    def guardar():
        cursor.execute("INSERT INTO profesores(nombre,especialidad) VALUES(?,?)",
                       (nombre.get(), esp.get()))
        conn.commit()
        cargar()

    def actualizar():
        if sel["id"]:
            cursor.execute("UPDATE profesores SET nombre=?,especialidad=? WHERE id=?",
                           (nombre.get(), esp.get(), sel["id"]))
            conn.commit()
            cargar()

    def eliminar():
        if sel["id"]:
            cursor.execute("DELETE FROM profesores WHERE id=?",
                           (sel["id"],))
            conn.commit()
            cargar()

    def seleccionar(event):
        item = tabla.selection()
        if item:
            sel["id"] = tabla.item(item)["text"]
            datos = tabla.item(item)["values"]

            nombre.delete(0, tk.END)
            nombre.insert(0, datos[0])

            esp.delete(0, tk.END)
            esp.insert(0, datos[1])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # ===== BOTONES =====
    btn(frame, "💾 Guardar", SUCCESS, guardar).grid(row=2, column=0, pady=10)
    btn(frame, "✏️ Actualizar", PRIMARY, actualizar).grid(row=2, column=1)
    btn(frame, "🗑 Eliminar", DANGER, eliminar).grid(row=2, column=2)

    cargar()

# ================= MATERIAS =================
def materias():
    limpiar()

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=10)

    tk.Label(frame,text="📚 Materias",bg=BG,fg="white",
             font=("Segoe UI",16,"bold")).grid(row=0,columnspan=2)

    tk.Label(frame,text="Nombre:",bg=BG,fg="white").grid(row=1,column=0)
    n=inp(frame); n.grid(row=1,column=1); n.insert(0,"Ej: Física")

    tk.Label(frame,text="Horas:",bg=BG,fg="white").grid(row=2,column=0)
    h=inp(frame); h.grid(row=2,column=1); h.insert(0,"Ej: 4")

    sel={"id":None}

    tabla=ttk.Treeview(content,columns=("Nom","Horas"),show="headings")
    tabla.heading("Nom",text="Materia")
    tabla.heading("Horas",text="Horas")
    tabla.pack(fill="both",expand=True)

    def cargar():
        for i in tabla.get_children(): tabla.delete(i)
        for r in cursor.execute("SELECT * FROM materias"):
            tabla.insert("", "end", text=r[0], values=r[1:])

    def guardar():
        cursor.execute("INSERT INTO materias(nombre,horas) VALUES(?,?)",(n.get(),h.get()))
        conn.commit(); cargar()

    def actualizar():
        if sel["id"]:
            cursor.execute("UPDATE materias SET nombre=?,horas=? WHERE id=?",(n.get(),h.get(),sel["id"]))
            conn.commit(); cargar()

    def eliminar():
        if sel["id"]:
            cursor.execute("DELETE FROM materias WHERE id=?",(sel["id"],))
            conn.commit(); cargar()

    def select(e):
        item=tabla.selection()
        if item:
            sel["id"]=tabla.item(item)["text"]
            d=tabla.item(item)["values"]
            n.delete(0,tk.END); n.insert(0,d[0])
            h.delete(0,tk.END); h.insert(0,d[1])

    tabla.bind("<<TreeviewSelect>>",select)

    btn(frame,"💾 Guardar",SUCCESS,guardar).grid(row=3,column=0)
    btn(frame,"✏️ Actualizar",PRIMARY,actualizar).grid(row=3,column=1)
    btn(frame,"🗑 Eliminar",DANGER,eliminar).grid(row=3,column=2)

    cargar()

# ================= INSCRIPCIONES =================
def inscripciones():
    limpiar()

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=10)

    tk.Label(frame, text="🧾 Gestión de Inscripciones",
             bg=BG, fg="white", font=("Segoe UI", 16, "bold")).grid(row=0, columnspan=5, pady=10)

    # ===== FORMULARIO =====
    tk.Label(frame, text="Estudiante:", bg=BG, fg="white").grid(row=1, column=0)
    ce = ttk.Combobox(frame, width=20)
    ce.grid(row=1, column=1)

    tk.Label(frame, text="Materia:", bg=BG, fg="white").grid(row=1, column=2)
    cm = ttk.Combobox(frame, width=20)
    cm.grid(row=1, column=3)

    tk.Label(frame, text="Profesor:", bg=BG, fg="white").grid(row=2, column=0)
    cp = ttk.Combobox(frame, width=20)
    cp.grid(row=2, column=1)

    tk.Label(frame, text="Tanda:", bg=BG, fg="white").grid(row=2, column=2)
    tanda = ttk.Combobox(frame, values=["Mañana", "Tarde", "Noche"], width=18)
    tanda.grid(row=2, column=3)

    tk.Label(frame, text="Horas:", bg=BG, fg="white").grid(row=3, column=0)
    horas = inp(frame)
    horas.grid(row=3, column=1)
    horas.insert(0, "Ej: 4")

    sel = {"id": None}

    # ===== TABLA =====
    tabla = ttk.Treeview(content,
        columns=("Estudiante", "Materia", "Profesor", "Tanda", "Horas"),
        show="headings")

    for col in ("Estudiante", "Materia", "Profesor", "Tanda", "Horas"):
        tabla.heading(col, text=col)

    tabla.pack(fill="both", expand=True)

    # ===== FUNCIONES =====
    def cargar():
        # Combobox
        ce['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM estudiantes")]
        cm['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM materias")]
        cp['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM profesores")]

        # Tabla
        for i in tabla.get_children():
            tabla.delete(i)

        cursor.execute("""
        SELECT i.id, e.nombre, m.nombre, p.nombre, i.tanda, i.horas
        FROM inscripciones i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN materias m ON i.materia_id = m.id
        JOIN profesores p ON i.profesor_id = p.id
        """)

        for r in cursor.fetchall():
            tabla.insert("", "end", text=r[0], values=r[1:])

    def guardar():
        cursor.execute("""
        INSERT INTO inscripciones(estudiante_id,materia_id,profesor_id,tanda,horas)
        VALUES(?,?,?,?,?)
        """, (
            ce.get().split("-")[0],
            cm.get().split("-")[0],
            cp.get().split("-")[0],
            tanda.get(),
            horas.get()
        ))
        conn.commit()
        cargar()

    def actualizar():
        if sel["id"]:
            cursor.execute("""
            UPDATE inscripciones
            SET estudiante_id=?, materia_id=?, profesor_id=?, tanda=?, horas=?
            WHERE id=?
            """, (
                ce.get().split("-")[0],
                cm.get().split("-")[0],
                cp.get().split("-")[0],
                tanda.get(),
                horas.get(),
                sel["id"]
            ))
            conn.commit()
            cargar()

    def eliminar():
        if sel["id"]:
            cursor.execute("DELETE FROM inscripciones WHERE id=?", (sel["id"],))
            conn.commit()
            cargar()

    def seleccionar(event):
        item = tabla.selection()
        if item:
            sel["id"] = tabla.item(item)["text"]
            datos = tabla.item(item)["values"]

            # reconstruir valores con ID (buscando en combobox)
            for v in ce['values']:
                if datos[0] in v:
                    ce.set(v)

            for v in cm['values']:
                if datos[1] in v:
                    cm.set(v)

            for v in cp['values']:
                if datos[2] in v:
                    cp.set(v)

            tanda.set(datos[3])

            horas.delete(0, tk.END)
            horas.insert(0, datos[4])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # ===== BOTONES =====
    btn(frame, "💾 Guardar", SUCCESS, guardar).grid(row=4, column=0, pady=10)
    btn(frame, "✏️ Actualizar", PRIMARY, actualizar).grid(row=4, column=1)
    btn(frame, "🗑 Eliminar", DANGER, eliminar).grid(row=4, column=2)

    cargar()

# ================= TAREAS =================
def tareas():
    limpiar()

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=10)

    tk.Label(frame, text="📝 Gestión de Tareas",
             bg=BG, fg="white", font=("Segoe UI", 16, "bold")).grid(row=0, columnspan=4)

    # ===== FORMULARIO =====
    tk.Label(frame, text="Estudiante:", bg=BG, fg="white").grid(row=1, column=0)
    ce = ttk.Combobox(frame, width=25)
    ce.grid(row=1, column=1)

    tk.Label(frame, text="Materia:", bg=BG, fg="white").grid(row=1, column=2)
    cm = ttk.Combobox(frame, width=25)
    cm.grid(row=1, column=3)

    tk.Label(frame, text="Descripción:", bg=BG, fg="white").grid(row=2, column=0)
    desc = inp(frame)
    desc.grid(row=2, column=1, columnspan=3, sticky="we")
    desc.insert(0, "Ej: Proyecto final")

    sel = {"id": None}

    # ===== TABLA =====
    tabla = ttk.Treeview(content,
        columns=("Estudiante","Materia","Descripción"),
        show="headings")

    for col in tabla["columns"]:
        tabla.heading(col, text=col)

    tabla.pack(fill="both", expand=True)

    # ===== FUNCIONES =====
    def cargar():
        ce['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM estudiantes")]
        cm['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM materias")]

        for i in tabla.get_children():
            tabla.delete(i)

        cursor.execute("""
        SELECT t.id, e.nombre, m.nombre, t.descripcion
        FROM tareas t
        JOIN estudiantes e ON t.estudiante_id = e.id
        JOIN materias m ON t.materia_id = m.id
        """)

        for r in cursor.fetchall():
            tabla.insert("", "end", text=r[0], values=r[1:])

    def guardar():
        cursor.execute("""
        INSERT INTO tareas(estudiante_id,materia_id,descripcion)
        VALUES(?,?,?)
        """, (
            ce.get().split("-")[0],
            cm.get().split("-")[0],
            desc.get()
        ))
        conn.commit()
        cargar()

    def actualizar():
        if sel["id"]:
            cursor.execute("""
            UPDATE tareas
            SET estudiante_id=?, materia_id=?, descripcion=?
            WHERE id=?
            """, (
                ce.get().split("-")[0],
                cm.get().split("-")[0],
                desc.get(),
                sel["id"]
            ))
            conn.commit()
            cargar()

    def eliminar():
        if sel["id"]:
            cursor.execute("DELETE FROM tareas WHERE id=?", (sel["id"],))
            conn.commit()
            cargar()

    def seleccionar(event):
        item = tabla.selection()
        if item:
            sel["id"] = tabla.item(item)["text"]
            datos = tabla.item(item)["values"]

            # Set estudiante
            for v in ce['values']:
                if datos[0] in v:
                    ce.set(v)

            # Set materia
            for v in cm['values']:
                if datos[1] in v:
                    cm.set(v)

            desc.delete(0, tk.END)
            desc.insert(0, datos[2])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # ===== BOTONES =====
    btn(frame, "💾 Guardar", SUCCESS, guardar).grid(row=3, column=0, pady=10)
    btn(frame, "✏️ Actualizar", PRIMARY, actualizar).grid(row=3, column=1)
    btn(frame, "🗑 Eliminar", DANGER, eliminar).grid(row=3, column=2)

    cargar()

# ================= CALIFICACIONES =================
def calificaciones():
    limpiar()

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=10)

    tk.Label(frame, text="📊 Gestión de Calificaciones",
             bg=BG, fg="white", font=("Segoe UI", 16, "bold")).grid(row=0, columnspan=4)

    # ===== FORMULARIO =====
    tk.Label(frame, text="Estudiante:", bg=BG, fg="white").grid(row=1, column=0)
    ce = ttk.Combobox(frame, width=25)
    ce.grid(row=1, column=1)

    tk.Label(frame, text="Materia:", bg=BG, fg="white").grid(row=1, column=2)
    cm = ttk.Combobox(frame, width=25)
    cm.grid(row=1, column=3)

    # Notas
    a = inp(frame); a.insert(0, "Asignación")
    p = inp(frame); p.insert(0, "Práctica")
    pr = inp(frame); pr.insert(0, "Prueba")
    ex = inp(frame); ex.insert(0, "Examen")

    a.grid(row=2, column=0)
    p.grid(row=2, column=1)
    pr.grid(row=2, column=2)
    ex.grid(row=2, column=3)

    sel = {"id": None}

    # ===== TABLA =====
    tabla = ttk.Treeview(content,
    columns=("Estudiante","Materia","Asignación","Práctica","Prueba","Examen","Promedio","Letra"),
    show="headings")

    for col in tabla["columns"]:
        tabla.heading(col, text=col)

    tabla.pack(fill="both", expand=True)

    # ===== FUNCIONES =====
    def cargar():
        ce['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM estudiantes")]
        cm['values'] = [f"{x[0]}-{x[1]}" for x in cursor.execute("SELECT id,nombre FROM materias")]

        for i in tabla.get_children():
            tabla.delete(i)

        cursor.execute("""
SELECT c.id, e.nombre, m.nombre,
       c.asignacion, c.practica, c.prueba, c.examen,
       ROUND((c.asignacion*0.2 + c.practica*0.2 + c.prueba*0.2 + c.examen*0.4),2)
FROM calificaciones c
JOIN estudiantes e ON c.estudiante_id = e.id
JOIN materias m ON c.materia_id = m.id
""")

        for r in cursor.fetchall():
            promedio = r[7]
            letra = estado_nota(promedio)
            
            tabla.insert("", "end", text=r[0], 
                         values=r[1:] + (letra,))

    def guardar():
        cursor.execute("""
        INSERT INTO calificaciones(estudiante_id,materia_id,asignacion,practica,prueba,examen)
        VALUES(?,?,?,?,?,?)
        """, (
            ce.get().split("-")[0],
            cm.get().split("-")[0],
            float(a.get()),
            float(p.get()),
            float(pr.get()),
            float(ex.get())
        ))
        conn.commit()
        cargar()

    def actualizar():
        if sel["id"]:
            cursor.execute("""
            UPDATE calificaciones
            SET estudiante_id=?, materia_id=?, asignacion=?, practica=?, prueba=?, examen=?
            WHERE id=?
            """, (
                ce.get().split("-")[0],
                cm.get().split("-")[0],
                float(a.get()),
                float(p.get()),
                float(pr.get()),
                float(ex.get()),
                sel["id"]
            ))
            conn.commit()
            cargar()

    def eliminar():
        if sel["id"]:
            cursor.execute("DELETE FROM calificaciones WHERE id=?", (sel["id"],))
            conn.commit()
            cargar()

    def seleccionar(event):
        item = tabla.selection()
        if item:
            sel["id"] = tabla.item(item)["text"]
            datos = tabla.item(item)["values"]

            # set estudiante
            for v in ce['values']:
                if datos[0] in v:
                    ce.set(v)

            # set materia
            for v in cm['values']:
                if datos[1] in v:
                    cm.set(v)

            a.delete(0, tk.END); a.insert(0, datos[2])
            p.delete(0, tk.END); p.insert(0, datos[3])
            pr.delete(0, tk.END); pr.insert(0, datos[4])
            ex.delete(0, tk.END); ex.insert(0, datos[5])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # ===== BOTONES =====
    btn(frame, "💾 Guardar", SUCCESS, guardar).grid(row=3, column=0)
    btn(frame, "✏️ Actualizar", PRIMARY, actualizar).grid(row=3, column=1)
    btn(frame, "🗑 Eliminar", DANGER, eliminar).grid(row=3, column=2)

    cargar()

# ================= MENÚ =================
btn(sidebar,"🏠 Dashboard",PRIMARY,dashboard).pack(fill="x")

tk.Label(sidebar,text="Gestión",bg="#020617",fg="gray").pack()
btn(sidebar,"👨‍🎓 Estudiantes",PRIMARY,estudiantes).pack(fill="x")
btn(sidebar,"👨‍🏫 Profesores",PRIMARY,profesores).pack(fill="x")
btn(sidebar,"📚 Materias",PRIMARY,materias).pack(fill="x")

tk.Label(sidebar,text="Académico",bg="#020617",fg="gray").pack()
btn(sidebar,"🧾 Inscripciones",PRIMARY,inscripciones).pack(fill="x")
btn(sidebar,"📝 Tareas",PRIMARY,tareas).pack(fill="x")
btn(sidebar,"📊 Calificaciones",PRIMARY,calificaciones).pack(fill="x")

dashboard()
root.mainloop()