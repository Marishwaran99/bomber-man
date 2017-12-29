import pygame,random,time
pygame.init()
black=(0,0,0)
red=(255,0,0)
white=(255,255,255)
yellow=(255,255,0)
green=(0,255,0)
yellow=(255,255,0)
blue=(0,0,255)
purple=(255,0,255)
light_blue=(0,255,255)
dh=512
dw=512
pygame.init()
pygame.mixer.init()
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,game):
        super().__init__()
        self.image=pygame.image.load("bfront.png")
        self.image=pygame.transform.scale(self.image,[32,32])
        self.i2=pygame.image.load("bright.png")
        self.i2=pygame.transform.scale(self.i2,[32,32])
        self.i3=pygame.image.load("bback.png")
        self.i3=pygame.transform.scale(self.i3,[32,32])
        self.i4=pygame.image.load("bright.png")
        self.i4=pygame.transform.scale(self.i4,[32,32])
        self.i4=pygame.transform.flip(self.i4,1,0)
        self.i1=self.image
        self.rect=self.image.get_rect()
        self.game=game
        self.x=x
        self.y=y
    def move(self,dx=0,dy=0):
        if not self.collide(dx,dy) and self.collide1(dx,dy) :
            self.x+=dx
            self.y+=dy
    def collide(self,dx=0,dy=0):
        for w in self.game.walls: 
             if w.x==self.x+dx and w.y==self.y+dy:
                 return True                
        return False
    def collide1(self,dx=0,dy=0):
        for b in self.game.breakables: 
             if b.x==self.x+dx and b.y==self.y+dy:
                 return False                
        return True
    def bomber(self):       
        bomb=Bomb(self.rect.x,self.rect.y,self,self.game)
        self.game.all_sprites.add(bomb)
        self.game.bombs.add(bomb)
    def update(self):
        self.rect.x=self.x*32
        self.rect.y=self.y*32
        if self.rect.left<=0:
            self.rect.left=0
        if self.rect.right>=dw:
            self.rect.right=dw
        if self.rect.top<=0:
            self.rect.top=0
        if self.rect.bottom>=dh:
            self.rect.bottom=dh
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("wall.png")
        self.image=pygame.transform.scale(self.image,[32,32])
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x=self.x*32
        self.rect.y=self.y*32
class Breakable(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("bwall.png")
        self.image=pygame.transform.scale(self.image,[32,32])
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x=self.x*32
        self.rect.y=self.y*32
class Fire(pygame.sprite.Sprite):
    def __init__(self,x,y,vx,vy,game):
        super().__init__()
        self.image=pygame.image.load("flame.png")
        self.image=pygame.transform.scale(self.image,[32,32])
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.game=game
        self.vx=vx
        self.vy=vy
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        self.last=pygame.time.get_ticks()
    def update(self):
        hits=pygame.sprite.groupcollide(self.game.fires,self.game.breakables,1,1)
        now=pygame.time.get_ticks()
        if now-self.last>1000:
            self.kill()
        
class Bomb(pygame.sprite.Sprite):
    def __init__(self,x,y,player,game):
        super().__init__()
        self.image=pygame.image.load("bomb.png")
        self.image=pygame.transform.scale(self.image,[32,32])
        self.rect=self.image.get_rect()
        self.last=pygame.time.get_ticks()
        self.rect.x=x
        self.rect.y=y
        self.player=player
        self.game=game
    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last>1000:
            self.last=now
            self.kill()
            fire1=Fire(self.rect.x,self.rect.y,30,0,self.game)
            self.game.all_sprites.add(fire1)
            self.game.fires.add(fire1)
            fire2=Fire(self.rect.x,self.rect.y,-30,0,self.game)
            self.game.all_sprites.add(fire2)
            self.game.fires.add(fire2)
            fire3=Fire(self.rect.x,self.rect.y,0,30,self.game)
            self.game.all_sprites.add(fire3)
            self.game.fires.add(fire3)
            fire4=Fire(self.rect.x,self.rect.y,0,-30,self.game)
            self.game.all_sprites.add(fire4)
            self.game.fires.add(fire4)
            fire5=Fire(self.rect.x,self.rect.y,0,0,self.game)
            self.game.all_sprites.add(fire5)
            self.game.fires.add(fire5)      
class Map:
    def __init__(self,file_name):
        self.data=[]
        with open(file_name,'r+') as f:
            for line in f:
                self.data.append(line)
class Game:
    def __init__(self):
        self.screen=pygame.display.set_mode([dw,dh])
        pygame.display.set_caption("Bomber Man")
        self.clock=pygame.time.Clock()
    def new(self):
        self.map=Map("map2.txt")
        self.all_sprites=pygame.sprite.Group()
        self.bombs=pygame.sprite.Group()
        self.walls=pygame.sprite.Group()
        self.fires=pygame.sprite.Group()
        self.breakables=pygame.sprite.Group()
        for col,tiles in enumerate(self.map.data):
            for row,tile in enumerate(tiles):
                if tile=='1':
                    self.wall=Wall(col,row)
                    self.all_sprites.add(self.wall)
                    self.walls.add(self.wall)
                if tile=='2':    
                    self.bwall=Breakable(col,row)
                    self.all_sprites.add(self.bwall)
                    self.breakables.add(self.bwall)
                if tile=='p':
                    
                    self.player=Player(4,4,self)
                    self.all_sprites.add(self.player)
        
    def run(self):
        self.play=True
        while self.play:
            self.events()
            self.update()
            self.draw()
    def events(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    self.player.move(0,-1)
                elif event.key==pygame.K_DOWN:
                    self.player.move(0,1)
                elif event.key==pygame.K_RIGHT:
                    self.player.move(1,0)
                elif event.key==pygame.K_LEFT:
                    self.player.move(-1,0)
                elif event.key==pygame.K_SPACE:
                    self.player.bomber()
    def update(self):
        self.all_sprites.update()
        hits=pygame.sprite.spritecollide(self.player,self.fires,True)
        if hits:
            self.gameover()

            self.new()
    def draw(self):
        self.screen.fill(white)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
    def msg(self,txt,color,size,x,y):
        self.font=pygame.font.SysFont("comicsansms",size,bold=1)
        msgtxt=self.font.render(txt,1,color)
        msgrect=msgtxt.get_rect()
        msgrect.x=x
        msgrect.y=y
        self.screen.blit(msgtxt,msgrect)
    def gameover(self):
        wait=True
        while wait:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        wait=0
            self.screen.fill(white)            
            self.msg("Game Over!",blue,50,160,100)
            self.msg("Press Enter to Play Again",blue,20,160,300)
            pygame.display.flip()  
    def start(self):
        wait=1
        while wait:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        wait=0
            self.screen.fill(white)            
            self.msg("Bomber",blue,50,160,100)
            self.msg("Press Enter to Play",blue,20,160,300)
            pygame.display.flip()
g=Game()
while g.run:
    g.start()
    g.new()
    g.run()
