function adjustButtonWidth() {
    var img = document.getElementById('portada');
    var btn = document.getElementById('dropdownBtn');
    btn.style.width = img.clientWidth + 'px';
}

function toggleDropdown() {
    document.getElementById("dropdownContent").classList.toggle("show");
}

function setStatus(status) {
    const libroId = "{{ libro.id }}";
    $.ajax({
        url: "{% url 'actualizar_estado_libro' %}",
        type: "POST",
        data: {
            libro_id: libroId,
            estado: status,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(response) {
            if (response.success) {
                document.querySelector('.dropbtn').textContent = response.estado_text;
                toggleDropdown();
            } else {
                alert('Error al actualizar el estado');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Error al actualizar el estado');
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




window.onload = adjustButtonWidth;
window.onresize = adjustButtonWidth;
