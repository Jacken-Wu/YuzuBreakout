import pygame


def init():
    global button_down, button_wait, block_break1, block_break2
    button_down = pygame.mixer.Sound('./source/sound/button_down.wav')
    button_wait = pygame.mixer.Sound('./source/sound/button_wait.wav')
    block_break1 = pygame.mixer.Sound('./source/sound/block_break1.wav')
    block_break2 = pygame.mixer.Sound('./source/sound/block_break2.wav')
    
    button_down.set_volume(0.2)
    button_wait.set_volume(0.2)
    block_break1.set_volume(0.2)
    block_break2.set_volume(0.2)
