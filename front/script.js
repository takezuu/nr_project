const gameContainer = document.getElementById('game-container');
const winer = document.getElementById('win');
const page = document.querySelector('body');
let playerPosition = { x: 0, y: 0 }; 
let main_map;

// Функция для создания и отображения карты
function renderMap() {
    gameContainer.innerHTML = '';  // Очищаем контейнер
	gameContainer.style.gridTemplateColumns = `repeat(${main_map.length}, 50px)`;
	gameContainer.style.gridTemplateRows = `repeat(${main_map[0].length}, 50px)`;

    main_map.forEach(row => {
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
			  case 3:
				cellDiv.classList.add('exit');
				break;
			  default:
				cellDiv.classList.add('empty');
			}
			
            gameContainer.appendChild(cellDiv);
       
        });
    });
}

function movePlayer(newPosition)
{
	//index=row×num_columns+column
	var old_pos = playerPosition.y * main_map.length + playerPosition.x;
	var new_pos = newPosition.y *  main_map.length + newPosition.x;
	gameContainer[indx];
}

// Получение карты с сервера
async function getMap() {
    const response = await fetch('/map');
    const data = await response.json();
	main_map = data.map;
	playerPosition.y = data.playerPosition.y;
	playerPosition.x = data.playerPosition.x;
	renderMap(data.map);
	
}

// Отправка направления для перемещения игрока
async function sendMoveRequest() {
    const response = await fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playerPosition: playerPosition })
    });

    const data = await response.json();
    renderMap(data.map);// Обновляем карту с новыми позициями
	if (data.complete == 1)
	{
		page.style.backgroundImage = "url('static/bg2.jpg')"
		//alert("U found exit!");
		gameContainer.style.display = "none";
		winer.style.display = "contents";
	}
	//movePlayer(data.playerPosition);
	renderMap();
}

// Добавляем прослушивание нажатий клавиш для перемещения
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
		playerPosition.x+=1;
    } else if (event.key === 'ArrowLeft') {
        playerPosition.x-=1;
    } else if (event.key === 'ArrowUp') {
        playerPosition.y+=1;
    } else if (event.key === 'ArrowDown') {
        playerPosition.y-=1;
    }
	sendMoveRequest();
});

// Инициализируем карту при загрузке страницы
getMap();
