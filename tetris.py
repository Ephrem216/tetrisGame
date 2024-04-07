import pygame,sys,random,time
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 720
WINDOWHEIGHT = 1555
BOXSIZE = 55
BOARDWIDTH = 12
BOARDHEIGHT = 24
BOARDX = BOXSIZE * BOARDWIDTH
BOARDY = BOXSIZE * (BOARDHEIGHT - 4)
TIMEOUT = 0.3
CLICKTIMEOUT = 0.01
 
BLUE =                        (  60,   60,195)
GREEN =                     (   60,195,   60)
YELLOW =                  (195,195,   60)
RED =                           (195,   60,  60)
TEAL =                        (      0,100,100)
ORANGE =                  (195,128,   60)
AQUA =                       (    60,195,195)
BLACK =                     (      0,     0,     0)
WHITE =                      (255,255,255)
PURPLE =                    (128,    60,128)
FUCHSIA =                 (195,   60,195)
MAROON =                 (128,    60,   60)
NAVYBLUE =              (   60,    60,128)
OLIVE =                        ( 128, 128,  60)
SILVER =                      (192, 192, 192)
DARKTURQUOISE=   (    0,   50,    70)
GRAY =                         (128, 128, 128)
LIGHTRED =                (255,      0,      0)

WORKSPACECOLOR = DARKTURQUOISE
BGCOLOR = TEAL
BOARDERCOLOR = NAVYBLUE

T   = 'T'
S   = 'S'
Z   = 'Z'
J   = 'J'
L   = 'L'
I    = 'I'
O  = 'O'
P  = 'P'
Q  = 'Q'
M = 'M'
N  = 'N'
F   = 'F'
R = 'R'
H = 'H'
W = 'W'
C = 'C'
D = 'D'
E = 'E'
G = 'G'

LEFT     =      'left'
RIGHT   =       'right'
DOWN  =       'down'

XMARGIN = int((WINDOWWIDTH - BOARDX) / 2)

XEDGE = XMARGIN + BOXSIZE * BOARDWIDTH


def main():
	global FPSCLOCK,DISPLAYSURF , boardColor, color, difficulty, playSound, playMusic
	
	pygame.init()
	
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('Tetris')
	FPSCLOCK = pygame.time.Clock()
	
	color = {T : RED, R : RED, H : RED, W : RED, C: YELLOW, D : YELLOW , E : FUCHSIA , G : FUCHSIA, I : GREEN, O : BLUE, P : YELLOW, Q : FUCHSIA, S : ORANGE, J : YELLOW, L : FUCHSIA, Z : AQUA, N : AQUA, M : GREEN, F : ORANGE}
	
	difficulty = 'Medium'
	playSound = True
	playMusic = True
	while True:
		displayHomeScreen()


