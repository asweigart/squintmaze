# S q u i n t   M a z e
# By Al Sweigart al@inventwithpython.com @AlSweigart

# You are the blue dot.
# Go to the green dot.
#
# Arrow keys / WASD to move.
# Esc to quit. (Autosaves)
# T to view time elapsed.
# M to restart game.

# Simplified BSD License, Copyright 2014 Al Sweigart

# Attribution:
# Orchestra Tuning In Concert Hall, Crowd Gathering In Background; Orchestra Washes https://www.sounddogs.com/previews/2665/mp3/1137458_SOUNDDOGS__or.mp3
# Everything you thought of VII-VIII - Unthunk http://freemusicarchive.org/music/Unthunk/
# Radio Tuning Sound Effect - Audio Productions https://www.youtube.com/watch?v=JdPlUyMW6NQ



# NOTE: Seriously, don't play this game that much. You'll ruin your eyes. Just edit the SAVED_GAME.txt file and cheat like everyone else does.


import pygame, sys, time, os, datetime
from pygame.locals import *

# Various constants here
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (51, 0, 255)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

pygame.init()
DISPLAY = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('Squint')
pygame.mouse.set_visible(False)
CLOCK = pygame.time.Clock()

FPS = 10
SAVE_GAME_FILE = 'SAVED_GAME.txt'
END_POINT = (1914, 1074)
END_POINT_RECT = pygame.Rect((END_POINT[0], END_POINT[1], 2, 2))
CELLSIZE = 2
GAME_START_TIME = None

MAZE_IMAGE = pygame.image.load('maze.png')
MAZE_RECT = MAZE_IMAGE.get_rect()

#FONT = pygame.font.SysFont(None, 24)
FONT = pygame.font.Font('freesansbold.ttf', 24)

def main():
    global PX, PY, STEPS, ELAPSED, GAME_START_TIME

    PX, PY, STEPS, ELAPSED = loadSavedGame()
    titleSequence()

    GAME_START_TIME = time.time() - ELAPSED
    moveDirection = None

    # initially display maze
    DISPLAY.blit(MAZE_IMAGE, MAZE_RECT)
    pygame.draw.rect(DISPLAY, BLUE, getPlayerRect())
    pygame.draw.rect(DISPLAY, GREEN, END_POINT_RECT)
    pygame.display.update()

    # play the background music
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1, 0.0)

    while True:
        # handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key in (K_UP, ord('w')):
                    moveDirection = UP
                elif event.key in (K_DOWN, ord('s')):
                    moveDirection = DOWN
                elif event.key in (K_LEFT, ord('a')):
                    moveDirection = LEFT
                elif event.key in (K_RIGHT, ord('d')):
                    moveDirection = RIGHT
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == ord('m'):
                    fadeScreen()
                    displayMToRestartScreen()
                elif event.key == ord('t'):
                    fadeScreen()
                    displayElapsed()

        # move the player
        if moveDirection:
            pixArr = pygame.PixelArray(DISPLAY)
            probe = getPlayerRect().topleft
            # NOTE: In order for this probe code to work, the outline of the maze image must be black. (This code doesn't check if the probe has gone off the screen.)
            if moveDirection == UP:
                while True:
                    probe = (probe[0], probe[1] - CELLSIZE) # move up one cell
                    if pixArr[probe] == DISPLAY.map_rgb(BLACK): # hit a black cell
                        probe = (probe[0], probe[1] + CELLSIZE) # go back
                        break
                    if pixArr[probe[0] - CELLSIZE, probe[1]] == DISPLAY.map_rgb(WHITE) or pixArr[probe[0] + CELLSIZE, probe[1]] == DISPLAY.map_rgb(WHITE):
                        break # hit an intersection
            elif moveDirection == DOWN:
                while True:
                    probe = (probe[0], probe[1] + CELLSIZE) # move down one cell
                    if pixArr[probe] == DISPLAY.map_rgb(BLACK): # hit a black cell
                        probe = (probe[0], probe[1] - CELLSIZE) # go back
                        break
                    if pixArr[probe[0] - CELLSIZE, probe[1]] == DISPLAY.map_rgb(WHITE) or pixArr[probe[0] + CELLSIZE, probe[1]] == DISPLAY.map_rgb(WHITE):
                        break # hit an intersection
            elif moveDirection == LEFT:
                while True:
                    probe = (probe[0] - CELLSIZE, probe[1]) # move left one cell
                    if pixArr[probe] == DISPLAY.map_rgb(BLACK): # hit a black cell
                        probe = (probe[0] + CELLSIZE, probe[1]) # go back
                        break
                    if pixArr[probe[0], probe[1] - CELLSIZE] == DISPLAY.map_rgb(WHITE) or pixArr[probe[0], probe[1] + CELLSIZE] == DISPLAY.map_rgb(WHITE):
                        break # hit an intersection
            elif moveDirection == RIGHT:
                while True:
                    probe = (probe[0] + CELLSIZE, probe[1]) # move right one cell
                    if pixArr[probe] == DISPLAY.map_rgb(BLACK): # hit a black cell
                        probe = (probe[0] - CELLSIZE, probe[1]) # go back
                        break
                    if pixArr[probe[0], probe[1] - CELLSIZE] == DISPLAY.map_rgb(WHITE) or pixArr[probe[0], probe[1] + CELLSIZE] == DISPLAY.map_rgb(WHITE):
                        break # hit an intersection
            del pixArr

            # Do the movement animation
            while getPlayerRect().topleft != probe:
                STEPS += 1
                if moveDirection == UP:
                    PY -= CELLSIZE
                elif moveDirection == DOWN:
                    PY += CELLSIZE
                elif moveDirection == LEFT:
                    PX -= CELLSIZE
                elif moveDirection == RIGHT:
                    PX += CELLSIZE

                # display maze
                DISPLAY.blit(MAZE_IMAGE, MAZE_RECT)
                pygame.draw.rect(DISPLAY, BLUE, getPlayerRect())
                pygame.draw.rect(DISPLAY, GREEN, END_POINT_RECT)

                pygame.display.update()
                CLOCK.tick(FPS)
            moveDirection = None

            if (PX, PY) == END_POINT:
                displayEndSequence()

        # draw the blinking player
        if (time.time() % 1) / 4 < 0.125:
            pygame.draw.rect(DISPLAY, BLUE, getPlayerRect())
        else:
            pygame.draw.rect(DISPLAY, WHITE, getPlayerRect())
        pygame.display.update()
        CLOCK.tick(FPS)


