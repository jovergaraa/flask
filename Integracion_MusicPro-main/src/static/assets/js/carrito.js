// Variables globales
const templateCard = document.getElementById("template-card").content;
const templateFooter = document.getElementById("template-footer").content;
const templateCarrito = document.getElementById("template-carrito").content;
const templateBoleta = document.getElementById("template-boleta").content;
const cards = document.getElementById("cards");
const items = document.getElementById("items");
const footer = document.getElementById("footer");
const fragment = document.createDocumentFragment();
const tipomueble =  document.getElementById

let carrito = {};
let productos = [];  // Variable para almacenar todos los productos

const fechaActual = new Date();
const dia = fechaActual.getDate();
const mes = fechaActual.getMonth() + 1;
const anio = fechaActual.getFullYear();
const fechaCompleta = `${anio}-${mes < 10 ? '0' + mes : mes}-${dia < 10 ? '0' + dia : dia}`;

document.addEventListener("DOMContentLoaded", () => {
    fetchData();
});

const fetchData = async () => {
    try {
        const res = await fetch("api/productos");
        const data = await res.json();
        productos = data.productos;
        mostrarBodega(productos);
    } catch (error) {
        console.log(error);
    }
};

cards.addEventListener("click", e => {
    addCarrito(e);
});

items.addEventListener("click", e => {
    btnAccion(e);
});


document.querySelectorAll(".categoria").forEach(button => {
    button.addEventListener("click", e => {
        const categoria = e.target.dataset.categoria;
        
        if (categoria === "todos") {
            mostrarBodega(productos); // Mostrar todos los productos
        } else if (categoria === "repuestos" || categoria === "liberty" || categoria === "garcia" || categoria === "antonieta") {
            const productosFiltrados = productos.filter(producto => producto.Categoria.toLowerCase() === categoria);
            mostrarBodega(productosFiltrados); // Mostrar productos filtrados por categoría
        } else {
            console.log("Categoría no reconocida o no implementada.");
        }
    });
});

document.querySelectorAll(".tipomueble").forEach(button => {
    button.addEventListener("click", e => {
        const tipomueble = e.target.dataset.categoria;
        
        if (tipomueble === "todos") {
            mostrarBodega(productos); // Mostrar todos los productos
        } else if (tipomueble === "dormitorio" || tipomueble === "cocina" || tipomueble === "baño") {
            const productosFiltrados = productos.filter(producto => producto.tipomueble.toLowerCase() === tipomueble);
            mostrarBodega(productosFiltrados); // Mostrar productos filtrados por categoría
        } else {
            console.log("Categoría no reconocida o no implementada.");
        }
    });
});

const mostrarBodega = data => {
    cards.innerHTML = '';  // Limpiar el contenido previo
    data.forEach(producto => {
        templateCard.querySelector('h1').textContent = producto.Nombre;
        //templateCard.querySelector('h3').textContent = `Precio:$ ${producto.Precio}`; // Agregar "Precio: $" antes del precio
        templateCard.querySelector('h3').textContent = producto.Precio;
        templateCard.querySelector('p').textContent = `Descripción: ${producto.Descripcion}`;
        templateCard.querySelector('h4').textContent = `Linea: ${producto.Categoria}`;
        templateCard.querySelector('img').src = `/static/uploads/${producto.Imagen}`;
        templateCard.querySelector('.btn-dark').dataset.id = producto.idProductos;
        const clone = templateCard.cloneNode(true);
        fragment.appendChild(clone);
    });
    cards.appendChild(fragment);
};

const mostrarCarrito = () => {
    items.innerHTML = '';
    let indice = 1;
    Object.values(carrito).forEach(producto => {
        templateCarrito.querySelector('th').textContent = indice++;
        templateCarrito.querySelectorAll('td')[0].textContent = producto.nombre;
        templateCarrito.querySelectorAll('td')[1].textContent = producto.cantidad;
        templateCarrito.querySelector('.btn-info').dataset.id = producto.id;
        templateCarrito.querySelector('.btn-danger').dataset.id = producto.id;
        templateCarrito.querySelector('span').textContent = producto.cantidad * producto.precio;
        const clone = templateCarrito.cloneNode(true);
        fragment.appendChild(clone);
    });
    items.appendChild(fragment);
    mostrarFooter();
};

function generarIdAleatoria(longitud) {
    let id = '';
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < longitud; i++) {
        const indice = Math.floor(Math.random() * caracteres.length);
        id += caracteres.charAt(indice);
    }
    return id;
}

const addCarrito = e => {
    if (e.target.classList.contains('btn-dark')) {
        setCarrito(e.target.parentElement);
    }
    e.stopPropagation();
};

const setCarrito = objeto => {
    const producto = {
        id: objeto.querySelector('.btn-dark').dataset.id,
        nombre: objeto.querySelector('h1').textContent,
        precio: parseFloat(objeto.querySelector('h3').textContent),
        cantidad: 1
    };
    if (carrito.hasOwnProperty(producto.id)) {
        producto.cantidad = carrito[producto.id].cantidad + 1;
    }
    carrito[producto.id] = { ...producto };
    mostrarCarrito();
};

