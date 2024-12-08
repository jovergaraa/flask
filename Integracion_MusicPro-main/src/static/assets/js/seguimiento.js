document.getElementById("btn-seguir").addEventListener("click", async () => {
    const codigoSeguimiento = document.getElementById("idSeguimiento").value;
    console.log(codigoSeguimiento)
    const urlApiFlask = `/api/productos/seguimiento/${codigoSeguimiento}`;

    try {
        const response = await fetch(urlApiFlask);

        if (response.ok) {
            const responseData = await response.json();
            const estadoPedido = responseData.estado_pedido;
            // Mapeo de estados de pedido a pasos
            const pasos = {
                'PREPARANDO': 'step1',
                'ASIGNADO': 'step2',
                'PEDIDO TOMADO': 'step3',
                'PEDIDO FINALIZADO': 'step4'
            };
            // Marca todos los pasos hasta el estado actual como completados
            for (let paso in pasos) {
                const stepElement = document.getElementById(pasos[paso]);
                if (paso === estadoPedido) {
                    stepElement.classList.add('complete');
                    break;
                } else {
                    stepElement.classList.add('complete');
                }
            }
            // Muestra el modal
            var myModal = new bootstrap.Modal(document.getElementById('modalEstadoPedido'), {});
            myModal.show();
        } else {
            throw new Error('Error en la solicitud');
        }
    } catch (error) {
        console.error('Error en la solicitud:', error);
    }
});


