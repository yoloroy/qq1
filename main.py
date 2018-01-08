import pygame
from random import choice, randint, random
from math import sin, pi, cos

pygame.init()
size = width, height = 1000, 540
screen = pygame.display.set_mode(size)
running = True
font = pygame.font.Font('Concib__.ttf', 15)

class Player: # for menu
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.cellscount = 0
        self.cells = []
        self.cash = 0
    
    def cell_amount(self):
        return self.cellscount
        #return len(self.cells)
    
    def info(self):
        return {'name': self.name, 'color': self.name}


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yes = 0
        self.player = -1
        #Player('Empty', (0, 0, 0))
        self.income = 3
        self.units = 0
        self.clicked = False
        self.direct = False

    def upgrade(self, x):
        if self.player!=-1:
            self.income=self.income+x
    
    def change_player(self, a):
        old=self.player
        if old!=-1:
            players[old].cellscount=players[old].cellscount-1
            players[a].cellscount=players[a].cellscount+1
        self.player = a
    
    def color(self):
        return 255 * self.income // 20
    
    def __str__(self):
        return str(self.income)
    
    def capture(self, another):  # self cell capture by another cell
        if playerS_turn == another.player:
            if self.units <= another.units and another.units > 0:
                if self.units < 1:
                    self.units = 1
                self.units = another.units - self.units
                another.units = 0
                self.change_player(another.player)
                return True
            else:
                self.units -= another.units
                another.units = 0
                return False
        else:
            return False
    
    def supply(self):
        return self.income * 3


class Button:
    def __init__(self, display, image, text, ox, oy, func, info = None, whois = 0, resolution = None):
        self.text = text   # must be rendered
        self.image = image # must be load or rendered
        self.ox = ox
        self.oy = oy
        self.resolution = resolution if resolution != None else self.image.get_size()
        self.width = self.resolution[0]
        self.height =  self.resolution[1]
        self.display = display
        self.function = func
        self.status = 0
        self.info = info
        self.whois = whois
    
    def click (self):
        global action 
        print (self.whois)
        if self.whois == 1:
            action='Capture'
        if self.whois == 2:
            action='Upgrade'
        if self.whois == 3:
            action='Downgrade'
        if self.whois == 4:
            action='End_turn'
    
    def draw(self):
        rx=0
        ry=0
        if self.status==1:
            rx=2
            ry=2
        if self.status==2:
            rx=-1

        self.display.blit(self.image, (self.ox+rx, self.oy+ry))
        screen.blit(self.text, (self.ox + 1+rx, self.oy + 1+ry))
    
    def call(self):
        x, y = pygame.mouse.get_pos()
        if self.ox > x > self.ox + self.resolution[0] and self.oy > x > self.oy + self.resolution[1]:
            return self()
        return False
    
    def __call__(self, *args):
        return (self.function+'('+''.join('{}' for i in range(len(args)))+')').format(args)


def find_point_on_circle(radius, gradus, ox, oy):
    ax = ox + radius*cos(gradus * pi / 180)
    ay = oy + radius*sin(gradus * pi / 180)
    
    return ax, ay

def check_pos(a, b):
    if a[0] in range(b[0][0], b[1][0]+1) and a[1] in range(b[0][1], b[1][1]+1):
        return True
    return False

#               tool tip missing
#for i in range(n):
#    players.append(Player(input('name: '), eval(input('tuple of color(RGB): '))))
players = [Player('Red', (255, 0, 0)), Player('Blue', (0, 0, 255))]#, Player('green', (0, 255, 0)), Player('white', (255, 255, 255)), Player('pink', (200, 50, 255)), Player('orange', (255, 150, 0))]
buttons = []
button_font = pygame.font.Font('Concib__.ttf', 15)
buttons.append(Button(screen, pygame.image.load('button_image.png'), button_font.render('Capture', 1, pygame.Color('#ffffff')), 600, 345, 'capture', "Capture",  1))
buttons.append(Button(screen, pygame.image.load('button_image.png'), button_font.render('Upgrade', 1, pygame.Color('#ffffff')), 600, 395, '', "Upgrade", 2))
buttons.append(Button(screen, pygame.image.load('button_image.png'), button_font.render('Downgrade', 1, pygame.Color('#ffffff')), 600, 445, '', "Downgrade", 3))
buttons.append(Button(screen, pygame.image.load('button_image.png'), button_font.render('End turn', 1, pygame.Color('#ffffff')), 600, 495, '', "End_turn", 4))

playerS_turn = 0
map_size = (9, 9)
cell_size = 60
grid_color = pygame.Color(255, 255, 255)
map_grid = [[Cell(i, j) for j in range(map_size[0])] for i in range(map_size[1])]

for j in range(map_size[0]):
    for i in range(map_size[1]):
        map_grid[i][j].x=j
        map_grid[i][j].y=i
        map_grid[i][j].player=-1
        
