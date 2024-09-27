 const dot = document.getElementById('dot');
        let currentPosition = 1;

        function moveDot(position) {
            const squareWidth = document.querySelector('.square').offsetWidth;
            dot.style.left = squareWidth * (position - 1) + squareWidth / 2 - dot.offsetWidth / 2 + 'px';
        }

		async function sendMoveRequest(direction) {
			try {
				console.log('Sending request with direction:', direction, 'and position:', currentPosition);  // Добавляем лог до запроса
				
				const response = await fetch('/move', {  // Убедитесь, что правильный путь
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ direction: direction, position: currentPosition })
				});

				// Проверим статус ответа
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				const data = await response.json();
				console.log('Response data:', data);  // Логируем данные ответа

				if (data.position) {
					currentPosition = data.position;
					moveDot(currentPosition);
				} else if (data.error) {
					console.error('Server error:', data.error);
				}
			} catch (error) {
				console.error('Error moving dot:', error);
			}
		}


        document.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowRight') {
                sendMoveRequest('right');
            } else if (event.key === 'ArrowLeft') {
                sendMoveRequest('left');
            }
        });

        // Инициализируем начальное положение точки
        moveDot(currentPosition);