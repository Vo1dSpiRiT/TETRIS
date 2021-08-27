import pygame
from pygame.math import Vector2
from random import randint
pygame.font.init()
from Piece import Piece

resolution = Vector2(1000, 700)
gridResolution = Vector2(300, 600)
rows = 20
cols = 10
blockSize = 30
gridPosition = Vector2((resolution.x - gridResolution.x) // 2, resolution.y - gridResolution.y)
WIN = pygame.display.set_mode((int(resolution.x), int(resolution.y)))
pygame.display.set_caption("TETRIS")
gameWin = pygame.Rect(int(gridPosition.x), int(gridPosition.y), int(gridResolution.x), int(gridResolution.y))

grid = []
lastScores = []
pieces = [
    [
        [1, 1],
        [1, 1]
    ],
    
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    
    [
        [0, 0, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    
    [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ],
    
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    
    [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0]
    ],
    
    [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
    ],
    ]

colors = [
    (255, 255, 0),
    (0, 255, 255),
    (255, 125, 0),
    (0, 0, 255),
    (150, 0, 255),
    (0, 255, 0),
    (255, 0, 0)
    ]

def collided(piece, grid):
    rectPositions = piece.getRectPositions()
    for rectPosition in rectPositions:
        if rectPosition.y >= 20:
            return True
        elif rectPosition.x <= -1:
            return True
        elif rectPosition.x >= cols:
            return True
        for fixedPiece in grid:
            for fixedRectPosition in fixedPiece[0]:
                if rectPosition.x == fixedRectPosition.x:
                    if rectPosition.y == fixedRectPosition.y:
                        return True
    return False

def checkLost(grid):
    for fixedPiece in grid:
        for fixedPosition in fixedPiece[0]:
            if fixedPosition.y <= 0:
                return True
            
def getNewFallSpeed(duration, fallSpeedLimit, initialFallSpeed):
    duration /= 500
    if duration < initialFallSpeed - fallSpeedLimit:
        return initialFallSpeed - duration
    return fallSpeedLimit

def checkFullRows(grid):
    Ytotal = []
    for fixedPiece in grid:
        for fixedPosition in fixedPiece[0]:
            Ytotal.append(fixedPosition.y)
    
    fullRows = []
    for row in range(rows):
        if Ytotal.count(row) == cols:
            fullRows.append(row)
    return fullRows

def deleteRows(fullRows):
    for i in range(len(grid)):
        for j in range(len(grid[i][0])-1, -1, -1):
            fixedPosition = grid[i][0][j]
            if fixedPosition.y in fullRows:
                grid[i][0].remove(fixedPosition)
            else:
                for row in fullRows:
                    if fixedPosition.y < row:
                        grid[i][0][j].y = fixedPosition.y + 1



def getNewPiece(x, y):
    pieceNumber = randint(0, 6)
    return Piece(WIN, x, y, blockSize, colors[pieceNumber], pieces[pieceNumber], gridPosition)


def drawFixedPieces(grid):
    for rectPositions, color in grid:
        for rectPosition in rectPositions:
            pygame.draw.rect(WIN, color, ((int(gridPosition.x + rectPosition.x * blockSize),
                                             int(gridPosition.y + rectPosition.y * blockSize),
                                             blockSize, blockSize)))
        

def drawMatrix():
    """for i in range(rows):
        pygame.draw.line(WIN, (128,128,128),
                         (int(gridPosition.x), int(gridPosition.y)+ i * blockSize),
                         (int(gridPosition.x) + int(gridResolution.x), int(gridPosition.y) + i * blockSize)
                        )
    for j in range(cols):
        pygame.draw.line(WIN, (128,128,128),
                         (int(gridPosition.x) + j * blockSize, int(gridPosition.y)),
                         (int(gridPosition.x) + j * blockSize, int(gridPosition.y) + int(gridResolution.y))
                        )"""
    pygame.draw.rect(WIN, (255, 0, 0), gameWin, 3)
    
def drawGameText(score, lastScores):
    font = pygame.font.SysFont("comicsans", 60)
    titleText = font.render("TETRIS", 1, (255,255,255))
    WIN.blit(titleText, (int(resolution.x / 2 - (titleText.get_width() / 2)), 30))
    
    font = pygame.font.SysFont("comicsans", 50)
    scoreText = font.render("SCORE", 1, (255, 255, 255))
    WIN.blit(scoreText, (int(gridPosition.x - gridResolution.x / 2 - (scoreText.get_width() / 2)), int(resolution.y / 2 - 90)))
    
    scoreNumberText = font.render(str(score), 1, (255, 255, 255))
    WIN.blit(scoreNumberText, (int(gridPosition.x - gridResolution.x / 2 - (scoreNumberText.get_width() / 2)), int(resolution.y / 2) - 25))
    
    nextText = font.render(("Next"), 1, (255, 255, 255))
    WIN.blit(nextText, (int(resolution.x / 2 + gridResolution.x - (nextText.get_width() / 2) + 27), int(resolution.y / 2 - 90)))
    
    if lastScores:
        topScoresText = font.render(("TOP 3:"), 1, (255, 255, 255))
        WIN.blit(topScoresText, (int(gridPosition.x - gridResolution.x / 2 - (topScoresText.get_width() / 2)), int(resolution.y / 2 + 120)))
        scoreNumberLimit = len(lastScores)
        if scoreNumberLimit > 3:
            scoreNumberLimit = 3
        for i in range(1, scoreNumberLimit+1):
            lastScoreText = font.render(str(lastScores[i-1]), 1, (255, 255, 255))
            WIN.blit(lastScoreText, (int(gridPosition.x - gridResolution.x / 2 - (lastScoreText.get_width() / 2) - 3), int(resolution.y / 2 + 120 + i * (50))))
            

def drawWindow(currentPiece, nextPiece, grid, score, lastScores):
    WIN.fill((0, 0, 0))
    currentPiece.draw()
    nextPiece.draw()
    drawFixedPieces(grid)
    drawMatrix()
    drawGameText(score, lastScores)
    
    pygame.display.update()

def main():
    global grid
    global scores
    clock = pygame.time.Clock()
    currentScore = 0
    currentPiece = getNewPiece(4, -1)
    nextPiece = getNewPiece(14.5, 7)
    fallSpeedLimit = 0.2
    initialFallSpeed = 0.6
    fallSpeed = initialFallSpeed
    fallTime = 0
    gameDuration = 0
    running = True
    while running:
        TimePerFrame  = clock.tick(60) * .001
        fallTime += TimePerFrame
        gameDuration += TimePerFrame
        if fallTime >= fallSpeed:
            currentPiece.move(0, 1)
            fallTime = 0
            if collided(currentPiece, grid):
                currentPiece.move(0, -1)
                grid.append((currentPiece.getRectPositions(), currentPiece.color))
                currentPiece = nextPiece
                currentPiece.position = Vector2(4, -1)
                nextPiece = getNewPiece(14.5, 7)
                fullRows = checkFullRows(grid)
                if fullRows:
                    deleteRows(fullRows)
                    currentScore += (len(fullRows) * 100) + ((len(fullRows)-1) * 20)
                    
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.move(-1, 0)
                    if collided(currentPiece, grid):
                        currentPiece.move(1, 0)

                if event.key == pygame.K_RIGHT:
                    currentPiece.move(1, 0)
                    if collided(currentPiece, grid):
                        currentPiece.move(-1, 0)
                
                if event.key == pygame.K_UP:
                    currentShape = currentPiece.shape
                    currentPiece.rotateShape()
                    if collided(currentPiece, grid):

                        currentPiece.shape = currentShape
                if event.key == pygame.K_DOWN:
                    currentPiece.move(0, 1)
                    if collided(currentPiece, grid):
                        currentPiece.move(0, -1)
                    else:
                        currentScore += 1
            
        currentPiece.update()
        fallSpeed = getNewFallSpeed(gameDuration, fallSpeedLimit, initialFallSpeed)
        if checkLost(grid):
            grid.clear()
            lastScores.append(currentScore)
            lastScores.sort(reverse=True)
            currentScore = 0
            gameDuration = 0
        drawWindow(currentPiece, nextPiece, grid, currentScore, lastScores)

    pygame.quit()



if __name__ == "__main__":
    main()