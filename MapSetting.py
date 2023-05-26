import pygame
from lib import color, image, block_constant, sound
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
title_img = title_font.render('Map Setting!', True, color.black)
title_img1 = myfont2.render('Select Game Window Size', True, color.black)
title_img2 = myfont2.render(f'(width x height, Now Size is {window_width} x {window_height})', True, color.black)

# 小界面、中界面、大界面按钮文字
size_img1 = myfont.render(f'{block_constant.block_width_small * 6} x {block_constant.block_height_small * 30}', True, color.black)
size_img2 = myfont.render(f'{block_constant.block_width_middle * 6} x {block_constant.block_height_middle * 30}', True, color.black)
size_img3 = myfont.render(f'{block_constant.block_width_large * 6} x {block_constant.block_height_large * 30}', True, color.black)


# 循环运行标志
running_chose_size = True
running_game = False

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

    screen = pygame.display.set_mode((window_width, window_height))

    # 初始化砖块
    layer1 = ClassBlock('./data/layer1')
    layer2 = ClassBlock('./data/layer2')
    layer3 = ClassBlock('./data/layer3')

    myfont3 = pygame.font.Font('./source/font/ARIALN.TTF', block_height)
    layer1_img = myfont3.render('layer1', True, color.black)
    layer2_img = myfont3.render('layer2', True, color.black)
    layer3_img = myfont3.render('layer3', True, color.black)
    confirm_img = myfont3.render('confirm', True, color.black)

    last_mouse_button = 0

    # 是否是添加砖块模式
    add_layer1 = False
    add_layer2 = False
    add_layer3 = False


pygame.mixer.music.stop()
pygame.mixer.music.load('./source/BGM/Hue.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# 游戏主循环
while running_game:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_left_up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_left_up = True

    # 选层
    # 鼠标是否在按钮上的标志
    is_on_button1 = False
    is_on_button2 = False
    is_on_button3 =  False
    is_on_button4 = False

    button_width = block_width * 2
    button_height = block_height * 2
    button_top = block_height * 27
    button_left = 0
    if (button_left < mouse_x < button_left + button_width) and (button_top < mouse_y < button_top + button_height):
        is_on_button1 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (button_left, button_top, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (button_left, button_top, button_width, button_height))
            if last_mouse_button != 1:
                sound.button_wait.play()
        if mouse_left_up:
            add_layer1 = True
            add_layer2 = False
            add_layer3 = False
            sound.button_down.play()
        last_mouse_button = 1
    else:
        pygame.draw.rect(screen, color.white, (button_left, button_top, button_width, button_height))
    screen.blit(layer1_img, (button_left + (button_width - layer1_img.get_width()) / 2, block_height * 27.4))

    button_left = button_width
    if (button_left < mouse_x < button_left + button_width) and (button_top < mouse_y < button_top + button_height):
        is_on_button2 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (button_left, button_top, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (button_left, button_top, button_width, button_height))
            if last_mouse_button != 2:
                sound.button_wait.play()
        if mouse_left_up:
            add_layer1 = False
            add_layer2 = True
            add_layer3 = False
            sound.button_down.play()
        last_mouse_button = 2
    else:
        pygame.draw.rect(screen, color.white, (button_left, button_top, button_width, button_height))
    screen.blit(layer2_img, (button_left + (button_width - layer2_img.get_width()) / 2, block_height * 27.4))

    button_left = button_width * 2
    if (button_left < mouse_x < button_left + button_width) and (button_top < mouse_y < button_top + button_height):
        is_on_button3 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (button_left, button_top, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (button_left, button_top, button_width, button_height))
            if last_mouse_button != 3:
                sound.button_wait.play()
        if mouse_left_up:
            add_layer1 = False
            add_layer2 = False
            add_layer3 = True
            sound.button_down.play()
        last_mouse_button = 3
    else:
        pygame.draw.rect(screen, color.white, (button_left, button_top, button_width, button_height))
    screen.blit(layer3_img, (button_left + (button_width - layer3_img.get_width()) / 2, block_height * 27.4))

    button_top += button_height
    button_width *= 3
    button_height = block_height
    if (0 < mouse_x < button_width) and (button_top < mouse_y < button_top + block_height):
        is_on_button4 = True
        if mouse_buttons[0]:
            pygame.draw.rect(screen, color.deepgray, (0, button_top, button_width, button_height))
        else:
            pygame.draw.rect(screen, color.lightgray, (0, button_top, button_width, button_height))
            if last_mouse_button != 4:
                sound.button_wait.play()
        if mouse_left_up:
            layer1.write()
            layer2.write()
            layer3.write()
            sound.button_down.play()
        last_mouse_button = 4
    else:
        pygame.draw.rect(screen, color.white, (0, button_top, button_width, button_height))
    screen.blit(confirm_img, ((button_width - confirm_img.get_width()) / 2, block_height * 29))

    if (is_on_button1 or is_on_button2 or is_on_button3 or is_on_button4) == False:
        last_mouse_button = 0


    # 编辑砖块
    line = int(mouse_y // block_height)
    num = int(mouse_x // block_width)
    if (0 <= line <= 26) and (0 <= num <= 5):
        if mouse_buttons[0]:
            if add_layer1 and (layer1.map[line][num] == '0'):
                layer1.map[line][num] = '1'
                layer1.block_count += 1
            elif add_layer2 and (layer2.map[line][num] == '0'):
                layer2.map[line][num] = '1'
                layer2.block_count += 1
            elif add_layer3 and (layer3.map[line][num] == '0'):
                layer3.map[line][num] = '1'
                layer3.block_count += 1

        if mouse_buttons[2]:
            if add_layer1 and (layer1.map[line][num] == '1'):
                layer1.map[line][num] = '0'
                layer1.block_count -= 1
            elif add_layer2 and (layer2.map[line][num] == '1'):
                layer2.map[line][num] = '0'
                layer2.block_count -= 1
            elif add_layer3 and (layer3.map[line][num] == '1'):
                layer3.map[line][num] = '0'
                layer3.block_count -= 1


    # 更新砖块画面
    screen.blit(image.bkg0, (0, 0))
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
    if add_layer1:
        screen.blits(layer1_forward_blits)
        screen.blits(layer1_blits)
    elif add_layer2:
        screen.blits(layer1_blits)
        screen.blits(layer2_forward_blits)
        screen.blits(layer2_blits)
    elif add_layer3:
        screen.blits(layer1_blits)
        screen.blits(layer2_blits)
        screen.blits(layer3_forward_blits)
        screen.blits(layer3_blits)

    pygame.display.flip()

    clock.tick(60)
