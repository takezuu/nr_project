const gameContainer = document.getElementById('game-container');

// Функция для создания и отображения карты
function renderMap(gameMap) {
    gameContainer.innerHTML = '';  // Очищаем контейнер
	
	// Высота двумерного массива (количество строк)
	const height = array.length;

	// Ширина двумерного массива (количество элементов в первой строке)
	const width = array[0].length;
	gameContainer.style.gridTemplateColumns = 'repeat('  + gameMap.length +', 50px)';
	gameContainer.style.gridTemplateRows = 'repeat('  + gameMap[0].length +', 50px)';
 
    gameMap.forEach(row => {
        row.forEach(cell => {
            const cellDiv = document.createElement('div');
            cellDiv.classList.add('cell');
          			
			switch(cell) {
			  case 1:
				cellDiv.classList.add('filed');
				break;
			  case 2:
				cellDiv.classList.add('player');
				break;
			  case 3
				cellDiv.classList.add('exit');
				break;
			  default:
				cellDiv.classList.add('empty');
			}
			
            gameContainer.appendChild(cellDiv);
        });
    });
}

// Получение карты с сервера
async function getMap() {
    const response = await fetch('/map');
    const data = await response.json();
	renderMap(data.map);
	if (data.complite == 1)
		alert("U found exit!");
}

// Отправка направления для перемещения игрока
async function sendMoveRequest(direction) {
    const response = await fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction: direction })
    });

    const data = await response.json();
    renderMap(data.map);  // Обновляем карту с новыми позициями
}

// Добавляем прослушивание нажатий клавиш для перемещения
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

// Инициализируем карту при загрузке страницы
getMap();
