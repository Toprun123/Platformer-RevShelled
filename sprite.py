# import
import pygame as p
import random as r
from os import path
from config import *
""" Create Sprite Player """
class Player               (p.sprite.Sprite):
    def __init__(self,game):
        p.sprite.Sprite.__init__(self)
        self.game        = game
        self.image       = p.image.load(path.join(img_dir, "alienBeige.png")).convert()
        self.rect        = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos         = vec(START_X, START_Y)
        self.vel         = vec(0, 0)
        self.acc         = vec(0, 0)
        self.image.set_colorkey(BLACK)
    def jump(self, snd):
        player_png  = p.image.load(path.join(img_dir, "alienBeige.png")).convert()
        self.image  = player_png
        hits        = p.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -player_jmp
            snd.set_volume(0.15)
            snd.play()
        hits        = p.sprite.spritecollide(self, self.game.vMovingplats, False)
        if hits:
            self.vel.y = -player_jmp
            snd.set_volume(0.15)
            snd.play()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
    def update(self):
        hits = p.sprite.spritecollide(self, self.game.hMovingplats, False)
        if hits:
            if hits[0].mode:
                self.pos.x -= 2
            else:
                self.pos.x += 2
        hits = p.sprite.spritecollide(self, self.game.vMovingplats, False)
        if hits:
            if not hits[0].mode:
                self.pos.y += 2
        self.rect = self.image.get_rect()
        self.acc = vec(0, PLAYER_GRA)
        k = p.key.get_pressed()
        if k[p.K_LEFT]:
            self.acc.x     = -PLAYER_ACC
            player_pngorig = p.image.load(path.join(img_dir, "alienBeige_stand.png")).convert()
            player_png     = player_pngorig
            player_png     = p.transform.flip(player_pngorig, True, False)
            self.image     = player_png
            self.rect      = self.image.get_rect()
            self.image.set_colorkey(BLACK)
        if k[p.K_RIGHT]:
            self.acc.x     = PLAYER_ACC
            player_png     = p.image.load(path.join(img_dir, "alienBeige_stand.png")).convert()
            self.image     = player_png
            self.rect      = self.image.get_rect()
            self.image.set_colorkey(BLACK)
        self.acc.x += self.vel.x * -PLAYER_FRI
        self.vel   += self.acc
        self.pos   += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
