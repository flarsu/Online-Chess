class GameState() :
    
    def __init__(self):
        self.board = [
                ['bR','bN','bB','bQ','bK','bB','bN','bR'],
                ['bP','bP','bP','bP','bP','bP','bP','bP'],
                ['0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0'],
                ['wP','wP','wP','wP','wP','wP','wP','wP'],
                ['wR','wN','wB','wQ','wK','wB','wN','wR']
                ]

        self.whiteToMove = True
        self.moveLog = []            

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] ='0'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = [Move((1,0),(2,0), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn  = self.board[r][c][0]
                if (turn=='w'and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    if piece == 'R':
                        self.getRookMoves(r, c, moves)    

                    if piece == 'N':
                        self.getNightMoves(r, c, moves)    
                        
        return moves


    def getPawnMoves(self,r, c, moves):
            if self.whiteToMove:
                if self.board[r-1][c] == '0' :
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if self.board[r-2][c]=='0' and r==6:
                       moves.append(Move((r,c),(r-2, c),self.board))
                if c-1>=0:
                    if self.board[r-1][c-1][0] == 'b':
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                if c+1<=len(self.board[0])-1:    
                    if self.board[r-1][c+1][0]=='b' :
                        moves.append(Move((r,c),(r-1,c+1),self.board))       

            if not self.whiteToMove:
                if self.board[r+1][c] == '0' or self.board[r+2][c]=='0':
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if self.board[r+2][c]=='0' and r==1:
                       moves.append(Move((r,c),(r+2, c),self.board))
                if c-1>=0:
                    if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r,c),(r+1,c-1),self.board))
                if c+1<=len(self.board[0])-1:    
                    if self.board[r+1][c+1][0]=='w' :
                        moves.append(Move((r,c),(r+1,c+1),self.board))  

    def getRookMoves(self, r, c, moves):
       opposite = 'b' if self.whiteToMove  else 'w'
       directions = ((-1,0),(1,0),(0,-1),(0,1))

       for d in directions:
           for i in range(1,8):
               endRow = r +d[0]*i
               endCol = c +d[1]*i

               if 0<=endRow<8 and 0<=endCol<8:
                   endPiece = self.board[endRow][endCol]
                   if endPiece == '0':
                       moves.append(Move((r,c),(endRow,endCol), self.board))
                   elif endPiece[0] == opposite:
                       moves.append(Move((r,c),(endRow, endCol), self.board))
                       break
                   else:
                       break
               else:
                   break            

    def getNightMoves(self, r, c, moves):
        opposite = 'b' if  self.whiteToMove else 'w'
        directions = ((1,2),(-1,2),(2,1),(-2,1),(1,-2),(-1,-2),(2,-1),(-2,-1))
        for d in directions:
            endRow = r + d[0]  
            endCol = c + d[1]

            if 0<=endRow<8  and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == opposite or endPiece == '0':
                    moves.append(Move((r,c),(endRow,endCol), self.board))
                else :
                    continue
            else :
                continue    



class Move():
    ranksToRows = {'1':7,'2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v : k for k,v in ranksToRows.items()}
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v :k for k, v in filesToCols.items()}
    def __init__(self,startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow*1000+self.startCol*100 +self.endRow*10+self.endCol
        # print(self.moveId)
 # Override
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False        

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+ self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]    

