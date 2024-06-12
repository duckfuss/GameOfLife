import random
import numpy as np
import pygame

WIDTH = 2000
HEIGHT = 1000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

colours = {
    "Dark0":(237,239,240),
    "Dark1":(225,226,227),
    "Dark2":(98,99,99)
}

class Grid():
    def __init__(self) -> None:
        self.cell_size = 10
        self.cell_padding = 1
        self.grid_width = int(WIDTH/(self.cell_padding+self.cell_size))
        self.grid_height = int(HEIGHT/(self.cell_padding+self.cell_size))
        self.grid = np.zeros((self.grid_width, self.grid_height), dtype=object)
        self.override_state = 'dead'
    def change_override_state(self):
        new_state = "alive"
        self.override_state = new_state
    def fill_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if x == 12 and y == 12:
                    self.grid[x][y] = Cell_Alive(self.cell_size, x, y, (self.cell_padding+self.cell_size))
                    print("Done")
                else:
                    self.grid[x][y] = Cell_Dead(self.cell_size, x, y, (self.cell_padding+self.cell_size))
    def update(self, mouse_pos=None, draw_only=True):
        new_grid = np.copy(self.grid)
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                cell = self.grid[x][y]
                if not draw_only:
                    new_grid = cell.update(self.grid, new_grid)
                if mouse_pos != None: #mouse click code
                    if mouse_pos[0]/(grid.cell_padding+grid.cell_size) >= x and mouse_pos[1]/(grid.cell_padding+grid.cell_size) >= y and mouse_pos[0]/(grid.cell_padding+grid.cell_size) <= x+(self.cell_size/(grid.cell_padding+grid.cell_size)) and mouse_pos[1]/(grid.cell_padding+grid.cell_size) <= y+self.cell_size/((grid.cell_padding+grid.cell_size)):
                        new_grid[x][y] = Cell_Alive(self.cell_size, x, y, (self.cell_padding+self.cell_size))
                cell.draw()
        self.grid = np.copy(new_grid)

class Cell():
    def __init__(self, w, x, y, padding, colour=(colours["Dark2"])) -> None:
        self.colour = colour
        self.width = w
        self.grid_coords = (x,y)
        self.rect = pygame.Rect(self.grid_coords[0]*padding, self.grid_coords[1]*padding, self.width, self.width)
        self.neighbours = {(1,0):"", (0,1):"", (1,1):"", (-1,0):"", (0,-1):"", (-1,-1):"", (-1,1):"", (1,-1):""}
    def find_neighbours(self, grid, search):
        neighbours = 0
        for neighbour in self.neighbours:
            if grid[self.grid_coords[0]+neighbour[0]][self.grid_coords[1]+neighbour[1]].type == search:
                neighbours += 1
                self.neighbours[neighbour] = search
        return neighbours
    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect)

class Cell_Dead(Cell):
    def __init__(self, w, x, y, padding) -> None:
        super().__init__(w, x, y, padding)
        self.type = "dead"
        self.p = padding
    def update(self, grid, new_grid):
        if self.grid_coords[0]+1 < len(grid) and self.grid_coords[1]+1 < len(grid[0]) and self.grid_coords[0]-1 > 0 and self.grid_coords[1]-1 > 0:
            #rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            if self.find_neighbours(grid, "alive") == 3:
                new_grid[self.grid_coords[0]][self.grid_coords[1]] = Cell_Alive(self.width, self.grid_coords[0], self.grid_coords[1], self.p)
        return new_grid

class Cell_Alive(Cell):
    def __init__(self, w, x, y, padding, colour=colours["Dark1"]) -> None:
        super().__init__(w, x, y, padding, colour)
        self.p = padding
        self.type = "alive"
    def update(self, grid, new_grid):
        # checks it is not going to call a cell off the edge
        if self.grid_coords[0]+1 < len(grid) and self.grid_coords[1]+1 < len(grid[0]) and self.grid_coords[0]-1 > 0 and self.grid_coords[1]-1 > 0:
            neighbours = self.find_neighbours(grid, "alive")
            #rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            if neighbours < 2:
                new_grid[self.grid_coords[0]][self.grid_coords[1]] = Cell_Dead(self.width, self.grid_coords[0], self.grid_coords[1], self.p)
            #rule 2: Any live cell with two or three live neighbours lives on to the next generation.
            #rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
            if neighbours > 3:
                new_grid[self.grid_coords[0]][self.grid_coords[1]] = Cell_Dead(self.width, self.grid_coords[0], self.grid_coords[1], self.p)
        return new_grid


grid = Grid()
grid.fill_grid()

tick = pygame.USEREVENT + 0
pygame.time.set_timer(tick, 100)

pause = 1
while True:
    screen.fill((0,0,0))
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                pause +=1
        if ev.type == pygame.MOUSEBUTTONDOWN:
            grid.update(mouse_pos=pygame.mouse.get_pos())
        if ev.type == tick and pause%2 == 0:
            grid.update(draw_only=False)
    grid.update()
    mouse_pos = pygame.mouse.get_pos()
    #print(mouse_pos[0]/(grid.cell_padding+grid.cell_size),mouse_pos[1]/grid.grid_height, grid.grid_height)
    pygame.display.update()
    clock.tick(120)