def fadeScreen():
    origSurface = DISPLAY.copy()
    fadeSurface = pygame.Surface((1920, 1080)).convert_alpha()

    for alpha in range(0, 192, 16):
        DISPLAY.blit(origSurface, (0, 0))
        fadeSurface.fill((0, 0, 0, alpha))
        DISPLAY.blit(fadeSurface, (0, 0))
        pygame.display.update()


def displayMToRestartScreen():
    pressM = pygame.image.load('pressMAgain.png')
    r = pressM.get_rect()
    r.center = (1920 / 2, 1080 / 2)
    DISPLAY.blit(pressM, r)
    displaySpaceToContinue()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key in (K_ESCAPE, ord(' '), K_RETURN):
                    DISPLAY.blit(MAZE_IMAGE, MAZE_RECT)
                    pygame.display.update()
                    return
                elif event.key == ord('m'):
                    restartGame()
                    DISPLAY.blit(MAZE_IMAGE, MAZE_RECT)
                    pygame.display.update()
                    return


def restartGame():
    global PX, PY, STEPS, ELAPSED, GAME_START_TIME

    # Start the game over by reseting all the global variables
    PX = CELLSIZE
    PY = CELLSIZE
    STEPS = 0
    ELAPSED = 0
    GAME_START_TIME = time.time()


def displayEndSequence():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('radiotuning.mp3')
    pygame.mixer.music.play(0, 0.0)
    fadeScreen()

    theEnd = pygame.image.load('theEnd.png')
    r = theEnd.get_rect()
    r.center = (1920 / 2, 200)
    DISPLAY.blit(theEnd, r)

    displayElapsed()
    restartGame()

    # restart the background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1, 0.0)


def displayElapsed():
    textObj = FONT.render('Elapsed: %s' % (datetime.timedelta(seconds=(round(time.time() - GAME_START_TIME)))), 1, WHITE)
    textRect = textObj.get_rect()
    textRect.midtop = (1920 / 2, 400)
    pygame.draw.rect(DISPLAY, BLACK, textRect)
    DISPLAY.blit(textObj, textRect)

    textObj = FONT.render('Steps: %s' % (STEPS), 1, WHITE)
    textRect = textObj.get_rect()
    textRect.midtop = (1920 / 2, 500)
    pygame.draw.rect(DISPLAY, BLACK, textRect)
    DISPLAY.blit(textObj, textRect)

    displaySpaceToContinue()
    displayPlayerLocationAndHold()

    # refresh display away from faded out look
    DISPLAY.blit(MAZE_IMAGE, MAZE_RECT)
    pygame.display.update()

def loadSavedGame():
    if os.path.exists(SAVE_GAME_FILE):
        fp = open(SAVE_GAME_FILE)
        px, py, steps, elapsed = fp.readline().split(',')
        px, py, steps, elapsed = int(px), int(py), int(steps), float(elapsed)
        fp.close()
        return px, py, steps, elapsed
    else:
        return (CELLSIZE, CELLSIZE, 0, 0)


def getPlayerRect():
    return pygame.Rect((PX, PY, CELLSIZE, CELLSIZE))


def terminate():
    if GAME_START_TIME is not None:
        ELAPSED = time.time() - GAME_START_TIME
    fp = open(SAVE_GAME_FILE, 'w')
    fp.write('%s,%s,%s,%s' % (PX, PY, STEPS, ELAPSED))
    fp.close()

    pygame.quit()
    sys.exit()


def waitUntilEscOrSpace(duration=None, flashImage=None, flashRect=None):
    startTime = time.time()
    while True:
        if duration is not None and startTime + duration < time.time():
            return 'space'

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return 'esc'
                if event.key in (ord(' '), K_RETURN):
                    return 'space'

        if flashImage is not None:
            if (time.time() % 1) / 2 < 0.25:
                DISPLAY.blit(flashImage, flashRect)
                pygame.display.update()
            else:
                pygame.draw.rect(DISPLAY, BLACK, flashRect)
                pygame.display.update()