""" All Types of platforms """
# Normal Ground Type Platform
class Platform             (p.sprite.Sprite):
    def __init__(self, x, y, w, h):
        p.sprite.Sprite.__init__(self)
        self.plat = "night.png"
        self.orig = p.image.load(path.join(img_dir, self.plat)).convert_alpha()
        self.image = p.transform.scale(self.orig, (int(w), int(h+15)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
# Metal Type Platform
class MetalPlat            (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, "metalHalf.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
# Moving Type Platform
class HorizontalMovingPlat (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, "bridge.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mode = False
    def update(self):
        if self.rect.x + 70 > WIDTH:
            self.mode = True
        elif self.rect.x < 0:
            self.mode = False
        if not self.mode:
            self.rect.x = self.rect.x+2
        elif self.mode:
            self.rect.x = self.rect.x-2
class VerticalMovingPlat   (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, "bridgeLogs.png")).convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.end = r.randrange(200, HEIGHT-90)
        self.start = 0
        self.mode = False
    def update(self):
        if self.rect.y > self.end:
            self.mode = True
        elif self.rect.y < self.start:
            self.mode = False
        if not self.mode:
            self.rect.y = self.rect.y+2
        elif self.mode:
            self.rect.y = self.rect.y-2
# Custom Platform
class CustomPlat           (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir, "boxAlt.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
""" Aesthetic Elements """
class Torch                (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "torchLit.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image = p.transform.scale(self.image, (int(70), int(80)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Window               (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "window.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image = p.transform.scale(self.image, (int(80), int(80)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
""" Statistics Based Elements """
class Lives                (p.sprite.Sprite):
    def __init__(self, x, y, state):
        p.sprite.Sprite.__init__(self)
        if state:
            self.plat = "heart.png"
        else:
            self.plat = "empty_heart.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class KeyHUD               (p.sprite.Sprite):
    def __init__(self, x, y, state):
        p.sprite.Sprite.__init__(self)
        if state:
            self.plat = "hud_keyYellow.png"
        else:
            self.plat = "hud_keyYellow_disabled.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
""" Enemy Elements & Mobs """
# Elements
class Spike                (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "spikes.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image = p.transform.scale(self.image, (int(80), int(30)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 30
class Bomb                 (p.sprite.Sprite):
    def __init__(self, x, y, game):
        p.sprite.Sprite.__init__(self)
        self.explosion_anim = list()
        for i in [1, 2, 1, 2, 1, 2]:
            filename = f'bomb{i}.png'
            img = p.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = p.transform.scale(img, (75, 75))
            self.explosion_anim.append(img_lg)
        self.game = game
        self.image = self.explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.active = False
        self.pos = vec(r.randrange(0,WIDTH), -30)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_update = p.time.get_ticks()
        self.frame_rate = 180
    def update(self):
        if self.active:
            now = p.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.explosion_anim):
                    omega = True
                    hit = p.sprite.spritecollide(self, self.game.bombs, False)
                    if hit:
                        for i in hit:
                            i.active = True
                    if self.game.checkCollide(self, self.game.player):
                        omega = False
                        self.game.player.vel.y = r.randrange(-50, -10)
                        self.game.player.vel.x = r.randrange(-30, 30)
                        self.game.lives -= 1
                    for i in self.game.mobs:
                        if self.game.checkCollide(self, i):
                            i.vel.y = r.randrange(-40, -10)
                            i.vel.x = r.randrange(-30, 30)
                    huts = p.sprite.spritecollide(self, self.game.gt, True)
                    b = Explosion(self.rect.center, self.game, not omega, self.game.expl_snd)
                    self.game.all_sprites.add(b)
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = self.explosion_anim[self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
        self.acc = vec(0, PLAYER_GRA)
        self.vel += self.acc
        self.pos += self.vel + 0 * self.acc
        self.rect.midbottom = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
class Explosion            (p.sprite.Sprite):
    def __init__(self, center, game, omega, snd):
        p.sprite.Sprite.__init__(self)
        self.explosion_anim = list()
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = p.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = p.transform.scale(img, (75, 75))
            self.explosion_anim.append(img_lg)
        self.snd = snd
        self.image = self.explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = p.time.get_ticks()
        self.frame_rate = 50
        self.game = game
        self.omega = omega
    def update(self):
        now = p.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim):
                self.kill()
            elif self.frame == 1:
                self.game.expl_snd.play()
            else:
                hit = p.sprite.spritecollide(self, self.game.bombs, False)
                if hit:
                    for i in hit:
                        i.active = True
                if not self.omega:
                    if self.game.checkCollide(self, self.game.player):
                        self.game.player.vel.y = r.randrange(-50, -10)
                        self.game.player.vel.x = r.randrange(-30, 30)
                        self.game.lives -= 1
                for i in self.game.mobs:
                    if self.game.checkCollide(self, i):
                        i.vel.y = r.randrange(-40, -10)
                        i.vel.x = r.randrange(-30, 30)
                huts = p.sprite.spritecollide(self, self.game.gt, True)
                center = self.rect.center
                try:
                    self.image = self.explosion_anim[self.frame]
                except:
                    pass
                self.rect = self.image.get_rect()
                self.rect.center = center
# Mobs
class Blocker              (p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = p.image.load(path.join(img_dir,"blockerMad.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(r.randrange(0,WIDTH), -30)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    def update(self):
        self.acc = vec(0, PLAYER_GRA)
        self.acc.x += self.vel.x * -PLAYER_FRI
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
""" Powerups & Other good stuff """
class Jumper               (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "jump.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mode = "down"
        self.rect.x = x
        self.rect.y = y
    def up(self, snd):
        snd.play()
        self.plat = "jumpUp.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.mode = "up"
    def down(self):
        self.plat = "jump.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.mode = "down"
    def toggle(self):
        if self.mode == "down":
            self.up()
            self.mode = "up"
        elif self.mode == "up":
            self.down()
            self.mode = "down"
class Heart                (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "gemRed.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class CustomPlatCollector  (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "box.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Coin                 (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "hud_coins.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert_alpha()
        self.image = p.transform.scale(self.image, (int(30), int(30)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Key                  (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "keyYellow.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert_alpha()
        self.image = p.transform.scale(self.image, (int(30), int(30)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class SurpriseBox          (p.sprite.Sprite):
    def __init__(self, x, y):
        p.sprite.Sprite.__init__(self)
        self.plat = "lock_yellow.png"
        self.image = p.image.load(path.join(img_dir, self.plat)).convert_alpha()
        self.image = p.transform.scale(self.image, (int(50), int(50)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
