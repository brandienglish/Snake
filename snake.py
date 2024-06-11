import pygame , sys, random
from pygame.math import Vector2
  
pygame.init()

# game screen color
GREEN = (173,205,96)
DARK_GREEN = (43,51,24)

# GRID OF 750 
cell_size= 30 
number_of_cells=25

OFFSET = 75

# Food class 
class Food:
    def __init__(self, snake_body) :
        self.position= self.generate_random_pos(snake_body)

    #displaying and positiong the food 
    def draw(self):
        food_rect= pygame.Rect(OFFSET+self.position.x * cell_size,OFFSET+ self.position.y *cell_size,cell_size,cell_size)
        screen.blit(food_image, food_rect)
    
    def generate_random_cell(self):
        x=random.randint(0, number_of_cells-1)
        y= random.randint(0, number_of_cells-1)
        return     Vector2(x,y)
    
    # generating the food in random positions
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

       

# class for snake 
class Snake:
    def __init__(self):
        self.body=[Vector2(6,9),  Vector2(5,9), Vector2(4,9)]
        self.direction= Vector2(1,0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect =(OFFSET + segment.x* cell_size, OFFSET+segment.y*cell_size, cell_size ,cell_size)
            pygame.draw.rect(screen,DARK_GREEN, segment_rect,0,10)
    
    def update(self):
         #adding a segment to the head of the snake 
        self.body.insert(0,self.body[0]+self.direction)
        if self.add_segment == True:  
            self.add_segment = False
        else:
            self.body= self.body[:-1]

    def reset(self):
        # goes back to orginal body length 
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]    
        self.direction = Vector2(1,0)

class Game:
    def __init__(self):
        self.snake= Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"

    def draw(self):
        self.food.draw()
        self.snake.draw()
    
    def update(self):
        if self.state =="RUNNING":
            self.snake.update()
            self.collision_with_food()
            self.collision_with_edges()
            self.collision_with_tail()

    def collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            #food doesnt spawn on snake 
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
    
    def collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        #moving food to new position 
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"

    def collision_with_tail(self):
        no_head = self.snake.body[1:]
        if self.snake.body[0] in no_head:
            self.game_over() 
            #Test


#creating the game display screen (game window)
screen = pygame.display.set_mode((2*OFFSET+cell_size*number_of_cells,2*OFFSET+cell_size*number_of_cells))

pygame.display.set_caption("Snake")

# controls frame rate of the game 
clock = pygame.time.Clock()
game = Game()
food_image= pygame.image.load("Graphics/food.png")

SNAKE_UPDATE= pygame.USEREVENT

#updates the snake position every 200ms
pygame.time.set_timer(SNAKE_UPDATE, 200)
#game loop
while True: 
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # triggers new game once player press any key 
            #the game resets
            if game.state == "STOPPED":
                game.state = "RUNNING"
            ###
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1):
                #decrease the y cord to move up
                game.snake.direction = Vector2(0,-1)
                #increase the y cord to move down 
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction=Vector2(0,1)

             #decrease the x cord to move left
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction=Vector2(-1,0)

            #increase the x cord to move right
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction=Vector2(1,0)

    
     
    #drawing 
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, 
		(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
    game.draw() 
    pygame.display.update()

    #game runs 60 frames per second
    clock.tick(60)
