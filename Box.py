class Box:

    def __init__(self):
        self.lines = []
        # owner value is the player which one the box (1 for player1 and -1 for player2)
        self.owner = 0

    def set_lines(self, lines):
        self.lines = lines

    def get_owner(self):
        return self.owner

    def set_owner(self, player):
        if player == 1:
            self.owner = 1
        else:
            self.owner = -1
