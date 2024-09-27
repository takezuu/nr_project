const dot = document.getElementById('dot');
let currentPosition = 1;

function moveDot(position) {
    const squareWidth = document.querySelector('.square').offsetWidth;
    dot.style.left = squareWidth * (position - 1) + squareWidth / 2 - dot.offsetWidth / 2 + 'px';
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        currentPosition = Math.min(currentPosition + 1, 3); // ограничиваем до 3
    } else if (event.key === 'ArrowLeft') {
        currentPosition = Math.max(currentPosition - 1, 1); // ограничиваем до 1
    }
    moveDot(currentPosition);
});

// Инициализируем начальное положение точки
moveDot(currentPosition);
