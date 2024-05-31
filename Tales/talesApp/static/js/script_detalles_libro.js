function adjustButtonWidth() {
    var img = document.getElementById('portada');
    var btn = document.getElementById('dropdownBtn');
    btn.style.width = img.clientWidth + 'px';
}

function toggleDropdown() {
    document.getElementById("dropdownContent").classList.toggle("show");
}

function setStatus(status) {
    $.ajax({
        url: actualizarEstadoLibroUrl,
        type: "POST",
        data: {
            id_libro: libroId,
            estado: status,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(response) {
            if (response.success) {
                document.querySelector('.dropbtn').textContent = response.estado_text;
                toggleDropdown();
            } else {
                console.error(error);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

document.getElementById('resenaForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const valoracion = document.getElementById('valoracion').value;
    const opinion = document.getElementById('opinion').value;

    $.ajax({
        url: enviarReseña,
        type: "POST",
        data: {
            valoracion: valoracion,
            opinion: opinion,
            id_libro: libroId,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(response) {
            if (response.success) {
                location.reload();
            } else {
                alert('Error enviar la reseña');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
});

window.onload = adjustButtonWidth;
window.onresize = adjustButtonWidth;
