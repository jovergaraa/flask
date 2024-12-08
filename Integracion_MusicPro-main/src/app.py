from config import config
from routes import Producto
from flask_cors import CORS
from operator import itemgetter
import psycopg2
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed
from flask import Flask, g, render_template, request, jsonify, g, session, url_for, send_file, flash, redirect
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed
from config import config
from routes import Producto
from flask_cors import CORS
from operator import itemgetter
import psycopg2
import requests
from io import BytesIO
import json
from datetime import datetime
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for

app = Flask(__name__)

CORS(app, resources={"*"})


def get_productos(page=1, per_page=10):
    conn = psycopg2.connect(
        dbname="MusicPro",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    offset = (page - 1) * per_page
    cur.execute("SELECT * FROM productos LIMIT %s OFFSET %s", (per_page, offset))
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return productos


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname="MusicPro",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
    return g.db


# --------------- login user


conn = psycopg2.connect(
    dbname="MusicPro",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432")


def login_required(rol='user'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if 'loggedin' in session and session['loggedin'] and session['rol'] == rol:
                return view_func(*args, **kwargs)
            else:
                return redirect(url_for('login_user'))

        return wrapped_view

    return decorator


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'loggedin' in session and session['loggedin'] and session['rol'] == 'admin':
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('login_admin'))

    return wrapped_view



@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT id, username, password, rol FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            password_hash = account['password']

            if check_password_hash(password_hash, password):
                if account['rol'] == 'user':
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    session['rol'] = account['rol']
                    return redirect(url_for('shop'))
                else:
                    flash('No estás autorizado para acceder a esta página.')
            else:
                flash('Usuario/contraseña incorrectos')
        else:
            flash('Usuario/contraseña incorrectos')

    return render_template('login_user.html')


@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT id, username, password, rol FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            password_hash = account['password']

            if check_password_hash(password_hash, password):
                if account['rol'] == 'admin':
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    session['rol'] = account['rol']
                    return redirect(url_for('admin'))
                else:
                    flash('No estás autorizado para acceder a esta página.')
            else:
                flash('Usuario/contraseña incorrectos')
        else:
            flash('Usuario/contraseña incorrectos')

    return render_template('login_admin.html')


@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        rol = 'user'  # Assign 'user' role

        _hashed_password = generate_password_hash(password)

        # Check if account exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash('La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Dirección de correo inválida!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username sólo debe contener caracteres y números!')
        elif not username or not password or not email:
            flash('Por favor, completa el formulario')
        else:
            # Account doesn't exist and the form data is valid, insert new account into users table
            cursor.execute("INSERT INTO users (fullname, username, password, email, rol) VALUES (%s,%s,%s,%s,%s)",
                           (fullname, username, _hashed_password, email, rol))
            conn.commit()
            flash('Te has registrado exitosamente!')

    return render_template('register_user.html')


@app.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username", "password" and "email" POST requests exist (admin submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        rol = 'admin'  # Assign 'admin' role

        _hashed_password = generate_password_hash(password)

        # Check if account exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash('La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Dirección de correo inválida!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username sólo debe contener caracteres y números!')
        elif not username or not password or not email:
            flash('Por favor, completa el formulario')
        else:
            # Account doesn't exist and the form data is valid, insert new account into users table
            cursor.execute("INSERT INTO users (fullname, username, password, email, rol) VALUES (%s,%s,%s,%s,%s)",
                           (fullname, username, _hashed_password, email, rol))
            conn.commit()
            flash('Admin registrado exitosamente!')

    return render_template('register_admin.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/profile')
@login_required(rol='user')
def profile():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)

    return redirect(url_for('login'))


@app.route('/admin_profile')
@admin_required
def admin_profile():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('admin_profile.html', account=account)

    return redirect(url_for('login'))


@app.route('/consumir')
def consumir_app_express():
    import requests
    try:
        # en response hay que cambiar la url segun corresponde
        response = requests.get('https://fce7-2800-150-124-1e82-d9df-7b23-279-e87b.ngrok-free.app/saludo')
        resultado = response.text
        # Realiza cualquier operación adicional con la variable 'resultado' aquí
        return resultado
    except requests.exceptions.RequestException:
        return 'Error al consumir la API de Express.'


@app.route('/mostrar_resultado')
def mostrar_resultado():
    resultado = consumir_app_express()  # Llamada a la función existente para obtener 'resultado'
    return render_template('resultado.html', resultado=resultado)


@app.route('/saludo', methods=['GET'])
def obtener_saludo():
    return 'Hola'


@app.route("/apiPrueba")
def apiPrueba():
    return render_template("apiSaludo.html")

@app.route("/seguimiento")
def seguimiento():
    return render_template("seguimiento.html")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
@admin_required
def admin():
    return render_template("vistaAdmin.html")


@app.route("/tables")
def tables():
    return render_template("tables.html")


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    productos = get_productos(page, per_page)

    if request.method == 'POST':
        sort_option = request.form.get('sort_option',
                                       '')  # asumimos que este es el nombre de tu select input en tu formulario

        if sort_option == "Destacado":
            # ordenar por destacados
            # esto dependerá de cómo estén estructurados tus datos
            pass
        elif sort_option == "De la A a la Z":
            # ordenar alfabéticamente
            productos.sort(
                key=itemgetter(1))  # asumiendo que el nombre del producto es el segundo elemento en cada tupla
        elif sort_option == "Por categoría":
            # ordenar por categoría
            productos.sort(
                key=itemgetter(5))  # asumiendo que la categoría del producto es el sexto elemento en cada tupla

    return render_template('shop.html', productos=productos, page=page, per_page=per_page)


@app.route("/agregar")
@admin_required
def agregar():
    return render_template("agregarProducto.html")

@app.route("/agregarRepuesto")
@admin_required
def agregarRepuesto():
    return render_template("agregarRepuesto.html")

@app.route("/listar")
@admin_required
def listar():
    return render_template("listarProducto.html")



@app.route("/informes")
@admin_required
def informes():
    return render_template("informes.html")


@app.route("/proveedores")
@admin_required
def proveedores():
    return render_template("proveedores.html")


@app.route("/bodega")
@admin_required
def bodega():
    return render_template("bodega.html")


@app.route("/tienda")
def tienda():
    return render_template("tienda.html")

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/reparar")
def reparar():
    return render_template("reparar.html")

@app.route("/personalizar")
def personalizar():
    return render_template("personalizar.html")

@app.route('/categorias/<categoria>')
def categorias(categoria):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM productos WHERE categoria = %s', (categoria,))
    productos = cur.fetchall()
    return render_template('shop.html', productos=productos)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    # Realizar la búsqueda en función de la consulta (variable "query")
    # Luego, renderiza la plantilla de resultados de búsqueda
    return render_template("search_results.html", query=query)




@app.errorhandler(404)
def error404(error):
    return render_template('page404.html'), 404


if __name__ == "__main__":
    # Forma mas practica de tener el modo debug activo (acordarse de desactivarlo al finalizar la app)
    app.config.from_object(config["development"])
    app.register_error_handler(404, error404)
    # Blueprint
    app.register_blueprint(Producto.main, url_prefix="/api/productos")
    app.run()