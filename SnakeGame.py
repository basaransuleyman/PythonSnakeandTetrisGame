import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.display.set_caption('Snake Game Staj')
s_width = 800
s_height = 700
play_width = 800  #  300 // 10 = 30
play_height = 400  # meaning 600 // 20 = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
SURFACE = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), SURFACE)
pygame.display.set_caption("Background Image")
background_image = pygame.image.load('C:/Users/yavru/OneDrive/Masaüstü/SnakeGame/images2.jpg')


class cube(object):  # kup sınıfı
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        self.score = 0

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # konumu degistirme

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   # kup genislik ve boy
        i = self.pos[0]    # row
        j = self.pos[1]     # column

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        # kupun satir ve sutun degerleri  her kupun genisiği ve yüksekliği ile çarpılarak çizilecek yer belirlenir

        if eyes:  # gözlerin çizimi
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)





class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # yılanın kafası
        self.body.append(self.head) # kafaya küp ekleme

        # yılanın hareket yönünü belirleme
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # yılan kendinin herhangi yerine çarpar ise
                pygame.quit()

            keys = pygame.key.get_pressed()   # basılan tuşları gösterme

            for key in keys:          # tuşların tamamını dolaşma
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): # body'deki küplerin içinden geçme
            p = c.pos[:]   # küplerin konumunu grid'de saklama
            if p in self.turns:  # küplerin konumu mevcut konum ise
                turn = self.turns[p]   # dönülecek yön
                c.move(turn[0], turn[1]) # küpü dönülecek yönde hareket ettirme
                if i == len(self.body) - 1:  # body'deki son küp ise  dönüş kalkar
                    self.turns.pop(p)
            else:  # küp dönmüyor ise buraya girecek

                # küp  kenara geldiğinde  karşıya geçmesini sağlar

                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)  # kenara gelmedi ise  devam eden yönde ilerle

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

  # Küpleri yılanın hangi tarafına ekleyeceğimizi bulmak için  hangi yöne hareket ettiğine bakıyoruz sonra küpü sağ,sol,yukarı,aşağıya eklemek sağlanıyor

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))


   # Küplerin  yönünü yılanın gidiş yönüne ayarlanır

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):  # yılanın gözleri
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)   # true ise göz çizim
            else:
                c.draw(surface)   # değiş ise sadece küp cizimi


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows  # cizgiler arası mesafeyi belrirtme

    x = 0  # x kordinat kaydı
    y = 0  # y kordinat kaydı
    for l in range(rows):  # for döngüsü ile yatay ve dikey çizgi çizme
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(background_image, (0, 0, 0), (x, 0), (x, w))
        pygame.draw.line(background_image, (0, 0, 0), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    window.blit(background_image, (0, 0))
    s.draw(surface)   # gridlerin çizilmesi
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update() # ekran güncellemesi


def randomSnack(rows, item):
    positions = item.body  #  yılana ait tüm küplerin pozisyonlarını almak

    while True:   # döngü ile geçerli konum oluşana dek rastgele konum almak
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:

             # yukarıda aldığımız konumun yılan tarafından kullanıldığı kontrol edilir

            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def main(win):  # Oyunun döngüsü oluşturuluyor.
    global width, rows, s, snack
    width = 500 # Ekran boyutu
    rows = 20 # satır
    win = pygame.display.set_mode((width, width)) # ekran nesnesi
    s = snake((255, 0, 0), (10, 10)) #yılan nesnesi
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # main  fonksiyonuna  gider
    flag = True

    clock = pygame.time.Clock() # saat  nesnesi

    while flag:
        pygame.time.delay(50) # Oyun hız ayarı
        clock.tick(10) # fps ayarı 10
        s.move()
        if s.body[0].pos == snack.pos: # head ' in  yenilecek yem ile karşılaştığı kontrol edilir

            s.addCube()  # yılan yemi yer ise küp ekler
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # yenilen yem sonrası yeni yem oluşturma

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                #  body ' deki  pozisyonlardan herhangi bir çakışma olup olmadığı kontrol ediliyor

                print('Score: ', len(s.body))
                message_box('Kaybettin!', 'Tekrar denemek icin tamam demelisin...')
                s.reset((10, 10))
                break

        redrawWindow(win) # ekran yenileme


def main_menu(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Başlamak için bir tuşa basın', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Snake Game Staj')
main_menu(win)