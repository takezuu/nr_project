class Player:

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def get_player_position(self):
        return {"y": self.y, "x": self.x}
