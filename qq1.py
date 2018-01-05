import pygame
from random import choice, randint, random
from math import sin, pi, cos

pygame.init()
size = width, height = 1000, 540
screen = pygame.display.set_mode(size)
running = True
font = pygame.font.Font('Concib__.ttf', 15)


class Player: # for cell
    def __init__(self, name, color):
        self.name = name
        self.color = color


class PlayerInfo: # for menu
    def __init__(self, player):
        self.name = player.name
        self.color = player.color
    
    def info(self): pass #


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yes = 0
        self.player = Player('Empty', (0, 0, 0))
        self.supply = 20
        self.units = 0
        self.income = 3
        self.army = self.income - 2
        self.clicked = False
    
    def change_player(self, a):
        self.player = a
    
    def color(self):
        return 255 * self.income // 20
    
    def __str__(self):
        return str(self.income)
    
    def capture(self_cell, another_cell):  # self_cell capture by another_cell
        n = 0
        for i in range(3):
            another_boost = randint(-1,1)
            self_boost    = randint(-1,1)
            if self_cell.units + self_boost < another_cell.units + another_boost:
                n += 1
        if n >= 2:
            self_cell.units = another_cell.units - self_cell.units
            if self_cell.units <= 0:
                self_cell.units = 1
            self_cell.income -= another_cell.units
            self_cell.change_player(another_cell.player)
            return True
        else:
            self_cell.units = self_cell.units - another_cell.units
            another_cell.units = another_cell.units - self_cell.units
            if self_cell.units <= 0:
                self_cell.units = 1
            if another_cell.units <= 0:
                another_cell.units = 1
            self_cell.income -= 1
            return False


class Button:
    def __init__(self, display, image, text, ox, oy, func, info = None, resolution = None):
        self.text = text   # must be rendered
        self.image = image # must be rendered
        self.ox = ox
        self.oy = oy
        self.display = display
        self.function = func
        self.resolution = resolution if resolution != None else self.image.get_size()
    
    def draw(self):
        self.display.blit(self.image, (self.ox, self.oy))
        self.display.blit(pygame.transform.scale(self.text), (self.ox, self.oy))
    
    def __call__(self, *args):
        self.function(args)


def find_point_on_circle(radius, gradus, ox, oy):
    ax = ox + radius*cos(gradus * pi / 180)
    ay = oy + radius*sin(gradus * pi / 180)
    
    return ax, ay

#               tool tip missing
#for i in range(n):
#    players.append(Player(input('name: '), eval(input('tuple of color(RGB): '))))
players = [Player('Red',(255, 0, 0)), Player('Blue', (0, 0, 255))]#, Player('green', (0, 255, 0)), Player('white', (255, 255, 255)), Player('pink', (200, 50, 255)), Player('orange', (255, 150, 0))]


playerS_turn = 0
cell_size = 60
map_size = (9, 9)
grid_color = pygame.Color(255, 255, 255)
map_grid = [[Cell(i, j) for j in range(map_size[0])] for i in range(map_size[1])]
center = (map_size[0]//2, map_size[1]//2)


# standing players
n=len(players)
aaa=360//n
for i in range(n):
    x, y = find_point_on_circle(min(center)//2, i * aaa,center[0], center[1])
    map_grid[int(y)][int(x)].change_player(players[i])
    map_grid[int(y)][int(x)].income = 5


# drawing
def draw():
    screen.fill((0, 0, 0))
    draw_grid()

def draw_cell(num_x, num_y, ob):
    x = num_x * cell_size
    y = num_y * cell_size
    
    pygame.draw.rect(screen, ob.player.color, (x, y, cell_size, cell_size // 2))
    #pygame.draw.circle(screen, ob.player.color, (x + cell_size//2, y + cell_size//2), cell_size // 2)
    text = font.render(str(ob.player.name), 1, (255, 255, 255))
    screen.blit(text, (x+1, y+1))
    
    #pygame.draw.rect(screen, ob.color(), (x, y + cell_size // 2, cell_size, cell_size // 2))
    
    #screen.blit(pygame.image.load('circle(d).png'),(x, y))
    #dhoc = pygame.image.load('circle(g).png')
    #dhoc.set_alpha(ob.color())
    
    #screen.blit(dhoc,(x, y))
    #text = font.render('income: '+str(ob), 1, (255, 255, 255))
    #screen.blit(text, (x+1, y+1+cell_size // 2))
    #rect=(x,y,cell_size,cell_size)
    
    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1)

def draw_grid():
    for y in range(map_size[1]):
        for x in range(map_size[0]):
            draw_cell(x, y, map_grid[y][x])

def info():
    font = pygame.font.Font('Concib__.ttf', 25)
    screen.blit(font.render('Turn of '+players[playerS_turn].name, 1, (255, 255, 255)), (cell_size * (map_size[0]+0.5), cell_size // 2))
    


while running:
    draw_grid()
    info()
    pygame.display.flip()
    if pygame.event.wait().type == pygame.QUIT:
        running = False

pygame.quit()
