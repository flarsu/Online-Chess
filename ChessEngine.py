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
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.Checkmate = False
        self.Stalemate = False
              

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] ='0'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)    

    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)    
    def getValidMoves(self):
        moves =  self.getAllPossibleMoves()
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()    
        if len(moves)==0:
            if self.inCheck():
                self.Checkmate = True
            else:
                self.Stalemate = True
        else:
            self.Checkmate = False
            self.Stalemate = False                

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.sqInAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.sqInAttack(self.blackKingLocation[0], self.blackKingLocation[1])    

    def sqInAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        

    def getAllPossibleMoves(self):
        moves = []
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
                    if piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    if piece == 'Q':
                        self.getQueenMoves(r, c, moves)    

                    if piece == 'K':
                        self.getKingMoves(r, c, moves)    



                        
        return moves


    def getPawnMoves(self,r, c, moves):
            if self.whiteToMove:
                if r == 0:
                    self.board[r][c] = 'wQ'
                    
                else:
                    if self.board[r-1][c] == '0':
                        moves.append(Move((r,c),(r-1,c), self.board))
                        if r==6 and self.board[r-2][c]=='0':
                            moves.append(Move((r,c),(r-2,c),self.board))
                    if c-1>=0:
                        if self.board[r-1][c-1][0]== 'b':
                            moves.append(Move((r,c),(r-1,c-1),self.board))
                    if c+1<=7:
                        if self.board[r-1][c+1][0]=='b':
                            moves.append(Move((r,c),(r-1,c+1),self.board))
            else:
                if r == 7:
                    self.board[r][c] = 'bQ'
                else:
                    if self.board[r+1][c] == '0':
                        moves.append(Move((r,c),(r+1,c), self.board))
                        if r==1 and self.board[r+2][c]=='0':
                            moves.append(Move((r,c),(r+2,c),self.board))
                    if c-1>=0:
                        if self.board[r+1][c-1][0]== 'w':
                            moves.append(Move((r,c),(r+1,c-1),self.board))
                    if c+1<=7:
                        if self.board[r+1][c+1][0]=='w':
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
    def getBishopMoves(self, r, c, moves):
        opposite = 'b' if  self.whiteToMove else 'w'
        directions = ((1,1),(1,-1),(-1,1),(-1,-1))

        for d in directions:
            for i in range(1,8):
                endRow = r+ d[0]*i
                endCol = c+ d[1]*i

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
                        
                        
    def getQueenMoves(self, r, c, moves):
        opposite = 'b' if  self.whiteToMove else 'w'
        directions = ((1,1),(1,-1),(-1,1),(-1,-1),(-1,0),(1,0),(0,-1),(0,1))
        for d in directions:
            for i in range(1,8):
                endRow = r+ d[0]*i
                endCol = c+ d[1]*i

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
    def getKingMoves(self, r, c, moves):
        opposite = 'b' if  self.whiteToMove else 'w'
        directions = ((1,1),(1,-1),(-1,1),(-1,-1),(-1,0),(1,0),(0,-1),(0,1))
        for d in directions:
            endRow = r + d[0]  
            endCol = c + d[1]

            if 0<=endRow<8 and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece== '0' or endPiece[0]==opposite:
                    moves.append(Move((r,c),(endRow,endCol), self.board))
                else:
                    continue
            else:
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

