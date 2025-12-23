import pygame, random, math, os
pygame.init()

# ----- CONFIG -----
WIDTH, HEIGHT = 1000, 560
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tupai Courier - Manual Graphics Optimized")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ----- SAFE LOAD FUNCTION -----
def safe_load(path, w=None, h=None, fill=(80,80,80)):
    """
    Memuat gambar dengan aman.
    Jika file tidak ada, buat surface placeholder.
    """
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            if w and h:
                img = pygame.transform.smoothscale(img, (w, h))
            return img
        except:
            pass
    surf = pygame.Surface((w or 100, h or 100), pygame.SRCALPHA)
    surf.fill(fill)
    return surf

# ----- ASSETS -----
PLAYER_W, PLAYER_H = 120, 120
ENEMY_W, ENEMY_H = 80, 80

player_img = safe_load("courier.png", PLAYER_W, PLAYER_H, (30,140,220))

# Background sesuai level
bg_day    = safe_load("bg_pemandangan.jpg", WIDTH, HEIGHT, (18,40,20))
bg_sunset = safe_load("bg_sunset.png", WIDTH, HEIGHT, (80,40,10))
bg_night  = safe_load("bg_night.jpg", WIDTH, HEIGHT, (10,10,40))
bg_arena  = safe_load("bg_arena.jpg", WIDTH, HEIGHT, (20,20,20))
bg_list = [bg_day, bg_sunset, bg_night, bg_arena]

# ----- GAME STATE -----
player_x = WIDTH//4
player_y = HEIGHT - 140
player_speed = 4
player_scale = 1.0
player_hp = 120
max_hp = 120
facing_right = True

boomerang = None
boomerang_speed = 12

enemies = []
powerups = []
particles = []
PROJECTILE_LIMIT = 6
ENEMY_LIMIT_BASE = 6

score = 0
level = 1
prev_level = 1
transition_alpha = 0
level_changed = False
spawn_enemy_timer = 0
spawn_power_timer = 0
game_over = False

# ----- HELPER FUNCTIONS -----
def clamp(v,a,b):
    """Batasi nilai v agar berada di antara a dan b"""
    return max(a,min(b,v))

def rect_coll(ax,ay,aw,ah,bx,by,bw,bh):
    """Cek collision antara dua rectangle"""
    return ax<bx+bw and ax+aw>bx and ay<by+bh and ay+ah>by

# ----- 1. Algoritma Garis (DDA) -----
def draw_line(screen,x0,y0,x1,y1,color):
    """
    Menggambar garis dari (x0,y0) ke (x1,y1) secara manual menggunakan DDA.
    Digunakan untuk ground, health bar, polygon musuh/powerup.
    """
    dx,dy = x1-x0, y1-y0
    steps = max(abs(dx),abs(dy))
    if steps==0:
        screen.set_at((x0,y0),color)
        return
    x_inc = dx/steps
    y_inc = dy/steps
    x,y = x0,y0
    for _ in range(int(steps)+1):
        xi,yi = int(round(x)),int(round(y))
        if 0<=xi<WIDTH and 0<=yi<HEIGHT:
            screen.set_at((xi,yi),color)
        x+=x_inc
        y+=y_inc

# ----- 2. Algoritma Lingkaran (Midpoint Circle) -----
def draw_circle(screen,xc,yc,r,color):
    """
    Menggambar lingkaran di (xc,yc) dengan radius r.
    Digunakan untuk boomerang, partikel, dan efek hit.
    """
    x=0
    y=r
    d=1-r
    while x<=y:
        points = [(xc+x,yc+y),(xc-x,yc+y),(xc+x,yc-y),(xc-x,yc-y),
                  (xc+y,yc+x),(xc-y,yc+x),(xc+y,yc-x),(xc-y,yc-x)]
        for px,py in points:
            if 0<=px<WIDTH and 0<=py<HEIGHT:
                screen.set_at((px,py),color)
        if d<0:
            d+=2*x+3
        else:
            d+=2*(x-y)+5
            y-=1
        x+=1

