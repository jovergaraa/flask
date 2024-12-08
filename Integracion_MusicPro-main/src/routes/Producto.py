from flask import Blueprint, jsonify, request, send_file, render_template
from models.ProductoModel import ProductoModel
from models.entities.Productos import Producto, Boleta, BoletaBodega
import os
import base64
import uuid
import requests
from datetime import datetime
import imghdr

main = Blueprint("producto_blueprint", __name__)


@main.route("/")
def get_productos():
    try:
        productos = ProductoModel.get_productos()
        productos_json = [producto.to_json() for producto in productos]
        return jsonify(productos=productos_json)
    except Exception as ex:
        return jsonify({"mensaje": str(ex)}), 500

@main.route("/repuestos")
def get_productos_repuesto():
    try:
        productos = ProductoModel.get_productos_repuestos()
        productos_json = [producto.to_json() for producto in productos]
        return jsonify(productos=productos_json)
    except Exception as ex:
        return jsonify({"mensaje": str(ex)}), 500

@main.route("/muebles")
def get_productos_muebles():
    try:
        productos = ProductoModel.get_productos_muebles()
        productos_json = [producto.to_json() for producto in productos]
        return jsonify(productos=productos_json)
    except Exception as ex:
        return jsonify({"mensaje": str(ex)}), 500

@main.route("/<nombre>")
def get_producto(nombre):
    try:
        producto = ProductoModel.get_producto(nombre)
        if producto is not None:
            return jsonify(producto)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({"Mensaje:": str(ex)}), 500

@main.route("/uploads/<Nombre>", methods=["GET"])
def get_imagen_producto(Nombre):
    try:
        ruta_archivo = "static" + "/" + "uploads" + "/" + Nombre

        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, "rb") as archivo:
                imagen_bytes = archivo.read()

            extension = imghdr.what("", h=imagen_bytes)
            # Lista de extensiones permitidas
            extensiones_permitidas = ['jpeg', 'jpg', 'png', 'gif']

            if not extension or extension not in extensiones_permitidas:
                raise ValueError("La imagen proporcionada no tiene una extensión válida o no está permitida.")

            ruta_archivo = os.path.join("static", "uploads", f"{Nombre}.{extension}")

            return send_file(ruta_archivo, mimetype=f"image/{extension}")
        else:
            ruta_marcador = os.path.join("static", "placeholder.jpg")
            return send_file(ruta_marcador, mimetype="image/jpeg")
    except Exception as ex:
        print(str(ex))
        return jsonify({"mensaje": "Error al cargar la imagen"}), 500

@main.route("/add", methods=["POST"])
def add_producto():
    try:
        Nombre = request.json["nombre"]
        Precio = int(request.json["precio"])
        Descripcion = request.json["descripcion"]
        Imagen = request.json["imagen"]
        Stock = int(request.json["stock"])
        Categoria = request.json["categoria"] 
        tipomueble = request.json["tipomueble"]
        idProductos = str(uuid.uuid4())  # Convertir a cadena el ID generado 
        # Decodificar la imagen en base64
        imagen_decodificada = base64.b64decode(Imagen)
        
        # Obtener la extensión de la imagen (por ejemplo, .jpg, .png)
        extension = imghdr.what("", h=imagen_decodificada)
        if not extension:
            raise ValueError("La imagen proporcionada no tiene una extensión válida.")
        
        # Guardar la imagen en un archivo en el directorio "uploads"
        nombre_archivo = Nombre + "." + extension
        ruta_archivo = os.path.join("src", "static", "uploads", nombre_archivo)
        with open(ruta_archivo, "wb") as archivo:
            archivo.write(imagen_decodificada)

        producto = Producto(idProductos, Nombre, Precio, Descripcion, nombre_archivo, Stock, Categoria, tipomueble)

        affected_rows = ProductoModel.add_producto(producto)

        if affected_rows == 1:
            return jsonify({"id": producto.idProductos})
        else:
            return jsonify({"Mensaje": "Fallo en la inserción"}), 500
    except Exception as ex:
        return jsonify({"Mensaje": str(ex)}), 500

@main.route("/delete/<idProductos>", methods=["DELETE"])
def delete_producto(idProductos):
    try:
        affected_rows = ProductoModel.delete_producto(idProductos)

        if affected_rows == 1:
            return jsonify({idProductos})
        else:
            return jsonify({"Mensaje:": "No existe"}), 500
    except Exception as ex:
        return jsonify({"Mensaje:": str(ex)}), 500



@main.route("/update/<idProductos>", methods=["PUT"])
def update_producto(idProductos):
    try:
        Nombre = request.json["nombre"]
        Precio = int(request.json["precio"])
        Descripcion = request.json["descripcion"]
        Imagen = request.json["imagen"]
        Stock = int(request.json["stock"])
        Categoria = request.json["categoria"] 
        
        # Obtener el producto existente en la base de datos
        producto_existente = ProductoModel.get_producto(idProductos)
        if not producto_existente:
            return jsonify({"Mensaje": "El producto no existe"}), 404
        
        # Actualizar los campos del producto existente
        producto_existente.Nombre = Nombre
        producto_existente.Precio = Precio
        producto_existente.Descripcion = Descripcion
        producto_existente.Stock = Stock
        producto_existente.Categoria = Categoria
        
        # Verificar si se proporcionó una nueva imagen para actualizar
        if Imagen:
            # Decodificar la imagen en base64
            imagen_decodificada = base64.b64decode(Imagen)
            
            # Obtener la extensión de la imagen (por ejemplo, .jpg, .png)
            extension = imghdr.what("", h=imagen_decodificada)
            if not extension:
                raise ValueError("La imagen proporcionada no tiene una extensión válida.")
            
            # Guardar la imagen en un archivo en el directorio "uploads"
            nombre_archivo = Nombre + "." + extension
            ruta_archivo = os.path.join("src", "static", "uploads", nombre_archivo)
            with open(ruta_archivo, "wb") as archivo:
                archivo.write(imagen_decodificada)
            
            # Actualizar el campo de imagen del producto existente
            producto_existente.Imagen = nombre_archivo
        
        # Guardar los cambios en el producto existente
        affected_rows = ProductoModel.update_producto(producto_existente)

        if affected_rows == 1:
            return jsonify({"id": producto_existente.idProductos})
        else:
            return jsonify({"Mensaje": "Fallo en la actualización"}), 500
    except Exception as ex:
        return jsonify({"Mensaje": str(ex)}), 500

