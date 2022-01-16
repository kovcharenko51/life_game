class Creature:

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def __hash__(self):
        return hash(self.x_pos) ^ hash(self.y_pos)

    def __eq__(self, other):
        return (self.x_pos == other.x_pos) and (self.y_pos == other.y_pos)