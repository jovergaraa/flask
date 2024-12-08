$(document).ready(function() {
    $("#banner-carousel").owlCarousel({
        items: 1, // Cantidad de elementos visibles a la vez
        loop: true, // Repetir el carrusel en bucle
        autoplay: true, // Activar reproducción automática
        autoplayTimeout: 2000, // Intervalo de tiempo entre cada cambio de elemento (en milisegundos)
        autoplayHoverPause: true, // Pausar reproducción automática al pasar el cursor sobre el carrusel
        animatedOut: 'fadeOut', // Efecto de salida
        animateIn: 'fadeIn', // Efecto de entrada

    });
});