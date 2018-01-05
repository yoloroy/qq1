import pygame
from random import choice, randint, random
from math import sin, pi, cos

pygame.init()
size = width, height = 750, 750
screen = pygame.display.set_mode(size)
running = True
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yes = 0
        self.player = Player('Empty', (55, 55, 55))
        self.supply = 20
        self.units = 0
        self.income = randint(1,5)
    
    def change_player(self, a):
        self.player = a
    
    def color(self):
        return (255 * self.income // 20, 215 * self.income // 20, 0)
    
    def __str__(self):
        return str(self.income)


players = []

def find_point_on_circle(radius, gradus, ox, oy):
    ax = ox + radius * cos(gradus * pi / 180)
    ay = oy + radius * sin(gradus * pi / 180)
    
    return ax, ay

# tool tip missing
#for i in range(n):
#    players.append(Player(input('name: '), eval(input('tuple of color(RGB): '))))
players = [Player('red',(255, 0, 0)), Player('green', (0, 255, 0)), Player('blue', (0, 0, 255))]


cell_size = 50
map_size = (width//cell_size, height//cell_size)
grid_color = pygame.Color(255, 255, 255)
map_grid = [[Cell(i, j) for j in range(map_size[0])] for i in range(map_size[1])]
center = (map_size[0]//2, map_size[1]//2)


# broken
n=len(players)
aaa=360//n
for i in range(n):
    x,y=find_point_on_circle(min(center)-4,i*aaa,center[0],center[1])
    map_grid[int(y)][int(x)].change_player(players.pop())
    map_grid[int(y)][int(x)].income=5


def draw():
    screen.fill((0, 0, 0))
    draw_grid()
    
def fill_quad(x1, y1, x2, y2, col):
    for y in range(y1, y2):
        for x in range(x1, x2):
            screen.set_at((x, y), col)

def draw_cell(num_x, num_y, ob):
    x = num_x * cell_size
    y = num_y * cell_size
    pygame.draw.rect(screen, ob.player.color, (x, y, cell_size, cell_size // 2))
    #except: pass
    pygame.draw.rect(screen, ob.color(), (x, y + cell_size // 2, cell_size, cell_size // 2))
    font = pygame.font.Font(None, cell_size//2)
    text = font.render(str(ob), 1, (255, 255, 255))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size,  cell_size), 1)
    screen.blit(text, (x+1, y+1+cell_size // 2))

def draw_grid():
    for y in range(map_size[1]):
        for x in range(map_size[0]):
            draw_cell(x, y, map_grid[y][x])


draw_grid()
pygame.display.flip()

while running:
    if pygame.event.wait().type == pygame.QUIT:
        running = False

pygame.quit()
