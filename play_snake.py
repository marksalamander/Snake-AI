import pygame
import sys
import random

pygame.init()

SW, SH = 600,600
BLOCK_SIZE = 30
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE*2)
DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xDir = 1
        self.yDir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.wall_collision = False
        self.self_collision = False

    def update(self):
        global food

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.self_collision = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.wall_collision = True

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xDir * BLOCK_SIZE
        self.head.y += self.yDir * BLOCK_SIZE
        self.body.remove(self.head)

    def up(self):
        self.yDir = -1
        self.xDir = 0
    def down(self):
        self.yDir = 1
        self.xDir = 0
    def left(self):
        self.yDir = 0
        self.xDir = -1
    def right(self):
        self.yDir = 0
        self.xDir = 1

class Food:
    """ For spawning food randomly """
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

    def eaten(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    """ For spawning food in the four corners """
    # def __init__(self):
    #     self.current_corner = 3  # Randomly select a starting corner
    #     self.spawn_in_corner()

    # def spawn_in_corner(self):
    #     if self.current_corner == 0:
    #         self.x = SW - BLOCK_SIZE * 3
    #         self.y = BLOCK_SIZE * 2
    #     elif self.current_corner == 1:
    #         self.x = SW - BLOCK_SIZE * 3
    #         self.y = SH - BLOCK_SIZE * 3
    #     elif self.current_corner == 2:
    #         self.x = BLOCK_SIZE * 2
    #         self.y = SH - BLOCK_SIZE * 3
    #     elif self.current_corner == 3:
    #         self.x = BLOCK_SIZE * 2
    #         self.y = BLOCK_SIZE * 2
        
    #     self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    # def update(self):
    #     pygame.draw.rect(screen, "red", self.rect)

    # def eaten(self):
    #     self.current_corner = (self.current_corner + 1) % 4  # Move to the next corner in a clockwise fashion
    #     self.spawn_in_corner()

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (150,150,150), rect, 1)


def main():
    score = FONT.render("1", True, "white")
    score_rect = score.get_rect(center=(SW/2, 25))

    drawGrid()

    snake = Snake()
    food = Food()
    curr_dir="right"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and curr_dir != "down":
                    snake.up()
                    curr_dir = "up"
                elif event.key == pygame.K_DOWN and curr_dir != "up":
                    snake.down()
                    curr_dir = "down"
                elif (event.key == pygame.K_LEFT) and curr_dir != "right":
                    snake.left()
                    curr_dir = "left"
                elif event.key == pygame.K_RIGHT and curr_dir != "left":
                    snake.right()
                    curr_dir = "right"

        snake.update()
        screen.fill('black')
        drawGrid()

        food.update()

        player_score = len(snake.body) + 1
        score = FONT.render(f"{player_score}", True, "white")

        pygame.draw.rect(screen, "green", snake.head)

        for square in snake.body:
            pygame.draw.rect(screen, "green", square)

        screen.blit(score, score_rect)

        if snake.self_collision == True:
            print(player_score)
            exit()
        elif snake.wall_collision == True:
            print(player_score)
            exit()

        if snake.head.x == food.x and snake.head.y == food.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            player_score +=5
            food.eaten()

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()