def runGame():
	global boardColor
	if difficulty == 'Easy':
		FPS = 3
	elif difficulty == 'Medium':
		FPS = 5
	elif difficulty == 'Hard':
		FPS = 9
	boardColor = getStartingBoardColor()
	middlex = int(BOARDWIDTH / 2)
	bottomYCoord = 3
	upcomingShape = getRandomShape()
	currentShape = getRandomShape()
	leftRect = pygame.Rect(0, 4 * BOXSIZE,int(WINDOWWIDTH / 2),BOARDY)
	rightRect = pygame.Rect(int(WINDOWWIDTH / 2),4 * BOXSIZE,int(WINDOWWIDTH / 2),BOARDY)
	downRect =pygame.Rect(100,1350, 200, 200)
	rotateRect = pygame.Rect(500 - 90, 1430 - 90, 180, 180)
	settingRect = pygame.Rect(530, 50, 140, 140)
	oldBest = getBestScore(0)
	newBest = False
	called = False
	isFirstLandTime = True
	downButtonIsClicked = False
	warningSignal = False
	score = 0
	on = True
	r, g, b = BGCOLOR
	touched = False
	leftButtonIsPressedDown = False
	rightButtonIsPressedDown = False
	downButtonIsPressedDown = False
	rotateButtonIsPressedDown = False
	while True:
		drawBoard()
		drawBoardColors()
		drawShape(currentShape, middlex, bottomYCoord)
		orginalSurface = DISPLAYSURF.copy()
		drawQuickTools(upcomingShape, score)
		if warningSignal:
			r, g, b, on = displayWarningAnimation(r, g, b, on)
		if score > oldBest and not called:
			newBest = True
			called = True
			newBestAnimation(150, score)
			DISPLAYSURF.blit(orginalSurface, (0, 0))
			pygame.display.update()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				touched = False
				leftButtonIsPressedDown = False
				rightButtonIsPressedDown = False
				downButtonIsPressedDown = False
				rotateButtonIsPressedDown = False
				if leftRect.collidepoint(event.pos):
					if isValidMove(currentShape, LEFT,middlex, bottomYCoord):
						middlex -= 1
				elif rightRect.collidepoint(event.pos):
					if isValidMove(currentShape, RIGHT,middlex, bottomYCoord):
						middlex += 1
				elif downRect.collidepoint(event.pos):
					downButtonIsClicked = True
					drawDownButton(SILVER)
					pygame.display.update()
					while isValidMove(currentShape, DOWN,middlex, bottomYCoord):
						bottomYCoord += 1
				elif rotateRect.collidepoint(event.pos):
					drawRotateButton(WHITE)
					pygame.display.update()
					currentShape, middlex, bottomYCoord = getRotatedShape(currentShape, middlex, bottomYCoord)
				elif settingRect.collidepoint(event.pos):
					drawSettingButton(WHITE)
					pygame.display.update()
					pygame.time.wait(300)
					drawSettingButton(SILVER)
					
					difficultyBeforeCall = difficulty
					drawSettingWindow()
					if difficulty != difficultyBeforeCall:
						runGame()
			elif event.type == MOUSEBUTTONDOWN:
				touched = True
				lastClickTime = time.time()
				if leftRect.collidepoint(event.pos):
					leftButtonIsPressedDown = True
				elif rightRect.collidepoint(event.pos):
					rightButtonIsPressedDown = True
				elif downRect.collidepoint(event.pos):
					downButtonIsPressedDown = True
				elif rotateRect.collidepoint(event.pos):
					rotateButtonIsPressedDown = True
		if touched and (time.time() - lastClickTime >=  CLICKTIMEOUT):
			if leftButtonIsPressedDown:
				if isValidMove(currentShape, LEFT,middlex, bottomYCoord):
					middlex -= 1
			elif rightButtonIsPressedDown:
				if isValidMove(currentShape, RIGHT,middlex, bottomYCoord):
					middlex += 1
			elif downButtonIsPressedDown:
				downButtonIsClicked = True
				drawDownButton(SILVER)
				pygame.display.update()
				while isValidMove(currentShape, DOWN,middlex, bottomYCoord):
					bottomYCoord += 1
			elif rotateButtonIsPressedDown:
				drawRotateButton(WHITE)
				pygame.display.update()
				currentShape, middlex, bottomYCoord = getRotatedShape(currentShape, middlex, bottomYCoord)
						
		if isValidMove(currentShape, DOWN, middlex, bottomYCoord):
			bottomYCoord += 1
		else:
			if isFirstLandTime:
				landTime = time.time()
				isFirstLandTime = False
			if downButtonIsClicked or time.time() - landTime >= TIMEOUT:		
				if bottomYCoord == 3:
					if newBest:
						drawBoard()
						drawBoardColors()
						drawShape(currentShape, middlex, bottomYCoord)
						drawQuickTools(upcomingShape, score)
						newBestAnimation(500, score)
					else:
						displayGameOverScreen(score)
				updateBoardColors(currentShape, middlex, bottomYCoord)
				bottomYCoord = 3
				middlex = int(BOARDWIDTH / 2)
				currentShape = upcomingShape
				upcomingShape = getRandomShape()
				isFirstLandTime  = True
				downButtonIsClicked = False
	
		score = checkIfAnyRowIsFull(score, upcomingShape)
		warningSignal = False
		for y in range(11):
			for x in range(BOARDWIDTH):
				if boardColor[y][x] != WORKSPACECOLOR:
					warningSignal = True
		
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def displayHomeScreen():
	DISPLAYSURF.fill(WORKSPACECOLOR)
	
	drawM(4, 15, 18)
	drawM(5, 15, 18)
	drawI(5, 20, 18)
	drawT(5, 16, 18)
	
	drawM(10, 15, 18)
	drawE(9, 16, 18)
	drawI(9, 20, 18)
	drawM(10, 17, 18)
	drawM(10, 20, 18)
	drawC(9, 20, 18)
	drawR(9, 18, 18)
	
	drawM(15, 15, 18)
	drawM(16, 15, 18)
	drawI(16, 20, 18)
	drawT(16, 16, 18)
	drawP(16, 17, 18)
	
	drawE(20, 16, 18)
	drawP(20, 20, 18)
	drawD(24, 16, 18)
	drawR(20, 18, 18)
	drawZ(21, 18, 18)
	drawZ(23, 20, 18)
	drawG(24, 17, 18)
	
	drawI(26, 18, 18)
	drawI(26, 20, 18)
	
	drawM(30, 15, 18)
	drawM(29, 20, 18)
	drawE(28, 16, 18)
	drawC(28, 17, 18)
	drawD(32, 18, 18)
	drawG(32, 20, 18)
	
	pygame.draw.circle(DISPLAYSURF,SILVER,(WINDOWWIDTH/2,WINDOWHEIGHT/2),130,5)
	pygame.draw.polygon(DISPLAYSURF,SILVER,((320,710),(320,850),(450,770)))	
	playRect = pygame.Rect(WINDOWWIDTH / 2 -130, WINDOWHEIGHT / 2 -130, 260, 260)
	
	
	drawM(1,29,50)
	drawO(5, 29, 50)
	drawH(4, 29, 50)
	drawS(8, 29, 50)
	drawJ(10, 29, 50)
	drawO(11, 29, 50)
	drawF(7, 28, 50)
	drawN(2,  28, 50)
	drawL(0, 28, 50)
	drawO(8, 27, 50)
	drawR(2, 26, 50)
	drawI(1, 27, 50)
	drawP(0, 25, 50)
	drawN(7, 26, 50)
	drawQ(4, 26, 50)
	drawP(5, 27, 50)
	drawH(11, 27, 50)
	drawI(12, 27, 50)
	drawO(9, 25, 50)
	drawT(11, 24, 50)
	drawW(6, 24, 50)
	drawS(9, 23, 50)
	drawZ(2, 23, 50)
	drawI(0, 22, 50)
	drawJ(12, 22, 50)
	drawN(7, 21, 50)
	
	while True:
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				if playRect.collidepoint(event.pos):
					pygame.draw.circle(DISPLAYSURF,WHITE,(WINDOWWIDTH/2,WINDOWHEIGHT/2),130,5)
					pygame.draw.polygon(DISPLAYSURF,WHITE, ((320,710),(320,850),(450,770)))	
					pygame.display.update()
					pygame.time.wait(300)
					runGame()
					

def newBestAnimation(times, score):
	copySurf =DISPLAYSURF.copy()
	for size in range(500, 75, -25):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		color = r, g, b
		textSurf, textRect = makeText('NEW BEST', color, 200, 300, size, DISPLAYSURF)
		DISPLAYSURF.blit(copySurf, (0,0))
		textRect.center = (360, 300)
		DISPLAYSURF.blit(textSurf, textRect)
		pygame.display.update()
	
	if times > 300:
		scoreSurf, scoreRect = makeText(str(score), WHITE, 300, 550, 100, DISPLAYSURF)
		scoreRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 200)
		DISPLAYSURF.blit(copySurf, (0,0))
		DISPLAYSURF.blit(textSurf, textRect)
		DISPLAYSURF.blit(scoreSurf, scoreRect)
	orgiSurf = DISPLAYSURF.copy()
	value1 = list()
	for i in range (100, 1000, 50):
		value1.append(i)
	value2 = list()
	for x in range (-1000, 0, 100):
		value2.append(x)
	value3 = list()
	for x in range(720, 2000, 100):
		value3.append(x)
	value4 = list()
	for x in range(200, 500, 50):
		value4.append(x)
	rects = dict()
	key = 0
	for _ in range(times):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		color = r, g, b
		yCoord1 = random.choice(value1)
		xCoord1 = random.choice(value2)
		xCoord2 = random.choice(value3)
		yCoord2 = yCoord1
		xCoord3 = random.choice(value4)
		rects[key] = [color, xCoord1, yCoord1, xCoord2, yCoord2, xCoord3, color]
		key += 1
		for rect in rects:
			pygame.draw.rect(DISPLAYSURF, rects[rect][0], (rects[rect][1], rects[rect][2], 10, 10))
			pygame.draw.rect(DISPLAYSURF, rects[rect][0], (rects[rect][3], rects[rect][2], 10, 10))
			if rects[rect][4] < 1200:
				pygame.draw.rect(DISPLAYSURF, rects[rect][6], (rects[rect][5], rects[rect][4], 10, 10))
			rects[rect][1] += 5
			rects[rect][2] -= 2
			rects[rect][3] -= 5
			rects[rect][4] += 4
			if rects[rect][5] < 360:
				rects[rect][5] -= 0.5
			else:
				rects[rect][5] += 0.5
			if rects[rect][1] == 360:
				rects[rect][0] = WORKSPACECOLOR
			if rects[rect][1] <100 and rects[rect][2] < 100:
				rects[rect][0] = WORKSPACECOLOR
		pygame.display.update()
		DISPLAYSURF.blit(orgiSurf, (0, 0))
	if times > 300:
		replayRect = pygame.Rect(WINDOWWIDTH / 2 - 130,WINDOWHEIGHT / 2 +120 -130,260,260)
		pygame.draw.circle(DISPLAYSURF,SILVER,(WINDOWWIDTH /2, WINDOWHEIGHT / 2 + 120), 130, 5)
		pygame.draw.arc(DISPLAYSURF,SILVER,(WINDOWWIDTH / 2 - 70,WINDOWHEIGHT / 2  + 50,140,140),-1,4.2,15)
		pygame.draw.polygon(DISPLAYSURF,SILVER,((333,930),(310,960),(350,960)))
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONUP:
					if replayRect.collidepoint(event.pos):
						pygame.draw.circle(DISPLAYSURF,WHITE,(WINDOWWIDTH /2, WINDOWHEIGHT / 2 + 120), 130, 5)
						pygame.draw.arc(DISPLAYSURF,WHITE,(WINDOWWIDTH / 2 - 70,WINDOWHEIGHT / 2  + 50,140,140),-1,4.2,15)
						pygame.draw.polygon(DISPLAYSURF,WHITE,((333,930),(310,960),(350,960)))
						pygame.display.update()
						pygame.time.wait(300)
						runGame()
			pygame.display.update()

