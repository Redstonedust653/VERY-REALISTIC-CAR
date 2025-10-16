import pygame
from pygame import Vector2
mode = '' #input('MODE')

pygame.init()
screen = pygame.display.set_mode((1500, 1500+164))
clock = pygame.time.Clock()
running = True
DT = 1/60
speed_font = pygame.font.SysFont("Fira Sans", 64, bold=True, italic=True)


class Car:
    def __init__(self,mode,startpos:Vector2) -> None:
        self.mode = mode
        self.pos = startpos
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.width = 15
        self.length = 30
        self.rotation = 90
        self.thrust = 300

    def carPoly(self) -> list[Vector2]:
        top = self.pos.y+(self.length/2)
        left = self.pos.x-(self.width/2)
        bottom = self.pos.y-(self.length/2)
        right = self.pos.x+(self.width/2)
        return [Vector2(left,top),Vector2(right,top),Vector2(right,bottom),Vector2(left,bottom),Vector2(left,top)]

    def draw(self):
        pygame.draw.rect(screen,'black',(0,0,screen.get_width(),170))
        pygame.draw.polygon(screen, 'red', self.carPoly(), width=0)
        screen.blit(speed_font.render(f"SPEED: {round(self.vel.magnitude()/100,1)}",False,'white','black'),(0,0))
        pygame.draw.rect(screen,((min(int(self.vel.magnitude()/1500*255),255),(int(150/(max(self.vel.magnitude()/750,1)))),0)),(0,64,(self.vel.magnitude()/1500)*2000,100))

    def collide(self):
        car_poly = self.carPoly()
        x_hit = False
        y_hit = False
        for i in car_poly:
            if not x_hit:
                if i.x < 0:
                    self.vel.x = -self.vel.x/2
                    self.pos.x = self.width / 2
                    x_hit = True
                if i.x > screen.get_width():
                    self.vel.x = -self.vel.x/2
                    self.pos.x = screen.get_width() - self.width / 2
                    x_hit = True
            if not y_hit:
                if i.y < 170:
                    self.vel.y = -self.vel.y/2
                    self.pos.y = (self.length / 2) +170
                    y_hit = True
                if i.y > screen.get_height():
                    self.vel.y = -self.vel.y/2
                    self.pos.y = (screen.get_height() - self.length / 2)
                    y_hit = True

    def tickInteractive(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.acc.y = -self.thrust
        if keys[pygame.K_s]:
            self.acc.y = self.thrust
        if keys[pygame.K_a]:
            self.acc.x = -self.thrust
        if keys[pygame.K_d]:
            self.acc.x = self.thrust
        if keys[pygame.K_SPACE]:
            self.vel /= 1.1
        
        if (not keys[pygame.K_w]) and (not keys[pygame.K_s]):
            self.acc.y = 0
            self.vel.y *= 0.98
        if (not keys[pygame.K_a]) and (not keys[pygame.K_d]):
            self.acc.x = 0
            self.vel.x *= 0.98

        self.vel += self.acc*DT
        self.pos += self.vel*DT
        self.collide()

    #def tickAuto

c = Car(mode,Vector2(1000,1000))



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

    c.tickInteractive()

    screen.fill("white")

    c.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
print('All done!')