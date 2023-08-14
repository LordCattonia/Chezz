import random
import pygame
import pygame.font

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

font = pygame.font.Font(None, 100)

board = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
         ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

def main():
    
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
                        
                   
        tileList.draw(canvas)
        for i in tileList.sprites():
            [x, y] = find_element(tileList.sprites(), i, refList)
            if board[y][x] != " ":
                img = pygame.image.load(f"images\\{board[y][x]}.png")
                img = pygame.transform.scale(img,(100,100))
                canvas.blit(img, i)
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
            moves.append([row+1][col])
            # double move add en passant to fgn :/
            if row == 1 and lst[row + 2][col] == " ":
                moves.append([row-2][col])
        if col+1<7 and lst[row + 1][col+1] != " ":
            moves.append([row+1][col+1])
        if col-1>-1 and lst[row + 1][col-1] != " ":
            moves.append([row+1][col-1])
    if lst[row][col][0] == "w":
        if row-1<-1:
            return moves
        if lst[row - 1][col] == " ":
            moves.append([row-1][col])
             # double move add en passant to fgn :/
            if row == 7 and lst[row - 2][col] == " ":
                moves.append([row-2][col])
        if col+1<7 and lst[row + 1][col+1] != " ":
            moves.append([row+1][col+1])
        if col-1>-1 and (lst[row + 1][col-1] != " " or lst[row + 1][col-1] != "e"):
            moves.append([row+1][col-1])
    return moves

def rook_move(lst, row, col):
    moves = []
    for i in range(col-1, -1, -1):
        if lst[row][i] == " ": 



class Piece(pygame.sprite.Sprite):
    def __init__(self, locx, locy, colour, height, width, piece):
        super().__init__()
  
        self.image = pygame.Surface([width, height])

        img = pygame.image.load(f"images\\{colour}{piece}.png")
        img = pygame.transform.scale(img,(100,100))
        canvas.blit(img, self.image)

        self.colour = colour
        self.piece = piece

        def moveset(self):



        self.rect = self.image.get_rect()
        self.rect.x = locx*100
        self.rect.y = locy*100


class Tile(pygame.sprite.Sprite):
    def __init__(self, locx, locy, colour, height, width):
        super().__init__()
  
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)

        self.width = width
        self.height = height

        pygame.draw.rect(self.image,
                         colour,
                         pygame.Rect(0, 0, width, height))

        self.cb = False
        if colour != (90, 180, 120): self.cb = True

        self.selected = False

        self.rect = self.image.get_rect()
        self.rect.x = locx
        self.rect.y = locy

if __name__ == "__main__":
    main()