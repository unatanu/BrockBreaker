import random
import sys
from pygame.locals import *
import pygame
import math
import time

# pygame初期化
pygame.init()

# 画面サイズの設定
screen_WIDTH = 600     #  幅
screen_HEIGHT = 600    #  高さ（上から下向きに伸びる）
blank = 10
game_screen_W = screen_WIDTH * 2 // 3
game_screen_H = screen_HEIGHT - 4*blank
info_screen_W = screen_WIDTH // 4
info_screen_H = screen_HEIGHT // 3

# 画面の作成
screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))
line_width = 4  # ゲーム画面の枠線の太さ
game_x = 2*blank  # ゲーム画面の左上x座標
game_y = blank  # ゲーム画面の左上y座標
info_x = 3*blank + game_screen_W  # 情報ボックスの左上x座標
info_y = blank  # 情報ボックスの左上y座標


# ボールの設定
RADIUS = 10             # 半径
x0 = game_screen_W/2    # 初期x座標
y0 = game_screen_H*2/3  # 初期y座標
BALL_SPEED = 1.5        # 移動速度
BALL_NUM = 2            # ボールの個数
BALL_WAIT_TIME = 1.0    # ボールが複数個でゲームを開始したとき、動き始めのタイミングをずらす時間
BALL_SCORE = 100        # ボールが最後まで残ったときのボーナス得点


# ブロックの設定
BLOCK_NUM_B = 5  # 横に並べるブロックの数
BLOCK_NUM_V = 10  # 縦
BLOCK_POS_LIM = game_screen_H//2  # ブロックを配置する高さの制限
BLOCK_WIDTH = (game_screen_W - line_width)//BLOCK_NUM_B  # 幅
BLOCK_HEIGHT = BLOCK_POS_LIM//BLOCK_NUM_V  # 高さ


# バーの設定
BAR_WIDTH = 150  # バーの幅
BAR_HEIGHT = 20  # バーの高さ
BAR_POS_y = game_screen_H-10  # バーの底のy座標
BAR_COLOR = ["crimson", "silver"]  # バーの色


# 色の定義
COLOR_SET_1 = ["red","blue","forestgreen","gold"]
COLOR_SET_2 = ["darkorange","deepskyblue","lime","yellow"]
COLOR_SET_3 = ["blueviolet","dodgerblue","gold","orange"]
COLOR_SET_4 = ["limegreen","magenta","slateblue","cyan"]
COLORS = random.choice([COLOR_SET_1, COLOR_SET_2, COLOR_SET_3, COLOR_SET_4])  # カラーセットの中からランダムに一つのセットを選ぶ
        

class Bar:
    def __init__(self, screen, init_x):  # width, height, color
        self.screen = screen
        self.x = init_x
        self.y = BAR_POS_y
        self.color = "silver"

        # 指定した位置に矩形を表示
        pygame.draw.rect(self.screen, self.color, (self.x - BAR_WIDTH/2, self.y - BAR_HEIGHT, BAR_WIDTH, BAR_HEIGHT))
        # pygame.draw.rect(self.screen, self.color_center, (self.x - BAR_WIDTH/6, self.y - BAR_HEIGHT, BAR_WIDTH/3, BAR_HEIGHT))  # 真ん中は色を変える

    def move(self, pre_x, new_x):
        self.pre_x = pre_x
        self.new_x = new_x
        pygame.draw.rect(self.screen, "white", (self.pre_x - BAR_WIDTH/2, self.y - BAR_HEIGHT, BAR_WIDTH, BAR_HEIGHT))  # 移動前のバーを削除
        pygame.draw.rect(self.screen, self.color, (self.new_x - BAR_WIDTH/2, self.y - BAR_HEIGHT, BAR_WIDTH, BAR_HEIGHT))  # 移動後のバーを表示
        # pygame.draw.rect(self.screen, self.color_center, (self.new_x - BAR_WIDTH/6, self.y - BAR_HEIGHT, BAR_WIDTH/3, BAR_HEIGHT))

    def input(self, move_right, move_left, BAR_x):
        # 矢印キーが押されている間バーを動かし続けるための処理
        for event in pygame.event.get():
            if event.type == QUIT:  # ×が押されたらゲームを終了
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:  # キーが押されたとき
                if event.key == K_ESCAPE:  # escキーでゲームを終了
                    pygame.quit()
                    sys.exit()

                elif event.key == K_LEFT:
                    move_left = True
                elif event.key == K_RIGHT:
                    move_right = True

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    move_left = False
                elif event.key == K_RIGHT:
                    move_right = False

        pre_x = BAR_x
        if move_left:
            if BAR_x-BAR_WIDTH/2 <= game_x + line_width: # バーが画面外にはみ出たとき
                BAR_x -= 0
                
            else:
                BAR_x -= 3
        elif move_right:
            if BAR_x+BAR_WIDTH/2 >= game_x + game_screen_W - line_width:  # バーが画面外にはみ出たとき
                BAR_x += 0
            else:
                BAR_x += 3

        return move_right, move_left, BAR_x, pre_x


