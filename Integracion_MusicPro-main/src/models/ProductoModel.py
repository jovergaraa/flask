from database.db import get_connection
from .entities.Productos import Producto, Boleta, BoletaBodega
import base64

class ProductoModel:

    @classmethod
    def get_productos(self):
        try:
            connection = get_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT "idProductos", "nombre", "precio", "descripcion", "imagen", "stock", "categoria", "tipomueble" FROM public.productos;"""
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    productos.append(producto)

            connection.close()
            return productos
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_productos_repuestos(self):
        try:
            connection = get_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT "idProductos", nombre, precio, descripcion, imagen, stock, categoria
                    FROM public.productos
                    WHERE categoria = 'Repuesto';"""
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    productos.append(producto)

            connection.close()
            return productos
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_productos_muebles(self):
        try:
            connection = get_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT "idProductos", nombre, precio, descripcion, imagen, stock, categoria
                    FROM public.productos
                    WHERE categoria = 'Muebleria';"""
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    productos.append(producto)

            connection.close()
            return productos
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_producto(self, nombre):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT "idProductos", "nombre", "precio", "descripcion", "imagen", "stock", "categoria"
                                FROM public.productos WHERE "nombre" = %s""",
                    (nombre,),
                )
                row = cursor.fetchone()

                producto = None
                if row is not None:
                    imagen_base64 = row[4]
                    imagen_bytes = base64.b64decode(imagen_base64)
                    producto = Producto(row[0], row[1], row[2], row[3], imagen_bytes)
                    producto = producto.to_json()
            connection.close()
            return producto
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_producto(self, Producto):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.productos(
	                        "idProductos", "nombre", "precio", "descripcion", "imagen", "stock", "categoria", "tipomueble")
	                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (
                        Producto.idProductos,
                        Producto.Nombre,
                        Producto.Precio,
                        Producto.Descripcion,
                        Producto.Imagen,
                        Producto.Stock,
                        Producto.Categoria,
                        Producto.tipomueble
                    ),
                )
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_producto(self, idProductos):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM public.productos
	                            WHERE "idProductos" = %s;""",
                    (idProductos,),
                )

                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_boleta(self, Boleta):
            try:
                connection = get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO public.boleta(
                                "idBoleta","nombre", "telefono", "domicilio", "productos", "fechaBoleta", "fechaEntrega", "total")
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                        (
                            Boleta.idBoleta,
                            Boleta.nombre,
                            Boleta.telefono,
                            Boleta.domicilio,
                            Boleta.productos,
                            Boleta.fechaBoleta,
                            Boleta.fechaEntrega,
                            Boleta.total,
                        ),
                    )
                    affected_rows = cursor.rowcount
                    connection.commit()
                connection.close()
                return affected_rows
            except Exception as ex:
                raise Exception(ex)
            
    @classmethod
    def add_boletaBodega(self, BoletaBodega):
            try:
                connection = get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO public."boletaBodega"(
                            "idBoleta", sucursal, "fechaCompra", productos, total)
                            VALUES (%s, %s, %s, %s, %s);""",
                        (
                            BoletaBodega.idBoleta,
                            BoletaBodega.sucursal,
                            BoletaBodega.fechaBoleta,
                            BoletaBodega.productos,
                            BoletaBodega.total,
                        ),
                    )
                    affected_rows = cursor.rowcount
                    connection.commit()
                connection.close()
                return affected_rows
            except Exception as ex:
                raise Exception(ex)

    @classmethod
    def get_boletaBodega(self):
        try:
            connection = get_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT "idBoleta", sucursal, "fechaCompra", productos, total
                        FROM public."boletaBodega";"""
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    boleta = BoletaBodega(row[0], row[1], row[2], row[3], row[4])
                    productos.append(boleta)

            connection.close()
            return productos
        except Exception as ex:
            raise Exception(ex)