def drawSettingWindow():
	global difficulty, playSound, playMusic
	width = 600
	length = 600
	settingSurface = pygame.Surface((width, length))
	settingSurface = settingSurface.convert_alpha()
	r, g, b = SILVER
	settingSurface.fill((r, g, b, 150))
	xmargin = int((WINDOWWIDTH - width) / 2)
	ymargin = int((WINDOWHEIGHT - length) / 2)
	pygame.draw.line(settingSurface, RED, (width - 80, 20),(width - 20,80),20)
	pygame.draw.line(settingSurface, RED, (width - 20, 20),(width - 80,80),20)
	closeRect = pygame.Rect(xmargin + width - 100, ymargin + 0,width,100)
	homeRect = pygame.Rect(xmargin + 45, ymargin + 125, 150, 150)
	soundRect = pygame.Rect(xmargin + 225, ymargin + 125, 150, 150)
	musicRect = pygame.Rect(xmargin + 405, ymargin + 125, 150, 150)
	dropRect = pygame.Rect(xmargin + 450,ymargin + 350, 100, 100)
	drawHomeIcon(settingSurface, SILVER)
	drawBackgroundMusicIcon(settingSurface, SILVER)
	easyRect = pygame.Rect(xmargin + 300, ymargin + 453, 250, 30)
	mediumRect = pygame.Rect(xmargin + 300, ymargin + 486, 250, 30)
	hardRect = pygame.Rect(xmargin + 300, ymargin + 519, 250, 30)
	drawSoundIcon(settingSurface, SILVER)
	drawLevelDropDown(settingSurface, SILVER, xmargin, ymargin)
	if not playMusic:
		pygame.draw.line(settingSurface, SILVER, (540, 150),(420, 250), 10)
	if not playSound:
		pygame.draw.line(settingSurface, SILVER, (360, 150),(240, 250), 10)
	orginalSurface = DISPLAYSURF.copy()
	origSettingSurf = settingSurface.copy()
	dropDownIsShown = False
	drawDifficulty(difficulty, SILVER, origSettingSurf)
	DISPLAYSURF.blit(origSettingSurf, (xmargin, ymargin))	
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				if closeRect.collidepoint(event.pos):
					return 
				elif soundRect.collidepoint(event.pos):
					drawSoundIcon(origSettingSurf, SILVER)
					drawSoundIcon(settingSurface, SILVER)
					if playSound:
						playSound = False
						pygame.draw.line(origSettingSurf, SILVER, (360, 150),(240, 250), 10)
						pygame.draw.line(settingSurface, SILVER, (360, 150),(240, 250), 10)
					else:
						playSound = True
					DISPLAYSURF.blit(orginalSurface,(0,0))
					DISPLAYSURF.blit(origSettingSurf,(xmargin, ymargin))
				elif musicRect.collidepoint(event.pos):
					drawBackgroundMusicIcon(origSettingSurf, SILVER)
					drawBackgroundMusicIcon(settingSurface, SILVER)
					if playMusic:
						playMusic = False
						pygame.draw.line(origSettingSurf, SILVER, (540, 150),(420, 250), 10)
						pygame.draw.line(settingSurface, SILVER, (540, 150),(420, 250), 10)
					else:
						playMusic = True
					DISPLAYSURF.blit(orginalSurface,(0,0))
					DISPLAYSURF.blit(origSettingSurf,(xmargin, ymargin))
				elif dropRect.collidepoint(event.pos):
					DISPLAYSURF.blit(orginalSurface,(0,0))
					if not dropDownIsShown:
						drawLists(settingSurface, SILVER)
						DISPLAYSURF.blit(settingSurface, (xmargin, ymargin))
						dropDownIsShown = True
					else:
						dropDownIsShown = False
						drawDifficulty(difficulty, SILVER, origSettingSurf)
						DISPLAYSURF.blit(origSettingSurf, (xmargin, ymargin))	
				elif dropDownIsShown and easyRect.collidepoint(event.pos):
					difficulty = 'Easy'
					DISPLAYSURF.blit(orginalSurface,(0,0))
					dropDownIsShown = False
					drawDifficulty(difficulty, SILVER, origSettingSurf)
					DISPLAYSURF.blit(origSettingSurf, (xmargin, ymargin))
				elif dropDownIsShown and mediumRect.collidepoint(event.pos):
					difficulty = 'Medium'
					DISPLAYSURF.blit(orginalSurface,(0,0))
					dropDownIsShown = False
					drawDifficulty(difficulty, SILVER, origSettingSurf)
					DISPLAYSURF.blit(origSettingSurf, (xmargin, ymargin))
				elif dropDownIsShown and hardRect.collidepoint(event.pos):
					difficulty = 'Hard'
					DISPLAYSURF.blit(orginalSurface,(0,0))
					dropDownIsShown = False
					drawDifficulty(difficulty, SILVER, origSettingSurf)
					DISPLAYSURF.blit(origSettingSurf, (xmargin, ymargin))
				elif homeRect.collidepoint(event.pos):
					displayHomeScreen()
					
		pygame.display.update()