const mostrarFooter = () => {
    footer.innerHTML = '';
    if (Object.keys(carrito).length === 0) {
        footer.innerHTML = `
            <th scope="row" colspan="5">Carrito Vacío</th>
        `;
        return;
    }

    const nCantidad = Object.values(carrito).reduce((acc, { cantidad }) => acc + cantidad, 0);
    const nPrecio = Object.values(carrito).reduce((acc, { cantidad, precio }) => acc + precio * cantidad, 0);

    templateFooter.querySelectorAll('td')[0].textContent = nCantidad;
    templateFooter.querySelector('span').textContent = nPrecio.toFixed(2);

    const clone = templateFooter.cloneNode(true);
    fragment.appendChild(clone);
    footer.appendChild(fragment);

    const btnVaciar = document.getElementById('vaciar-carrito');
    btnVaciar.addEventListener("click", () => {
        carrito = {};
        mostrarCarrito();
    });

    const btnGenerarBoleta = document.getElementById('btn-generar-boleta');
    btnGenerarBoleta.addEventListener("click", mostrarBoleta);
};

const btnAccion = e => {
    if (e.target.classList.contains('btn-info')) {
        const producto = carrito[e.target.dataset.id];
        producto.cantidad++;
        carrito[e.target.dataset.id] = { ...producto };
        mostrarCarrito();
    }

    if (e.target.classList.contains('btn-danger')) {
        const producto = carrito[e.target.dataset.id];
        producto.cantidad--;
        if (producto.cantidad === 0) {
            delete carrito[e.target.dataset.id];
        }
        mostrarCarrito();
    }
    e.stopPropagation();
};

const mostrarBoleta = () => {
    const boletaContainer = document.getElementById("boleta");
    boletaContainer.innerHTML = "";

    const zonaEntregaSelect = document.getElementById("zona-entrega");
    const zonaEntrega = zonaEntregaSelect.options[zonaEntregaSelect.selectedIndex].text;

    const boletaItems = Object.values(carrito).map(producto => `
        <p>${producto.nombre} - Cantidad: ${producto.cantidad}</p>
    `).join("");

    const boletaTotal = Object.values(carrito).reduce((total, producto) => {
        return total + (producto.cantidad * producto.precio);
    }, 0);

    const clone = templateBoleta.cloneNode(true);
    clone.getElementById("boleta-items").innerHTML = boletaItems;
    clone.getElementById("boleta-total").textContent = boletaTotal.toFixed(2);
    clone.getElementById("fecha-boleta").textContent = fechaCompleta;
    clone.getElementById("id-boleta").textContent = generarIdAleatoria(8);
    clone.getElementById("domicilio-boleta").textContent = zonaEntrega;

    boletaContainer.appendChild(clone);
    const btnAgregarBoleta = document.getElementById('btn-agregar-boleta');
    btnAgregarBoleta.addEventListener("click", function() {
        agregarBoleta();
        enviarDatos();
    });
};

const agregarBoleta = async () => {
    const idBoleta = document.getElementById("id-boleta").textContent;
    const domicilio = document.getElementById("domicilio-boleta").textContent;
    const fechaBoleta = document.getElementById("fecha-boleta").textContent;
    const fechaEntrega = document.getElementById("fecha-entrega").textContent;
    const productos = document.getElementById("boleta-items").textContent;
    const telefono = document.getElementById("telefono-boleta").value;
    const nombre = document.getElementById("nombre-boleta").value;
    const total = document.getElementById("boleta-total").textContent;

    const data = {
        idBoleta,
        nombre,
        telefono,
        domicilio,
        fechaBoleta,
        fechaEntrega,
        productos,
        total
    };

    try {
        const response = await fetch("/api/productos/addBoleta", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
};

const enviarDatos = async () => {
    const urlApiExterna = 'http://25.2.54.205/cybercore/api/pedidosapi_sucursal.php/pedidos';

    // Crear un objeto FormData y agregar los datos
    const formData = new FormData();
    formData.append('nombre_origen', 'Music Pro');
    formData.append('direccion_origen', 'Puente alto');
    formData.append('celular_origen', '222111222');
    formData.append('nombre_destino', document.getElementById("nombre-boleta").value);
    formData.append('direccion_destino', document.getElementById("domicilio-boleta").textContent);
    formData.append('celular_destino', document.getElementById("telefono-boleta").value);
    formData.append('obs', document.getElementById("boleta-items").textContent);

    try {
        const response = await fetch(urlApiExterna, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const responseData = await response.json();
            alert(JSON.stringify("Gracias por su compra! Codigo de seguimiento: " + responseData.codigo_seguimiento));
        } else {
            throw new Error('Error en la solicitud');
        }
    } catch (error) {
        console.error('Error en la solicitud:', error);
    }
};
