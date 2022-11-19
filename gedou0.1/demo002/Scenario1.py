import pygame       #pygame库
import sys          #系统模块
pygame.init()       #初始化模块
import color

from pygame.locals import *     #将不是以下划线_开头的名字都导入到当前的作用域中
white = 255, 255, 255   #白色
blue = 0, 0, 200        #蓝色

#屏幕
SCREEN_WIDTH = 1000     #宽度
SCREEN_HEIGHT = 600     #高度
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#设置屏幕的宽高，screen(屏幕)


#标题
pygame.display.set_caption("牛马")


#帧率
clock = pygame.time.Clock()
FPS = 60

#定义角色1变量
WARRIOR_SIZE = 162
WARRRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFEST = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFEST]


#玩家图片
warrior_sheet = pygame.image.load('img/jige.png').convert_alpha()

wizard_sheet = pygame.image.load('img/jige.png').convert_alpha()

#定义每个动画的动作
WARRIOR_ANIMATION_STEPS = [1]#一行只有一帧动画
#如果一个角色的动画帧一共有三行则，每行有不同的帧动作
#则如果第一行只有一帧动作。第二行有四个帧动作，第三行有六个帧动作第，四行有两个帧动作，写法如下
#WARRTIOR_ANIMATION_STEPS = [1, 4, 6, 2]
WIZARD_ANIMATION_STEPS = [1]

#加载图片
bg_image = pygame.image.load('img/005.png').convert_alpha()
#convert_alpha()方法会使用透明的方法绘制前景对象，
# 因此在加载一个有alpha通道的素材时（比如PNG TGA），需要使用convert_alpha()方法，
# 当然普通的图片也是可以使用这个方法的，用了也不会有什么副作用。
bg2_image = pygame.image.load('img/003.png').convert_alpha()


#背景
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))#变换比例，值是bg_image 背景图片
    screen.blit(scaled_bg, (0, 0))#屏幕位块传送，
#地面
def draw_bg2():
    scaled_bg2 = pygame.transform.scale(bg2_image, (SCREEN_WIDTH, 110))
    screen.blit(scaled_bg2, (0, 490))

#创建角色
class Fighter():#类
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):#__init__方法
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0闲置，1跑步，2跳跃，3攻击，4攻击2，5伤害，6死亡
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]


        self.flip = flip#是否翻转
        self.rect = pygame.Rect((x, y, 80, 180)) #角色rect的宽高
        self.vel_y = 0
        self.jump = False#自己 跳跃
        self.attacking = False#自己 攻击
        self.attack_type = 0#自己 攻击类型
        self.health = 100#自己 健康(血量)
    
    def load_images(self, sprite_sheet, animation_steps):
        #从图像矩阵中遍历图像
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    
    def move(self, screen_width, screer_height, surface, target ):#move 移动
        SPEED = 10 #速度
        GRAVITY = 2 #重力
        dx = 0
        dy = 0

        #按键
        key = pygame.key.get_pressed()

        #攻击判断，如果没有正在攻击可以操作其他操作
        #if self.attacking == False:



        #移动
        if key[pygame.K_a]:#如果按a
            dx = -SPEED
        if key[pygame.K_d]:#如果按d
            dx = SPEED
        

        #跳跃
        if key[pygame.K_w] and self.jump == False:#如果按w
            self.jump = True#角色跳跃真
            self.vel_y = -3
        


        #攻击按键
        if key[pygame.K_r] or key[pygame.K_t]:
            self.attack(surface, target)
            #攻击类型
            if key[pygame.K_r]:
                self.attack_type = 1
            if key[pygame.K_t]:
                self.attack_type = 2




        #调用重力
        self.vel_y += GRAVITY
        dy += self.vel_y

        #确保角色始终在屏幕内
        if self.rect.left + dx < 0: #如果角色的rect的左边小于零
            dx = -self.rect.left    #角色的图像的左边等于它相反的方向，负的方向
            #left(左边)，rect(直，全称rectangle意思是 长方形，pygame里表示图片的图形信息)，self(自己)
        if self.rect.right + dx > screen_width:#如果角色的rect的右边加dx 大于屏幕的宽度
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screer_height - 110:
            self.jump = False#角色跳跃 假，防止还没落在地面上时无限跳跃
            self.vel_y = 0
            dy = screer_height - 110 -self.rect.bottom

        #角色始终面对敌人
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #更新位置
        self.rect.x += dx
        self.rect.y += dy
    #攻击
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            print("攻击")
        pygame.draw.rect(surface, (color.bg_Red), attacking_rect)

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface,(color.bg_Grey), self.rect)#角色的颜色


#创建角色的实例
fighter_1 = Fighter(1, 200,310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)#创建角色实例并设置位置x,y坐标
fighter_2 = Fighter(2, 700,310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
        

run = True
while run:#死循环
    clock.tick(FPS)#帧率

    #绘制背景
    draw_bg()#背景
    draw_bg2()#地面

    #移动方法
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)

    #绘制角色
    fighter_1.draw(screen)#将角色画在屏幕上(draw 画)
    fighter_2.draw(screen)

    for event in pygame.event.get():#对于pygame.event(事件).get()收到，赋值给event
        if event.type == pygame.QUIT:#如果事件type(类型)是 退出，按键
            run = False
            pygame.quit()#关闭pygame
            sys.exit()#退出程序
    
    pygame.display.update()#刷新pygame的屏幕    (display展示、显示，这里的意思是pygame显示器，update更新、刷新)