document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelector('#items');
    const footer = document.querySelector('#footer');
    const templateFooter = document.querySelector('#template-footer').content;
    const templateCarrito = document.querySelector('#template-carrito').content;
    const templateBoleta = document.querySelector('#template-boleta').content;
    const fragment = document.createDocumentFragment();
    let carrito = {};

    document.getElementById('btn-generar-boleta').addEventListener('click', function() {
        const zonaEntrega = document.getElementById('zona-entrega').value;
        generarBoleta(zonaEntrega);
    });

    items.addEventListener('click', e => {
        btnAccion(e);
    });

    const addToCartButtons = document.querySelectorAll('.btn-add');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const card = button.closest('.card');
            const product = {
                id: card.querySelector('.card-title').textContent,
                title: card.querySelector('.card-title').textContent,
                precio: card.querySelector('.card-text').textContent,
                cantidad: 1
            };

            carrito[product.id] = {...product};
            renderCarrito();
        });
    });

    const renderCarrito = () => {
        items.innerHTML = '';
        Object.values(carrito).forEach(product => {
            const clone = templateCarrito.cloneNode(true);
            clone.querySelector('th').textContent = product.id;
            clone.querySelectorAll('td')[0].textContent = product.title;
            clone.querySelectorAll('td')[1].textContent = product.cantidad;
            clone.querySelectorAll('td')[2].textContent = product.precio * product.cantidad;
            fragment.appendChild(clone);
        });
        items.appendChild(fragment);

        renderFooter();
    };

    const renderFooter = () => {
        footer.innerHTML = '';
        if (Object.keys(carrito).length === 0) {
            footer.innerHTML = '<th scope="row" colspan="5">Carrito Vacio</th>';
            return;
        }

        const nCantidad = Object.values(carrito).reduce((acc, {cantidad}) => acc + cantidad, 0);
        const nPrecio = Object.values(carrito).reduce((acc, {cantidad, precio}) => acc + cantidad * precio, 0);

        templateFooter.querySelectorAll('td')[0].textContent = nCantidad;
        templateFooter.querySelector('span').textContent = nPrecio;
        const clone = templateFooter.cloneNode(true);
        fragment.appendChild(clone);
        footer.appendChild(fragment);

        const btnVaciar = document.getElementById('vaciar-carrito');
        btnVaciar.addEventListener('click', () => {
            carrito = {};
            renderCarrito();
        });
    };

    const btnAccion = e => {
        if (e.target.classList.contains('btn-info')) {
            const producto = carrito[e.target.dataset.id];
            producto.cantidad++;
            carrito[e.target.dataset.id] = {...producto};
            renderCarrito();
        }

        if (e.target.classList.contains('btn-danger')) {
            const producto = carrito[e.target.dataset.id];
            producto.cantidad--;
            if (producto.cantidad === 0) {
                delete carrito[e.target.dataset.id];
            } else {
                carrito[e.target.dataset.id] = {...producto};
            }
            renderCarrito();
        }

        e.stopPropagation();
    };

    function generarBoleta(zonaEntrega) {
        const boletaContainer = document.getElementById('boleta');
        const templateBoleta = document.getElementById('template-boleta').content.cloneNode(true);

        // Rellena la información de la boleta
        templateBoleta.querySelector('#id-boleta').textContent = '12345'; // Ejemplo de ID de boleta
        templateBoleta.querySelector('#domicilio-boleta').textContent = zonaEntrega;
        templateBoleta.querySelector('#fecha-boleta').textContent = new Date().toLocaleDateString();
        templateBoleta.querySelector('#boleta-total').textContent = calcularTotal(); // Función para calcular el total

        // Añade los productos al detalle de la boleta
        const boletaItems = templateBoleta.querySelector('#boleta-items');
        const items = document.querySelectorAll('#items tr');
        items.forEach(item => {
            const itemClone = item.cloneNode(true);
            boletaItems.appendChild(itemClone);
        });

        // Limpia el contenedor de boleta y añade la nueva boleta
        boletaContainer.innerHTML = '';
        boletaContainer.appendChild(templateBoleta);
    }

    function calcularTotal() {
        let total = 0;
        const items = document.querySelectorAll('#items tr');
        items.forEach(item => {
            const itemTotal = parseFloat(item.querySelector('td:nth-child(5) span').textContent);
            total += itemTotal;
        });
        return total.toFixed(2);
    }
});
