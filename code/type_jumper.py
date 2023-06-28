import pygame as pg
import math
import random as rdm
from sys import exit
pg.init()

# - Game Variables
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960
FPS = 60

# - Game Window Defaults
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Type Jumper')
pg.display.set_icon(pg.image.load("gfx\logos\TJ Icon.png"))  # 32x32
clock = pg.time.Clock()
game_active = False

# - Graphic/Fonts Imports
tj_logo = pg.image.load("gfx/logos/Logo.png").convert_alpha()
start_screen = pg.image.load("gfx/bg/Start.png").convert_alpha()
bg_blur_space = pg.image.load("gfx/bg/Blur Space.png").convert_alpha()
bg_lines = pg.image.load("gfx/bg/Lines.png").convert_alpha()
score_counter = pg.image.load("gfx/bg/Score Counter.png").convert_alpha()
space_man = pg.image.load("gfx/character/Small No Moon.png").convert_alpha()
score_font = pg.font.Font('font/Mont-Heavy.otf', 60)
words_font = pg.font.Font('font/upheavtt.ttf', 45)

# - Infinite Lines Scrolling
lines_height = bg_lines.get_height()
tiles = math.ceil(SCREEN_HEIGHT / lines_height) + 1


def updateScore(score):  # - Score Updater
    score_text = score_font.render(str(score), True, 'White')
    score_pos = score_text.get_rect(center=(SCREEN_WIDTH/2, 50))
    return score_text, score_pos


def getScore():  # - Score Grabber
    score_text = score_font.render(str(score), True, 'White')
    score_pos = score_text.get_rect(center=(SCREEN_WIDTH/2, 50))
    return score_text, score_pos


def getPlat(letCnt):  # - Gets Platform for Word Size
    gfx_link = f'gfx/platforms/{letCnt} Letter.png'
    platform = pg.image.load(gfx_link).convert_alpha()
    return platform


def newWord():  # - Gets a New Word
    randWord = rdm.choice(open("code/word_list.txt", "r").read().split())
    pfrm_gfx = getPlat(len(randWord))
    text = words_font.render(randWord, True, '#CAA8F5')
    return text, pfrm_gfx, randWord


# - Default Variables
getWrd = newWord()
game_speed = 1
line_scroll = 0
score = 0
tScore = 5
curScore = getScore()
wordInd = 0  # Used for Word Completion detection
wordComp = 'y'  # Used for word X location
side = 'R'  # Which way Spaceman Starts Facing
userWrd = ''
lastX = 270

while True:
    # - Background Displays
    screen.blit(bg_blur_space, (0, 0))  # X , Y

    # - BG Line Scrolling
    for i in range(0, tiles):
        y_pos = i * lines_height + line_scroll - lines_height
        screen.blit(bg_lines, (0, y_pos))
    line_scroll += game_speed / 2
    if abs(line_scroll) > lines_height:
        line_scroll = 0

    if game_active:  # ? ACTIVE GAME
        # - Words Display
        if wordComp == 'y':  # Moves Words on X based on word size
            if len(getWrd[2]) >= 6:
                randX = rdm.randint(140, 400)
            if len(getWrd[2]) < 6:
                randX = rdm.randint(100, 440)
            textY = pfrmY = -30
            wordComp = 'n'

        text_pos = getWrd[0].get_rect(center=(randX, textY))
        pfrm_pos = getWrd[1].get_rect(center=(randX, pfrmY))

        # ? User Typing Word
        user_text = words_font.render(userWrd, True, '#B10F2E')
        typer_txt_pos = user_text.get_rect(
            midleft=(text_pos.midleft[0], textY))

        # - Handles Words Lowering and Game Over Event
        if textY < SCREEN_HEIGHT:  # Lowers Words Vertically
            textY += game_speed
            pfrmY += game_speed
        if score == tScore and score % 5 == 0:  # Increases Speed Every 5
            game_speed = game_speed + 0.5
            tScore += 5
        if textY >= 770:  # If word goes lower, game over
            game_active = False
            score = 0

        screen.blit(getWrd[0], text_pos)
        screen.blit(getWrd[1], pfrm_pos)
        screen.blit(user_text, typer_txt_pos)  # ? PRINTS Typing Word

        # - Character Movement
        if randX < lastX:
            # if side == 'R':
            #     space_man = pg.transform.flip(space_man, True, False)
            #     side = 'L'
            for i in range(randX, lastX):
                spaceman_rect = space_man.get_rect(midbottom=(i, 960))
                screen.blit(space_man, spaceman_rect)
        elif randX > lastX:
            # if side == 'L':
            #     space_man = pg.transform.flip(space_man, True, False)
            #     side = 'R'
            for i in range(lastX, randX):
                spaceman_rect = space_man.get_rect(midbottom=(i, 960))
                screen.blit(space_man, spaceman_rect)
        elif randX == lastX:
            spaceman_rect = space_man.get_rect(midbottom=(randX, 960))
            screen.blit(space_man, spaceman_rect)
        lastX = randX

        # - Score Counter Display
        screen.blit(score_counter, (138.5, 0))
        screen.blit(curScore[0], curScore[1])

        # <> Event Loop
        for event in pg.event.get():  # Accepts User Input
            if event.type == pg.QUIT:  # - Quit Game
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # - Pause Game
                game_active = False
                score = 0
                curScore = updateScore(score)

            # - Typing Input and Score Updater
            word = getWrd[2]
            letter = word[wordInd]
            key = getattr(pg, 'K_' + letter)  # pg.K_letter
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    getWrd = newWord()
                if event.key == key and wordInd < len(word):
                    wordInd += 1
                    # ? Adds User Typing Visibilty
                    userWrd += letter

            if wordInd >= len(word):  # Word has been completed
                wordInd = 0
                wordComp = 'y'
                score += 1
                curScore = updateScore(score)
                getWrd = newWord()
                userWrd = ''
    else:  # When Game is over
        screen.blit(start_screen, (0, 0))
        game_speed = 1
        userWrd = ''
        tScore = 5
        score = wordInd = textY = pfrmY = 0
        curScore = updateScore(score)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:  # - Start Game
                getWrd = newWord()
                game_active = True
    clock.tick(FPS)
    pg.display.update()
