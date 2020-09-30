import pygame as p

import ChessEngine as cE

WIDTH = HEIGHT = 680
DIMENSION = 8

SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
Images = {}

def load_images():
    pieces = ['bR','bN','bB','bQ','bK','bP', 'wQ','wK','wB','wN','wR','wP']
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load('./images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))




def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = cE.GameState()
    validMoves= gs.getValidMoves()
    madeMove = False
    load_images()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks)==2 :
                    move = cE.Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        madeMove = True
                    sqSelected =()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()      
                    madeMove = True
        if madeMove:
            validMoves = gs.getValidMoves()
            madeMove = False          
            
        elif gs.Stalemate:
            print('Draw')           
               
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()     


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    if gs.Checkmate:
            if gs.whiteToMove:
                drawText(screen,'Black Won', (255,255,255))
            else:
            
                drawText(screen,'White Won', (0,0,0))
            

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('dark red')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j)%2)]
            p.draw.rect(screen, color, p.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))



def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece!= '0':
                screen.blit(Images[piece],p.Rect(j*SQ_SIZE,i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawText(screen, text, color):
    font = p.font.Font('futur.ttf', 64) 
    text = font.render(text,True, color)
    textRect = text.get_rect()
    textRect.center = DIMENSION*SQ_SIZE//2,DIMENSION*SQ_SIZE//2
    screen.blit(text, textRect)
if __name__ == '__main__':
    main()