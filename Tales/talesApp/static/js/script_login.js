document.addEventListener('DOMContentLoaded', function() {
  const quote = document.getElementById('quote');
  const loginForm = document.getElementById('loginForm');
  const toggleBtn = document.getElementById('toggleBtn');

  function handleToggle() {
      quote.classList.toggle('slideUp');
      loginForm.classList.toggle('slideDown');
      toggleBtn.classList.toggle('open');
  }

  function checkScreenWidth() {
      if (window.innerWidth < 500) {
          handleToggle();
      }
  }

  // Añadir el event listener para el clic en el botón
  toggleBtn.addEventListener('click', handleToggle);

  // Verificar el ancho de la pantalla al cargar la página y al cambiar el tamaño de la ventana
  checkScreenWidth();
  window.addEventListener('resize', function() {
      if (window.innerWidth >= 500) {
          // Si la pantalla es mayor o igual a 500px, restablecer las clases
          quote.classList.remove('slideUp');
          loginForm.classList.remove('slideDown');
          toggleBtn.classList.remove('open');
      } else {
          // Si la pantalla es menor de 500px, activar el event listener
          checkScreenWidth();
      }
  });
});

