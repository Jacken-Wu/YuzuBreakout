import pygame
from lib import color


bkg0 = pygame.image.load('./source/background/bkg0.png')
bkg1 = pygame.image.load('./source/background/bkg1.png')
bkg2 = pygame.image.load('./source/background/bkg2.png')
bkg3 = pygame.image.load('./source/background/bkg3.png')
ball = pygame.image.load('./source/item/ball.png')


def init(block_height):
    global bkg0, bkg1, bkg2, bkg3, ball, block_forward1, block_forward2, block_forward3, board
    block_width = block_height * 3
    bkg_width = block_width * 6
    bkg_height = block_height * 27
    ball_width = block_height / 2
    bkg0 = pygame.transform.scale(bkg0, (bkg_width, bkg_height))
    bkg1 = pygame.transform.scale(bkg1, (bkg_width, bkg_height))
    bkg2 = pygame.transform.scale(bkg2, (bkg_width, bkg_height))
    bkg3 = pygame.transform.scale(bkg3, (bkg_width, bkg_height))
    ball = pygame.transform.scale(ball, (ball_width, ball_width))
    block_forward1 = pygame.Surface((block_width + 4, block_height + 4))
    block_forward1.fill(color.lightblue)
    block_forward2 = pygame.Surface((block_width + 4, block_height + 4))
    block_forward2.fill(color.pink)
    block_forward3 = pygame.Surface((block_width + 4, block_height + 4))
    block_forward3.fill(color.red)
    board = pygame.Surface((block_width * 2, block_height))
    board.fill(color.deepgray)
