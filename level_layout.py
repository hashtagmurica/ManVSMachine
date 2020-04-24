import random

class SolutionPath(object):
    def __init__(self):
        self.findSolution()
        for row in self.level:
            print(row)

    def findSolution(self):
        '''
            Random Level Generation, modeled after Spelunky
            Reference: http://tinysubversions.com/spelunkyGen/

            This algorithm creates a 4x4 matrix of rooms and assigns
            each a value, 0-3
                0 rooms are not part of solution path
                1 rooms can be passed through left and right
                2 rooms can be passed through left, right, and bottom
                3 rooms can be passed through left, right, and top

            Upon generation, the sequence of rooms is guaranteed to have
            a continuous path from the top row to the bottom row
        '''
        self.level = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        i = 0
        j = random.randint(0,3)

        # Make random room in top row a 1
        self.level[i][j] = 1

        # Decide where to go next randomly
        # 1 or 2 = Left; 3 or 4 = Right; 5 = Down
        # Moving left into left edge or right into right edge
        # calls for moving down instead
        while i < 3:
            go = random.randint(1,5)
            dropped = False
            if go == 1 or go==2:
                if j - 1 < 0:
                    if self.level[i][j] == 3:
                        continue
                    dropped = True
                    self.level[i][j] = 2
                    i += 1
                else:
                    j -= 1
            elif go==3 or go==4:
                if j + 1 > 3:
                    if self.level[i][j] == 3:
                        continue
                    dropped = True
                    self.level[i][j] = 2
                    i += 1
                else:
                    j += 1
            else:
                if self.level[i][j] == 3:
                    continue
                dropped = True
                self.level[i][j] = 2
                i += 1
            # Place next room
            if dropped or self.level[i][j] == 3:
                self.level[i][j] = 3
            else:
                self.level[i][j] = 1

room1 = [
    "      XXXXXXXXXXXX  ",
    "XXXXXXXXXXXXXXXXXXXX ",
    "                    ",
    "                    ",
    "                    ",
    "         XXXXX      ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "          XXXXXXXX  ",
    "                    ",
    "                    ",
    "  XXXXXXX           ",
    "                    ",
    "                    ",
    "                    ",
    "XXXXXXX   XXXXXXXXXX",
    "     XXXXXXXXXXXXXX "
]

room1_2 = [
    "  XXXXXXXXXXXXX   XX",
    "XXXXXXXXXXXXXXXXXXXX ",
    "                    ",
    "          XXXX      ",
    "               XX   ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    " XXXXXX             ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "         XXXXXXXXXXX",
    "                    ",
    "      XXXXXXXXX  XXX",
    "   XXX    XX  XXXX  ",
    "XXXXXXXX            "
]

room2 = [
    "  XXXXXXXXXXXXX   XX",
    "XXXXXXXXXXXXXXXXXXXX ",
    "                    ",
    "          XXXX      ",
    "                    ",
    "                    ",
    "            XXX     ",
    "                    ",
    "                    ",
    "    XXX             ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "               XXXXX",
    "                    ",
    "XXXX                ",
    "   XXX        XXXX  ",
    "                    "
]

room2_2 = [
    "  XXXXXXXXXXXXX   XX",
    "XXXXXXXXXXXXXXXXXXXX ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "   XXXXXXXXXX       ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "            XXXXXXXX",
    "                    ",
    "XXXXXXXXX           ",
    "   XXX          XXXX",
    "                    "
]

room3 = [
    "  XXX        XX   XX",
    "XXXXXXXX    XXXXXXXX ",
    "                    ",
    "                    ",
    "               XX   ",
    "         XXXXX      ",
    "                    ",
    "                    ",
    "                    ",
    " XXXXXX             ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "         XXXXXXXXXXX",
    "                    ",
    " XXXX XXXXXXXXX     ",
    "   XXX    XX  XXXX X",
    "                    "
]

room3_2 = [
    "  XXXXXXXX        XX",
    "XXXXX         XXXXXX ",
    "                    ",
    "          XXXX      ",
    "               XX   ",
    "       XX           ",
    "                    ",
    "                    ",
    "                    ",
    " XXXXXX             ",
    "                    ",
    "                    ",
    "           XXX      ",
    "                    ",
    "                    ",
    "         XXXXXXXXXXX",
    "XXXXXXXXX           ",
    "      XXXXXXXXX     ",
    "   XXX    XX  XXXX  ",
    "                    "
]

room0 = [
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    "
]

room0_2 = [
    "                    ",
    "                    ",
    "                    ",
    "    XXX             ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "        XXXXXXXXX   ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "   XXXXXXXX         ",
    "                    ",
    "                    ",
    "                    ",
    "                    "
]