# ----- 3. Algoritma Poligon -----
def draw_polygon(screen,points,color):
    """
    Menggambar poligon manual dengan menghubungkan titik-titik.
    Setiap sisi digambar dengan DDA.
    Digunakan untuk enemy dan powerup.
    """
    n=len(points)
    for i in range(n):
        x0,y0=points[i]
        x1,y1=points[(i+1)%n]
        draw_line(screen,x0,y0,x1,y1,color)

# ----- 4. Transformasi Geometris 2D (Rotasi, Translasi, Skala) -----
def rotate_polygon(points, angle_deg, cx, cy):
    """
    Rotasi polygon di sekitar titik (cx,cy) sebesar angle_deg.
    Digunakan untuk animasi musuh berputar.
    """
    angle = math.radians(angle_deg)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    new_points = []
    for x,y in points:
        dx = x-cx
        dy = y-cy
        rx = dx*cos_a - dy*sin_a + cx
        ry = dx*sin_a + dy*cos_a + cy
        new_points.append((rx,ry))
    return new_points

# ----- SPAWN FUNCTIONS -----
def spawn_enemy():
    """Membuat enemy baru sesuai level"""
    limit = ENEMY_LIMIT_BASE + (level-1)*2
    if len(enemies)>=limit: return
    x = WIDTH + random.randint(10,200)
    y = HEIGHT-100
    spd = 1.6 + (level-1)*0.3 + random.random()*0.6
    hp = 50 + (level-1)*20
    enemies.append({"x":x,"y":y,"spd":spd,"hp":hp,"spawn_t":pygame.time.get_ticks(),"angle":0})

def spawn_powerup():
    """Membuat powerup (skala player + HP)"""
    if len(powerups)>=2: return
    px = random.randint(200,WIDTH-200)
    powerups.append({"x":px,"y":HEIGHT-90,"w":28,"h":28})

def spawn_leaf():
    """Membuat partikel daun jatuh (lingkaran)"""
    if len(particles)>220: return
    particles.append({"x":random.randint(0,WIDTH),"y":-10,
                      "dx":random.uniform(-1.2,1.2),"dy":random.uniform(1.0,3.0),
                      "size":random.randint(3,6),"life":random.randint(80,160),
                      "col":(random.randint(40,120),random.randint(90,190),random.randint(20,80))})

def spawn_hit_particles(x,y,col=(255,140,0),count=10):
    """Partikel efek saat terkena musuh/boomerang/powerup"""
    limit = 220-len(particles)
    for _ in range(min(count,max(0,limit))):
        particles.append({"x":x,"y":y,"dx":random.uniform(-4,4),
                          "dy":random.uniform(-4,1),
                          "size":random.randint(3,6),
                          "life":random.randint(18,36),
                          "col":col})

def draw_background(curr_level):
    """Gambar background sesuai level"""
    idx = clamp(curr_level-1,0,len(bg_list)-1)
    screen.blit(bg_list[idx],(0,0))

