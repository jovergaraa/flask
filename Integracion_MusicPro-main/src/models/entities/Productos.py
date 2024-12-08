class Producto:
    def __init__(
        self, idProductos, Nombre=None, Precio=None, Descripcion=None, Imagen=None, Stock=None, Categoria=None, tipomueble=None
    ) -> None:
        self.idProductos = idProductos
        self.Nombre = Nombre
        self.Precio = Precio
        self.Descripcion = Descripcion
        self.Imagen = Imagen
        self.Stock = Stock
        self.Categoria = Categoria
        self.tipomueble = tipomueble

    def to_json(self):
        product_json = {
            "idProductos": self.idProductos,
            "Nombre": self.Nombre,
            "Precio": self.Precio,
            "Descripcion": self.Descripcion,
            "Imagen": self.Imagen,
            "Stock": self.Stock,
            "Categoria": self.Categoria,
            "tipomueble":self.tipomueble
        }
        return product_json

class Boleta:
    def __init__(self, idBoleta, domicilio, productos, fechaBoleta, fechaEntrega, telefono, nombre, total):
        self.idBoleta = idBoleta
        self.domicilio = domicilio
        self.productos = productos
        self.fechaBoleta = fechaBoleta
        self.fechaEntrega = fechaEntrega
        self.telefono = telefono
        self.nombre = nombre
        self.total = total


    def to_json_boleta(self):
        boleta_json = {
            "idBoleta": self.idBoleta,
            "domicilio": self.domicilio,
            "productos": self.productos,
            "fechaBoleta": self.fechaBoleta,
            "fechaEntrega": self.fechaEntrega,
            "telefono": self.telefono,
            "nombre": self.nombre,
            "total": self.total,
        }
        return boleta_json

class BoletaBodega:
    def __init__(self, idBoleta, sucursal=None ,fechaBoleta=None, productos=None, total=None):
        self.idBoleta = idBoleta
        self.sucursal = sucursal
        self.fechaBoleta = fechaBoleta
        self.productos = productos
        self.total = total


    def to_json_boletaBodega(self):
        boletaBodega_json = {
            "idBoleta": self.idBoleta,
            "sucursal": self.sucursal,
            "fechaBoleta": self.fechaBoleta,
            "productos": self.productos,
            "total": self.total,

        }
        return boletaBodega_json

    