def displaySpaceToContinue():
    # display space to continue
    space = pygame.image.load('space.png')
    r = space.get_rect()
    r = space.get_rect()
    r.center = (1920 / 2, 900)
    DISPLAY.blit(space, r)
    pygame.display.update()


def displayPlayerLocationAndHold():
    # display "You are the blue dot"
    # TODO - deal with other quadrants in case of the text going off the screen later
    youAre = pygame.image.load('youAre.png')
    r = youAre.get_rect()
    r.topleft = (PX + 6 + 10 + 20, PY + 3)
    DISPLAY.blit(youAre, r)

    upLeft = pygame.image.load('upLeftArrow.png')
    r = upLeft.get_rect()
    r.topleft = (PX + 6, PY + 3)
    displaySpaceToContinue()
    pygame.display.update()
    return waitUntilEscOrSpace(None, upLeft, r)


def titleSequence():
    introSound = pygame.mixer.Sound('intro.wav')
    introSound.play()

    # display "Esc to skip"
    DISPLAY.fill(BLACK)
    escToSkip = pygame.image.load('escToSkip.png')
    r = escToSkip.get_rect()
    r.bottomright = (1900, 1060)
    DISPLAY.blit(escToSkip, r)
    pygame.display.update()
    if waitUntilEscOrSpace(2) == 'esc':
        introSound.stop()
        return

    # display black screen
    DISPLAY.fill(BLACK)
    pygame.display.update()
    if waitUntilEscOrSpace(1) == 'esc':
        introSound.stop()
        return

    # display title & credits
    title = pygame.image.load('title.png')
    r = title.get_rect()
    r.center = (1920 / 2, 1080 / 2)
    DISPLAY.blit(title, r)

    credit1 = pygame.image.load('credit1.png')
    r = credit1.get_rect()
    r.topleft = (1200, 700)
    DISPLAY.blit(credit1, r)
    credit2 = pygame.image.load('credit2.png')
    r = credit2.get_rect()
    r.topleft = (1200, 740)
    DISPLAY.blit(credit2, r)

    pygame.display.update()
    if waitUntilEscOrSpace(4) == 'esc':
        introSound.stop()
        return

    displaySpaceToContinue()
    pygame.display.update()
    if waitUntilEscOrSpace() == 'esc':
        introSound.stop()
        return

    # display instructions
    DISPLAY.fill(BLACK)
    pygame.display.update()
    if waitUntilEscOrSpace(0.25) == 'esc':
        introSound.stop()
        return

    arrowKeys = pygame.image.load('arrowkeys.png')
    r = arrowKeys.get_rect()
    r.topleft = (800, 500)
    DISPLAY.blit(arrowKeys, r)
    pygame.display.update()
    if waitUntilEscOrSpace(0.25) == 'esc':
        introSound.stop()
        return

    esc = pygame.image.load('esc.png')
    r = esc.get_rect()
    r.topleft = (800, 540)
    DISPLAY.blit(esc, r)
    pygame.display.update()
    if waitUntilEscOrSpace(0.25) == 'esc':
        introSound.stop()
        return

    t = pygame.image.load('t.png')
    r = t.get_rect()
    r.topleft = (800, 580)
    DISPLAY.blit(t, r)
    pygame.display.update()
    if waitUntilEscOrSpace(0.25) == 'esc':
        introSound.stop()
        return

    m = pygame.image.load('m.png')
    r = m.get_rect()
    r.topleft = (800, 620)
    DISPLAY.blit(m, r)
    pygame.display.update()
    if waitUntilEscOrSpace(0.25) == 'esc':
        introSound.stop()
        return


    displaySpaceToContinue()


    if waitUntilEscOrSpace() == 'esc':
        introSound.stop()
        return


    DISPLAY.fill(BLACK)
    pygame.draw.rect(DISPLAY, BLUE, getPlayerRect())
    pygame.draw.rect(DISPLAY, GREEN, END_POINT_RECT)

    if displayPlayerLocationAndHold() == 'esc':
        introSound.stop()
        return

    DISPLAY.fill(BLACK)
    pygame.draw.rect(DISPLAY, BLUE, getPlayerRect())
    pygame.draw.rect(DISPLAY, GREEN, END_POINT_RECT)

    # display "Go to the green dot"
    goTo = pygame.image.load('goTo.png')
    r = goTo.get_rect()
    r.bottomright = (END_POINT[0] - 4 - 10 - 20, END_POINT[1] - 4)
    DISPLAY.blit(goTo, r)

    downRight = pygame.image.load('downRightArrow.png')
    r = downRight.get_rect()
    r.bottomright = (END_POINT[0] - 4, END_POINT[1] - 4)
    displaySpaceToContinue()
    pygame.display.update()
    if waitUntilEscOrSpace(None, downRight, r) == 'esc':
        introSound.stop()
        return

    introSound.stop()


if __name__ == '__main__':
    main()