def drawHomeIcon(surface,color):
	pygame.draw.circle(surface,WORKSPACECOLOR,(120,200),75)
	pygame.draw.circle(surface,color,(120,200),82, 10)
	pygame.draw.polygon(surface, color, ((70,200),(120,150),(170,200)))
	pygame.draw.rect(surface, color,(80,200,80,40))
	pygame.draw.rect(surface, WORKSPACECOLOR,(100,200,40,60),0,20)
	pygame.draw.line(surface,color,(60,210),(120,150),10)
	pygame.draw.line(surface, color,(119,150),(180,210),10)
	

def drawSoundIcon(surface,color):
	pygame.draw.circle(surface,WORKSPACECOLOR, (300,200),75)
	pygame.draw.circle(surface,color, (300,200),82, 10)
	pygame.draw.polygon(surface, color, ((285,187),(330,160),(330,240),(285,213)))
	pygame.draw.rect(surface, color, (270,187,10,26))


def drawBackgroundMusicIcon(surface, color):
	pygame.draw.circle(surface, WORKSPACECOLOR, (480, 200), 75)
	pygame.draw.circle(surface, color, (480, 200), 82, 10)
	pygame.draw.line(surface,color,(460,175),(520,160),20)
	ellipseSurf = pygame.Surface((30, 15))
	ellipseSurf.fill(WORKSPACECOLOR)
	pygame.draw.ellipse(ellipseSurf, color,(0, 0, 30, 15))
	ellipseSurf = pygame.transform.rotate(ellipseSurf, 20)
	surface.blit(ellipseSurf,(431, 220))
	surface.blit(ellipseSurf,(491, 205))
	pygame.draw.line(surface, color, (460,170),(460,230), 3)
	pygame.draw.line(surface, color, (520,155),(520,215), 3)


def drawLevelDropDown(surface, color, xmargin, ymargin):
	pygame.draw.rect(surface, WORKSPACECOLOR, (50,350,500,100))
	pygame.draw.lines(surface, color, False, ((490,390),(510,410),(530,390)),5)
	makeText('Difficulty', color , 55, 370, 70, surface)


def drawDifficulty(difficulty, color, surface):
	pygame.draw.rect(surface, WORKSPACECOLOR, (300, 455, 250, 50))
	makeText(difficulty, color, 300, 455, 50, surface)
	

def drawLists(surface, color):
	pygame.draw.rect(surface, WORKSPACECOLOR, (300, 453, 250, 30))	
	pygame.draw.rect(surface, WORKSPACECOLOR, (300, 486, 250, 30))
	pygame.draw.rect(surface, WORKSPACECOLOR, (300, 519, 250, 30))
	makeText('Easy', color, 350, 453, 30, surface)
	makeText('Medium', color, 350, 486, 30, surface)
	makeText('Hard', color, 350, 519, 30, surface)		


def drawBoard():
	DISPLAYSURF.fill(BGCOLOR)
	pygame.draw.rect(DISPLAYSURF, WORKSPACECOLOR, (XMARGIN, 4 * BOXSIZE,  BOARDX, BOARDY))
	pygame.draw.rect(DISPLAYSURF, BOARDERCOLOR, (XMARGIN, 4 * BOXSIZE,  BOARDX, BOARDY), 10)
	

def makeText(text, color, x, y, size, surface):
	textFont = pygame.font.Font('freesansbold.ttf',size)
	textSurf = textFont.render(text, 1, color)
	textRect = textSurf.get_rect()
	textRect.topleft = x, y
	surface.blit(textSurf,textRect)
	return textSurf, textRect	


def drawBoardColors():
	for y in range(BOARDHEIGHT):
		for x in range(BOARDWIDTH):
			drawBox(boardColor[y][x], x, y)


def getRotatedShape(shape, x, y):
	newShape = shape
	if shape == T:
		if boardColor[y -2][x] == WORKSPACECOLOR:
			newShape = H
	elif shape == H:
		if (BOARDWIDTH > x + 1) and(boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR ):
			newShape = W
	elif shape == W:
		if (boardColor[y - 2][x] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR):
			newShape = R
	elif shape == R:
		if (x - 1 >= 0) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			newShape = T
	elif shape == J:
		if (BOARDWIDTH > x + 2) and (boardColor [y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x + 2] == WORKSPACECOLOR):
			newShape = C
	elif shape == C:
		if (boardColor[y - 2][x] == WORKSPACECOLOR) and (boardColor[y - 2][x + 1] == WORKSPACECOLOR):
			newShape = P
	elif shape == P:
		if (x - 2 >= 0) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 2] == WORKSPACECOLOR):
			newShape = D
	elif shape == D:
		if (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x] == WORKSPACECOLOR):
			newShape = J
	elif shape == Q:
		if (x - 2 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y][x - 2] == WORKSPACECOLOR):
			newShape = G
	elif shape == G:
		if (BOARDWIDTH > x + 1) and (boardColor[y - 2][x] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR):
			newShape = L
	elif shape == L:
		if (BOARDWIDTH > x + 2) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 2] == WORKSPACECOLOR):
			newShape = E
	elif shape == E:
		if (x - 1 >= 0) and (boardColor[y - 2][x] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR):
			newShape = Q
	elif shape == S:
		if (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y -2][x - 1]):
			newShape = F
	elif shape == F:
		if (BOARDWIDTH > x + 1) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			newShape = S
	elif shape == Z:
		if (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y - 2][x + 1] == WORKSPACECOLOR):
			newShape = N
	elif shape == N:
		if (x - 1 >= 0) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR):
			newShape = Z
	elif shape == O:
		newShape = O
	elif shape == I:
		if (BOARDWIDTH > x + 2) and (x - 1 >= 0) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x +2] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			newShape = M
		elif (BOARDWIDTH > x + 1) and (x - 2 >= 0) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y][x - 2] == WORKSPACECOLOR):
			newShape = M
			x -= 1
		elif (x - 3 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y][x - 2] == WORKSPACECOLOR) and (boardColor[y][x - 3] == WORKSPACECOLOR):
			newShape = M
			x -= 2	
		elif (BOARDWIDTH > x + 3) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x +2] == WORKSPACECOLOR) and (boardColor[y][x + 3] == WORKSPACECOLOR):
			newShape = M	
			x += 1
	elif shape == M:
		if (boardColor[y - 1][x] == WORKSPACECOLOR) and (boardColor[y - 2][x] == WORKSPACECOLOR) and (boardColor[y - 3][x] == WORKSPACECOLOR):
			newShape = I
		elif (x - 1 >= 0) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR) and (boardColor[y - 3][x - 1] == WORKSPACECOLOR):
			newShape = I
			x -= 1
		elif (BOARDWIDTH > x + 1) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y - 2][x + 1] == WORKSPACECOLOR) and (boardColor[y - 3][x + 1] == WORKSPACECOLOR):
			newShape = I
			x += 1
		elif (BOARDWIDTH > x + 2) and  (boardColor[y - 1][x + 2] == WORKSPACECOLOR) and (boardColor[y - 2][x + 2] == WORKSPACECOLOR) and (boardColor[y - 3][x + 2] == WORKSPACECOLOR):
			newShape = I
			x += 2
			
	return newShape,x ,y
	

