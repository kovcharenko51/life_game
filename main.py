import pygame
from field import Field
from creature import Creature
import pickle
from copy import deepcopy


width = 720
height = 720
fps = 60
cell_color = (225, 8, 19)
grid_color = (138, 6, 12)
change_time = 150
alpha = 255
cell_size = 20
x_start_point = 0
y_start_point = 0

field = Field()


def main():
    global alpha
    global cell_size
    global x_start_point
    global y_start_point
    start_grid = {}

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Life Game")
    clock = pygame.time.Clock()

    change_generation_event = pygame.USEREVENT + 1
    pygame.time.set_timer(change_generation_event, change_time)

    started = False
    running = True

    mouse_creating = True

    while running:
        clock.tick(fps)

        screen.fill((0, 0, 0))
        surface = pygame.Surface((screen.get_width(), screen.get_height()))
        surface.set_alpha(alpha)
        for x in range(0, screen.get_height() // cell_size):
            pygame.draw.line(surface, grid_color, (0, x * cell_size), (screen.get_width(), x * cell_size), 2)
        for x in range(0, screen.get_width() // cell_size):
            pygame.draw.line(surface, grid_color, (x * cell_size, 0), (x * cell_size, screen.get_height()), 2)
        screen.blit(surface, (0, 0))
        if started:
            if alpha > 0:
                alpha -= 35
        elif alpha < 255:
            alpha += 35
        for x_pos in field.grid.keys():
            for y_pos in field.grid[x_pos].keys():
                pygame.draw.rect(screen, cell_color, (x_start_point + x_pos * cell_size,
                                                      y_start_point + y_pos * cell_size,
                                                      cell_size, cell_size))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                x_pos, y_pos = pygame.mouse.get_pos()
                creature = Creature((x_pos - x_start_point) // cell_size, (y_pos - y_start_point) // cell_size)
                click = pygame.mouse.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if field.check_creature(creature):
                        mouse_creating = False
                        field.kill(creature)
                    else:
                        mouse_creating = True
                        field.create(creature)
                elif click[0] and not started:
                    if mouse_creating:
                        field.create(creature)
                    elif not mouse_creating and field.check_creature(creature):
                        field.kill(creature)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_grid = deepcopy(field.grid)
                    started = True
                if event.key == pygame.K_LEFT:
                    x_start_point += cell_size
                if event.key == pygame.K_RIGHT:
                    x_start_point -= cell_size
                if event.key == pygame.K_UP:
                    y_start_point += cell_size
                if event.key == pygame.K_DOWN:
                    y_start_point -= cell_size
                if event.key == pygame.K_z:
                    if cell_size > 1:
                        cell_size -= 1
                if event.key == pygame.K_x:
                    cell_size += 1
                if event.key == pygame.K_DELETE:
                    field.grid = {}
                    if started:
                        started = False
                if event.key == pygame.K_s:
                    with open("save", "wb") as file:
                        pickle.dump(start_grid, file)
                if event.key == pygame.K_l and not started:
                    with open("save", "rb") as file:
                        field.grid = pickle.load(file)

            if event.type == change_generation_event and started:
                field.change_generation()

    pygame.quit()


if __name__ == '__main__':
    main()
