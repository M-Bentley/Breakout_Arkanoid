import pygame
from pygame.locals import *



class Player():

    def __init__(self, screen_rect):

        self.image = pygame.image.load("H:\Itchy.png")
        self.image = pygame.transform.scale(self.image, (50,100))

        self.rect = self.image.get_rect()
 
        self.rect.bottom = screen_rect.bottom 
        self.rect.centerx = screen_rect.centerx

        self.move_x = 0

        self.shots = []
        self.shots_count = 0

        self.max_shots = 1

    def event_handler(self, event):

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.move_x = -5
            elif event.key == K_RIGHT:
                self.move_x = 5
            elif event.key == K_SPACE:
                if len(self.shots) < self.max_shots:
                    self.shots.append(Bullet(self.rect.centerx, self.rect.top))

        if event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT):
                self.move_x = 0
     

    def update(self):
        
        self.rect.x += self.move_x

        for s in self.shots:
            s.update()

        for i in range(len(self.shots)-1, -1, -1):
            print "debug: Player.update: testing bullet ", i
            if not self.shots[i].is_alive:
                print "debug: Player.update: removing bullet ", i
                del self.shots[i]

    def draw(self, screen):

        screen.blit(self.image, self.rect.topleft)

        for s in self.shots:
            s.draw(screen)

    def bullet_detect_collison(self, enemy_list):

        for s in self.shots:
            for e in enemy_list:
                if pygame.sprite.collide_circle(s, e):
                    s.is_alive = False
                    e.is_alive = False

class Bullet():

    def __init__(self, x, y):

        self.image = pygame.image.load("H:619px-Chainsaw_symbol_2010-02-16.svg.png")
        self.image = pygame.transform.scale(self.image, (50,25))
        self.image = pygame.transform.rotate(self.image, (270))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.is_alive = True


    def update(self):

        self.rect.y -= 15

        if self.rect.y < 0:
            self.is_alive = False


    def draw(self, screen):

        screen.blit(self.image, self.rect.topleft)


class Enemy(): 

    def __init__(self, x, y):

        self.image = pygame.image.load("H:Scratchy.gif")
        self.image = pygame.transform.scale(self.image, (70,170))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.is_alive = True

    def update(self):
        
        self.rect.y += 1

    def draw(self, screen):

        screen.blit(self.image, self.rect.topleft)

class Game():
    
    def __init__(self):
        pygame.init()

        w, h = 800, 800
        self.screen = pygame.display.set_mode((w,h))

        pygame.mouse.set_visible(False)

        self.ship = Player(self.screen.get_rect())

        self.enemies = []

        for i in range(100, 800, 100):
            self.enemies.append(Enemy(i,100))

        font = pygame.font.SysFont("", 72)
        self.text_paused = font.render("PAUSED", True, (255, 0, 0))
        self.text_paused_rect = self.text_paused.get_rect(center=self.screen.get_rect().center)

    def run(self):

        clock = pygame.time.Clock()

        RUNNING = True
        PAUSED = False

        while RUNNING:
            pygame.timer.set_timer(pygame.QUIT,400)

            clock.tick(30)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        RUNNING = False

                    if event.key == K_p:
                        PAUSED = not PAUSED

                if not PAUSED:
                    self.ship.event_handler(event)

            if not PAUSED:

                self.ship.update()

                for e in self.enemies:
                    e.update()

                self.ship.bullet_detect_collison(self.enemies)

                for i in range(len(self.enemies)-1, -1, -1):
                    print "debug: Player.update: testing bullet ", i
                    if not self.enemies[i].is_alive:
                        print "debug: Player.update: removing bullet ", i
                        del self.enemies[i]


            self.screen.fill((0,0,0))

            self.ship.draw(self.screen)

            for e in self.enemies:
                e.draw(self.screen)

            if PAUSED:
                self.screen.blit(self.text_paused, self.text_paused_rect)

            pygame.display.update()


        pygame.quit()


Game().run()