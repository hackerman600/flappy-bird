import pygame
import random
import os
import random
pygame.init()


win_w, win_h = 480, 640
window = pygame.display.set_mode((win_w, win_h))

img_path = '/home/kali/Desktop/machine_learning/reinforcement_learning/imgs'
imgs = os.listdir(img_path)
#print(imgs)
bird1 = pygame.image.load(os.path.join(img_path,imgs[0]))
bird2 = pygame.image.load(os.path.join(img_path,imgs[2]))
bird3 = pygame.image.load(os.path.join(img_path,imgs[-1]))
background = pygame.transform.scale(pygame.image.load(os.path.join(img_path,imgs[1])),(win_w,win_h))
pipe = pygame.image.load(os.path.join(img_path,imgs[3]))
base = pygame.image.load(os.path.join(img_path,imgs[-2]))

#140(y_pipe) x 70 (x_pipe) x 640(win_height) do q table by range of 30.    
class Pipe:
    def __init__(self):
        self.pipe_x1 = random.randint(140,220)
        self.pipe_x2 = self.pipe_x1 + 200
        self.pipe_x1_original , self.pipe_x2_original = self.pipe_x1, self.pipe_x2 

        self.pipe_y1 = random.randint(-200,0)
        self.pipe_y1_bottom = self.pipe_y1 + 530

        self.pipe_y2 = random.randint(-80,0)
        self.pipe_y2_bottom = self.pipe_y2 + 530

        self.closest_pipe = [self.pipe_x1, self.pipe_y1_bottom]
        
    def draw(self):
        window.blit(pygame.transform.scale(pygame.transform.rotate(pipe, 180), (pipe.get_width(), 410)),(self.pipe_x1,self.pipe_y1))
        window.blit(pygame.transform.scale(pipe, ((pipe.get_width(), 400))),(self.pipe_x1,self.pipe_y1_bottom))
        window.blit(pygame.transform.scale(pygame.transform.rotate(pipe, 180), (pipe.get_width(), 410)),(self.pipe_x2,self.pipe_y2))
        window.blit(pygame.transform.scale(pipe, ((pipe.get_width(), 400))),(self.pipe_x2,self.pipe_y2_bottom))

    def move(self):
        self.pipe_x1 -= 1
        self.pipe_x2 -= 1

    def spawn(self):
        if self.pipe_x1 <= 0:
            self.pipe_x1 = self.pipe_x2_original + 80
            self.pipe_y1 = random.randint(-200,0)
            self.pipe_y1_bottom = self.pipe_y1 + 530
            self.closest_pipe[0] = [self.pipe_x2, self.pipe_y2_bottom]
            return True

        elif self.pipe_x2 <= 0:
            self.pipe_x2 = self.pipe_x2_original + 80
            self.pipe_y2 = random.randint(-80,0)
            self.pipe_y2_bottom = self.pipe_y2 + 530
            self.closest_pipe[0] = [self.pipe_x1, self.pipe_y1_bottom]
            return True
        
        
    def reset(self):
        self.__init__()



class Bird:
    def __init__(self):
        self.action = False
        self.x = 50
        self.y = win_h // 2 - bird1.get_height() + 10 // 2
        self.original_x , self.oiginal_y = self.x, self.y
        self.birds = [bird1,bird2,bird3]
        self.sec = 0
        
    def draw(self,sec):
        if self.action == False:
                window.blit(pygame.transform.rotate(pygame.transform.scale(bird2,(bird2.get_width() + 10, bird2.get_height() + 10)), -sec//2),(self.x,self.y))

        else:
            window.blit(pygame.transform.scale(bird3,(bird3.get_width() + 10, bird3.get_height() + 10)),(self.x,self.y))


    def move(self, up = True):
        if up:
            self.action = True
            self.y -= 5
        else:
            self.action = False
            if self.y < 180:
                val = 180
            else:
                val = self.y
            self.y += (val // 180)   
        

    def reset(self):
        self.x = self.original_x
        self.y = self.oiginal_y    
      
 
class Game:
    def __init__(self):
        self.x1 = 0
        self.x2 = win_w  
        self.pipe = Pipe()
        self.bird = Bird()
        self.score = 0
        self.sec = 0 #BIRD X COORD, BIRD Y COORD, DISTANCE FROM PIPE, Y VAL OF BOTTOM PIPE
        
        
    def draw(self):
        window.blit(background,(self.x1,0))
        window.blit(background,(self.x2,0))
        self.pipe.draw()
        self.bird.draw(self.sec)
        font = pygame.font.Font(None, 35)
        text_surface = font.render(f"Score: {self.score}", True,(255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (30, 10)
        window.blit(text_surface, text_rect)

    def move(self):
        self.x1 -= 1
        self.x2 -= 1

        if self.x1 <= 0-win_w:
            self.x1 = win_w

        elif self.x2 <= 0-win_w:
            self.x2 = win_w

        self.pipe.move()    
        out = self.pipe.spawn()
        if out == True:
            self.score += 1 

        if self.bird.y <= self.pipe.pipe_y1 + 410 and self.bird.x + bird1.get_width() >= self.pipe.pipe_x1 or self.bird.y <= self.pipe.pipe_y2 + 410 and self.bird.x + bird1.get_width() >= self.pipe.pipe_x2:
            self.reset()

        elif self.bird.y + bird1.get_height() - 2 >= self.pipe.pipe_y1_bottom and self.bird.x + bird1.get_width() >= self.pipe.pipe_x1 or self.bird.y + bird1.get_height() - 2 >= self.pipe.pipe_y2_bottom and self.bird.x + bird1.get_width() >= self.pipe.pipe_x2:
            self.reset()


    def handle_bird_movement_player(self,bird):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.move(up = True)
            self.sec = 0
        else:
            bird.move(up = False)   
            
            if self.sec > 100:
                self.sec = 100    
            else:
                self.sec += 1      

    def handle_bird_movement_agent(self):  
        pass

    def reset(self):
            self.bird.reset()   
            self.pipe.reset()
            self.score = 0
            self.sec = 0

def main():

    game = Game()
    run = True
    epsilon_rate = 1

    def draw():
        window.fill((0,0,0))
        game.draw()
        pygame.display.update()

                           
    #BIRD X COORD, BIRD Y COORD, DISTANCE FROM PIPE, Y VAL OF BOTTOM PIPE
    while run:

        game.move()
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        print(game.bird.y)
        game.handle_bird_movement_player(game.bird)


main()