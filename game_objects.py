import pygame

class Block():
    def __init__(self, screen, x, y, width, height, color):
        self.screen = screen
        self.screen_width = screen.get_rect().right
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

def init(screen):
    global obstacles
    obstacles = []
    # block1 = Block(screen, 220, 520, 200, 20, (255,0,0))
    block2 = Block(screen, 500, 475, 200, 20, (255,0,0))
    block3 = Block(screen, 225, 350, 200, 20, (255,0,0))
    block4 = Block(screen, 525, 250, 75, 20, (255, 0, 0))
    block5 = Block(screen, 700, 250, 100, 20, (255, 0, 0))
    block6 = Block(screen, 310, 0, 100, 220, (128, 128, 128))
    start_block = Block(screen, 50, 530, 50, 110, (0,0,255))
    end_block = Block(screen, 900, 430, 50, 210, (0, 0, 255))

    # obstacles.append(block1)
    obstacles.append(block2)
    obstacles.append(block3)
    obstacles.append(block4)
    obstacles.append(block5)
    obstacles.append(block6)
    obstacles.append(start_block)
    obstacles.append(end_block)