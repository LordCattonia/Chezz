import random
import pygame
import pygame.font

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
colour = (90, 180, 120)
colourb = (180, 200, 180)
canvasColour = (120, 120, 120)

pygame.init()

  
canvas = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chessish kindof thing")

font = pygame.font.Font(None, 50)
def main():
    # Make the map of mines and put it through the processing function.


    spriteList = pygame.sprite.Group()
    
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
            spriteList.add(Sprite(i*100, j*100, intcolour, 100, 100))


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
                clicked_sprites = [s for s in spriteList if s.rect.collidepoint(pygame.mouse.get_pos())]
                for i in clicked_sprites:
                    x, y = 0, 0
                    [x, y] = find_element(spriteList, i, refList)

                    pygame.draw.rect(i.image,
                                canvasColour,
                                pygame.Rect(0, 0, i.width, i.height))

                    # Get centre
                    square_center_x = i.width // 2
                    square_center_y = i.height // 2

                    # Render the text
                    text_surface = font.render(str(map[x][y]), True, (0, 0, 0))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (square_center_x, square_center_y)

                    # Draw the text on the square's surface
                    i.image.blit(text_surface, text_rect.topleft)
                   
        spriteList.draw(canvas)
        pygame.display.update()


# Thanks ChatGPT (shhh)
def find_adjacent_places(lst, row, col):
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
        if 0 <= r < rows and 0 <= c < cols:
            adjacent_places.append([r,c])

    return adjacent_places

class Sprite(pygame.sprite.Sprite):
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
        if colour != (25, 200, 10): self.cb = True

        self.rect = self.image.get_rect()
        self.rect.x = locx
        self.rect.y = locy

if __name__ == "__main__":
    main()