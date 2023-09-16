import pygame
import pygame.font

def main():
    COLOR = (255, 100, 98)
    SURFACE_COLOR = (167, 255, 100)
    colour = (90, 180, 120)
    colourb = (180, 200, 180)
    selectColour = (255, 120, 120)

    '''
    try: input = int(input("How many players(1/2): "))
    except: print("Please input a correct number, though im lazy so ur starting in 2 player mode :P")
    if input>2 or input<1:
        print("Please input a correct number, though im lazy so ur starting in 2 player mode :P") '''

    pygame.init()

    canvas = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chessish kindof thing")

    board = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
    
    turn = "w"
    halfmoves = 0

    piecesRemainingW = ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    piecesRemainingB = ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"]

    pieceMoves = {
        "k": king_move,
        "p": pawn_move,
        "r": rook_move,
        "b": bishop_move,
        "n": knight_move,
        "q": queen_move
        }


    tileList = pygame.sprite.Group()
    
    def find_element(Intlist, searchObj,refList):
        y=0
        for i in Intlist:
            if i == searchObj: break
            y+=1
        for i in range(len(refList)):
            for j in range(len(refList[i])):
                if refList[i][j] == y:
                    return [i, j]
        return -1

    colourchange = False

    for i in range(8):
        colourchange = not colourchange
        for j in range(8): 
            if colourchange: 
                intcolour = colour
            else: intcolour = colourb
            colourchange = not colourchange
            tileList.add(Tile(i*100, j*100, intcolour, 100, 100))


    refList = []
    x=0
    for i in range(8):
        inList = []
        for j in range(8):
            inList.append(x)
            x+=1
        refList.append(inList.copy())
        inList.clear()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Left Click
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in tileList if s.rect.collidepoint(pygame.mouse.get_pos())]
                for i in clicked_sprites:
                    if i.selected:
                        i.selected = False
                        if i.cb:
                            pygame.draw.rect(i.image,
                                colourb,
                                pygame.Rect(0, 0, i.width, i.height))
                        else:
                            pygame.draw.rect(i.image,
                                colour,
                                pygame.Rect(0, 0, i.width, i.height))
                        for j in tileList.sprites():
                            if j.selected:
                                j.selected = False
                                if j.cb:
                                    pygame.draw.rect(j.image,
                                        colourb,
                                        pygame.Rect(0, 0, j.width, j.height))
                                else:
                                    pygame.draw.rect(j.image,
                                        colour,
                                        pygame.Rect(0, 0, j.width, j.height))
                    else:
                        for j in tileList.sprites():
                            if j.selected:
                                j.selected = False
                                if j.cb:
                                    pygame.draw.rect(j.image,
                                        colourb,
                                        pygame.Rect(0, 0, j.width, j.height))
                                else:
                                    pygame.draw.rect(j.image,
                                        colour,
                                        pygame.Rect(0, 0, j.width, j.height))
                        i.selected = True
                        pygame.draw.rect(i.image,
                                    selectColour,
                                    pygame.Rect(0, 0, i.width, i.height), 2)
                    if i.moveable:
                        [x, y] = find_element(tileList.sprites(), i, refList)
                        a, b = i.oldLoc
                        if i.pieceSelected[1] == "p" and a == 1 and y == 3:
                            board[2][x] = "be"
                        if i.pieceSelected[1] == "p" and a == 6 and y == 4:
                            board[5][x] = "we"
                        if board[y][x] == "we":
                            board[y-1][x] = " "
                        if board[y][x] == "be":
                            board[y+1][x] = " "
                        board[a][b] = " "
                        if i.pieceSelected == "wp" and y == 0:
                             board[y][x] = "wq"
                        elif i.pieceSelected == "bp" and y == 7:
                             board[y][x] = "bq"
                        else: board[y][x] = i.pieceSelected
                        if turn == "w":
                            for i in pieceList:
                                if i.colour == "b":
                                    for j in pieceMoves[i.piece](board, int(i.rect.y/100), int(i.rect.x/100)):
                                        if is_check(board, turn, pieceMoves, j, i.piece, (a,b)):
                                            break
                                    else: continue
                                    break
                                else: 
                                    if is_check(board, turn, pieceMoves, (int(i.rect.y/100), int(i.rect.x/100)), i.piece, (int(i.rect.y/100), int(i.rect.x/100))):
                                        return "Draw by stalemate"
                                    return "White wins by checkmate"
                            turn = "b"
                            for j in range(len(board)):
                                for k in range(len(board[j])):
                                    if "be" in board[j][k]:
                                        board[j][k] = " "
                        else: 
                            for i in pieceList:
                                if i.colour == "w":
                                    for j in pieceMoves[i.piece](board, int(i.rect.y/100), int(i.rect.x/100)):
                                        if is_check(board, turn, pieceMoves, k, board[b][a], (a,b)):
                                            break
                                    else: break
                                else: 
                                    if is_check(board, turn, pieceMoves, (int(i.rect.y/100), int(i.rect.x/100)), i.piece, (int(i.rect.y/100), int(i.rect.x/100))):
                                        return "Draw by stalemate"
                                    return "Black wins by checkmate"
                            turn = "w"
                            for j in range(len(board)):
                                for k in range(len(board[j])):
                                    if "we" in board[j][k]:
                                        board[j][k] = " "
                        if halfmoves>=50: return "draw by 50 move rule"
                        wcanMate = False
                        for i in ["wr", "wp", "wq"]:
                            if i in piecesRemainingW:
                                wcanMate = True
                                break
                        bishopCount = 0
                        knightCount = 0
                        for i in piecesRemainingW:
                            if "b" in i: bishopCount+=1
                            if "n" in i: knightCount+=1
                        if bishopCount>=2 or knightCount>=3: wcanMate = True
                        bcanMate = False
                        for i in ["br", "bp", "bq"]:
                            if i in piecesRemainingB:
                                bcanMate = True
                                break
                        bishopCount = 0
                        knightCount = 0
                        for i in piecesRemainingB:
                            if "b" in i: bishopCount+=1
                            if "n" in i: knightCount+=1
                        if bishopCount>=2 or knightCount>=3: bcanMate = True
                        if not bcanMate and not wcanMate: return "draw by insufficient material"
                        # Lmao im not making draw by repetition im sorry
                        # if I ever add fgn i will but b4 that f you lol

        
                for i in tileList:
                    if i.cb:
                            pygame.draw.rect(i.image,
                                colourb,
                                pygame.Rect(0, 0, i.width, i.height))
                    else:
                        pygame.draw.rect(i.image,
                            colour,
                            pygame.Rect(0, 0, i.width, i.height))
                    i.moveable = False
                    i.pieceSelected = " "
                    i.oldLoc = " "
                    
        
            pieceList = []
            for i in range(8):
                for j in range(8):
                    if board[j][i] != " " and not "e" in board[j][i]:
                        pieceList.append(Piece(i, j, board[j][i][0], board[j][i][1]))            
            for i in tileList.sprites():
                if i.selected:
                    x, y = i.rect.x, i.rect.y
                    [a, b] = find_element(tileList.sprites(), i, refList)
                    for j in pieceList:
                        if j.rect.x == x and j.rect.y == y and board[b][a][0] == turn:
                            for k in pieceMoves[j.piece](board, b, a):
                                if is_check(board, turn, pieceMoves, k, board[b][a], (a,b)):
                                    MoveTo = tileList.sprites()[refList[k[1]][k[0]]]
                                    pygame.draw.circle(MoveTo.image, (255, 255, 255), (50,50), 20)
                                    MoveTo.moveable = True
                                    MoveTo.pieceSelected = board[b][a]
                                    MoveTo.oldLoc = [b, a]
        tileList.draw(canvas)
        for i in pieceList:
            canvas.blit(i.image, (i.rect.x, i.rect.y))
        pygame.display.update()

