const dot = document.getElementById('dot');
let currentPosition = 3; // Начальная позиция в центре (позиция 3)

const positions = [
    { top: '16.66%', left: '50%' },  // Позиция 1 - Верхняя
    { top: '50%', left: '16.66%' },  // Позиция 2 - Левая
    { top: '50%', left: '50%' },     // Позиция 3 - Центральная
    { top: '50%', left: '83.33%' },  // Позиция 4 - Правая
    { top: '83.33%', left: '50%' },  // Позиция 5 - Нижняя
];

function moveDot(position) {
    dot.style.top = positions[position - 1].top;
    dot.style.left = positions[position - 1].left;
}

async function sendMoveRequest(direction) {
    try {
        const response = await fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                direction: direction,
                position: currentPosition
            })
        });

        const data = await response.json();
        if (data.position) {
            currentPosition = data.position;
            moveDot(currentPosition);
        } else {
            console.error('Server error:', data);
        }
    } catch (error) {
        console.error('Error sending move request:', error);
    }
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        sendMoveRequest('right');
    } else if (event.key === 'ArrowLeft') {
        sendMoveRequest('left');
    } else if (event.key === 'ArrowUp') {
        sendMoveRequest('up');
    } else if (event.key === 'ArrowDown') {
        sendMoveRequest('down');
    }
});

// Инициализируем точку в начальном положении
moveDot(currentPosition);
