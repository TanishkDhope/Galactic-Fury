import pygame
from random import randint,choice
from os import path
pygame.init()

screen=pygame.display.set_mode((640,640))
pygame.display.set_caption("Space Shooter")
clock=pygame.time.Clock()
bg=pygame.image.load(path.join("Graphics","Backgrounds","Purple.png")).convert_alpha()
bg=pygame.transform.scale(bg,(640,640))
bg_rect=bg.get_rect(topleft=(0,0))

bg_music=[]
bg_music.append(pygame.mixer.Sound(path.join("Audio","level3.ogg")))
bg_music.append(pygame.mixer.Sound(path.join("Audio","level4.ogg")))
bg_music.append(pygame.mixer.Sound(path.join("Audio","boss.ogg")))
bg_music_play=bg_music[randint(0,2)]

bg_music_play.play(loops=-1)
running=True
pause=False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(path.join("Graphics", "PNG", "playerShip2_red.png")).convert_alpha()
        self.image=pygame.transform.rotozoom(self.image,0, 0.9)
        self.rect=self.image.get_rect(center=(320,200))
        self.laser_sound=pygame.mixer.Sound("C:\Projects\Python\Galactic Fury\Audio\sfx_laser1.ogg")
        self.explosion_sound=pygame.mixer.Sound(path.join("Audio","explode.wav"))
        self.explosion_sound.set_volume(0.2)
        self.can_shoot=True

        #cooldown
        self.laser_shoot_time=0
        self.laser_cooldown=400    #400ms

        #mask
        self.mask=pygame.mask.from_surface(self.image)

        self.rotation_angle=0

    def create_bullet(self):
        bullet=Bullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        bullet_group.add(bullet)
        self.laser_sound.play()

    def create_asteroid(self,pos_x,pos_y):
        asteroid=Asteroid(pos_x,pos_y)
        asteroid_group.add(asteroid)
        
    def collision_check(self):
        global running
        if asteroid_group:
            for bullet in bullet_group:
                collided = pygame.sprite.spritecollide(bullet,asteroid_group,True)
                if collided:
                    self.explosion_sound.play()
                    explosion_group.add(Animated_Explosion(explosion_frames,bullet.rect.midtop))
                    bullet.kill()

            # if pygame.sprite.groupcollide(asteroid_group,bullet_group,True,True):
            #     self.explosion_sound.play()
            if pygame.sprite.spritecollide(self,asteroid_group,True,pygame.sprite.collide_mask):
                running=False

    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_shoot_time>=self.laser_cooldown:
                self.can_shoot=True


    def update(self):
        self.collision_check()
        pygame.mouse.set_visible(False)
        mouse_pos=pygame.mouse.get_pos()
        self.rect.center=mouse_pos
        self.laser_timer()

        mouse_press=pygame.mouse.get_just_pressed()
        if mouse_press[0] and self.can_shoot:
            self.create_bullet()
            self.can_shoot=False
            self.laser_shoot_time=pygame.time.get_ticks()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image=pygame.image.load(path.join("Graphics", "PNG","Lasers","laserRed03.png")).convert_alpha()
        self.rect=self.image.get_rect(center=(x_pos,y_pos))
        #mask
        self.mask=pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.rect.center+=bullet_direction*bullet_speed*dt
        if self.rect.y<=-20:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        image=[]
        image.append(pygame.image.load("C:\Projects\Python\Asteroids\Graphics\PNG\Enemies\enemyBlack1.png").convert_alpha())
        image.append(pygame.image.load("C:\Projects\Python\Asteroids\Graphics\PNG\Enemies\enemyBlack2.png").convert_alpha())
        image.append(pygame.image.load("C:\Projects\Python\Asteroids\Graphics\PNG\Enemies\enemyBlack3.png").convert_alpha())
        image.append(pygame.image.load("C:\Projects\Python\Asteroids\Graphics\PNG\Enemies\enemyRed3.png").convert_alpha())
        image.append(pygame.image.load("C:\Projects\Python\Asteroids\Graphics\PNG\Enemies\enemyRed1.png").convert_alpha())
        image.append(pygame.image.load("C:\Projects\Python\Asteroids\Graphics\PNG\Enemies\enemyRed2.png").convert_alpha())
        self.image=image[randint(0,5)]
        self.image=pygame.transform.scale_by(self.image,0.5)
        self.rect=self.image.get_rect(center=(pos_x,pos_y))

        #mask
        self.mask=pygame.mask.from_surface(self.image)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        image_list=[]
        image_list.append(pygame.image.load(path.join("Graphics", "PNG","Meteors","meteorGrey_big1.png")).convert_alpha())
        image_list.append(pygame.image.load(path.join("Graphics", "PNG","Meteors","meteorGrey_big2.png")).convert_alpha())
        image_list.append(pygame.image.load(path.join("Graphics", "PNG","Meteors","meteorGrey_big3.png")).convert_alpha())
        image_list.append(pygame.image.load(path.join("Graphics", "PNG","Meteors","meteorGrey_big4.png")).convert_alpha())
        image_list.append(pygame.image.load(path.join("Graphics", "PNG","Meteors","meteorGrey_med1.png")).convert_alpha())
        image_list.append(pygame.image.load(path.join("Graphics", "PNG","Meteors","meteorGrey_med2.png")).convert_alpha())
        self.original_surf=image_list[randint(0,5)]
        self.image=self.original_surf
        self.rect=self.image.get_rect(center=(pos_x,pos_y))
        self.asteroid_direction=pygame.math.Vector2(0,0)
        self.asteroid_speed=0
        self.init_char(pos_x)

        #mask
        self.mask=pygame.mask.from_surface(self.image)

        #transform
        self.rotation_speed=randint(40,80)
        self.rotation_direction=choice([-1,1])
        self.rotation_angle=0

    def init_char(self,pos_x):
        if pos_x in range(-200,int(screen.get_width()/2)):
            self.asteroid_direction+=(2,3)
        else:
            self.asteroid_direction+=(-2,3)

        if randint(0,2):
            self.asteroid_speed=200
        else:
            self.asteroid_speed=100

    def update(self):
        self.rect.center+=self.asteroid_direction*self.asteroid_speed*dt

        if self.rect.y>=int(screen.get_height())+40 or self.rect.x<=-50 or self.rect.x>=screen.get_width()+40:
            self.kill()

        #rotation logic
        self.rotation_angle+=self.rotation_speed*self.rotation_direction*dt
        self.image=pygame.transform.rotozoom(self.original_surf,self.rotation_angle,1)
        self.rect=self.image.get_rect(center=self.rect.center)

