const gameBoard = document.getElementById('gameBoard');
const win = document.getElementById('win');
const page = document.querySelector('body');


let gameMap = [0,0]; 
let cellSize = 24; // Размер клетки (в пикселях)
let playerPosition = { row: null, col: null };
let prevPosition = { row: null, col: null };
let exitPosition = { row: null, col: null };
let exitEnabled = false;
// Функция для создания игрового поля
function createGameBoard(cellSize) {
    // Очищаем поле перед пересозданием
	gameBoard.innerHTML = '';
    var columns = gameMap[0].length;
	var rows = gameMap.length; 
    // Устанавливаем размер контейнера под количество колонок и строк
    gameBoard.style.width = `${columns * cellSize}px`;
    gameBoard.style.height = `${rows * cellSize}px`;

    // Генерация клеток
    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < columns; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.style.width = `${cellSize}px`;
            cell.style.height = `${cellSize}px`;
            
			switch (gameMap[row][col])
			{
				case 1:
					cell.classList.add('active');
					break;
				case 2:
					cell.classList.add('player');
					playerPosition.row = row;
					playerPosition.col = col;
					break;
				case 3:
					if (exitEnabled){
						cell.classList.add('exit');
					}
					else {
						cell.classList.add('exitdisabled');
					}
					exitPosition.row = row;
					exitPosition.col = col;
					break;
				case 4:
				    cell.classList.add('falseCell');
				    break;
				case 5:
				    cell.classList.add('item');
				    break;
				
			}
			cell.addEventListener('click', () => moveHandler(row, col));
            gameBoard.appendChild(cell);
        }
    }
}

async function moveHandler(row, col) {

	if (gameMap[row][col] == 1 || gameMap[row][col] == 3 || gameMap[row][col] == 5){
		// Делаем кликнутую клетку активной
		var check = await sendMoveRequest(col, row);
		if (check == true){
			gameMap[prevPosition.row][prevPosition.col] = 1;
			var vic = gameMap[row][col] == 3
			gameMap[row][col] = 2;
			// Обновляем активную клетку
			playerPosition = { row, col };
			// Перерисовываем поле с обновленным массивом
			createGameBoard(cellSize);
			if (vic) {
				//await sendMoveRequest(col, row);
				displayVictoryScreen();
				setTimeout(() => {	getMap('/remap'); }, 5000);
			}
		}
	}
	
	
}

function displayVictoryScreen() {
    // Скрываем игровое поле
	exitEnabled = false;
    gameBoard.style.display = 'none';

    // Создаем контейнер для победного экрана
    const victoryScreen = document.createElement('div');
    victoryScreen.id = 'victoryScreen';

    // Добавляем изображение и текст
    const victoryImage = document.createElement('img');
    victoryImage.src = '/static/bg2.jpg'; // Укажите путь к изображению
    const victoryText = document.createElement('h1');
    victoryText.textContent = 'You won this round!!!\r\nNew map loading...';

    victoryScreen.appendChild(victoryImage);
    victoryScreen.appendChild(victoryText);

	victoryScreen.style.width = gameBoard.style.width;
    victoryScreen.style.height = gameBoard.style.height;
    // Добавляем победный экран в документ
    document.body.appendChild(victoryScreen);

    // Отображаем победный экран
    victoryScreen.style.display = 'block';
}


document.addEventListener('keydown', (event) => {
	
	prevPosition = playerPosition;
	var row =  playerPosition.row;
	var col  =  playerPosition.col;
	if (event.key === 'ArrowRight') {
		col+=1;
	} else if (event.key === 'ArrowLeft') {
		col-=1;
	} else if (event.key === 'ArrowUp') {
		row-=1;
	} else if (event.key === 'ArrowDown') {
		row+=1;
	}
	
	moveHandler(row, col);
	 
	
});


async function getMap(url) {
    const response = await fetch(url);
    const data = await response.json();
	gameMap = data.map;
	playerPosition = data.playerPosition;
	createGameBoard(cellSize);
	gameBoard.style.display = 'flex';
	victoryScreen.style.display = 'none';
	victoryScreen.remove();
}


async function sendMoveRequest(col, row) {
	//return !false;  // заглушка 
    const response = await fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"col": col, "row": row})
    });

    const data = await response.json();
	//main_map = data.map;
  	playerPosition = data.playerPosition;
	exitEnabled = data.exitEnabled;
	return data.moveForward;
}

getMap('/map');


 