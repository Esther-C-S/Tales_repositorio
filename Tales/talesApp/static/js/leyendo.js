const semicircles = document.querySelectorAll('.semicircle');
const timer = document.querySelector('.timer');
const plusButton = document.getElementById('plusButton');
const pauseResumeButton = document.getElementById('pauseResumeButton');
const stopButton = document.getElementById('stopButton');
let timerLoop;
let paused = false;
let remainingTime;
let futureTime;
let totalTime;
let startTime;
let timeElapsed = 0; // Inicializa timeElapsed en 0

// Inicializa el temporizador con 00:00:00 al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    timer.innerHTML = `
        <div>00</div>
        <div class="colon">:</div>
        <div>00</div>
        <div class="colon">:</div>
        <div>00</div>
    `;
    stopButton.disabled = true;
});

document.getElementById('startTimer').addEventListener('click', function() {
    const hr = parseInt(document.getElementById('hours').value) || 0;
    const min = parseInt(document.getElementById('minutes').value) || 0;
    const sec = parseInt(document.getElementById('seconds').value) || 0;

    const hours = hr * 3600000;
    const minutes = min * 60000;
    const seconds = sec * 1000;
    totalTime = hours + minutes + seconds;
    startTime = Date.now();
    futureTime = startTime + totalTime;
    remainingTime = totalTime;
    timeElapsed = 0; // Reinicia timeElapsed

    if (timerLoop) clearInterval(timerLoop);
    timerLoop = setInterval(countDownTimer, 1000);
    countDownTimer();

    // Deshabilita el botón de "+"
    plusButton.disabled = true;
    // Habilita el botón de cuadrado
    stopButton.disabled = false;

    // Cierra el modal
    $('#startModal').modal('hide');
});

pauseResumeButton.addEventListener('click', function() {
    const pauseResumeIcon = pauseResumeButton.querySelector('i');
    if (paused) {
        // Reanudar
        futureTime = Date.now() + remainingTime;
        timerLoop = setInterval(countDownTimer, 1000);
        pauseResumeIcon.classList.remove('bi-play-fill');
        pauseResumeIcon.classList.add('bi-pause');
        paused = false;
    } else {
        // Pausar
        clearInterval(timerLoop);
        remainingTime = futureTime - Date.now();
        timeElapsed = totalTime - remainingTime; // Actualiza timeElapsed al pausar
        pauseResumeIcon.classList.remove('bi-pause');
        pauseResumeIcon.classList.add('bi-play-fill');
        paused = true;
    }
});

stopButton.addEventListener('click', function() {
    clearInterval(timerLoop);
    if (!paused) {
        timeElapsed = totalTime - remainingTime;
    }
    

    // Abre el modal de páginas leídas
    $('#pagesReadModal').modal('show');
});

document.getElementById('savePagesRead').addEventListener('click', function() {
    const pagesRead = parseInt(document.getElementById('pagesRead').value) || 0;
    const totalMinutes = Math.floor(timeElapsed / 60000); // Minutos totales
    console.log('Total minutes:', totalMinutes);
    console.log('Total time:', totalTime);
    console.log('Remaining time:', remainingTime);
    console.log('Time elapsed:', timeElapsed);
    
    // Llamada AJAX para enviar los datos
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            paginas_leidas: pagesRead,
            tiempo_sesion: totalMinutes,
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            if (response.success) {
                location.reload(); // Recargar la página para mostrar los cambios
            } else {
                console.error("Error", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
});

function countDownTimer() {
    const currentTime = Date.now();
    remainingTime = futureTime - currentTime;
    const angle = (remainingTime / totalTime) * 360;

    // progress indicator
    if (angle > 180) {
        semicircles[2].style.display = 'none';
        semicircles[0].style.transform = 'rotate(180deg)';
        semicircles[1].style.transform = `rotate(${angle}deg)`;
    } else {
        semicircles[2].style.display = 'block';
        semicircles[0].style.transform = `rotate(${angle}deg)`;
        semicircles[1].style.transform = `rotate(${angle}deg)`;
    }

    // timer
    const hrs = Math.floor((remainingTime / 3600000) % 24).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });
    const mins = Math.floor((remainingTime / 60000) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });
    const secs = Math.floor((remainingTime / 1000) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });

    timer.innerHTML = `
        <div>${hrs}</div>
        <div class="colon">:</div>
        <div>${mins}</div>
        <div class="colon">:</div>
        <div>${secs}</div>
    `;

    // 5s condition
    if (remainingTime <= 6000) {
        semicircles[1].style.backgroundColor = 'red';
        semicircles[0].style.backgroundColor = 'red';
        timer.style.color = 'red';
    }

    // end
    if (remainingTime < 0) {
        clearInterval(timerLoop);
        timeElapsed = totalTime;
        semicircles[1].style.display = 'none';
        semicircles[0].style.display = 'none';
        timer.style.color = '#EBD9B4';

        timer.innerHTML = `
            <div>00</div>
            <div class="colon">:</div>
            <div>00</div>
            <div class="colon">:</div>
            <div>00</div>
        `;

        // Habilita el botón de "+"
        plusButton.disabled = false;
        
        // Deshabilita el botón de cuadrado
        stopButton.disabled = true;

        // Abre el modal automáticamente
        $('#pagesReadModal').modal('show');
    }
}