class Animated_Explosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos):
        super().__init__()
        self.frames=frames
        self.frame_index=0
        self.image=frames[self.frame_index]
        self.rect=self.image.get_rect(center=pos)

    def update(self):
        
        self.frame_index+=10*dt
        if self.frame_index<len(self.frames):
            self.image=self.frames[int(self.frame_index)]
        else:
            self.kill()
        


               


player=Player()
player_group=pygame.sprite.Group()
player_group.add(player)

bullet_group=pygame.sprite.Group()
enemy_group=pygame.sprite.Group()
asteroid_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
star_group=pygame.sprite.Group()

bullet_direction=pygame.math.Vector2(0,-2)
bullet_speed=200

explosion_frames=[]

for i in range(12):
    frame=pygame.image.load(path.join("Graphics","Explosion_alt",f"tile{i}.png")).convert_alpha()
    # frame=pygame.transform.rotozoom(frame,0,0.2)
    explosion_frames.append(frame)

asteroid_timer=pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 100)


while running:
    dt=clock.tick(120)/1000
    fps=clock.get_fps()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:
                pause=not pause
        if event.type==asteroid_timer:
            pos_x=randint(-600,screen.get_width()+600)
            pos_y=randint(0,200) if pos_x in range(-600, 0) or pos_x in range(690,1240) else randint(-150,-100)
            player.create_asteroid(pos_x,pos_y)

    screen.fill("cyan")
    screen.blit(bg, bg_rect)

    explosion_group.draw(screen)
    bullet_group.draw(screen)
    player_group.draw(screen)
    asteroid_group.draw(screen)
    enemy_group.draw(screen)

    if not pause:
        bullet_group.update(dt)
        player_group.update()
        asteroid_group.update()
        explosion_group.update()

    
    pygame.display.update()

pygame.quit()