class Ball:
    def __init__(self, screen, x, y):
        # 関数内の変数と外部の変数の紐づけ
        self.screen = screen
        self.x = x
        self.y = y

        self.degree = math.radians(random.randint(45,135))  # ボールの射出角度
        self.vel_x = BALL_SPEED * math.cos(self.degree)
        self.vel_y = BALL_SPEED * math.sin(self.degree)
        self.r = RADIUS
        self.accel = 1.0  # ボールの加速度（下の方でこの値をいじっている）

        # ボールとその枠線の描画
        pygame.draw.circle(screen, "yellow", (self.x, self.y), self.r)
        pygame.draw.circle(screen, "black", (self.x, self.y), self.r, width=1)

    # ボールの位置を更新
    def move(self):
        # self.accel = accel
        self.x += self.vel_x * self.accel
        self.y += self.vel_y * self.accel
        # 移動前のボールを削除
        pygame.draw.circle(screen, "white", (self.x - self.vel_x * self.accel, self.y - self.vel_y * self.accel), self.r)
        # 移動後のボールを描画
        pygame.draw.circle(screen, "yellow", (self.x, self.y), self.r)
        pygame.draw.circle(screen, "black", (self.x, self.y), self.r, width=1)

    # ボールの衝突判定
    def check_collision(self):

        # ボールが画面の側面に当たったとき
        if self.x - self.r <= game_x + line_width or self.x + self.r >= game_x + game_screen_W - line_width:
            self.vel_x *= -1
        # ボールが画面の上部に当たったとき
        if self.y - self.r <= game_y + line_width:
            self.vel_y *= -1
        
        # バーの衝突判定
        if (BAR_POS_y - BAR_HEIGHT <= self.y + self.r <= BAR_POS_y) and self.vel_y >= 0:  # バーの高さにきたとき　かつ　ボールが下向きに動いているとき

            if BAR_x - BAR_WIDTH/2 <= self.x <= BAR_x + BAR_WIDTH/2:
                # self.degree = math.atan2(self.vel_y, self.vel_x)  # ぶつかる瞬間のボールの角度を計算（右向きから時計回り、ラジアン）
                # theta = math.radians(30)  # バーの端の方に当たったときに変化させる角度
                self.vel_y *= -1

                """
                if bar_mode == 0:
                    self.vel_y *= -1
                    return
                elif bar_mode == 1:  # 左向きに反射
                    if self.vel_x >= 0:
                        self.degree += -2*self.degree - theta  # 垂直寄りに変化
                    else:
                        self.degree += 2*(math.pi - self.degree) - theta  # 角度を浅く変化 
                else:  # 右向きに反射
                    if self.vel_x >= 0:
                        self.degree += -2*self.degree + theta  # 角度を浅く変化
                    else:
                        self.degree += 2*(math.pi - self.degree) + theta  # 垂直寄りに変化
                
                self.vel_x = BALL_SPEED * math.cos(self.degree) * self.accel
                self.vel_y = BALL_SPEED * math.sin(self.degree) * self.accel
                """


      
