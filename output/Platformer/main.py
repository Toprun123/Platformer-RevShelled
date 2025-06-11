# Import Modules
import pygame as p
import random as r
import os as o
# Import Files
from config import *
from sprite import *
# setting the URL you want to monitor
""" Init Class Game """
class Game:
    """ Initialize Script """
    def __init__(self):
        # initialize game window, etc
        p.init()
        p.mixer.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        p.display.set_caption(TITLE)
        self.clock = p.time.Clock()
        self.running = True
        self.font_name = p.font.match_font(FONT)
        self.go = ""
        self.go2= ""
    """ New Game Functions """
    # TODO: BUG: Show Start Screen
    def show_start_screen(self):
        # game splash/start screen
        self.draw_text("Press space to Start The Game", 125, BLACK, WIDTH / 2, HEIGHT / 2 - 50)
    # Start New Game
    def new(self, run=True):
        # start a new game
        """ Init Variables & set to defaults"""
        # Import from config file
        self.score        = SCORE_DEF
        self.imgo         = not SURPMODE
        # Import from database
        hsf = open('info.pydb', 'r')
        self.hs = int(hsf.read())
        # Numerical       = 0
        self.y            = -10
        self.lives        = 3
        self.x            = 0
        self.boxes        = 0
        self.index        = 0
        self.coin_count   = 0
        # Flags           = True or False
        self.box          = False
        self.fl           = False
        self.flo          = False
        self.key          = False
        self.isEnd        = False
        self.start        = True
        # Strings         = "Text"
        self.go           = ""
        self.go2          = ""
        # Sound_snd       = p.mixer.Sound(o.path.join(snd_dir, 'snd.wav'   ))
        self.jumpB_snd    = p.mixer.Sound(o.path.join(snd_dir, 'boink.wav' ))
        self.coin_snd     = p.mixer.Sound(o.path.join(snd_dir, 'coin.wav'  ))
        self.key_snd      = p.mixer.Sound(o.path.join(snd_dir, 'key.wav'   ))
        self.heart_snd    = p.mixer.Sound(o.path.join(snd_dir, 'heart.wav' ))
        self.jump_snd     = p.mixer.Sound(o.path.join(snd_dir, 'jump.wav'  ))
        self.expl_snd     = p.mixer.Sound(o.path.join(snd_dir, 'exp.wav'   ))
        # SpriteGroups    = p.sprite.Group()
        self.all_sprites  = p.sprite.Group()
        self.sBoxes       = p.sprite.Group()
        self.platforms    = p.sprite.Group()
        self.hMovingplats = p.sprite.Group()
        self.vMovingplats = p.sprite.Group()
        self.spikes       = p.sprite.Group()
        self.mobs         = p.sprite.Group()
        self.bombs        = p.sprite.Group()
        self.jumpers      = p.sprite.Group()
        self.hearts       = p.sprite.Group()
        self.coins        = p.sprite.Group()
        self.col          = p.sprite.Group()
        self.keys         = p.sprite.Group()
        self.gt           = p.sprite.Group()
        """ Create New player """
        self.player = Player(self)
        self.all_sprites.add(self.player)
        """ Create Init Platforms """
        for plat in PLATFORM_LIST:
            width = r.randrange(90, 250)
            self.x = r.randrange(0, WIDTH - width)
            self.y = r.randrange(-20, 0)
            p1 = Platform(*plat)
            self.all_sprites.add(p1)
            self.platforms.add(p1)
        """ Start The game """
        if run:
            self.run()
    # Run new Game
    def run(self):
        # Game Loop
        # Enable Playing Attribute
        self.playing = True
        # Start game loop
        while self.playing:
            # Tick the timer for smoothness in graphics
            self.clock.tick(FPS)
            # Check for events
            self.keyEvents()
            # Update accordingly
            self.update()
            # Finally, Draw the Contents onto the screen
            self.draw()
    # Check for KeyBoard Events
    def keyEvents(self):
        # Game Loop - events
        for event in p.event.get():
            # check for closing window
            if event.type == p.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # KeyDown Events
            if event.type == p.KEYDOWN:
                # Jump Player
                if event.key == p.K_SPACE:
                    self.player.jump(self.jump_snd)
                if event.key == p.K_UP:
                    self.player.jump(self.jump_snd)
                # New Game
                if event.key == p.K_r:
                    self.new(True)
                # Some in game options
                if event.key == p.K_q:
                    self.fl = True
                if event.key == p.K_w:
                    self.flo = True
            # KeyUp events
            if event.type == p.KEYUP:
                # Refix the options
                if event.key == p.K_q:
                    self.fl = False
                if event.key == p.K_w:
                    self.flo = False
    # Update game loop
    def update(self):
        # Game Loop - Update
        if not self.isEnd:
            self.index += 1
            self.all_sprites.update()
            # Calculate collides
            mobscol  = p.sprite.spritecollide(self.player, self.mobs  , True )
            spikecol = p.sprite.spritecollide(self.player, self.spikes, False)
            sBoxCol  = p.sprite.spritecollide(self.player, self.sBoxes, False)
            # Place CustomBox if Key 'Q' Pressed
            if self.fl:
                if self.boxes >= 1:
                    self.box = True
                else:
                    self.box = False
                if self.box:
                    self.boxes -= 1
                    self.fl = False
                    width = r.randrange(90, 250)
                    x = r.randrange(50, WIDTH - width)
                    y = r.randrange(200, HEIGHT-200)
                    c = CustomPlat(x, y)
                    self.platforms.add(c)
                    self.all_sprites.add(c)
            # Use the collides
            if sBoxCol:
                if self.key:
                    if self.flo:
                        self.key = False
                        self.flo = False
                        sBoxCol[0].kill()
                        h = r.randrange(3, 8)#9
                        if h == 4:
                            j = Jumper(sBoxCol[0].rect.x, sBoxCol[0].rect.y)
                            self.all_sprites.add(j)
                            self.jumpers.add(j)
                            print("Jumper")
                        elif h == 5:
                            s = Spike(sBoxCol[0].rect.x, sBoxCol[0].rect.y + 30)
                            self.all_sprites.add(s)
                            self.spikes.add(s)
                            print("Spike")
                        elif h == 3:
                            col = CustomPlatCollector(sBoxCol[0].rect.x, sBoxCol[0].rect.y)
                            self.all_sprites.add(col)
                            self.col.add(col)
                            print("Box")
                        elif h == 7:
                            heart = Coin(sBoxCol[0].rect.x, sBoxCol[0].rect.y)
                            self.all_sprites.add(heart)
                            self.coins.add(heart)
                            coin = True
                            print("Coin")
                        #elif h == 8:
                            #p2 = Bomb(sBoxCol[0].rect.x, sBoxCol[0].rect.y, self)
                            #p2.active = True
                            #self.all_sprites.add(p2)
                            #self.bombs.add(p2)
                            #print("Bomb")
                        else:
                            heart = Heart(sBoxCol[0].rect.y, sBoxCol[0].rect.x)
                            self.all_sprites.add(heart)
                            self.hearts.add(heart)
                            print("Heart")
                else:
                    if self.player.vel.y > 0:
                        self.player.pos.y = sBoxCol[0].rect.top
                        self.player.vel.y = 0
            if mobscol:
                point = r.randrange(50, 90)
                if self.score > point:
                    self.score -= point
                else:
                    self.score = 0
            if spikecol:
                if self.player.vel.y >= 0:
                    spikecol[0].kill()
                    self.lives -= 1
                else:
                    self.player.vel.y = -19
            # Get onto platforms
            if self.player.vel.y >= 0:
                hits = p.sprite.spritecollide(self.player, self.platforms, False)
                if hits:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -0
                hitsug = p.sprite.spritecollide(self.player, self.hMovingplats, False)
                if hitsug:
                    self.player.pos.y = hitsug[0].rect.top
                    self.player.vel.y = -0
                hitsluggy = p.sprite.spritecollide(self.player, self.vMovingplats, False)
                if hitsluggy:
                    self.player.pos.y = hitsluggy[0].rect.top
                    self.player.vel.y = -0
            # Some more Collides
            #for curr_plat in self.platforms:
                #collide = p.sprite.spritecollide(curr_plat, self.platforms, False)
                #if collide:
                    #if not collide[0] == curr_plat:
                        #curr_plat.kill()
            for bomb in self.bombs:
                if self.checkCollide(bomb, self.player):
                    bomb.active = True
                if bomb.vel.y > 0:
                    hitn = p.sprite.spritecollide(bomb, self.platforms, False)
                    if hitn:
                        bomb.pos.y = hitn[0].rect.top
                        bomb.vel.y = 0
            for mob in self.mobs:
                if mob.vel.y > 0:
                    hitsun = p.sprite.spritecollide(mob, self.platforms, False)
                    if hitsun:
                        mob.pos.y = hitsun[0].rect.top
                        mob.vel.y = 0
            for jum in self.jumpers:
                if self.checkCollide(jum, self.player):
                    jum.up(self.jumpB_snd)
                    self.player.vel.y = -40
            for heart in self.hearts:
                if self.checkCollide(heart, self.player):
                    heart.kill()
                    self.heart_snd.play()
                    if self.lives != 3:
                        self.lives += 1
            for key in self.keys:
                if self.checkCollide(key, self.player):
                    self.key = True
                    self.key_snd.play()
                    key.kill()
            for coin in self.coins:
                if self.checkCollide(coin, self.player):
                    coin.kill()
                    self.coin_snd.play()
                    self.coin_count += 1
            for col in self.col:
                if self.checkCollide(col, self.player):
                    col.kill()
                    self.boxes += 1
            # Jump some mobs
            for mob in self.mobs:
                if mob.rect.y > HEIGHT:
                    mob.kill()
            # Scroll The screen
            if self.player.rect.y <= int(HEIGHT / 3.75):
                vely = abs(self.player.vel.y)
                self.player.pos.y += vely
                for plat in self.vMovingplats:
                    plat.end += vely
                    plat.start += vely
                    plat.rect.y += vely
                    if plat.rect.top >= HEIGHT+plat.end:
                        plat.kill()
                        self.score += 10
                for plat in self.platforms:
                    plat.rect.y += vely
                    if plat.rect.top >= HEIGHT:
                        plat.kill()
                        self.score += 10
                for bomb  in self.bombs:
                    bomb.rect.y += vely
                    if bomb.rect.top >= HEIGHT:
                        bomb.kill()
                for spike in self.spikes:
                    spike.rect.y += vely
                    if spike.rect.top >= HEIGHT:
                        spike.kill()
                        self.score += 10
                for jumper in self.jumpers:
                    jumper.rect.y += vely
                    if jumper.rect.top >= HEIGHT:
                        jumper.kill()
                        self.score += 10
                for heart in self.hearts:
                    heart.rect.y += vely
                    if heart.rect.top >= HEIGHT:
                        heart.kill()
                        self.score += 10
                for key in self.keys:
                    key.rect.y += vely
                    if key.rect.top >= HEIGHT:
                        key.kill()
                        self.score += 10
                for col in self.col:
                    col.rect.y += vely
                    if col.rect.top >= HEIGHT:
                        col.kill()
                        self.score += 10
                for coin in self.coins:
                    coin.rect.y += vely
                    if coin.rect.top >= HEIGHT:
                        coin.kill()
                        self.score += 10
            # Create Platforms
            if len(self.platforms) < 6:
                if r.randrange(-1,6) == 3:
                    dl = VerticalMovingPlat(self.x, self.y)
                    self.all_sprites.add(dl)
                    self.vMovingplats.add(dl)
                width = r.randrange(90, 250)
                old_x = self.x
                old_y = self.y
                self.x = r.randrange(0, WIDTH - width)
                self.y = r.randrange(-20, 0)
                while self.y > old_y+15:
                    self.y = r.randrange(-20, 0)
                if r.randrange(-1,1) == 0:
                    # Add Powerups and Spikes
                    h = r.randrange(2, 10)
                    if h == 5:
                        s = Spike(self.x + r.randrange(0, width-80), self.y)
                        self.all_sprites.add(s)
                        self.gt.add(s)
                        self.spikes.add(s)
                    if h == 7:
                        j = Jumper(self.x + r.randrange(0, width-80), self.y - 75)
                        self.all_sprites.add(j)
                        self.gt.add(j)
                        self.jumpers.add(j)
                    if r.randrange(-7, 7) == 0:
                        heart = Heart(self.x + r.randrange(0, width-80), self.y-50)
                        self.all_sprites.add(heart)
                        self.gt.add(heart)
                        self.hearts.add(heart)
                    if r.randrange(-6, 6) == 0:
                        col = CustomPlatCollector(self.x + r.randrange(0, width-80), self.y-50)
                        self.all_sprites.add(col)
                        self.gt.add(col)
                        self.col.add(col)
                    if self.imgo:
                        imgo = r.randrange(-6, 6) == 0
                    else:
                        imgo = True
                    if imgo:
                        col = SurpriseBox(self.x + r.randrange(0, width-80), self.y-50)
                        self.all_sprites.add(col)
                        self.gt.add(col)
                        self.sBoxes.add(col)
                        self.platforms.add(col)
                    # Add Platform
                    p1 = Platform(self.x, self.y, width, 20)
                    self.platforms.add(p1)
                    self.all_sprites.add(p1)
                    # Add Point Eating Mob
                    if r.random() < 0.15:
                        if r.random() < 0.5:
                            p2 = Blocker()
                            self.all_sprites.add(p2)
                            self.mobs.add(p2)
                        if r.random() < 0.4:
                            p2 = Bomb(r.randrange(0, WIDTH), -10, self)
                            if r.random() < 0.4:
                                p2.active = True
                            self.all_sprites.add(p2)
                            self.bombs.add(p2)
                else:
                    if r.randrange(-2,1) == 0:
                        p1 = HorizontalMovingPlat(self.x, self.y)
                        coin = False
                        self.hMovingplats.add(p1)
                        self.platforms.add(p1)
                        self.all_sprites.add(p1)
                        if r.randrange(-2, 2) == 0:
                            heart = Coin(self.x+20, self.y-50)
                            self.all_sprites.add(heart)
                            self.gt.add(heart)
                            self.coins.add(heart)
                            coin = True
                        if self.imgo:
                            imgo = r.randrange(-6, 6) == 0 and not coin
                        else:
                            imgo = True
                        if imgo:
                            heart = Key(self.x+20, self.y-50)
                            self.all_sprites.add(heart)
                            self.gt.add(heart)
                            self.keys.add(heart)
                        if r.random() < 0.4:
                            p2 = Bomb(r.randrange(0, WIDTH), -10, self)
                            if r.random() < 0.4:
                                p2.active = True
                            self.all_sprites.add(p2)
                            self.bombs.add(p2)
                    else:
                        coin = False
                        p1 = MetalPlat(self.x, self.y)
                        self.platforms.add(p1)
                        self.all_sprites.add(p1)
                        if r.randrange(-2, 2) == 0:
                            heart = Coin(self.x+21, self.y-50)
                            self.all_sprites.add(heart)
                            self.gt.add(heart)
                            self.coins.add(heart)
                            coin = True
                        if r.randrange(-6, 6) == 0 and not coin:
                            heart = Key(self.x+20, self.y-50)
                            self.all_sprites.add(heart)
                            self.gt.add(heart)
                            self.keys.add(heart)
                    if r.random() < 0.1:
                        if r.random() < 0.5:
                            p2 = Blocker()
                            self.all_sprites.add(p2)
                            self.mobs.add(p2)
            # Check For Fall
            if self.player.rect.y > HEIGHT:
                self.lives -= 1
                self.player.pos.y = 30
                self.player.pos.x = WIDTH / 2
                plat = MetalPlat(WIDTH/2-30, 37)
                self.all_sprites.add(plat)
                self.platforms.add(plat)
            # Finalize death
            if self.lives < 0:
                self.show_go_screen()
                self.isEnd = True
            else:
                self.final = self.score
            # Finalize Score
            self.score = self.final
            hsf = open('info.pydb', 'r')
            hs = int(hsf.read())
            if hs < self.final:
                hsf = open('info.pydb', 'w')
                hsf.write(str(self.final))
                self.hs = self.final
    # Finally, Draw Output on Screen
    def draw(self):
        # Game Loop - draw
        # Print BG
        background1 = p.image.load(o.path.join(img_dir, "bg_castle.png")).convert()
        background1 = p.transform.scale(background1, (WIDTH, HEIGHT))
        background_rect1 = background1.get_rect()
        self.screen.blit(background1, background_rect1)
        ba = p.image.load(o.path.join(img_dir, "bg_castle.png")).convert_alpha()
        self.screen.blit(ba, ba.get_rect())
        # Print lives
        Num = list([False, False, False])
        if self.lives == 0:
            pass
        elif self.lives == 1:
            Num[0] = True
        elif self.lives == 2:
            Num[0] = True
            Num[1] = True
        elif self.lives == 3:
            Num[0] = True
            Num[1] = True
            Num[2] = True
        st = p.sprite.Group()
        emp = Lives(10, HEIGHT-100, Num[0])
        st.add(emp)
        emp = Lives(60, HEIGHT-100, Num[1])
        st.add(emp)
        emp = Lives(110, HEIGHT-100, Num[2])
        st.add(emp)
        # Print other Aesthetic Elements
        tor = Torch(50,70)
        st.add(tor)
        tor2 = Torch(300,300)
        st.add(tor2)
        tor2 = Torch(30,330)
        st.add(tor2)
        key = KeyHUD(29, 110, self.key)
        st.add(key)
        # window = Window(150,200)
        # st.add(window)
        st.update()
        st.draw(self.screen)
        # Print some other Statistics of the player
        ba = p.image.load(o.path.join(img_dir, "boxAltHud.png")).convert_alpha()
        self.screen.blit(ba, (30,30))
        ba = p.image.load(o.path.join(img_dir, "coins.png")).convert_alpha()
        self.screen.blit(ba, (30,70))
        self.draw_text(str(self.boxes), 22, BLACK, 70, 40)
        self.draw_text(str(self.coin_count), 22, BLACK, 70, 77)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.final), 22, BLACK, WIDTH / 2, 15)
        self.draw_text('High Score: '+str(self.hs), 22, WHITE, WIDTH / 2, 28)
        self.draw_text(self.go, 125, BLACK, WIDTH / 2, HEIGHT / 2 - 50)
        self.draw_text(self.go2, 25, BLACK, WIDTH / 2, HEIGHT / 2 + 50)
        # *after* drawing everything, flip the display
        p.display.flip()
    """ Show GameOver Screen """
    def show_go_screen(self):
        # game over/continue
        # Kill player
        self.player.kill()
        # Inform user
        self.go = "Game over"
        self.go2 = "click r to continue"
    """ Universal Functions """
    # Draw text - Universal Function
    def draw_text(self, text, size, color, x, y):
        # Universal function used by the computer
        font = p.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    # Check for collide - Universal Function
    def checkCollide(self, sp, sprite):
        return sp.rect.colliderect(sprite.rect)
