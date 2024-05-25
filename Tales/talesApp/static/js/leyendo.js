const semicircles = document.querySelectorAll('.semicircle');
const timer = document.querySelector('.timer');

/* input */

const hr = 0;
const min = 0;
const sec = 30;

const hours = hr * 3600000;
const minutes = min * 60000;
const seconds = sec * 1000;
const setTime = hours + minutes + seconds;
const starTime = Date.now();
const futureTime = starTime + setTime;

const timerLoop = setInterval(countDownTimer);
countDownTimer();

function countDownTimer() {

    const currentTime = Date.now();
    const remainigTime = futureTime - currentTime;
    const angle = ( remainigTime / setTime ) * 360;

    //progress indicator
    if (angle > 180) {
        semicircles[2].style.display = 'none';
        semicircles[0].style.transform = 'rotate(180deg)';
        semicircles[1].style.transform = `rotate(${angle}deg)`;
    }else{
        semicircles[2].style.display = 'block';
        semicircles[0].style.transform = `rotate(${angle}deg)`;
        semicircles[1].style.transform = `rotate(${angle}deg)`;
    }

    //timer
    // const hrs = Math.floor((remainigTime / 1000 * 60 * 60) % 24).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});
    // const mins = Math.floor((remainigTime / 1000 * 60) % 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});;
    // const secs = Math.floor((remainigTime / 1000) % 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});;
    const hrs = Math.floor((remainigTime / 3600000) % 24).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });
    const mins = Math.floor((remainigTime / 60000) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });
    const secs = Math.floor((remainigTime / 1000) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });

    timer.innerHTML = `
    <div>${hrs}</div>
    <div class="colon">:</div>
    <div>${mins}</div>
    <div class="colon">:</div>
    <div>${secs}</div>
    `;

    //5s condition
    if (remainigTime <= 6000) {
        semicircles[1].style.backgroundColor = 'red';
        semicircles[0].style.backgroundColor = 'red';
        timer.style.color = 'red';
    }

    //end
    if (remainigTime < 0) {
        clearInterval(timerLoop)
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
    }
}