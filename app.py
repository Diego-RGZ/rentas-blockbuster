from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # solo para mostrar mensajes flash

# Conexión a Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rentas")
def rentas():
    data = supabase.table("renta").select("*").execute()
    rentas = data.data if data.data else []
    return render_template("rentas.html", rentas=rentas)

@app.route("/multas")
def multas():
    data = supabase.table("multa").select("*").execute()
    multas = data.data if data.data else []
    return render_template("multas.html", multas=multas)

@app.route("/registrar_multa", methods=["GET", "POST"])
def registrar_multa():
    if request.method == "POST":
        id_renta = int(request.form["id_renta"])
        fecha = request.form["fecha"]
        monto = float(request.form["monto"])
        motivo = request.form["motivo"]
        nueva_multa = {
            "id_renta": id_renta,
            "fecha": fecha,
            "monto": monto,
            "motivo": motivo
        }
        resp = supabase.table("multa").insert(nueva_multa).execute()
        if resp.data:
            flash("Multa registrada correctamente", "success")
            return redirect(url_for("multas"))
        else:
            flash("Error al registrar la multa", "error")
    rentas = supabase.table("renta").select("*").execute().data
    return render_template("registrar_multa.html", rentas=rentas)
    
@app.route("/registrar_renta", methods=["GET", "POST"])
def registrar_renta():
    if request.method == "POST":

        id_cliente = int(request.form["id_cliente"])
        id_empleado = int(request.form["id_empleado"])
        id_producto = int(request.form["id_producto"])
        fecha_renta = request.form["fecha_renta"]
        fecha_devolucion = request.form["fecha_devolucion"] or None
        pago_total = float(request.form["pago_total"])

        nueva_renta = {
            "id_cliente": id_cliente,
            "id_empleado": id_empleado,
            "id_producto": id_producto,
            "fecha_renta": fecha_renta,
            "fecha_devolucion": fecha_devolucion,
            "estado_renta": "Activa",
            "pago_total": pago_total
        }

        respuesta = supabase.table("renta").insert(nueva_renta).execute()

        if not respuesta.data:
            flash("Error al registrar la renta", "error")
        else:
            flash("Renta registrada correctamente", "success")

        return redirect(url_for("rentas"))

    clientes = supabase.table("cliente").select("*").execute().data
    empleados = supabase.table("empleado").select("*").execute().data
    productos = supabase.table("producto").select("*").execute().data

    return render_template("registrar_renta.html",
                           clientes=clientes,
                           empleados=empleados,
                           productos=productos,
                           hoy=str(date.today()))

@app.route("/registrar_cliente", methods=["GET", "POST"])
def registrar_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        estado_membresia = request.form["estado_membresia"]
        calle = request.form["calle"]
        numero = request.form["numero"]
        colonia = request.form["colonia"]
        ciudad = request.form["ciudad"]
        cp = request.form["cp"]

        nuevo_cliente = {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo": correo,
            "estado_membresia": estado_membresia,
            "calle": calle,
            "numero": numero,
            "colonia": colonia,
            "ciudad": ciudad,
            "cp": cp
        }

        response = supabase.table("cliente").insert(nuevo_cliente).execute()

        if response.data:
            flash("Cliente registrado correctamente", "success")
            return redirect(url_for("registrar_cliente"))
        else:
            flash("Error al registrar el cliente", "error")

    return render_template("registrar_cliente.html")
@app.route("/registrar_producto", methods=["GET", "POST"])
def registrar_producto():
    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]  # DVD, Blu-Ray, Videojuego

        nuevo_producto = {
            "titulo": titulo,
            "tipo": tipo
        }

        response = supabase.table("producto").insert(nuevo_producto).execute()

        if response.data:
            flash("Producto registrado correctamente", "success")
            return redirect(url_for("registrar_producto"))
        else:
            flash("Error al registrar el producto", "error")

    return render_template("registrar_producto.html")

@app.route("/registrar_empleado", methods=["GET", "POST"])
def registrar_empleado():
    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            salario = request.form.get("salario", "0").strip()
            # convertir salario a número (decimal)
            salario_val = float(salario) if salario != "" else 0.0
            tipo_empleado = request.form["tipo_empleado"]  # 'General'|'Cajero'|'Supervisor'
            caja_asignada = request.form.get("caja_asignada", None)
            turno = request.form.get("turno", None)
            area = request.form.get("area", None)

            nuevo_empleado = {
                "nombre": nombre,
                "salario": salario_val,
                "tipo_empleado": tipo_empleado,
                "caja_asignada": caja_asignada,
                "turno": turno,
                "area": area
            }

            resp = supabase.table("empleado").insert(nuevo_empleado).execute()

            if resp.data:
                flash("Empleado registrado correctamente", "success")
                return redirect(url_for("registrar_empleado"))
            else:
                # si supabase devuelve error dentro de resp.error u otro formato
                msg = getattr(resp, "error", None)
                flash(f"Error al registrar empleado: {msg}", "error")
        except Exception as e:
            flash(f"Error: {e}", "error")

    return render_template("registrar_empleado.html")

from flask import session
from functools import wraps

# --------- LOGIN ---------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        # Consulta segura
        response = (
            supabase.table("empleado")
            .select("*")
            .eq("correo", correo)
            .eq("password", password)
            .execute()
        )

        if response.data:
            session["empleado"] = response.data[0]["nombre"]
            flash("✔ Inicio de sesión exitoso", "success")
            return redirect(url_for("index"))
        else:
            flash("❌ Correo o contraseña incorrecta", "error")

    return render_template("login.html")


# --------- LOGOUT ---------
@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión", "success")
    return redirect(url_for("login"))


# --------- PROTECCIÓN DE RUTAS ---------
def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "empleado" not in session:
            flash("Debes iniciar sesión", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    app.run(debug=True)

