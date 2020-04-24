import pygame

obstacles = []

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
    random.seed(time.time())
    global obstacles
    obstacles = []

    count = 1

    # place goal block randomly
    len1 = 50
    x1 = random.randint(0, 911)
    y1 = random.randint(160, 441)
    goal = Block(screen, x1, y1, len1, 20, (0, 0, 255))

    obstacles.append(goal)

    while not len(obstacles) == 5:
        invalid = False
        # special considerations for last block to be reachable from ground
        if len(obstacles) == 4:
            pass
        # special consideration for 2nd to last block to be reachable from last
        if len(obstacles) == 3:
            pass

        # place next block within reach of previous block
        len2 = random.randint(75, 276)
        x2 = random.randint(x1-len2-80, x1+len1+80)
        y2 = random.randint(max(160, y1-185), y1+185)
        
        print(count, "next block values picked")

        # adjust reach if previous block is right above/below
        if x2 >= x1 and x2 < x1+len1:
            while y2 >= y1 and y2 < y1+80:
                y2 = random.randint(max(160, y1-185), y1+185)
        if x2 < 0:
            x2 = 0

        print(count, "adjust for block above/below")

        # if out of bounds or overlaps with another block, restart process
        if x2+len2 > 960 or y2+20 > 640:
            invalid = True
        for block in obstacles:
            x2s = set(range(x2, x2+len2+1))
            y2s = set(range(y2,y2+20+1))
            bxs = set(range(block.x, block.x + block.width + 1))
            bys = set(range(block.y, block.y + block.height + 1))
            if not len(x2s.intersection(bxs))==0 or not len(y2s.intersection(bys))==0:
                pass
                #invalid = True

        print(count, "set compare")

        # if valid, add block to level and prepare to add next
        if invalid:
            print(count, "invalid block")
            continue
        else:
            x1 = x2
            y1 = y2
            len1 = len2
            block = Block(screen, x2, y2, len2, 20, (255, 50, 50))
            obstacles.append(block)
            print("block", count, "works")
            count = count + 1



    '''
    block1 = Block(screen, 540, 520, 200, 20, (255,150,150))
    block2 = Block(screen, 655, 435, 100, 20, (255,50,0))
    block3 = Block(screen, 525, 250, 50, 20, (255, 100, 0))
    block4 = Block(screen, 700, 250, 100, 20, (255, 0, 0))
    end_block = Block(screen, 900, 430, 50, 210, (0, 0, 255))
    block5 = Block(screen, 310, 0, 100, 220, (128, 128, 128))
    start_block = Block(screen, 50, 530, 50, 110, (0,0,255))


    obstacles.append(block1)
    obstacles.append(block2)
    obstacles.append(block3)
    obstacles.append(block4)
    obstacles.append(end_block)
    obstacles.append(block5)
    # obstacles.append(start_block)
    '''