center = (map_size[0]//2, map_size[1]//2)
found = [-1, -1]
action=''
curuser=-1
curcell = 0
last4pos = (-1, -1)
last_click={'pos': [-1, -1], 'corr': False}


# standing players
n=len(players)
aaa=360//n
for i in range(n):
    #i = players[i].name
    x, y = find_point_on_circle(min(center) * 2 // 3, i * aaa,center[0], center[1])
    map_grid[int(y)][int(x)].change_player(i)
    map_grid[int(y)][int(x)].income = 5
    map_grid[int(y)][int(x)].units = 1

#players = [PlayerInfo(i) for i in players]

def end_turn():
    global playerS_turn, players
    for i in map_grid:
        for j in i:
            if j.player == playerS_turn:
                players[j.player].cash += j.income
    playerS_turn += 1
    if playerS_turn == len(players):
        playerS_turn =0

def draw_buttons():
    for b in buttons:
        b.draw()
        b.call()

def draw():
    screen.fill((0, 0, 0))
    draw_grid()
    draw_buttons()

def draw_cell(ob):
    x = ob.x * cell_size
    y = ob.y * cell_size
    num = ob.player
    if num == -1:
        pygame.draw.rect(screen, (0,0,0), (x, y, cell_size, cell_size))
    else:
        pl=players[num]
        pygame.draw.rect(screen, pl.color, (x, y, cell_size, cell_size))
        text = font.render(pl.name, 1, (255, 255, 255))
        screen.blit(text, (x+1, y+1))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1)

def draw_grid():
    for y in range(map_size[1]):
        for x in range(map_size[0]):
            draw_cell(map_grid[y][x])

def info():
    font_w = 25
    font = pygame.font.Font('Concib__.ttf', font_w)
    screen.blit(font.render('Turn of '+players[playerS_turn].name, 1, (255, 255, 255)), (cell_size * (map_size[0]+0.5), cell_size // 2))
    text = str((last_click['pos'][0], map_size[1] - 1 - last_click['pos'][1]))
    screen.blit(font.render(text, 1, (255, 255, 255)), (cell_size * (map_size[0]+0.5), cell_size//2 + font_w))
    text = 'income: '+str(map_grid[last_click['pos'][1]][last_click['pos'][0]].income)
    screen.blit(font.render(text, 1, (255, 255, 255)), (cell_size * (map_size[0]+0.5), cell_size//2 + font_w*2))
    text = 'units: '+str(map_grid[last_click['pos'][1]][last_click['pos'][0]].units)+'/'+str(map_grid[last_click['pos'][1]][last_click['pos'][0]].supply())
    screen.blit(font.render(text, 1, (255, 255, 255)), (cell_size * (map_size[0]+0.5), cell_size//2 + font_w*3))

    text = 'Action: '+str(action)
    screen.blit(font.render(text, 1, (255, 255, 255)), (cell_size * (map_size[0]+0.5), cell_size//2 + font_w*4))

def find_butt_found(xx):
    clicked=-1
    i=0
    for b in buttons:
        if (xx[0]>b.ox) and (xx[0]<(b.ox+b.width)) and (xx[1]>b.oy) and (xx[1]<(b.oy+b.height)):
            clicked=i
        i=i+1
    return clicked
        
        
def find_cell_found(xy):
    global found
    try:
        map_grid[found[0]][found[1]].direct = False
    except IndexError:
        pass
    
    try:
        map_grid[xy[0] // cell_size][xy[1] // cell_size].direct = True
        found = [xy[0] // cell_size, xy[1] // cell_size]
        return True
    except IndexError:
        return False 

def ColorNotError(err_color):
    for i in range(3):
        if err_color[i] > 255:
            err_color[i] = 255
        if err_color[i] < 0 :
            err_color[i] = 0
    return err_color

def draw_found(xy): # make transparent
    ox = xy[0] * cell_size
    oy = xy[1] * cell_size
    for y in range(cell_size):
        for x in range(cell_size):
            try:
                screen.set_at((ox+x, oy+y), screen.get_at((ox + x, oy + y)) + pygame.Color(100, 100, 100))
            except IndexError:
                return False


while running:
    for event in pygame.event.get():
        #print(event)
        if event.type == 12:
            running = False
            pygame.event.clear()
        if event.type == 5 and event.__dict__['button'] == 1:
            if last4pos == (-1, -1):
                last4pos = pygame.mouse.get_pos()
            else:
                if last4pos == pygame.mouse.get_pos():
                    map_grid[found[1]][found[0]].upgrade(1)
                    last4pos = (-1, -1)
                else:
                    last4pos = pygame.mouse.get_pos()
        if event.type == 5 and event.__dict__['button'] == 3:
            if last4pos == (-1, -1):
                last4pos = pygame.mouse.get_pos()
            else:
                if last4pos == pygame.mouse.get_pos():
                    map_grid[found[1]][found[0]].upgrade(-1)
                    last4pos = (-1, -1)
                else:
                    last4pos = pygame.mouse.get_pos()
    onbutton=find_butt_found(pygame.mouse.get_pos())
    i=0
    for b in buttons:
        if i!=onbutton:
            b.status=0
        i=i+1
    
    if onbutton>=0:
        if pygame.mouse.get_pressed()[0]:
            buttons[onbutton].status=1
        else:
            if buttons[onbutton].status==1:
                buttons[onbutton].click()
                print(buttons[onbutton].info)
            buttons[onbutton].status=2
    draw()
    
    if find_cell_found(pygame.mouse.get_pos()):
        draw_found(found)
        if pygame.mouse.get_pressed()[0]:
            last_click['pos'] = found
            if action=='':
                curuser=map_grid[found[1]][found[0]].player
                curcell=map_grid[found[1]][found[0]]
            if action=='Capture':
                map_grid[found[1]][found[0]].capture(curcell)
                action=''
            if action=='Upgrade':
                map_grid[found[1]][found[0]].upgrade(1)
                action=''
            if action=='Downgrade':
                map_grid[found[1]][found[0]].upgrade(-1)
                action=''
            if action=='End_turn':
                end_turn()
                action=''
    
    
    
    draw_found(last_click['pos'])
    info()
    pygame.display.flip()

pygame.quit()
