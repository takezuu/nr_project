# Maze Game API

A web-based maze game where players navigate through a dynamically generated maze, collect items, and aim for the exit. The game interacts with players via an API built with FastAPI.

## Features

- **Dynamic Maze Generation**: The maze, including paths, items, and the exit, is generated randomly.
- **Player Movement**: The player can move through the maze via API requests.
- **RESTful API**: Built using FastAPI, which allows interaction with the game through various endpoints.
- **Item Collection & Exit Conditions**: Players can collect items and must find their way to the exit to win.
- **Logging & Map Visualization**: Logs the gameplay and provides a visual representation of the maze.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **Pydantic**: Data validation and settings management.
- **Starlette**: Handling static files.
- **Random**: Randomly generating maze elements, player positions, and other elements.

## API Endpoints

### 1. `GET /`

- **Description**: Returns the home page of the game.
- **Response**: A basic home page or welcome message.

### 2. `GET /favicon.ico`

- **Description**: Returns the favicon for the game.
- **Response**: The favicon image.

### 3. `GET /map`

- **Description**: Retrieves the current map and player’s position.
- **Response**: A JSON response containing:
  - The current maze layout.
  - The player's current position in the maze.

### 4. `GET /remap`

- **Description**: Generates and returns a new maze. The current game must be completed before a new one can be started.
- **Response**: A new generated maze with the player's position and item locations.

### 5. `POST /move`

- **Description**: Moves the player within the maze based on the specified coordinates.
- **Request Body (JSON)**:
  ```json
  {
    "row": <int>,
    "col": <int>
  }
Response (JSON):
json
Copy code
{
  "player_position": {
    "row": <int>,
    "col": <int>
  },
  "move_successful": <bool>,
  "game_completed": <bool>
}
player_position: The updated position of the player.
move_successful: Whether the move was successful or not.
game_completed: Whether the player has reached the exit and won the game.
