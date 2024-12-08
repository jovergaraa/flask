const agregarSaludo = document.querySelector('#subirSaludo');

agregarSaludo.addEventListener('submit', async e => {
    e.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

    const saludos = agregarSaludo['resultado'].value
    const response = await fetch('/api/productos/addSaludo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            saludos
        })
    });
    const data = await response.json();

    if (response.ok) {
        alert("El saludo se agregó correctamente");
        console.log(data); // Mostrar el resultado en la consola
        agregarSaludo.reset(); // Restablece el formulario
    } else {
        alert("Hubo un error al agregar el saludo");
    }
});
