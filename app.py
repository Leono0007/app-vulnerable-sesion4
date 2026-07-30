import os
import ast
from flask import Flask, request
import sqlite3

app = Flask(__name__)
# Solucion SAST: Uso de variable de entorno para credenciales
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_secret_key")

@app.route("/buscar")
def buscar():
    termino = request.args.get("q", "")
    conexion = sqlite3.connect("datos.db")
    # Solucion SAST: Consulta parametrizada para evitar Inyeccion SQL
    consulta = "SELECT * FROM productos WHERE nombre = ?"
    resultado = conexion.execute(consulta, (termino,))
    return str(resultado.fetchall())

@app.route("/calcular")
def calcular():
    expresion = request.args.get("expr", "0")
    # Solucion SAST: Reemplazo de eval() por ast.literal_eval()
    try:
        resultado = ast.literal_eval(expresion)
    except (ValueError, SyntaxError):
        resultado = "Expresion invalida"
    return str(resultado)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