# Thanks ChatGPT (shhh)
def king_move(lst, row, col):
    adjacent_places = []
    rows = len(lst)
    cols = len(lst[0])

    # Define the neighboring positions
    positions = [
        (row - 1, col),     # Top
        (row + 1, col),     # Bottom
        (row, col - 1),     # Left
        (row, col + 1),     # Right
        (row - 1, col - 1), # Top Left
        (row - 1, col + 1), # Top Right
        (row + 1, col - 1), # Bottom Left
        (row + 1, col + 1)  # Bottom Right
    ]

    # Iterate over the neighboring positions
    for position in positions:
        r, c = position
        # Check if the neighboring position is within bounds
        if 0 <= r < rows and 0 <= c < cols and lst[r][c][0]!= lst[row][col][0]:
            adjacent_places.append([r,c])

    return adjacent_places


def pawn_move(lst, row, col):
    moves = []
    if lst[row][col][0] == "b":
        if row+1>7:
            return moves
        if lst[row + 1][col] == " ":
            moves.append([row+1, col])
            # double move add en passant to fgn :/
            if row == 1 and lst[row + 2][col] == " ":
                moves.append([row+2, col])
        if col+1<8 and (lst[row + 1][col+1][0] != lst[row][col][0] or lst[row + 1][col+1] == "we") and lst[row + 1][col+1] != " ":
            moves.append([row+1, col+1])
        if col-1>-1 and (lst[row + 1][col-1][0] != lst[row][col][0] or lst[row + 1][col-1] == "we") and lst[row + 1][col-1] != " ":
            moves.append([row+1,col-1])
    if lst[row][col][0] == "w":
        if row-1<-1:
            return moves
        if lst[row - 1][col] == " ":
            moves.append([row-1, col])
             # double move add en passant to fgn :/
            if row == 6 and lst[row - 2][col] == " ":
                moves.append([row-2, col])
        if col+1<8 and (lst[row - 1][col+1][0] != lst[row][col][0] or lst[row - 1][col+1] == "be") and lst[row - 1][col+1] != " ":
            moves.append([row-1, col+1])
        if col-1>-1 and (lst[row - 1][col-1][0] != lst[row][col][0] or lst[row - 1][col-1] == "be") and lst[row - 1][col-1] != " ":
            moves.append([row-1, col-1])
    return moves