class Block:

    def __init__(self, screen, x, y, color):
        # 関数内の変数と外部の変数の紐づけ
        self.screen = screen
        self.x1 = x
        self.y1 = y
        self.x2 = x + BLOCK_WIDTH
        self.y2 = y + BLOCK_HEIGHT
        self.color = color

        # 指定した位置に矩形を表示
        pygame.draw.rect(self.screen,self.color,(self.x1, self.y1, BLOCK_WIDTH, BLOCK_HEIGHT))

    # ボールとブロックの衝突判定
    def check_collision_x(self, ball_x, ball_y):  # x方向判定
        self.ball_x = ball_x
        self.ball_y = ball_y

        if ((self.x1 <= self.ball_x - RADIUS <= self.x2) and (self.y1 <= self.ball_y <= self.y2)) or ((self.x1 <= self.ball_x + RADIUS <= self.x2) and (self.y1 <= self.ball_y <= self.y2)):
            pygame.draw.rect(self.screen,"white",(self.x1, self.y1, BLOCK_WIDTH, BLOCK_HEIGHT))
            return True
        return False
    def check_collision_y(self, ball_x, ball_y):  # y方向判定
        self.ball_x = ball_x
        self.ball_y = ball_y

        if ((self.x1 <= self.ball_x <= self.x2) and (self.y1 <= self.ball_y - RADIUS <= self.y2)) or ((self.x1 <= self.ball_x <= self.x2) and (self.y1 <= self.ball_y + RADIUS <= self.y2)):
            pygame.draw.rect(self.screen,"white",(self.x1, self.y1, BLOCK_WIDTH, BLOCK_HEIGHT))
            return True
        return False
    


