import pygame, sys
from pygame.locals import *
import random
pygame.init()
pygame.font.init()

w_width=600
w_height=600
window=pygame.display.set_mode((w_width, w_height))


#this function displays the number of adjacent mines on the box after it is clicked
def shownum(rect, num):
    if num > 0:
        text = basicfont.render(str(num), False, (0,0,0), (120,120,120))
    else:
        text = basicfont.render("", False, (0,0,0), (120,120,120))
    text = pygame.transform.scale(text, (20,20))
    window.blit(text, rect)

#this function decides how much of the board to reveal after a click 
def reveal(x, y):
    if not revealed[x][y]:
        revealed[x][y] = True 
        if adjmines[x][y] == 0:
            shownum(grid[x][y], -1)
            for p in range (-1, 2):
                for q in range(-1, 2):
                    checkx = x + p
                    checky = y + q
                    if 0 <= checkx <= 9 and 0 <= checky <= 9 and not hasmine[checkx][checky]:
                        reveal(checkx, checky)
                    
        else:
            shownum(grid[x][y], adjmines[x][y])         
        

#defining variables
black=(0,0,0)
white=(255,255,255)
blue=(0,0,255)  
basicfont = pygame.font.SysFont(None,48)
flagfont = pygame.font.SysFont(None, 24)
pygame.display.set_caption('Minesweeper')
flags = 10
marked = 0 


lose = basicfont.render("Game Over!", True, (0,0,0))
loserect=lose.get_rect()
loserect.topleft=(400, 200)

win = basicfont.render("You win!", True, (0,0,0))
winrect = win.get_rect()
winrect.topleft = (400,200)

flagtext = flagfont.render("Flags Remaining: " + str(flags), True, (0,0,0))
flagrect = flagtext.get_rect()
flagrect.topleft = (400,100)

smallback=pygame.Surface((161, 17)).convert()
smallback.fill(white)


#set up window
background=pygame.Surface((w_width, w_height)).convert()
background.fill(white)
window.blit(background, (0,0))
box=pygame.Surface((20,20)).convert()
box.fill(blue)

#set up pictures
bomb=pygame.image.load('bomb.png').convert()
bomb=pygame.transform.scale(bomb, (20,20))
flag = pygame.image.load('flag.png').convert()
flag = pygame.transform.scale(flag, (20,20))


#create and fill lists/arrays
grid=[[0 for x in xrange(10)] for y in xrange(10)]
hasmine=[[False for x in xrange(10)] for y in xrange(10)]
adjmines=[[0 for x in xrange(10)] for y in xrange(10)]
revealed = [[False for x in xrange(10)] for y in xrange(10)]
flagged = [[False for x in xrange(10)] for y in xrange(10)]
mines=[]

for x in xrange(10):
    while 1:
        num1 = random.randrange(0,10)
        num2 = random.randrange(0,10)
        if hasmine[num1][num2] == False:
            hasmine[num1][num2] = True
            break

#create 2d grid array or box rects and blit each box
for x in xrange(10):
    for y in xrange(10):
        grid[x][y]=(pygame.Rect((100+5*x)+20*x, (100+5*y)+20*y, 20, 20))
        window.blit(box, grid[x][y])
    
# NOTE : THE GRID IS SUCH THAT THE X REPRESENTS THE NUMBER OF COLUMNS TO THE RIGHT, AND Y REPRESENTS THE NUMBER OF ROWS DOWN


#create a separate list of rects that represent the boxes with mines
for x in xrange(10):
    for y in xrange(10):
        if hasmine[x][y]:
            mines.append([grid[x][y], x, y])

#set the number of adjacent mines for each box on the grid
for i in mines:
    for x in range(-1,2):
        for y in range(-1,2):
            checkx = i[1] + x
            checky = i[2] + y
            if 0 <= checkx <= 9 and 0 <= checky <= 9 and not hasmine[checkx][checky]:
                adjmines[checkx][checky] += 1
                                                 
pygame.display.update()

#main loop
while 1:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()


        #if they left click on a box
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                
                #check if they clicked a mine
                for mine in mines:
                    if mine[0].collidepoint(pygame.mouse.get_pos()) and not flagged[mine[1]][mine[2]]:
                        for x in mines:
                            window.blit(bomb, x[0])
                            
                        window.blit(lose, loserect)
                        pygame.display.update()
                        pygame.time.wait(5000)
                        pygame.quit()
                        sys.exit() 
                        
                
                for x in xrange(10):
                    for y in xrange(10):
                        
                        #finds which box they clicked
                        if grid[x][y].collidepoint(pygame.mouse.get_pos()):
                            
                            #if they clicked an unflagged, normal box
                            if not flagged[x][y]:
                                reveal(x,y)
                                
                            #if they are left clicking a flagged box to get rid of a flag
                            elif flagged[x][y]:
                                flagged[x][y] = False
                                flags += 1
                                marked -= 1
                                window.blit(box, grid[x][y])
                                flagtext = flagfont.render("Flags Remaining: " + str(flags), True, (0,0,0))
                                window.blit(smallback, flagrect)
                                window.blit(flagtext, flagrect) 
            
            #if they right clicked a square
            elif event.button == 3:
                for x in xrange(10):
                    for y in xrange(10):
                        if grid[x][y].collidepoint(pygame.mouse.get_pos()) and not revealed[x][y] and not flagged[x][y] and flags > 0:
                            
                            #blits the flag to the box
                            window.blit(flag, grid[x][y])
                            flags -= 1
                            if hasmine[x][y]:
                                marked += 1
                            flagged[x][y] = True
                            flagtext = flagfont.render("Flags Remaining: " + str(flags), True, (0,0,0))
                            window.blit(smallback, flagrect)
                            window.blit(flagtext, flagrect)
                            #checks for win
                            if flags == 0 and marked == 10:
                                window.blit(win, winrect)
                                pygame.time.wait(2000)
                                pygame.quit()
                                sys.exit()  
                                
    pygame.display.update()