def rook_move(lst, row, col):
    moves = []
    for i in range(col-1, -1, -1):
        if lst[row][i] == " ": 
            moves.append([row, i])
        elif lst[row][i][0] == lst[row][col][0]: 
            break
        else:
            moves.append([row, i])
            break
    for i in range(col+1, 8):
        if lst[row][i] == " ": 
            moves.append([row, i])
        elif lst[row][i][0] == lst[row][col][0]: 
            break
        else:
            moves.append([row, i])
            break
    for i in range(row-1, -1, -1):
        if lst[i][col] == " ": 
            moves.append([i, col])
        elif lst[i][col][0] == lst[row][col][0]: 
            break
        else:
            moves.append([i, col])
            break
    for i in range(row+1, 8):
        if lst[i][col] == " ": 
            moves.append([i, col])
        elif lst[i][col][0] == lst[row][col][0]: 
            break
        else:
            moves.append([i, col])
            break
    return moves

def bishop_move(lst, row, col):
    moves = []
    i,j = row-1, col+1
    while i>-1 and j<8:
        if lst[i][j] == " " or  lst[i][j] == "e": 
            moves.append([i, j])
        elif lst[i][j][0] == lst[row][col][0]: 
            break
        else:
            moves.append([i, j])
            break
        i-=1
        j+=1
    i,j = row+1, col+1
    while i<8 and j<8:
        if lst[i][j] == " " or  lst[i][j] == "e": 
            moves.append([i, j])
        elif lst[i][j][0] == lst[row][col][0]: 
            break
        else:
            moves.append([i, j])
            break
        i+=1
        j+=1
    i,j = row-1, col-1
    while i>-1 and j>-1:
        if lst[i][j] == " " or  lst[i][j] == "e": 
            moves.append([i, j])
        elif lst[i][j][0] == lst[row][col][0]: 
            break
        else:
            moves.append([i, j])
            break
        i-=1
        j-=1
    i,j = row+1, col-1
    while i<8 and j>-1:
        if lst[i][j] == " " or  lst[i][j] == "e": 
            moves.append([i, j])
        elif lst[i][j][0] == lst[row][col][0]: 
            break
        else:
            moves.append([i, j])
            break
        i+=1
        j-=1
    return moves

