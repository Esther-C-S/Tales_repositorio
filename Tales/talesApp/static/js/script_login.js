const quote = document.getElementById('quote');
const loginForm = document.getElementById('loginForm');
const toggleBtn = document.getElementById('toggleBtn');

toggleBtn.addEventListener('click', function() {
  quote.classList.toggle('slideUp');
  loginForm.classList.toggle('slideDown');
  toggleBtn.classList.toggle('open');
});