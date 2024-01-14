import pygame as pg
import random as rand
import math 
import cv2
class BallCharacter:
  def get_ball(self,frame):
    self.ballv = frame%3+1
  def ball_set(self):
    self.r = self.ballv*15
    self.pos = pg.Vector2(450,173-self.r)
    self.v = pg.Vector2(0,0)
    self.a = pg.Vector2(0,0)
    self.c = pg.Color(self.ballv*25,self.ballv*10,250// self.ballv)
    self.dropped = False
    self.touched = False
class PlayerCharacter:
  def __init__(self):
    self.score = 0
    self.drop = False
    self.half = False
class retry:
  def __init__(self,disp_w,disp_h):
    self.x = disp_w/2
    self.y = disp_h/2-30
    self.color = (255,241,0)
  def update(self,u,d,l,r):
    for event in pg.event.get():
      if event.type == pg.MOUSEBUTTONDOWN:
        x,y = event.pos
        if y>=u and y<=d and x>=l and x<=r:
          return True

def istouch_ball(bi,bj):
  return (bi.pos.y-bj.pos.y)**2+(bi.pos.x-bj.pos.x)**2 <=  (bi.r+bj.r)**2
def power(a,b):
  rec = 1
  while(b>0):
    if(b%2==0):
      a*=a
      b/=2
    else:
      rec*=a
      b-=1
  return rec
def main():
  # 初期化処理
  pg.init() 
  pg.display.set_caption('Merge 2048')
  disp_w, disp_h = 1000, 750
  leftline_x = 150
  rightline_x = 750
  lowerline_y = 700
  upperline_y = 153
  screen = pg.display.set_mode((disp_w,disp_h)) # WindowSize
  clock  = pg.time.Clock()
  font   = pg.font.Font(None,15)
  frame  = rand.randint(0,5)
  frame_in = 0
  exit_flag = False
  exit_code = '000'
  cmd_c = 0
  e = 0.30
  ingame = True
  setup = True
  title = []
  title.append(pg.image.load(f'data/img/alphabet_m.png'))
  title.append(pg.image.load(f'data/img/alphabet_e.png'))
  title.append(pg.image.load(f'data/img/alphabet_r.png'))
  title.append(pg.image.load(f'data/img/alphabet_g.png'))
  title.append(pg.image.load(f'data/img/alphabet_e.png'))
  title.append(pg.image.load(f'data/img/alphabet_s.png'))
  title.append(pg.image.load(f'data/img/alphabet_c.png'))
  title.append(pg.image.load(f'data/img/alphabet_o.png'))
  title.append(pg.image.load(f'data/img/alphabet_r.png'))
  title.append(pg.image.load(f'data/img/alphabet_e.png'))
  title_size = pg.Vector2(48,48)
  number = []
  number.append(pg.image.load(f'data/img/keyboard_0_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_1_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_2_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_3_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_4_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_5_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_6_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_7_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_8_black.png'))
  number.append(pg.image.load(f'data/img/keyboard_9_black.png'))
  number_size = pg.Vector2(48,48)
  for i in range(len(title)):
    title[i] = pg.transform.smoothscale(title[i],title_size)
  for i in range(len(number)):
    number[i] = pg.transform.smoothscale(number[i],number_size)
  power_2 = []
  for i in range(10):
    power_2.append(power(2,i+1))
  # ゲームループ
  while not exit_flag:
    if(setup):
        player = PlayerCharacter()
        ball_arr = []
        ball_arr.append(BallCharacter())
        ball_arr[-1].get_ball(frame)
        ball_arr[-1].ball_set()
        setup = False
      # システムイベントの検出
    for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True
          exit_code = '001'
        if event.type == pg.KEYDOWN:
          # スペースキーが押下されたら jump を True に
          if event.key == pg.K_SPACE and frame_in == 0:
            player.drop = True
            player.score += power_2[ball_arr[-1].ballv-1]
            ball_arr[-1].dropped = True
            ball_arr.append(BallCharacter())
            ball_arr[-1].get_ball(frame)
            ball_arr[-1].ball_set()
            frame_in = 30
          if event.key == pg.K_LEFT:
            cmd_c = 1
          if event.key == pg.K_RIGHT:
            cmd_c = 2
        if event.type == pg.KEYUP:
          if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
            cmd_c = 0
    if(ingame):
        # 背景描画
        screen.fill(pg.Color('White'))
        # ボールの描画と位置計算
        for i in range(len(ball_arr)):
          bi = ball_arr[i]
          rpr2 = bi.r/(math.sqrt(2))
          pg.draw.circle(screen,bi.c,bi.pos,bi.r)
          font1 = pg.font.Font(None,(int)(rpr2)) 
          ballt = f'{power_2[bi.ballv-1]}'
          screen.blit(font1.render(ballt,True,'BLACK'),(bi.pos.x-rpr2/3*len(ballt),bi.pos.y-rpr2/2))
        if player.drop:
          ball_arr[-2].a.y = 0.8
          ball_arr[-2].v.x = rand.uniform(-0.10,0.10)
          player.drop = False
        if cmd_c==1:
          ball_arr[-1].pos.x = max(ball_arr[-1].pos.x-5,ball_arr[-1].r//2)
        if cmd_c==2:
          ball_arr[-1].pos.x = min(ball_arr[-1].pos.x+5,disp_w-ball_arr[-1].r//2)
        ## 地面との衝突処理
        for i in range(len(ball_arr)-1):
          bi = ball_arr[i]
          for j in range(i+1,len(ball_arr)):
            if(i!=j):
              bj = ball_arr[j]
              if (bi.dropped==False) or (bj.dropped==False):
                continue
              if istouch_ball(bi,bj) :
                #合成
                if(bi.touched):
                  bj.touched = True
                if(bj.touched):
                  bi.touched = True
                if bi.ballv == bj.ballv:
                  if bi.ballv==10:
                    player.score+=1024
                    ball_arr.pop(i)
                    ball_arr.pop(j)
                    break
                  player.score += power_2[bi.ballv-1]
                  bi.ballv+=1
                  bi.r +=15
                  bi.c = pg.Color(bi.ballv*25,bi.ballv*10,250// bi.ballv)
                  ball_arr.pop(j)
                  break
                #衝突計算   
                a = (bi.v.x)**2-2*(bi.v.x*bj.v.x)+(bj.v.x)**2+(bi.v.y)**2-2*(bi.v.y*bj.v.y)+(bj.v.y)**2
                b = 2*(bi.pos.x * bi.v.x)-2*(bi.pos.x * bj.v.x)-2*(bi.v.x*bj.pos.x)+2*(bj.pos.x * bj.v.x)+2*(bi.pos.y * bi.v.y)-2*(bi.pos.y * bj.v.y)-2*(bi.v.y * bj.pos.y)+2*(bj.pos.y * bj.v.y)
                c = (bi.pos.x)**2-2*(bi.pos.x*bj.pos.x)+(bj.pos.x)**2+(bi.pos.y)**2-2*(bi.pos.y*bj.pos.y)+(bj.pos.y)**2-(bi.r+bj.r)*(bi.r+bj.r)
                d = b*b-4*a*c
                if(d>0):
                  d = math.sqrt(d)
                  if(a==0):
                    f0 = 0
                    f1 = 0
                  else:
                    f0 = (-b-d)/(2*a)
                    f1 = (-b+d)/(2*a)
                  hit = False
                  if(f0>=0) and (f0<=1):
                    bi.pos.x += bi.v.x*f0
                    bi.pos.y += bi.v.y*f0
                    bj.pos.x += bj.v.x*f0
                    bj.pos.y += bj.v.y*f0
                    hit = True
                  elif(f0*f1<0):
                    vx = bi.pos.x-bj.pos.x
                    vy = bi.pos.y-bj.pos.y
                    D = math.sqrt(vx*vx+vy*vy)
                    distance = bi.r+bj.r-D
                    if(D>0):
                      D = 1/D
                    vx *= D
                    vy *= D
                    distance/=2.0
                    bi.pos.x += vx * distance
                    bi.pos.y += vy * distance
                    bj.pos.x -= vx * distance
                    bj.pos.y -= vy * distance
                    hit = True
                  if(hit):
                    vx = bj.pos.x-bi.pos.x
                    vy = bj.pos.y-bi.pos.y
                    t = -(vx*bi.v.x+vy*bi.v.y)/(vx*vx+vy*vy)
                    arx = bi.v.x+vx*t
                    ary = bi.v.y+vy*t
                    t = -(-vy*bi.v.x+vx*bi.v.y)/(vx*vx+vy*vy)
                    amx = bi.v.x-vy*t
                    amy = bi.v.y+vx*t
                    t = -(vx*bj.v.x+vy*bj.v.y)/(vx*vx+vy*vy)
                    brx = bj.v.x+vx*t
                    bry = bj.v.y+vy*t
                    t = -(-vy*bj.v.x+vx*bj.v.y)/(vx*vx+vy*vy)
                    bmx = bj.v.x-vy*t
                    bmy = bj.v.y+vx*t
                    adx = (bi.r*bi.r*amx+bj.r*bj.r*bmx+bmx*e*bj.r*bj.r-amx*e*bj.r*bj.r)/(bi.r*bi.r+bj.r*bj.r)
                    bdx = -e*(bmx-amx)+adx
                    ady = (bi.r*bi.r*amy+bj.r*bj.r*bmy+bmy*e*bj.r*bj.r-amy*bj.r*bj.r*e)/(bi.r*bi.r+bj.r*bj.r)
                    bdy = -e*(bmy-amy)+ady
                    bi.v.x = (adx+arx)
                    bi.v.y = (ady+ary)
                    bj.v.x = (bdx+brx)
                    bj.v.y = (bdy+bry)
          else:
            continue
          break
        # 地面描画
        for i in range(len(ball_arr)):
          bi = ball_arr[i]
          bi.pos += bi.v
          bi.v += bi.a
          #摩擦
          if bi.pos.y >= disp_h - lowerline_y-bi.r :
            bi.v.x*=0.9
          ## 地面との衝突
          if bi.pos.y >= lowerline_y - bi.r :
            bi.pos.y = lowerline_y - bi.r
            bi.v.y *= -0.3
            bi.touched = True
          ## 右端と左端との衝突
          if bi.pos.x + bi.r > rightline_x :
            bi.pos.x = rightline_x - bi.r
            bi.v.x *= -0.6
          elif bi.pos.x - bi.r < leftline_x:
            bi.pos.x = bi.r+leftline_x
            bi.v.x *= -0.6
          if abs(bi.v.y) <= 0.3:
            bi.v.y = 0
          if abs(bi.v.x) < 0.3:
            bi.v.x = 0
          if(i!=len(ball_arr)-1):
            if(bi.pos.y-bi.r<=(upperline_y+20+lowerline_y)/4) and (bi.touched):
              player.half = True
            if(bi.pos.y-bi.r<=upperline_y+20) and (bi.touched):
              ingame = False
        for i in range(5):
          screen.blit(title[i],(((leftline_x+rightline_x)/2-title_size.x*6)+(title_size.x+5)*i,5))
        screen.blit(number[2],(((leftline_x+rightline_x)/2-title_size.x*6)+(title_size.x+5)*6-29,5))
        screen.blit(number[0],(((leftline_x+rightline_x)/2-title_size.x*6)+(title_size.x+5)*7-34,5))
        screen.blit(number[4],(((leftline_x+rightline_x)/2-title_size.x*6)+(title_size.x+5)*8-39,5))
        screen.blit(number[8],(((leftline_x+rightline_x)/2-title_size.x*6)+(title_size.x+5)*9-44,5))
        pg.draw.line(screen,10,(leftline_x,upperline_y),(leftline_x,lowerline_y))
        pg.draw.line(screen,10,(rightline_x,upperline_y),(rightline_x,lowerline_y))
        pg.draw.line(screen,10,(leftline_x,lowerline_y),(rightline_x,lowerline_y))
        scr_str = f'{player.score:04}'
        for i in range(5):
          screen.blit(title[i+5],((rightline_x+disp_w)/2-title_size.x*(7/2-i)+5*i,5))
        for i in range(4):
          screen.blit(number[int(scr_str[i])],((rightline_x+disp_w)/2-title_size.x*(1/2)-number_size.x*(2-i),(5+title_size.x+upperline_y)/2-number_size.x/2))
        if(player.half):
          for x in range(leftline_x,rightline_x,20):
            pg.draw.line(screen,10,(x,upperline_y+20),(x+10,upperline_y+20))
            player.half = False
    else:
        #
        pg.draw.rect(screen,(255,255,255),(disp_w/2-200,disp_h/2-300,400,420),200)
        pg.draw.rect(screen,(0,0,0),(disp_w/2-200,disp_h/2-300,400,420),5)
        font2 = pg.font.Font(None,90)
        screen.blit(font2.render(f'GAME OVER',True,'BLACK'),(disp_w/2-200+10,disp_h/2-300+10))
        scr_str = f'{player.score:04}'
        for i in range(5):
          screen.blit(pg.transform.smoothscale(title[i+5],(70,70)),(disp_w/2-75*(5/2-i),disp_h/2-220))
        for i in range(4):
          screen.blit(pg.transform.smoothscale(number[int(scr_str[i])],(90,90)),(disp_w/2-90*(2-i),disp_h/2-110))
        button = retry(disp_w,disp_h)
        pg.draw.rect(screen,(button.color),(disp_w/2-190,disp_h/2,380,100),190)
        screen.blit(pg.font.Font(None,100).render(f'RETRY',True,'BLACK'),(disp_w/2-120,disp_h/2+20))
        if(button.update(disp_h/2,disp_h/2+100,disp_w/2-190,disp_w/2+190)):
          ingame = True
          setup = True       
    # 画面の更新と同期
    frame += 1
    frame_in -= 1
    if(frame_in<0):
      frame_in = 0
    pg.display.update()
    clock.tick(60)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')