# ----- MAIN LOOP -----
running = True
while running:
    dt = clock.tick(FPS)/1000.0
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT: running=False
    keys = pygame.key.get_pressed()

    # ----- LEVEL MANAGEMENT -----
    new_level = 1
    if score>=50:new_level=4
    elif score>=25:new_level=3
    elif score>=10:new_level=2
    if new_level!=level:
        prev_level=level
        level=new_level
        level_changed=True
        transition_alpha=255
        player_hp=min(max_hp,player_hp+20)
        if len(enemies)>ENEMY_LIMIT_BASE+(level-1)*2:
            enemies=enemies[:ENEMY_LIMIT_BASE+(level-1)*2]

    draw_background(level)

    if not game_over:
        # ----- PLAYER MOVEMENT (Translasi) -----
        move_dx=0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_dx=-player_speed
            facing_right=False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_dx=player_speed
            facing_right=True
        # Dash
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            dash_dir = -1 if (keys[pygame.K_a] or keys[pygame.K_LEFT]) else (1 if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) else (1 if facing_right else -1))
            player_x+=dash_dir*140
            spawn_hit_particles(player_x,player_y,col=(160,220,255),count=8)
        player_x=clamp(player_x+move_dx,12,WIDTH-PLAYER_W-12)

        # ----- BOOMERANG (Lingkaran & Translasi) -----
        if keys[pygame.K_SPACE] and boomerang is None:
            dirx = 1 if facing_right else -1
            boomerang={"x":player_x+PLAYER_W//2+dirx*18,"y":player_y-40,"dx":dirx*boomerang_speed,"returning":False}
        if boomerang:
            if not boomerang["returning"]:
                boomerang["x"]+=boomerang["dx"]
                if boomerang["x"]<40 or boomerang["x"]>WIDTH-40: boomerang["returning"]=True
            else:
                dx=(player_x+PLAYER_W//2)-boomerang["x"]
                dy=(player_y-40)-boomerang["y"]
                dist=math.hypot(dx,dy)+1e-6
                boomerang["x"]+=dx/dist*boomerang_speed
                boomerang["y"]+=dy/dist*boomerang_speed
                if abs(dx)+abs(dy)<22: boomerang=None

        # ----- PUNCH -----
        now = pygame.time.get_ticks()
        if keys[pygame.K_j]:
            last = getattr(pygame,"_last_punch",0)
            if now-last>360:
                pygame._last_punch=now
                for ie in range(len(enemies)-1,-1,-1):
                    en = enemies[ie]
                    melee_box=(player_x+(60 if facing_right else -60),player_y-PLAYER_H//2,80,PLAYER_H)
                    if rect_coll(melee_box[0],melee_box[1],melee_box[2],melee_box[3],en["x"],en["y"]-ENEMY_H,ENEMY_W,ENEMY_H):
                        en["hp"]-=36*player_scale
                        spawn_hit_particles(en["x"]+ENEMY_W//2,en["y"]-ENEMY_H//2,(255,120,60),8)
                        if en["hp"]<=0:
                            score+=1
                            enemies.pop(ie)

        # ----- SPAWN TIMERS -----
        spawn_enemy_timer+=1
        spawn_power_timer+=1
        enemy_freq=70-(level-1)*8
        if spawn_enemy_timer>max(18,enemy_freq): spawn_enemy();spawn_enemy_timer=0
        if spawn_power_timer>700: spawn_powerup();spawn_power_timer=0
        if random.random()<0.6: spawn_leaf()

        # ----- ENEMY UPDATE -----
        for i in range(len(enemies)-1,-1,-1):
            en=enemies[i]
            en["x"]-=en["spd"]
            en["angle"]+=4  # Rotasi polygon musuh
            if boomerang and rect_coll(boomerang["x"]-12,boomerang["y"]-12,24,24,en["x"],en["y"]-ENEMY_H,ENEMY_W,ENEMY_H):
                en["hp"]-=int(32*player_scale)
                spawn_hit_particles(en["x"]+ENEMY_W//2,en["y"]-ENEMY_H//2,(255,80,80),8)
                en["x"]+=10 if boomerang["dx"]>0 else -10
                boomerang["returning"]=True
                if en["hp"]<=0: enemies.pop(i);score+=1
                continue
            if rect_coll(player_x,player_y-PLAYER_H//2,PLAYER_W,PLAYER_H,en["x"],en["y"]-ENEMY_H,ENEMY_W,ENEMY_H):
                player_hp-=6
                enemies.pop(i)
                continue
            if en["x"]<-ENEMY_W-10: enemies.pop(i);continue
            if en["hp"]<=0: enemies.pop(i);score+=1

        # ----- POWERUPS -----
        for i in range(len(powerups)-1,-1,-1):
            pu=powerups[i]
            if rect_coll(player_x,player_y-PLAYER_H//2,PLAYER_W,PLAYER_H,pu["x"],pu["y"]-pu["h"],pu["w"],pu["h"]):
                player_scale=min(1.9,player_scale+0.3)  # Skala player
                player_hp=min(max_hp,player_hp+28)
                powerups.pop(i)

        # ----- PARTICLES -----
        for i in range(len(particles)-1,-1,-1):
            p=particles[i]
            p["x"]+=p["dx"]
            p["y"]+=p["dy"]
            p["dy"]+=0.06
            p["life"]-=1
            if p["life"]<=0: particles.pop(i)

        if player_hp<=0: game_over=True

    # ----- RENDER -----
    draw_background(level)

    # ground
    draw_line(screen,0,HEIGHT-60,WIDTH,HEIGHT-60,(45,45,45))
    draw_line(screen,0,HEIGHT-54,WIDTH,HEIGHT-54,(90,90,90))

    # powerups
    for pu in powerups:
        pts=[(pu["x"],pu["y"]),(pu["x"]+pu["w"],pu["y"]),(pu["x"]+pu["w"],pu["y"]-pu["h"]),(pu["x"],pu["y"]-pu["h"])]
        draw_polygon(screen,pts,(26,180,50))

    # enemies
    for en in enemies:
        bob=int(4*math.sin(pygame.time.get_ticks()*0.007+en["x"]))
        pts=[(en["x"],en["y"]-ENEMY_H+bob),(en["x"]+ENEMY_W,en["y"]-ENEMY_H+bob),
             (en["x"]+ENEMY_W,en["y"]+bob),(en["x"],en["y"]+bob)]
        # rotasi polygon musuh
        cx = en["x"] + ENEMY_W/2
        cy = en["y"] - ENEMY_H/2 + ENEMY_H/2
        pts = rotate_polygon(pts,en["angle"],cx,cy)
        draw_polygon(screen,pts,(180,50,60))
        hpw=clamp(int((en["hp"]/float(60+(level-1)*20))*ENEMY_W),0,ENEMY_W)
        draw_line(screen,en["x"],en["y"]-ENEMY_H-12,en["x"]+ENEMY_W,en["y"]-ENEMY_H-12,(0,0,0))
        draw_line(screen,en["x"],en["y"]-ENEMY_H-12,en["x"]+hpw,en["y"]-ENEMY_H-12,(90,230,90))

    # boomerang
    if boomerang: draw_circle(screen,int(boomerang["x"]),int(boomerang["y"]),10,(255,230,90))

    # player
    pw=int(PLAYER_W*player_scale);ph=int(PLAYER_H*player_scale)
    pimg=pygame.transform.smoothscale(player_img,(pw,ph))  # skala
    if not facing_right: pimg=pygame.transform.flip(pimg,True,False)  # refleksi horizontal
    screen.blit(pimg,(player_x,player_y-ph//2))

    # particles
    for p in particles: draw_circle(screen,int(p["x"]),int(p["y"]),p["size"],p["col"])

    # HUD
    pygame.draw.rect(screen,(30,30,30),(18,16,260,28))
    pygame.draw.rect(screen,(200,40,40),(30,22,int(220*(player_hp/float(max_hp))),20))
    screen.blit(font.render(f"HP: {int(player_hp)}/{max_hp}",True,(255,255,255)),(260,18))
    screen.blit(font.render(f"SCORE: {score}",True,(255,255,255)),(WIDTH-160,18))
    screen.blit(font.render(f"LEVEL: {level}",True,(255,215,0)),(WIDTH-160,44))
    screen.blit(font.render("A/D: Move  LSHIFT: Dash  SPACE: Boomerang  J: Punch  R:Restart",True,(200,200,200)),(18,HEIGHT-28))

        # level transition
    if level_changed:
        overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        # Transparansi overlay sesuai transition_alpha
        overlay.fill((0,0,0,clamp(int(transition_alpha),0,255)))
        screen.blit(overlay,(0,0))
        txt=font.render(f"LEVEL {level}",True,(255,255,255))
        screen.blit(txt,(WIDTH//2-txt.get_width()//2,HEIGHT//2-txt.get_height()//2))
        transition_alpha-=5
        if transition_alpha<=0:
            level_changed=False
            transition_alpha=0

    # game over screen
    if game_over:
        overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        overlay.fill((8,8,12,180))
        screen.blit(overlay,(0,0))
        msg=font.render("GAME OVER - Press R to Restart",True,(255,160,160))
        screen.blit(msg,(WIDTH//2-msg.get_width()//2,HEIGHT//2-20))
        if keys[pygame.K_r]:
            # reset game
            player_hp=max_hp
            player_x=WIDTH//4
            player_scale=1.0
            enemies.clear()
            powerups.clear()
            particles.clear()
            boomerang=None
            score=0
            level=1
            prev_level=1
            level_changed=True
            transition_alpha=255
            game_over=False

    pygame.display.flip()

pygame.quit()
