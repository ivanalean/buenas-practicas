import pyodbc
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Conectar a la base de datos desde Access
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\cuc\desarrollo\tareas\Tasks.DB.accdb;')
cursor = conn.cursor()

# Rutas de la aplicación

@app.route('/')
def mostrar_tareas():
    try:
        cursor.execute('SELECT * FROM Tareas')
        tareas = cursor.fetchall()
        return render_template('mostrar_tareas.html', tareas=tareas)
    except Exception as e:
        return f"Error al recuperar las tareas: {str(e)}"

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        estado = 'No Completado'
        try:
            cursor.execute("INSERT INTO Tareas (descripcion, estado) VALUES (?, ?)", (descripcion, estado))
            conn.commit()
            return redirect(url_for('mostrar_tareas'))
        except Exception as e:
            return f"Error al agregar la tarea: {str(e)}"

@app.route('/completar_tarea/<int:id>')
def completar_tarea(id):
    try:
        cursor.execute("UPDATE Tareas SET estado='Completado' WHERE id=?", (id,))
        conn.commit()
        return redirect(url_for('mostrar_tareas'))
    except Exception as e:
        return f"Error al completar la tarea: {str(e)}"

@app.route('/eliminar_tarea/<int:id>')
def eliminar_tarea(id):
    try:
        cursor.execute("DELETE FROM Tareas WHERE id=?", (id,))
        conn.commit()
        return redirect(url_for('mostrar_tareas'))
    except Exception as e:
        return f"Error al eliminar la tarea: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
