const templateCard = document.getElementById("template-card").content;
const templateFooter = document.getElementById("template-footer").content;
const templateCarrito = document.getElementById("template-carrito").content;
const templateBoleta = document.getElementById("template-boleta").content;
const cards = document.getElementById("cards");
const items = document.getElementById("items");
const footer = document.getElementById("footer")
const fragment = document.createDocumentFragment();
let carrito = {}


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
        const res = await fetch("api/productos/bodega");
        const data = await res.json();

        mostrarBodega(data);
    } catch (error) {
        console.log(error);
    }
};

cards.addEventListener("click", e =>{
    addCarrito(e)
})

items.addEventListener("click", e =>{
    btnAccion(e)
})

const mostrarBodega = data => {
    data.productos.forEach(producto => {
        templateCard.querySelector('h1').textContent = producto.nombre;
        templateCard.querySelector('h3').textContent = producto.precio;
        templateCard.querySelector('p').textContent = producto.subcategoria;
        templateCard.querySelector('img').src = producto.imagen;
        templateCard.querySelector('.btn-dark').dataset.id = producto._id;
        const clone = templateCard.cloneNode(true);
        fragment.appendChild(clone);
    });
    cards.appendChild(fragment);
    console.log(data)
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
  // Ejemplo de uso:
const idAleatoria = generarIdAleatoria(8);

const addCarrito = e =>{
    //console.log(e.target.classList.contains('btn-dark'))
    if(e.target.classList.contains('btn-dark')){
        setCarrito(e.target.parentElement)
    }
    e.stopPropagation()
}



const mostrarCarrito = () => {
    console.log(carrito)
    indice = 1
    items.innerHTML = ''
    Object.values(carrito).forEach(producto => {
        templateCarrito.querySelector('th').textContent = indice++
        templateCarrito.querySelectorAll('td')[0].textContent = producto.nombre
        templateCarrito.querySelectorAll('td')[1].textContent = producto.cantidad
        templateCarrito.querySelector('.btn-info').dataset.id = producto.id
        templateCarrito.querySelector('.btn-danger').dataset.id = producto.id
        templateCarrito.querySelector('span').textContent = producto.cantidad * producto.precio
        const clone = templateCarrito.cloneNode(true)
        fragment.appendChild(clone)
    })
    items.appendChild(fragment)

    mostrarFooter()
    mostrarBoleta()
}

const mostrarFooter = () => {
    footer.innerHTML = ''
    if (Object.keys(carrito).length === 0){
        footer.innerHTML = `
        <th scope="row" colspan="5">Carrito Vacio</th>
        `
        return
    }
    const nCantidad = Object.values(carrito).reduce((acc, {cantidad}) => acc + cantidad,0)
    const nPrecio = Object.values(carrito).reduce((acc, {cantidad, precio}) => acc + precio * cantidad,0)
    //console.log(nPrecio)

    templateFooter.querySelectorAll('td')[0].textContent = nCantidad
    templateFooter.querySelector('span').textContent = nPrecio

    const clone = templateFooter.cloneNode(true)
    fragment.appendChild(clone)
    footer.appendChild(fragment)

    const btnVaciar = document.getElementById('vaciar-carrito')
    btnVaciar.addEventListener("click", () => {
        carrito = {}
        mostrarCarrito()
    })
}

const setCarrito = objeto => {
    const producto = {
        id: objeto.querySelector(".btn-dark").dataset.id,
        nombre: objeto.querySelector("h1").textContent,
        precio: objeto.querySelector("h3").textContent,
        cantidad: 1
    }
    if(carrito.hasOwnProperty(producto.id)){
        producto.cantidad = carrito[producto.id].cantidad + 1
    }

    carrito[producto.id] = {...producto}
    mostrarCarrito()
    mostrarFooter()
}
const btnAccion = e => {
    if (e.target.classList.contains('btn-info')) {
        const producto = carrito[e.target.dataset.id]
        producto.cantidad++
        carrito[e.target.dataset.id] = {...producto}
        mostrarCarrito()
    }

    if(e.target.classList.contains('btn-danger')) {
        const producto = carrito[e.target.dataset.id]
        producto.cantidad--
        if(producto.cantidad === 0){
            delete carrito[e.target.dataset.id]
        }
        mostrarCarrito()
    }
    e.stopPropagation()
}

const mostrarBoleta = () => {
    const boletaContainer = document.getElementById("boleta");
    boletaContainer.innerHTML = "";

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

    boletaContainer.appendChild(clone);
    const btnAgregarBoleta = document.getElementById('btn-agregar-boleta');
    btnAgregarBoleta.addEventListener("click", agregarBoleta);
};

const agregarBoleta = async () => {
    const idBoleta = document.getElementById("id-boleta").textContent;
    const fechaBoleta = document.getElementById("fecha-boleta").textContent;
    const productos = document.getElementById("boleta-items").textContent;
    const sucursal = document.getElementById("boleta-sucursal").value; // Obtener el valor seleccionado
    const total = document.getElementById("boleta-total").textContent;

    const data = {
        idBoleta,
        fechaBoleta,
        sucursal,
        productos,  
        total
    };
    console.log(data);

    try {
        const response = await fetch("/api/productos/addBoletaBodega", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            console.log("Boleta agregada correctamente");
        } else {
            console.error("Error al agregar la boleta");
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
};