def drawQuickTools(shape, score):
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (0, 0, WINDOWWIDTH,  4 * BOXSIZE ))
	pygame.draw.line(DISPLAYSURF, BOARDERCOLOR,  (XMARGIN, 4 * BOXSIZE),(XMARGIN + BOARDX, 4 * BOXSIZE), 5)
	for y in range(4):
		for x in range(5):
			drawBox(WORKSPACECOLOR, x + 9, y + 2, 30)
	drawShape(shape, 11, 5,30)	
	makeText(str(score), WHITE, 40,120,50,DISPLAYSURF)
	bestScore  = getBestScore(score)
	makeText(str(bestScore), ORANGE, 40,30,50, DISPLAYSURF)
	drawSettingButton()
	drawRotateButton(SILVER)
	drawDownButton()


def drawDownButton(color = BLACK):
	r, g, b = BGCOLOR
	for i in range(80):
		pygame.draw.rect(DISPLAYSURF, ( (r), (g - i),  (b -  i)), (150, 1370 + i, 60, 1))
	pygame.draw.polygon(DISPLAYSURF, color, ((120, 1450), (240, 1450), (180,1500)))
	if color != BLACK:
		for i in range (80):
			pygame.draw.rect(DISPLAYSURF, (r +2 * i, g+ i, b + i),(150, 1370 + i, 60, 1))


def drawRotateButton(color):
	
	pygame.draw.polygon(DISPLAYSURF, color, ((500, 1350),(500, 1390),(525,1374)))
	pygame.draw.arc(DISPLAYSURF, color, (500 - 70, 1430 - 70, 140, 140), 1.57, 2.5, 20)
	
	pygame.draw.polygon(DISPLAYSURF, color, ((540, 1430),(580, 1430),(557,1453)))
	pygame.draw.arc(DISPLAYSURF, color, (500 - 70, 1430 - 70, 140, 140), 0, 1, 20)
	
	pygame.draw.polygon(DISPLAYSURF, color, ((420, 1430),(460, 1430),(441,1407)))
	pygame.draw.arc(DISPLAYSURF, color, (500 - 70, 1430 - 70, 140, 140), 3.14, 4, 20)
	
	pygame.draw.polygon(DISPLAYSURF, color, ((500, 1470),(500, 1510),(475,1483)))
	pygame.draw.arc(DISPLAYSURF, color, (500 - 70, 1430 - 70, 140, 140), 4.7, 5.7, 20)



def drawSettingButton(color = SILVER):
	pygame.draw.circle(DISPLAYSURF,color ,(600,120),40,20)
	pygame.draw.line(DISPLAYSURF, color, (600,120 - 55),(600, 120 + 55),20)
	pygame.draw.line(DISPLAYSURF, color, (600 - 55,120),(600 + 55, 120),20)
	pygame.draw.line(DISPLAYSURF, color, (600 + 60 / 1.4 ,120 - 55 / 1.4),(600 - 60 / 1.4, 120 + 60 / 1.4),25)
	pygame.draw.line(DISPLAYSURF, color, (600 - 60 / 1.4 ,120 - 55 / 1.4),(600 + 60 / 1.4, 120 + 55 / 1.4),25)
	pygame.draw.circle(DISPLAYSURF, BGCOLOR ,(600,120),70, 20)
	pygame.draw.circle(DISPLAYSURF,BGCOLOR ,(600,120),23)


def displayWarningAnimation(r, g, b, on):
	if on:
		rPlus = 25
		gPlus = -10
		bPlus = -10
		if g == 20:
			on = False
	else:
		rPlus = -25
		gPlus = 10
		bPlus = 10
		if g == 60:
			on = True
	r += rPlus
	g += gPlus
	b += bPlus
	ymargin = 4 * BOXSIZE + BOARDY + 30
	height = WINDOWHEIGHT - ymargin
	numOfPieces = 100
	width = height / numOfPieces
	counter = 0
	i = 0
	while i < height:
		flashSurface = pygame.Surface((WINDOWWIDTH, int(width)))
		flashSurface = flashSurface.convert_alpha()
		flashSurface.fill((r, g, b, counter * 2.5))
		DISPLAYSURF.blit(flashSurface, (0, ymargin + i))
		counter += 1
		i += int(width)
	
	ymargin = 0
	height = 4 * BOXSIZE 
	width = height / numOfPieces
	counter = 0
	i = height
	while i > 0:
		flashSurface = pygame.Surface((WINDOWWIDTH, int(width)))
		flashSurface = flashSurface.convert_alpha()
		flashSurface.fill((r, g, b, counter * 2.3))
		DISPLAYSURF.blit(flashSurface, (0, ymargin + i))
		counter += 1
		i -= int(width)
	
	xmargin = XMARGIN + BOARDX
	height = XMARGIN
	width = height / numOfPieces
	counter = 0
	i = 0
	while i < height:
		flashSurface = pygame.Surface((1, WINDOWHEIGHT))
		flashSurface = flashSurface.convert_alpha()
		flashSurface.fill((r, g, b, counter ))
		DISPLAYSURF.blit(flashSurface, (xmargin + i, 0))
		counter += 1
		i += width
		
	xmargin = 0
	counter = 0
	i = height
	while i > 0:
		flashSurface = pygame.Surface((1, WINDOWHEIGHT))
		flashSurface = flashSurface.convert_alpha()
		flashSurface.fill((r, g, b, counter ))
		DISPLAYSURF.blit(flashSurface, (xmargin + i, 0))
		counter += 1
		i -= width
	pygame.display.update()
	return r, g, b, on
	

