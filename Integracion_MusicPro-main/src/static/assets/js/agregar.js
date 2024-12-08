const agregarProducto = document.querySelector('#agregarProducto')

agregarProducto.addEventListener('submit', async e => {
    e.preventDefault()

    // Obtener los valores de los campos del formulario
    const nombre = agregarProducto['nombreProducto'].value
    const precio = agregarProducto['precioProducto'].value
    const descripcion = agregarProducto['descripcionProducto'].value
    const stock = agregarProducto['stockProducto'].value
    const categoria = agregarProducto['categoriaProducto'].value
    const imagenInput = agregarProducto['imagenProducto']
    const imagenFile = imagenInput.files[0]
    const tipomueble= agregarProducto['tipoproducto'].value

    // Validar los campos requeridos
    if (!nombre || !precio || !descripcion || !stock || !categoria || !imagenFile ||!tipomueble) {
        alert('Todos los campos son obligatorios.')
        return
    }

    // Leer la imagen como base64
    const reader = new FileReader()
    reader.onloadend = async function () {
        const imagenBase64 = reader.result.split(',')[1]

        // Enviar los datos al servidor
        try {
            const response = await fetch('/api/productos/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre,
                    precio,
                    descripcion,
                    imagen: imagenBase64,
                    stock,
                    categoria,
                    tipomueble
                })
            })

            const data = await response.json()

            if (response.ok) {
                alert("El producto se agregó correctamente")
                document.getElementById("agregarProducto").reset()
            } else {
                alert(`Error al agregar el producto: ${data.Mensaje}`)
            }
        } catch (error) {
            alert(`Hubo un error al agregar el producto: ${error.message}`)
        }
    }

    // Leer la imagen como base64
    reader.readAsDataURL(imagenFile)
})
