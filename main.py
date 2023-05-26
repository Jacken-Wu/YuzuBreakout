import pygame
import math
import random
import time
from lib import color, image, block_constant, sound
from lib.ball_state import ClassBall
from lib.block_state import ClassBlock


pygame.init()
sound.init()

window_width = 480
window_height = 480
block_width = 0
block_height = 0
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

myfont = pygame.font.Font('./source/font/ARIALN.TTF', 25)
myfont2 = pygame.font.Font('./source/font/ARIALN.TTF', 30)
title_font = pygame.font.Font('./source/font/ARIALN.TTF', 50)

# 标题文字
title_img = title_font.render('Yuzu Breakout!', True, color.black)
title_img1 = myfont2.render('Select Game Window Size', True, color.black)
title_img2 = myfont2.render(f'(width x height, Now Size is {window_width} x {window_height})', True, color.black)

# 小界面、中界面、大界面按钮文字
size_img1 = myfont.render(f'{block_constant.block_width_small * 6} x {block_constant.block_height_small * 30}', True, color.black)
size_img2 = myfont.render(f'{block_constant.block_width_middle * 6} x {block_constant.block_height_middle * 30}', True, color.black)
size_img3 = myfont.render(f'{block_constant.block_width_large * 6} x {block_constant.block_height_large * 30}', True, color.black)


# 循环运行标志
running_chose_size = True
running_game = False
game_over = False

# 上一帧鼠标在哪个按钮上
last_mouse_button = 0