def knight_move(lst, row, col):
    moves = []
    if row-2>-1:
        if col+1<8 and lst[row-2][col+1][0] != lst[row][col][0]:
            moves.append([row-2, col+1])
        if col-1>-1 and lst[row-2][col-1][0] != lst[row][col][0]:
            moves.append([row-2, col-1])
    if row+2<8:
        if col+1<8 and lst[row-2][col+1][0] != lst[row][col][0]:
            moves.append([row+2, col+1])
        if col-1>-1 and lst[row-2][col-1][0] != lst[row][col][0]:
            moves.append([row+2, col-1])
    if col-2>-1:
        if row+1<8 and lst[row+1][col-2][0] != lst[row][col][0]:
            moves.append([row+1, col-2])
        if row-1>-1 and lst[row-1][col-2][0] != lst[row][col][0]:
            moves.append([row-1, col-2])
    if col+2<8:
        if row+1<8 and lst[row+1][col+2][0] != lst[row][col][0]:
            moves.append([row+1, col+2])
        if row-1>-1 and lst[row-1][col+2][0] != lst[row][col][0]:
            moves.append([row-1, col+2])
    return moves

def queen_move(lst, row, col):
    moves = [rook_move(lst, row, col), bishop_move(lst, row, col)]
    moves = [j for i in moves for j in i]
    return moves

def is_check(oldlst, turn, pieceMoves, move, piece, oldloc):
    canMove = True
    lst = []
    for i in oldlst:
        lst.append(i.copy())
    lst[oldloc[1]][oldloc[0]] = " "
    lst[move[0]][move[1]] = piece
    for i in lst:
        for j in i:
            if j[0] == turn:
                for a in range(len(lst)):
                    for b in range(len(lst[a])):
                        if len(lst[a][b])>1 and lst[a][b][0]!= turn and not "e" in lst[a][b]:
                            for k in pieceMoves[lst[a][b][1]](lst, a, b):
                                if ("k" in lst[k[0]][k[1]]):
                                    canMove = False
    return canMove

class Piece(pygame.sprite.Sprite):
    def __init__(self, locx, locy, colour, piece):
        super().__init__()
        img = pygame.image.load(f"images\\{colour}{piece}.png")
        img = pygame.transform.scale(img,(100,100))

        self.image = img
        self.colour = colour
        self.piece = piece

        self.rect = self.image.get_rect()
        self.rect.x = locx*100
        self.rect.y = locy*100


class Tile(pygame.sprite.Sprite):
    def __init__(self, locx, locy, colour, height, width):
        super().__init__()
  
        self.image = pygame.Surface([width, height])

        self.width = width
        self.height = height

        pygame.draw.rect(self.image,
                         colour,
                         pygame.Rect(0, 0, width, height))

        self.cb = False
        if colour != (90, 180, 120): self.cb = True

        self.oldLoc = [0,0]
        self.moveable = False
        self.pieceSelected = " "
        self.selected = False

        self.rect = self.image.get_rect()
        self.rect.x = locx
        self.rect.y = locy

if __name__ == "__main__":
    print(main())