from creature import Creature


class Field:

    def __init__(self):
        self.grid = {}

    def create(self, creature: Creature) -> None:
        self.grid.setdefault(creature.x_pos, {})
        self.grid[creature.x_pos][creature.y_pos] = True

    def kill(self, creature: Creature) -> None:
        del self.grid[creature.x_pos][creature.y_pos]

    def check_creature(self, creature: Creature) -> bool:
        return self.grid.get(creature.x_pos, {}).get(creature.y_pos) is not None

    def get_neighbours(self, creature: Creature) -> list[Creature]:
        neighbours = []
        for creature in self.get_adj_cells(creature):
            if self.grid.get(creature.x_pos, {}).get(creature.y_pos) is not None:
                neighbours.append(Creature(creature.x_pos, creature.y_pos))
        return neighbours

    @staticmethod
    def get_adj_cells(creature) -> list[Creature]:
        cells = []
        for x_pos in range(creature.x_pos - 1, creature.x_pos + 2):
            for y_pos in range(creature.y_pos - 1, creature.y_pos + 2):
                if x_pos == creature.x_pos and y_pos == creature.y_pos:
                    continue
                cells.append(Creature(x_pos, y_pos))
        return cells

    def change_generation(self) -> None:
        possible_new_list = []
        creatures_to_kill = []
        creatures_to_create = []
        for x_pos in self.grid.keys():
            for y_pos in self.grid[x_pos].keys():
                creature = Creature(x_pos, y_pos)
                neighbours = self.get_neighbours(creature)
                possible_new_list += Field.get_adj_cells(creature)
                if len(neighbours) < 2 or len(neighbours) > 3:
                    creatures_to_kill.append(creature)
        for creature in possible_new_list:
            if self.grid.get(creature.x_pos, {}).get(creature.y_pos) is None:
                if len(self.get_neighbours(creature)) == 3:
                    creatures_to_create.append(creature)
        for creature in creatures_to_kill:
            self.kill(creature)
        for creature in creatures_to_create:
            self.create(creature)