pygame.mixer.music.load('./source/BGM/Colorful Mess.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# 游戏界面尺寸选择
while running_chose_size:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_left_up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_chose_size = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_left_up = True

    screen.fill(color.gray)

    screen.blit(title_img, ((480 - title_img.get_width()) // 2, 60))
    screen.blit(title_img1, ((480 - title_img1.get_width()) // 2, 130))
    screen.blit(title_img2, ((480 - title_img2.get_width()) // 2, 160))

    button_left = 144
    button_right = 336
    button_width = 192
    button_height = 48
    button_pos_y = 240
    # 鼠标是否在按钮上的标志
    is_on_button1 = False
    is_on_button2 = False
    is_on_button3 =  False
    if (button_left < mouse_x < button_right) and (button_pos_y < mouse_y < button_pos_y + button_height):
        is_on_button1 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (button_left, button_pos_y, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (button_left, button_pos_y, button_width, button_height))
            if last_mouse_button != 1:
                sound.button_wait.play()
        if mouse_left_up:
            block_width = block_constant.block_width_small
            block_height = block_constant.block_height_small
            running_chose_size = False
            running_game = True
            sound.button_down.play()
        last_mouse_button = 1
    else:
        pygame.draw.rect(screen, color.white, (button_left, button_pos_y, button_width, button_height))
    screen.blit(size_img1, ((window_width - size_img1.get_width()) // 2, button_pos_y + 10))

    button_pos_y += 72
    if (button_left < mouse_x < button_right) and (button_pos_y < mouse_y < button_pos_y + button_height):
        is_on_button2 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (button_left, button_pos_y, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (button_left, button_pos_y, button_width, button_height))
            if last_mouse_button != 2:
                sound.button_wait.play()
        if mouse_left_up:
            block_width = block_constant.block_width_middle
            block_height = block_constant.block_height_middle
            running_chose_size = False
            running_game = True
            sound.button_down.play()
        last_mouse_button = 2
    else:
        pygame.draw.rect(screen, color.white, (button_left, button_pos_y, button_width, button_height))
    screen.blit(size_img2, ((window_width - size_img2.get_width()) // 2, button_pos_y + 10))

    button_pos_y += 72
    if (button_left < mouse_x < button_right) and (button_pos_y < mouse_y < button_pos_y + button_height):
        is_on_button3 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (button_left, button_pos_y, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (button_left, button_pos_y, button_width, button_height))
            if last_mouse_button != 3:
                sound.button_wait.play()
        if mouse_left_up:
            block_width = block_constant.block_width_large
            block_height = block_constant.block_height_large
            running_chose_size = False
            running_game = True
            sound.button_down.play()
        last_mouse_button = 3
    else:
        pygame.draw.rect(screen, color.white, (button_left, button_pos_y, button_width, button_height))
    screen.blit(size_img3, ((window_width - size_img3.get_width()) // 2, button_pos_y + 10))

    if (is_on_button1 or is_on_button2 or is_on_button3) == False:
        last_mouse_button = 0

    pygame.display.flip()

    clock.tick(60)


# 游戏资源初始化
if running_game:
    image.init(block_height)
    window_width = block_width * 6
    window_height = block_height * 30
    board_y_top = block_height * 29.5

    screen = pygame.display.set_mode((window_width, window_height))

    # 初始化砖块
    layer1 = ClassBlock('./data/layer1')
    layer2 = ClassBlock('./data/layer2')
    layer3 = ClassBlock('./data/layer3')

    is_start = False
    prop_time = time.time() + 65535

pygame.mixer.music.stop()
pygame.mixer.music.load('./source/BGM/Hue.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# 游戏主循环
while running_game:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_left_up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_left_up = True
    
    # 更新板子的状态
    board_x_left = mouse_x - (block_height * 3)
    board_x_right = mouse_x + (block_height * 3)
    if board_x_left < 0:
        board_x_left = 0
        board_x_right = block_width * 2
    elif board_x_right > block_width * 6:
        board_x_left = block_width * 4
        board_x_right = block_width * 6
    
    # 发球
    if is_start == False:
        if mouse_left_up:
            start_angle = math.pi / 2 + ((random.random() - 0.5) / 20)
            ClassBall(board_x_left + (block_height * 3), block_height * 29.25, block_height, start_angle, 3)
            prop_time = time.time()
            is_start = True
    if len(ClassBall.all_balls) == 0:
        is_start = False

    # 每10s生成道具
    if is_start:
        now_time = time.time()
        if now_time > prop_time + 20:
            prop_time = now_time

            ball = ClassBall.all_balls[random.randint(0, len(ClassBall.all_balls) - 1)]

            prop = random.randint(0, 1)
            if prop == 0:
                start_angle = ball.angle + ((random.random() - 0.5) / 3)
                if start_angle >= 2 * math.pi:
                    start_angle -= 2 * math.pi
                elif start_angle < 0:
                    start_angle += 2 * math.pi

                if 0 <= start_angle < math.pi / 6:
                    start_angle = math.pi / 6
                elif 5 * math.pi / 6 < start_angle <= math.pi:
                    start_angle = 5 * math.pi / 6
                elif math.pi < start_angle < 7 * math.pi / 6:
                    start_angle = 7 * math.pi / 6
                elif 11 * math.pi < start_angle < 2 * math.pi:
                    start_angle = 11 * math.pi / 6
                
                ClassBall(ball.x, ball.y, block_height, start_angle, 3)

            elif prop == 1:
                ball.speed += 2 * block_height / 20

    # 检测碰撞，更新状态
    out1 = []
    out2 = []
    out3 = []
    if layer3.block_count > 0:
        for ball in ClassBall.all_balls:
            crash_blocks = ball.crash_block(block_height, layer3.map)
            ball.crash_wall(block_height)
            ball.crash_board(block_height, board_x_left)
            is_out = ball.is_out(block_height)
            ball.update_state()

            for pos in crash_blocks:
                if layer3.map[pos[0]][pos[1]] == '1':
                    layer3.map[pos[0]][pos[1]] = '0'
                    layer3.block_count -= 1
                    if random.randint(0, 1) == 0:
                        sound.block_break1.play()
                    else:
                        sound.block_break2.play()
            if is_out:
                out3.append(ball)
        for ball in out3:
            ClassBall.all_balls.remove(ball)

    elif layer2.block_count > 0:
        for ball in ClassBall.all_balls:
            crash_blocks = ball.crash_block(block_height, layer2.map)
            ball.crash_wall(block_height)
            ball.crash_board(block_height, board_x_left)
            is_out = ball.is_out(block_height)
            ball.update_state()

            for pos in crash_blocks:
                if layer2.map[pos[0]][pos[1]] == '1':
                    layer2.map[pos[0]][pos[1]] = '0'
                    layer2.block_count -= 1
                    if random.randint(0, 1) == 0:
                        sound.block_break1.play()
                    else:
                        sound.block_break2.play()
            if is_out:
                out2.append(ball)
        for ball in out2:
            ClassBall.all_balls.remove(ball)

    elif layer1.block_count > 0:
        for ball in ClassBall.all_balls:
            crash_blocks = ball.crash_block(block_height, layer1.map)
            ball.crash_wall(block_height)
            ball.crash_board(block_height, board_x_left)
            is_out = ball.is_out(block_height)
            ball.update_state()

            for pos in crash_blocks:
                if layer1.map[pos[0]][pos[1]] == '1':
                    layer1.map[pos[0]][pos[1]] = '0'
                    layer1.block_count -= 1
                    if random.randint(0, 1) == 0:
                        sound.block_break1.play()
                    else:
                        sound.block_break2.play()
            if is_out:
                out1.append(ball)
        for ball in out1:
            ClassBall.all_balls.remove(ball)

    # 判断是否结束
    if (layer1.block_count == 0) and (layer2.block_count == 0) and (layer3.block_count == 0):
        running_game = False
        game_over = True


    # 更新画面
    screen.fill(color.lightgray)
    screen.blit(image.bkg0, (0, 0))

    # 砖块
    layer1_forward_blits = []
    layer1_blits = []
    layer2_forward_blits = []
    layer2_blits = []
    layer3_forward_blits = []
    layer3_blits = []
    for line in range(27):
        for num in range(6):
            if layer1.map[line][num] == '1':
                layer1_forward_blit = (image.block_forward1, (num * block_width - 2, line * block_height - 2))
                layer1_blit = (image.bkg1, (num * block_width, line * block_height), (num * block_width, line * block_height, block_width, block_height))
                layer1_forward_blits.append(layer1_forward_blit)
                layer1_blits.append(layer1_blit)
            if layer2.map[line][num] == '1':
                layer2_forward_blit = (image.block_forward2, (num * block_width - 2, line * block_height - 2))
                layer2_blit = (image.bkg2, (num * block_width, line * block_height), (num * block_width, line * block_height, block_width, block_height))
                layer2_forward_blits.append(layer2_forward_blit)
                layer2_blits.append(layer2_blit)
            if layer3.map[line][num] == '1':
                layer3_forward_blit = (image.block_forward3, (num * block_width - 2, line * block_height - 2))
                layer3_blit = (image.bkg3, (num * block_width, line * block_height), (num * block_width, line * block_height, block_width, block_height))
                layer3_forward_blits.append(layer3_forward_blit)
                layer3_blits.append(layer3_blit)
    if (layer2.block_count == 0) and (layer3.block_count == 0):
        screen.blits(layer1_forward_blits)
    screen.blits(layer1_blits)
    if layer3.block_count == 0:
        screen.blits(layer2_forward_blits)
    screen.blits(layer2_blits)
    screen.blits(layer3_forward_blits)
    screen.blits(layer3_blits)

    # 板子
    screen.blit(image.board, (board_x_left, board_y_top))

    # 球
    if is_start:
        ball_blits = []
        for ball in ClassBall.all_balls:
            ball_blit = (image.ball, (ball.x - ball.r, ball.y - ball.r))
            ball_blits.append(ball_blit)
        screen.blits(ball_blits)
    else:
        ball_x = board_x_left + (block_height * 2.75)
        ball_y = block_height * 29
        screen.blit(image.ball, (ball_x, ball_y))

    pygame.display.flip()

    clock.tick(60)


if game_over:
    title_font = pygame.font.Font('./source/font/ARIALN.TTF', int(block_height * 1.8))
    game_over_img = title_font.render('You Win!', True, color.black)

    pygame.mixer.music.stop()
    pygame.mixer.music.load('./source/BGM/Pixel Time.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


# 结束画面
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
    
    screen.fill(color.lightgray)
    screen.blit(image.bkg0, (0, 0))

    screen.blit(game_over_img, ((window_width - game_over_img.get_width()) / 2, block_height * 27.5))

    pygame.display.flip()