class Message:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 70)
        self.font_message = pygame.font.SysFont(None, 45)
        self.font_common = pygame.font.SysFont(None, 35)


    # タイトル画面に表示する文字
    def title(self):
        self.text_title = self.font_title.render("BROCK BREAKER", True, "black")
        self.text_start = self.font_message.render("PRESS SPACE TO START", True, "black")
        self.rect_title = self.text_title.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 3))
        self.rect_start = self.text_start.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2))
        screen.blit(self.text_title, self.rect_title)
        screen.blit(self.text_start, self.rect_start)

        self.words = ["", "OPTION", "QUIT"]
        for i in range(len(self.words)):
            self.text = self.font_common.render(self.words[i], True, "black")
            self.rect = self.text.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2 + 40*(i+1)))
            screen.blit(self.text, self.rect)

    # タイトル画面の選択肢部分に表示する文字
    def select(self):
        pygame.draw.rect(screen,"white",(0, game_y + game_screen_H // 2 + 40, screen_WIDTH, game_screen_H // 2))  # 選択肢部分のみ白く塗りつぶし
        for i in range(len(self.words)):
            if i == select_num:  # 選ばれている選択肢の文字を大きくする
                self.text_selected = self.font_message.render(self.words[i], True, "black")
                self.rect_selected = self.text_selected.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2 + 40*(i+1)))
                screen.blit(self.text_selected, self.rect_selected)
            else:
                self.text_other = self.font_common.render(self.words[i], True, "black")
                self.rect_other = self.text_other.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2 + 40*(i+1)))
                screen.blit(self.text_other, self.rect_other)

    # タイトル画面のオプションを開いたときに表示する文字
    def option(self, BALL_NUM, BALL_SPEED):
        pygame.draw.rect(screen,"white",(0, game_y + game_screen_H // 2 + 40, screen_WIDTH, game_screen_H // 2))
        self.options = ["", "NUM BALL", "BALL SPEED", "TITLE"]
        for i in range(len(self.options)):
            if i == select_num:  # 選ばれている選択肢の文字を大きくする
                self.text_selected = self.font_message.render(self.options[i], True, "black")
                self.rect_selected = self.text_selected.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2 + 40*(i+1)))
                screen.blit(self.text_selected, self.rect_selected)
            else:
                self.text_other = self.font_common.render(self.options[i], True, "black")
                self.rect_other = self.text_other.get_rect(center=(screen_WIDTH // 2, screen_HEIGHT // 2 + 40*(i+1)))
                screen.blit(self.text_other, self.rect_other)

        # 数字の横につける矢印の表示
        self.font_path = pygame.font.match_font('Arial')
        self.font = pygame.font.Font(self.font_path, 35)
        self.num = [BALL_NUM, BALL_SPEED]
        self.arrow = ["<", ">"]
        for j in range(2):
            # 矢印の表示
            for k in range(2):
                self.text_arrow = self.font.render(self.arrow[k], True, "black")
                self.rect_arrow = self.text_arrow.get_rect(center=(screen_WIDTH // 2 + 100 + 60*k, screen_HEIGHT // 2 + 40*(j+2)))
                screen.blit(self.text_arrow, self.rect_arrow)
            # 数字の表示
            self.text_num = self.font_common.render(f"{self.num[j]}", True, "black")
            self.rect_num = self.text_num.get_rect(center=(screen_WIDTH // 2 + 100 + 30, screen_HEIGHT // 2 + 40*(j+2)))
            screen.blit(self.text_num, self.rect_num)

    # 画面右上の情報を表示
    def info(self, SCORE):
        pygame.draw.rect(screen, "white", (info_x + line_width, info_y + line_width, info_screen_W - 2*line_width, info_screen_H - 2*line_width))
        self.font_info = pygame.font.SysFont(None, 30)
        self.text_score = self.font_info.render(f"SCORE: {SCORE}", True, "black")
        self.rect_score = self.text_score.get_rect(center=(info_screen_W // 2 + info_x, info_screen_H // 2 + info_y))
        screen.blit(self.text_score, self.rect_score)

    # ゲームオーバーになったときの文字
    def gameover(self):
        transparent_surface = pygame.Surface((300, 100), pygame.SRCALPHA)  # メッセージボックス（幅、高さ）
        transparent_surface.fill((255, 50, 50, 200))  # メッセージボックスの色と透明度

        self.text_gameover = self.font_message.render("GAME OVER!", True, "black")
        self.text_score = self.font_common.render(f"SCORE: {SCORE}", True, "black")
        self.text_back = self.font_common.render("ENTER: BACK TO TITLE", True, "black")
        
        self.rect_message = self.text_gameover.get_rect(center=(transparent_surface.get_width() // 2, transparent_surface.get_height() // 2))
        self.rect1 = self.text_start.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y + 60))
        self.rect2 = self.text_score.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y + 120))
        self.rect3 = self.text_back.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y + 160))

        transparent_surface.blit(self.text_gameover, self.rect_message)
        screen.blit(transparent_surface, (game_screen_W // 2 + game_x - transparent_surface.get_width() // 2, game_screen_H // 2 + game_y - transparent_surface.get_height() // 2 - 100))
        screen.blit(self.text_start, self.rect1)
        screen.blit(self.text_score, self.rect2)
        screen.blit(self.text_back, self.rect3)

    # クリアしたときの文字
    def clear(self):
        self.text_clear = self.font_message.render("CLEAR!", True, "black")
        self.text_score = self.font_common.render(f"SCORE: {SCORE}", True, "black")
        self.text_back = self.font_common.render("ENTER: BACK TO TITLE", True, "black")

        self.rect_message = self.text_clear.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y - 100 ))
        self.rect1 = self.text_score.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y + 60))
        self.rect2 = self.text_start.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y + 120))
        self.rect3 = self.text_back.get_rect(center=(game_screen_W // 2 + game_x, game_screen_H // 2 + game_y + 160))

        screen.blit(self.text_clear, self.rect_message)
        screen.blit(self.text_score, self.rect1)
        screen.blit(self.text_start, self.rect2)
        screen.blit(self.text_back, self.rect3)

message = Message()




# フラグの初期設定
running = True          # プログラムを進行させるかを示す（ここはいじらない）
game_started = False    # ゲームが開始されたかどうかを示す
is_gameover = False     # ゲームオーバーになったかを示す
is_clear = False        # クリアしたかを示す
title = True            # タイトル画面かを示す

select_num = 0  # 何番目の選択肢を選んでいるか
option_window = 0  # 何番目の選択肢階層にいるか




# 実際に動く部分
while running:

    # ゲームが開始されていない場合
    if not game_started:

        # メッセージの表示
        if not is_gameover:  # タイトル画面
            screen.fill("white")
            message.title()
        else:
            if is_gameover and not is_clear:  # ゲームオーバーしたとき
                message.gameover()
            else:  # クリアしたとき
                message.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:  # enterが押されたとき
                        screen.fill("white")
                        message.title()
                        title = True
                        select_num = 0
                        option_window = 0
                    
                    # スペースキーが押されたらゲームを開始する
                    if event.key == pygame.K_SPACE:
                        set_up = False
                        is_gameover = False
                        is_clear = False
                        game_started = True           
        pygame.display.update()


        # タイトル画面での処理
        while title:
            # ゲーム開始の処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:  # escキーでゲームを終了
                        pygame.quit()
                        sys.exit()

                    # タイトル画面でオプションを選んでいるとき
                    if option_window == 0:
                        # 矢印キーの上下が押されたとき、対応する選択肢の文字を大きくする
                        if event.key == K_DOWN:
                            select_num += 1
                        elif event.key == K_UP:
                            select_num -= 1
                        select_num = select_num % len(message.words)  # 値が大きすぎたりマイナスになるのを回避
                        message.select()
                        pygame.display.update()

                        # 選択肢が選ばれたとき
                        if event.key == K_RETURN:  # enterが押されたとき
                            if message.words[select_num] == "OPTION":
                                select_num = 0
                                option_window = 1
                                message.option(BALL_NUM, BALL_SPEED)
                                pygame.display.update()
                            elif message.words[select_num] == "QUIT":
                                pygame.quit()
                                sys.exit()
                    
                    # オプションの中身を表示している場合
                    if option_window == 1:
                        # 矢印キーを押したとき、対応する文字を大きくするための変数管理
                        if event.key == K_DOWN:
                            select_num += 1
                        elif event.key == K_UP:
                            select_num -= 1
                        select_num = select_num % len(message.options) 

                        # 該当するオプションの数値を増減させる
                        if event.key == K_RIGHT:
                            if message.options[select_num] == "NUM BALL":
                                    BALL_NUM += 1
                            elif message.options[select_num] == "BALL SPEED":
                                BALL_SPEED += .1
                        elif event.key == K_LEFT:
                            if message.options[select_num] == "NUM BALL":
                                    BALL_NUM -= 1
                            elif message.options[select_num] == "BALL SPEED":
                                BALL_SPEED -= .1
                        BALL_NUM = BALL_NUM % 11  # 0~10の範囲内のみ
                        BALL_SPEED = BALL_SPEED % 5.1  # 0.0~5.0の範囲内のみ
                        BALL_SPEED = round(BALL_SPEED, 2)  # 少数第2位を四捨五入

                        message.option(BALL_NUM, BALL_SPEED)
                        pygame.display.update()

                        # 選択肢が選ばれたとき
                        if event.key == K_RETURN:  # enterが押されたとき
                            if message.options[select_num] == "TITLE":
                                select_num = 0
                                option_window = 0
                                message.select()
                                pygame.display.update()

                    # スペースキーが押されたらゲームを開始する
                    if event.key == pygame.K_SPACE:
                        set_up = False
                        is_gameover = False
                        is_clear = False
                        game_started = True
                        title = False
        


    # ゲームが開始されている場合
    while game_started:
        # ゲーム開始時の初回設定
        if not set_up:
            screen.fill("white")
            # ゲーム画面、インフォメーション画面の作成
            pygame.draw.rect(screen, "black", Rect(game_x, game_y, game_screen_W, game_screen_H),4)
            pygame.draw.rect(screen, "black", Rect(info_x, info_y, info_screen_W, info_screen_H), line_width)

            # 各ブロック、各ボールの生成
            blocks = [Block(screen, ix*BLOCK_WIDTH + game_x + line_width, iy*BLOCK_HEIGHT + game_y, random.choice(COLORS)) for ix in range(game_screen_W//BLOCK_WIDTH) for iy in range(BLOCK_POS_LIM//BLOCK_HEIGHT)]
            balls = [Ball(screen,x0,y0) for i in range(BALL_NUM)]
            # バーの位置の初期化
            BAR_x = game_screen_W/2  # バーの中心x座標
            bar = Bar(screen, BAR_x)
            # バーの入力の初期化
            move_left = False
            move_right = False

            SCORE = 0  # スコア
            message.info(SCORE)  # スコアの表示
            pre_time = time.time()  # 現在の時刻を取得
            limit_num = 0  # 開始直後に動けるボールの数（下の方で増える処理がある）

            set_up = True  # 準備完了
            pygame.display.update()

        

        # メインループ
        if not is_gameover or not is_clear:
            move_right, move_left, BAR_x, pre_x = bar.input(move_right, move_left, BAR_x)
            bar.move(pre_x, BAR_x)


            ball_count = 0  # 動いているボールのインデックス
            for ball in balls:
                ball.move()
                ball.check_collision()
                # ブロックとの接触判定
                for block in blocks:
                    if block.check_collision_x(ball.x, ball.y):
                        blocks.remove(block)
                        SCORE += 10
                        message.info(SCORE)
                        ball.vel_x *= -1
                    elif block.check_collision_y(ball.x, ball.y):
                        blocks.remove(block)
                        SCORE += 10
                        message.info(SCORE)
                        ball.vel_y *= -1


                # 残りのブロック数が少なくなるほどボールスピードが速くなる
                ball.accel = round(2.0 - len(blocks) / (BLOCK_NUM_B * BLOCK_NUM_V), 3)

                # ボールが画面底部を抜けたとき
                if ball.y - ball.r >= game_screen_H:
                    balls.remove(ball)
                    pygame.draw.circle(screen, "white", (ball.x, ball.y), ball.r)
                    if len(balls) == 0:  # ボールが全てなくなったとき
                        is_gameover = True
                        game_started = False


                # ゲーム開始時のボール待機の処理
                if limit_num < BALL_NUM - 1:
                    now_time = time.time()  # 現在の時刻を取得
                    ball_count += 1  # 現在動いているボールの番号

                    # ここでブレイクすることで、後続のボールが動く前に次のループに入る
                    if ball_count > limit_num:
                        if now_time - pre_time < BALL_WAIT_TIME:  # 経過時間が待機時間より短いとき
                            break
                        else:  # 充分待機したとき
                            pre_time = now_time
                            limit_num += 1  # 何番のボールまで動けるかを数える
                            break
                


            # 残りのブロック数が0になったとき（クリアしたとき）
            if len(blocks) == 0:
                SCORE += len(balls) * BALL_SCORE  # 残りのボールの数得点が加算
                is_clear = True
                game_started = False
            
            
            
            # 画面を更新する
            pygame.draw.rect(screen, "black", Rect(2*blank, blank, game_screen_W, game_screen_H),4)  # ゲーム画面の枠線を書き直し
            pygame.display.update()
            pygame.time.delay(10)
        

# Pygameの終了
pygame.quit()
sys.exit()