@main.route("/bodega")
def obtenerBodega():
    url = "https://musicproocyberedge.onrender.com/api/productos"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBydWViYSIsImlkIjoiNjQ4Njg1ZjNiMjY5Y2U3NGFiNGM3N2VlIiwiaWF0IjoxNjg2OTQzOTc1fQ.vr3jouIQaxSZ2zyELSc4c4r2ayKSPHWCthoZoODragg"
    headers = {
        "Auth-token": token
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return jsonify(productos=data)

@main.route("/addBoleta", methods=["POST"])
def add_boleta():
    try:
        idBoleta = request.json.get("idBoleta")
        domicilio = request.json.get("domicilio")
        productos = request.json.get("productos")
        fechaBoleta = request.json.get("fechaBoleta")  # Corregido aquí
        fechaEntrega = request.json.get("fechaEntrega")
        telefono = request.json.get("telefono")
        nombre = request.json.get("nombre")
        total = request.json.get("total")

        boleta = Boleta(idBoleta, domicilio, productos, fechaBoleta, fechaEntrega, telefono, nombre, total)

        affected_rows = ProductoModel.add_boleta(boleta)

        if affected_rows == 1:
            return jsonify({"idBoleta": idBoleta})
        else:
            return jsonify({"Mensaje": "No existe"}), 500
    except Exception as ex:
        return jsonify({"Mensaje": str(ex)}), 500

@main.route("/addBoletaBodega", methods=["POST"])
def add_boletaBodega():
    try:
        idBoleta = request.json.get("idBoleta")
        productos = request.json.get("productos")
        fechaBoleta = request.json.get("fechaBoleta")
        sucursal = request.json.get("sucursal")
        total = request.json.get("total")

        boleta = BoletaBodega(idBoleta, sucursal, fechaBoleta, productos, total)

        affected_rows = ProductoModel.add_boletaBodega(boleta)

        if affected_rows == 1:
            return jsonify({"idBoleta": idBoleta})
        else:
            return jsonify({"Mensaje": "No existe"}), 500
    except Exception as ex:
        return jsonify({"Mensaje": str(ex)}), 500

@main.route("/listarBodega")
def get_boletaBodega():
    try:
        boletas = ProductoModel.get_boletaBodega()
        boletas_json = [boleta.to_json_boletaBodega() for boleta in boletas]
        return jsonify(boletas=boletas_json)
    except Exception as ex:
        return jsonify({"mensaje": str(ex)}), 500

@main.route('/transporte', methods=['POST'])
def enviar_datos():
    url_api_externa = 'http://25.2.54.205/cybercore/api/pedidosapi_sucursal.php/pedidos'

    # Obtener los datos del formulario o la solicitud JSON
    nombre_origen = request.form.get('nombre_origen')
    direccion_origen = request.form.get('direccion_origen')
    celular_origen = request.form.get('celular_origen')
    nombre_destino = request.form.get('nombre_destino')
    direccion_destino = request.form.get('direccion_destino')
    celular_destino = request.form.get('celular_destino')
    obs = request.form.get('obs')

    # Crear un diccionario con los datos a enviar en el orden correcto
    datos = {
        'nombre_origen': nombre_origen,
        'direccion_origen': direccion_origen,
        'celular_origen': celular_origen,
        'nombre_destino': nombre_destino,
        'direccion_destino': direccion_destino,
        'celular_destino': celular_destino,
        'obs': obs
    }

    try:
        response = requests.post(url_api_externa, data=datos)
        
        if response.status_code == 200:
            orden_seguimiento = response.json()
            return jsonify(orden_seguimiento)
        else:
            return 'Error al enviar los datos a la API externa'

    except requests.exceptions.RequestException as e:
        return 'Error al conectarse a la API externa: ' + str(e)
    
@main.route('/seguimiento/<codigo_seguimiento>', methods=['GET'])
def obtener_estado_pedido(codigo_seguimiento):
    url_api_externa = 'http://25.2.54.205/cybercore/api/codigo_seguimientoAPI.php'
    # Crear un diccionario con el código de seguimiento
    datos = {
        'codigo_seguimiento': codigo_seguimiento
    }
    try:
        response = requests.get(url_api_externa, params=datos)

        if response.status_code == 200:
            estado_pedido = response.json().get('estado_pedido')
            return jsonify({'estado_pedido': estado_pedido})
        else:
            return 'Error al obtener el estado del pedido de la API externa'
    except requests.exceptions.RequestException as e:
        return 'Error al conectarse a la API externa: ' + str(e)