def displayGameOverScreen(score):
	orginalSurface = DISPLAYSURF.copy()
	gameOverSurface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
	gameOverSurface = gameOverSurface.convert_alpha()
	replayRect = pygame.Rect(WINDOWWIDTH / 2 - 130,WINDOWHEIGHT / 2 +120 -130,260,260)
	best = getBestScore(score)
	r, g, b = WORKSPACECOLOR
	for i in range(0, 150, 10):
		DISPLAYSURF.blit(orginalSurface, (0, 0))
		gameOverSurface.fill((r, g, b, i))		
		pygame.draw.circle(gameOverSurface,SILVER,(WINDOWWIDTH /2, WINDOWHEIGHT / 2 + 120), 130, 5)
		pygame.draw.arc(gameOverSurface,SILVER,(WINDOWWIDTH / 2 - 70,WINDOWHEIGHT / 2  + 50,140,140),-1,4.2,15)
		pygame.draw.polygon(gameOverSurface,SILVER,((333,930),(310,960),(350,960)))
		makeText('Game Over', SILVER, 27, 400, 120, gameOverSurface)
		makeText('Score', SILVER, 100, 550, 70, gameOverSurface)
		makeText('Best', SILVER, 100, 650, 70, gameOverSurface)
		makeText(str(score), SILVER, 400, 550, 70, gameOverSurface)
		makeText(str(best), SILVER, 400, 650, 70, gameOverSurface)
		DISPLAYSURF.blit(gameOverSurface, (0,0))
		pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				if replayRect.collidepoint(event.pos):
					pygame.draw.circle(DISPLAYSURF,WHITE,(WINDOWWIDTH /2, WINDOWHEIGHT / 2 + 120), 130, 5)
					pygame.draw.arc(DISPLAYSURF,WHITE,(WINDOWWIDTH / 2 - 70,WINDOWHEIGHT / 2  + 50,140,140),-1,4.2,15)
					pygame.draw.polygon(DISPLAYSURF,WHITE,((333,930),(310,960),(350,960)))
					pygame.display.update()
					pygame.time.wait(300)
					runGame()
		pygame.display.update()
		
		
def updateBoardColors(shape, x, y):
	global boardColor
	if shape == T:
		boardColor[y][x] = color[T]
		boardColor[y - 1][x] = color[T]
		boardColor[y - 1][x + 1] = color[T]
		boardColor[y - 1][x - 1] = color[T]
	elif shape == S:
		boardColor[y][x] = color[S]
		boardColor[y][x - 1] = color[S]
		boardColor[y - 1][x] = color[S]
		boardColor[y - 1][x + 1] = color[S]
	elif shape == Z:
		boardColor[y][x] = color[Z]
		boardColor[y - 1][x] = color[Z]
		boardColor[y][x + 1] = color[Z]
		boardColor[y - 1][x - 1] = color[Z]
	elif shape == J:
		boardColor[y][x] = color[J]
		boardColor[y - 1][x] = color[J]
		boardColor[y - 2][x] = color[J]
		boardColor[y][x - 1] = color[J]
	elif shape == L:
		boardColor[y][x] = color[L]
		boardColor[y - 1][x] = color[L]
		boardColor[y - 2][x] = color[L]
		boardColor[y][x + 1] = color[L]
	elif shape == I:
		boardColor[y][x] = color[I]
		boardColor[y - 1][x] = color[I]
		boardColor[y - 2][x] = color[I]
		boardColor[y - 3][x] = color[I]
	elif shape == O:
		boardColor[y][x] = color[O]
		boardColor[y - 1][x] = color[O]
		boardColor[y][x + 1] = color[O]
		boardColor[y - 1][x + 1] = color[O]
	elif shape == P:
		boardColor[y][x] = color[P]
		boardColor[y - 1][x] = color[P]
		boardColor[y - 2][x] = color[P]
		boardColor[y - 2][x + 1] = color[P]
	elif shape == Q:
		boardColor[y][x] = color[Q]
		boardColor[y - 1][x] = color[Q]
		boardColor[y - 2][x] = color[Q]
		boardColor[y - 2][x - 1] = color[Q]
	elif shape == M:
		boardColor[y][x] = color[M]
		boardColor[y][x + 1] = color[M]
		boardColor[y][x + 2] = color[M]
		boardColor[y][x - 1] = color[M]
	elif shape == N:
		boardColor[y][x] = color[N]
		boardColor[y - 1][x] = color[N]
		boardColor[y - 1][x + 1] = color[N]
		boardColor[y - 2][x + 1] = color[N]
	elif shape == F:
		boardColor[y][x] = color[F]
		boardColor[y - 1][x] = color[F]
		boardColor[y - 1][x -1] = color[F]
		boardColor[y - 2][x -1] = color[F]
	elif shape == R:
		boardColor[y][x] = color[R]
		boardColor[y - 1][x] = color[R]
		boardColor[y - 1][x + 1] = color[R]
		boardColor[y - 2][x] = color[R]
	elif shape == H:
		boardColor[y][x] = color[H]
		boardColor[y - 1][x] = color[H]
		boardColor[y - 1][x - 1] = color[H]
		boardColor[y - 2][x] = color[H]
	elif shape == W:
		boardColor[y][x] = color[W]
		boardColor[y][x + 1] = color[W]
		boardColor[y][x - 1] = color[W]
		boardColor[y - 1][x] = color[W]
	elif shape == C:
		boardColor[y][x] = color[C]
		boardColor[y - 1][x] = color[C]
		boardColor[y][x + 1] = color[C]
		boardColor[y][x + 2] = color[C]
	elif shape == D:
		boardColor[y][x] = color[D]
		boardColor[y - 1][x] = color[D]
		boardColor[y - 1][x - 1] = color[D]
		boardColor[y - 1][x - 2] = color[D]
	elif shape == E:
		boardColor[y][x] = color[E]
		boardColor[y - 1][x] = color[E]
		boardColor[y - 1][x + 1] = color[E]
		boardColor[y - 1][x + 2] = color[E]
	elif shape == G:
		boardColor[y][x] = color[G]
		boardColor[y - 1][x] = color[G]
		boardColor[y][x - 1] = color[G]
		boardColor[y][x - 2] = color[G]
		

def getRandomShape():
	shapes = [T, S, Z, J, C, D, E, G, H, W, R, L, I, O, M, P, Q, N, F]
	return random.choice(shapes)


def getStartingBoardColor():
	board = [ ]
	for y in range(BOARDHEIGHT):
		row = [ ]
		for x in range(BOARDWIDTH):
			row.append(WORKSPACECOLOR)
		board.append(row)
	return board
	

def getLeftTopOfBox(x, y, size = BOXSIZE):
	left = XMARGIN + size * x
	top =  size * y 
	return(left, top)


def checkIfAnyRowIsFull(score, shape):
	global boardColor
	isFull = list()
	for _ in range(BOARDHEIGHT):
		isFull.append(True)
	y = 0
	while y < BOARDHEIGHT:
		x = 0
		while x < BOARDWIDTH:
			if boardColor[y][x] == WORKSPACECOLOR:
				isFull[y] = False
				break
			x += 1
		y += 1
	counter = 0
	increment = 0
	numOfRow = 0
	while counter < len(isFull):
		if isFull[counter] == True:
			if difficulty == 'Easy':
				score += 1
				increment = 1
			elif difficulty == 'Medium':
				score += 5
				increment = 5
			elif difficulty == 'Hard':
				score += 10
				increment = 10
			numOfRow += 1
			xCoord = 0
			while xCoord < BOARDWIDTH:
				boardColor[counter][xCoord] = WORKSPACECOLOR
				xCoord += 1
			drawBoard()
			drawBoardColors()
			drawQuickTools(shape, score)
			pygame.display.update()
			boxy = counter
			while boxy > 0:
				boxx = 0
				while boxx < BOARDWIDTH:
					boardColor[boxy][boxx] = boardColor[boxy - 1][boxx]
					boxx += 1
				boxy -= 1
		counter += 1
	if numOfRow == 2:
		score += increment
	elif numOfRow == 3:
		score += increment * 2
	elif numOfRow == 4:
		score += increment  * 3
	return score		


