import pygame
import random

pygame.init()
size = width, height = 1940, 1024
screen = pygame.display.set_mode(size)
running = True

class Player:
    def __init__(s, name, color):
        s.name = name
        s.color = color


class Cell:
    def __init__(self, x, y, p = None):
        self.x = x
        self.y = y
        self.player = p
        self.supply = 20
        self.units = 0
        self.income = random.randint(0,10)
    
    def change_player(s, a):
        s.player = a
    
    def color(s):
        return (255 * (10 - s.income) // 10, 255 * s.income // 10, 0)
    
    def __str__(s):
        return str(s.income)


players = []

def find_point_on_circle(radius, gradus, ox, oy):
    import math
    
    radius = float(input())
    gradus = float(input())
    ox = float(input())
    oy = float(input())
    ax = ox + radius * math.sin((90 - gradus) * math.pi / 180)
    ay = oy + radius * math.sin(gradus * math.pi / 180)

# это для начала
#for i in range(n):
#    players.append(Player(input('name: '), eval(input('tuple of color(RGB): '))))
players = [Player('red',(255, 0, 0)), Player('green', (0, 255, 0)), Player('blue', (0, 0, 255))]
# потом исправь!


cell_size = 50
map_size = (width//cell_size, height//cell_size)
grid_color = pygame.Color(255, 255, 255)
map_grid = [[Cell(i, j) for j in range(map_size[0])] for i in range(map_size[1])]
center = (map_size[0]//2, map_size[1]//2)


#совсем халтурный кусок
n=len(players)
aaa=360//n
for i in range(n):
    x,y=find_point_on_circle(min(center),i*aaa,center[0],center[1])
    map_grid[int(x)][int(y)]=players.pop()
del aaa, x, y


def draw():
    screen.fill((0, 0, 0))
    draw_grid()

def fill_quad(x1, y1, x2, y2, ob):
    for y in range(y1, y2):
        for x in range(x1, x2):
            screen.set_at((x, y), ob.color())

def draw_cell(num_x, num_y, ob):
    x = num_x * cell_size
    y = num_y * cell_size
    fill_quad(x, y, x+cell_size, y+cell_size//2, ob)
    font = pygame.font.Font(None, cell_size//2)
    text = font.render(str(ob), 1, (255, 255, 255))
    screen.blit(text, (x+1, y+1))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size,  cell_size), 1)

def draw_grid():
    for y in range(map_size[1]+1):
        for x in range(map_size[0]+1):
            try:
                draw_cell(x, y, map_grid[y][x])
            except IndexError:
                pass

draw_grid()
pygame.display.flip()

while running:
    if pygame.event.wait().type == pygame.QUIT:
        running = False

pygame.quit()