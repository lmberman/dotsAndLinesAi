class Box:

    box_id = -1

    def __init__(self, box_id):
        self.lines = []
        # owner value is the player which one the box (1 for player1 and -1 for player2)
        self.owner = 0
        self.box_id = box_id

    def set_lines(self, lines):
        self.lines = lines

    def get_owner(self):
        return self.owner

    def set_owner(self, player):
        self.owner = player

    def update_line(self, new_line):
        for i in range(len(self.lines)):
            if self.lines[i].array_index == new_line.array_index:
                self.lines[i] = new_line

    def is_complete(self):
        for line in self.lines:
            if not line.drawn:
                return False