def getBestScore(score):
	openBestFile = open('tetrisBest.txt')
	readBestFile = openBestFile.read()
	best = int(readBestFile)
	if score > best:
		openBestFile.close()
		writeBestFile = open('tetrisBest.txt','w')
		best = score
		writeBestFile.write(str(best))
		writeBestFile.close()
	else:
		openBestFile.close()
	return best		
	

def drawShape(shape, x, y, size = BOXSIZE):
	if shape == T:
		drawT(x, y, size)
	elif shape == S:
		drawS(x,y, size)
	elif shape == Z:
		drawZ(x,y, size)
	elif shape == J:
		drawJ(x, y, size)
	elif shape == L:
		drawL(x, y, size)
	elif shape == I:
		drawI(x, y, size)
	elif shape == O:
		drawO(x, y, size)
	elif shape == P:
		drawP(x, y, size)
	elif shape == Q:
		drawQ(x, y, size)
	elif shape == M:
		drawM(x, y, size)
	elif shape == N:
		drawN(x, y, size)
	elif shape == F:
		drawF(x, y, size)
	elif shape == R:
		drawR(x, y, size)
	elif shape == H:
		drawH(x, y, size)
	elif shape == W:
		drawW(x, y, size)
	elif shape == C:
		drawC(x, y, size)
	elif shape == D:
		drawD(x, y, size)
	elif shape == E:
		drawE(x, y, size)
	elif shape == G:
		drawG(x, y, size)
		
		
def isValidMove(shape,direction, x, y):
	isValid = False
	if shape == T:
		isValid = hasTGetValidMove(direction, x, y)
	elif shape == S:
		isValid = hasSGetValidMove(direction, x, y)
	elif shape == Z:
		isValid = hasZGetValidMove(direction, x, y)
	elif shape == J:
		isValid = hasJGetValidMove(direction, x, y)
	elif shape == L:
		isValid = hasLGetValidMove(direction, x, y)
	elif shape == I:
		isValid = hasIGetValidMove(direction, x, y)
	elif shape == O:
		isValid = hasOGetValidMove(direction, x, y)
	elif shape == P:
		isValid = hasPGetValidMove(direction, x, y)
	elif shape == Q:
		isValid = hasQGetValidMove(direction, x, y)
	elif shape == M:
		isValid = hasMGetValidMove(direction, x, y)
	elif shape == N:
		isValid = hasNGetValidMove(direction, x, y)
	elif shape == F:
		isValid = hasFGetValidMove(direction, x, y)
	elif shape == E:
		isValid = hasEGetValidMove(direction, x, y)
	elif shape == C:
		isValid = hasCGetValidMove(direction, x, y)
	elif shape == D:
		isValid = hasDGetValidMove(direction, x, y)
	elif shape == G:
		isValid = hasGGetValidMove(direction, x, y)
	elif shape == R:
		isValid = hasRGetValidMove(direction, x, y)
	elif shape == H:
		isValid = hasHGetValidMove(direction, x, y)
	elif shape == W:
		isValid = hasWGetValidMove(direction, x, y)
			
	return isValid


def hasTGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 2] == WORKSPACECOLOR):
			isValid = True
	return isValid
				

def hasRGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 2] == WORKSPACECOLOR) and (boardColor[y - 2][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasHGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y - 2][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 2] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasWGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y + 1][x + 1] == WORKSPACECOLOR) and (boardColor[y + 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 2] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 2] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid
														

def hasSGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x - 1] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y -1][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 2] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid
	

def hasZGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x + 1] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 2] == WORKSPACECOLOR) and (boardColor[y -1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 2] == WORKSPACECOLOR):
			isValid = True
	return isValid
	

def hasOGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 2] == WORKSPACECOLOR) and (boardColor[y -1][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif (x - 1 >= 0) and direction == LEFT:
		if (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid
	

def hasMGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x - 1] == WORKSPACECOLOR) and (boardColor[y +1][x + 1] == WORKSPACECOLOR) and (boardColor[y + 1][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 3 < BOARDWIDTH) and (boardColor[y][x + 3] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 2] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasCGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x + 1] == WORKSPACECOLOR) and (boardColor[y + 1][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 3 < BOARDWIDTH) and (boardColor[y][x + 3] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and(boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasGGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x - 1] == WORKSPACECOLOR) and (boardColor[y + 1][x - 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y  - 1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 3 >= 0) and (boardColor[y][x - 3] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasDGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y][x - 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y  - 1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 3 >= 0) and (boardColor[y - 1][x - 3] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasEGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 3 < BOARDWIDTH) and (boardColor[y - 1][x + 3] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid
	
	
def hasIGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and(boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y -2][x + 1] == WORKSPACECOLOR) and (boardColor[y -3][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR) and (boardColor[y - 3][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid

		
def hasNGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 2] == WORKSPACECOLOR) and (boardColor[y -2][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasFGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y -2][x] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 2] == WORKSPACECOLOR) and (boardColor[y - 2][x - 2] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasPGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and(boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y -2][x + 2] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def hasQGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and(boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y - 1][x + 1] == WORKSPACECOLOR) and (boardColor[y -2][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 2] == WORKSPACECOLOR):
			isValid = True
	return isValid

		
def hasJGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x - 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 1 < BOARDWIDTH) and (boardColor[y][x + 1] == WORKSPACECOLOR) and (boardColor[y -1][x + 1] == WORKSPACECOLOR) and (boardColor[y -2][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 2 >= 0) and (boardColor[y][x - 2] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid
	
	
def hasLGetValidMove(direction, x, y):
	isValid = False
	if direction == DOWN:
		if (y + 1 < BOARDHEIGHT) and (boardColor[y + 1][x] == WORKSPACECOLOR) and (boardColor[y +1][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == RIGHT:
		if (x + 2 < BOARDWIDTH) and(boardColor[y][x + 2] == WORKSPACECOLOR) and (boardColor[y -1][x + 1] == WORKSPACECOLOR) and (boardColor[y -2][x + 1] == WORKSPACECOLOR):
			isValid = True
	elif direction == LEFT:
		if (x - 1 >= 0) and (boardColor[y][x - 1] == WORKSPACECOLOR) and (boardColor[y - 1][x - 1] == WORKSPACECOLOR) and (boardColor[y - 2][x - 1] == WORKSPACECOLOR):
			isValid = True
	return isValid


def drawBox(color, x, y, size = BOXSIZE):
	r, g, b = color
	if color == WORKSPACECOLOR:
		boardWidth = 2
		color1 = r , g - 10 , b - 10
		color2 = color3 = color4 = color1
	else:
		if size == BOXSIZE:
			boardWidth = 8
		else :
			boardWidth = 5
		color1 = r + 60, g + 60, b + 60
		color2 = r + 30, g  + 30, b + 30
		color3  = r - 60, g - 60, b - 60
		color4 = r - 30, g - 30, b - 30
	
	left,top = getLeftTopOfBox(x, y, size)
	pygame.draw.rect(DISPLAYSURF, color, (left, top, size -1,size -1))
	pygame.draw.polygon(DISPLAYSURF, color1, ((left, top), (left + boardWidth,top + boardWidth),(left + boardWidth,top + size - boardWidth),(left, top + size - 1)))
	pygame.draw.polygon(DISPLAYSURF, color2, ((left, top), (left + boardWidth,top + boardWidth),(left + size - boardWidth,top + boardWidth),(left + size - 1, top)))
	pygame.draw.polygon(DISPLAYSURF, color3, ((left + size - 1, top), (left + size - boardWidth,top + boardWidth),(left + size - boardWidth,top + size - boardWidth),(left + size - 1, top + size - 1)))
	pygame.draw.polygon(DISPLAYSURF, color4, ((left, top + size - 1), (left + boardWidth,top + size - boardWidth),(left + size - boardWidth,top + size - boardWidth),(left + size - 1, top + size - 1)))

		
def drawT(x, y, size = BOXSIZE):
	drawBox(color[T], x, y, size)
	x -= 1
	y -= 1
	drawBox(color[T], x, y, size)
	x += 1
	drawBox(color[T], x, y, size)
	x += 1
	drawBox(color[T], x, y, size)


def drawR(x, y, size = BOXSIZE):
	drawBox(color[R], x, y, size)
	y -= 1
	drawBox(color[R], x, y, size)
	x += 1
	drawBox(color[R], x, y, size)
	x -= 1
	y -= 1
	drawBox(color[R], x, y, size)


def drawH(x, y, size = BOXSIZE):
	drawBox(color[H], x, y, size)
	y -= 1
	drawBox(color[H], x, y, size)
	x -= 1
	drawBox(color[H], x, y, size)
	x += 1
	y -= 1
	drawBox(color[H], x, y, size)


def drawW(x, y, size = BOXSIZE):
	drawBox(color[W], x, y, size)
	x -= 1
	drawBox(color[W], x, y, size)
	x += 1
	y -= 1
	drawBox(color[W], x, y, size)
	x += 1
	y += 1
	drawBox(color[W], x, y, size)

		
def drawC(x, y, size = BOXSIZE):
	drawBox(color[C], x, y, size)
	y -= 1
	drawBox(color[C], x, y, size)
	x += 1
	y += 1
	drawBox(color[C], x, y, size)
	x += 1
	drawBox(color[C], x, y, size)


def drawG(x, y, size = BOXSIZE):
	drawBox(color[G], x, y, size)
	y -= 1
	drawBox(color[G], x, y, size)
	x -= 1
	y += 1
	drawBox(color[G], x, y, size)
	x -= 1
	drawBox(color[G], x, y, size)


def drawE(x, y, size = BOXSIZE):
	drawBox(color[E], x, y, size)
	y -= 1
	drawBox(color[E], x, y, size)
	x += 1
	drawBox(color[E], x, y, size)
	x += 1
	drawBox(color[E], x, y, size)


def drawD(x, y, size = BOXSIZE):
	drawBox(color[D], x, y, size)
	y -= 1
	drawBox(color[D], x, y, size)
	x -= 1
	drawBox(color[D], x, y, size)
	x -= 1
	drawBox(color[D], x, y, size)


def drawS(x, y, size):
	drawBox(color[S], x, y, size )
	x -= 1
	drawBox(color[S], x, y, size)
	x += 1
	y -= 1
	drawBox(color[S], x, y, size)
	x += 1
	drawBox(color[S], x, y, size)


def drawZ(x, y, size):
	drawBox(color[Z], x, y, size)
	x += 1
	drawBox(color[Z], x, y, size)
	x -= 1
	y -= 1
	drawBox(color[Z], x, y, size)
	x -= 1
	drawBox(color[Z], x, y, size)	


def drawJ(x, y, size):
	drawBox(color[J], x, y, size)
	x -= 1
	drawBox(color[J], x, y, size)
	x += 1
	y -= 1
	drawBox(color[J], x, y, size)
	y -= 1
	drawBox(color[J], x, y, size)


def drawL(x, y, size):
	drawBox(color[L], x, y, size)
	x += 1
	drawBox(color[L], x, y, size)
	x -= 1
	y -= 1
	drawBox(color[L], x, y, size)
	y -= 1
	drawBox(color[L], x, y, size)


def drawI(x, y, size):
	drawBox(color[I], x, y, size)
	y -= 1
	drawBox(color[I], x, y, size)
	y -= 1
	drawBox(color[I], x, y, size)
	y -= 1
	drawBox(color[I], x, y, size)	


def drawO(x, y, size):
	drawBox(color[O], x, y, size)
	x += 1
	drawBox(color[O], x, y, size)
	x -= 1
	y -= 1
	drawBox(color[O], x, y, size)
	x += 1
	drawBox(color[O], x, y, size)
	
	
def drawP(x, y, size):
	drawBox(color[P], x, y, size)
	y -= 1
	drawBox(color[P], x, y, size)
	y -= 1
	drawBox(color[P], x, y, size)
	x += 1
	drawBox(color[P], x, y, size)


def drawQ(x, y, size):
	drawBox(color[Q], x, y, size)
	y -= 1
	drawBox(color[Q], x, y, size)
	y -= 1
	drawBox(color[Q], x, y, size)
	x -= 1
	drawBox(color[Q], x, y, size)


def drawM(x, y, size):
	drawBox(color[M], x, y, size)
	x += 1
	drawBox(color[M], x, y, size)
	x += 1
	drawBox(color[M], x, y, size)
	x -= 3
	drawBox(color[M], x, y, size)

		
def drawN(x, y, size):
	drawBox(color[N], x, y, size)
	y -= 1
	drawBox(color[N], x, y, size)
	x += 1
	drawBox(color[N], x, y, size)
	y -= 1
	drawBox(color[N], x, y, size)
	
	
def drawF(x, y, size):
	drawBox(color[F], x, y, size)
	y -= 1
	drawBox(color[F], x, y, size)
	x -= 1
	drawBox(color[F], x, y, size)
	y -= 1
	drawBox(color[F], x, y, size)
	
	
if __name__ == '__main__':
	main()