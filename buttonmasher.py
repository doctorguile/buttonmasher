# Button Masher 0.3.0
# Joystick input logging program
# Copyright (C) 2004 Matthew Bennett

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (LICENSE.TXT) for more details.

# Refactoring: Move all drawing to display class?

import sys, pygame
from pygame.event import *

class JoystickState:
    def __init__(self):
        self.axes = [0, 0]
        self.changed = 0

        # Load arrows and rotate to cover all directions (numeric-keypad convention)
        # Note: positive angle means counter-clockwise rotation
        self.arrows = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # double fudge - 10 elements
        self.arrows[8] = pygame.image.load('arrow8.png')
        self.arrows[6] = pygame.transform.rotate (self.arrows[8], -90)
        self.arrows[4] = pygame.transform.rotate (self.arrows[8],  90)
        self.arrows[2] = pygame.transform.rotate (self.arrows[8], 180)
        self.arrows[9] = pygame.image.load('arrow9.png')
        self.arrows[7] = pygame.transform.rotate (self.arrows[9],  90)
        self.arrows[3] = pygame.transform.rotate (self.arrows[9], -90)
        self.arrows[1] = pygame.transform.rotate (self.arrows[9], 180)
        # Load neutral position 'arrow'
        self.arrows[5] = pygame.image.load('arrow5.png')

        # Load button circle
        self.circle = pygame.image.load('button.png')
        # Set button colours
        self.colours = [(0,   0,   255),
                        (0,   255, 255),
                        (0,   255, 0),
                        (255, 255, 255),
                        (255, 0,   255),
                        (255, 255, 0),
                        (255, 0, 0),

                        (0,   150, 150),
                        (0,   150, 0),
                        (150, 150, 150),
                        (170, 0,   100),
                        (150, 150, 0),
                        (150, 0, 0)]

        #Initialise buttons array with 20 0s
        self.buttons = []
        for i in range(20):
            self.buttons.append(0)


    def getStickPos(self):
        "Calculate the number corresponding to the stick's position"
        pos = neutral = 5
        pos += 1 * self.axes[0]	# x axis
        pos -= 3 * self.axes[1]	# y axis
        return pos


    def draw(self, x, y):
        "Draws the icons representing the stick and the pressed buttons"
        yStep = -23  # Vertical size of the icon plus a few pixels
        scr = pygame.display.get_surface()

        # Stick
        scr.blit(self.arrows[self.getStickPos()], (x, y))

        # Buttons
        for i in range(len(self.buttons)):
            if (self.buttons[i]):
                y += yStep
                i = i % len(self.colours)
                self.circle.set_palette([self.colours[i]])
                scr.blit(self.circle, (x, y))


    def hasChanged(self):
        "True if the state has changed since the last call, else false"
        c = self.changed
        self.changed = False
        return c


    def handleEvent(self, e):
        """Reads any event, and if it's a joystick button or axis movement,
        sets the appropriate element and marks self as having changed"""
        # Note: Deliberately doesn't distinguish between multiple joysticks.
        # This allows any of them to be used without explicitly choosing one.
        if e.type == pygame.JOYBUTTONDOWN:
            self.buttons[e.button] = True
            self.changed = True
        elif e.type == pygame.JOYBUTTONUP:
            self.buttons[e.button] = False
            self.changed = True
        # My PS-usb adapter 'moves' axes 2 and 3 on startup, so ignore non-0/1 axes
        elif (e.type == pygame.JOYAXISMOTION and
            (e.axis == 0 or e.axis == 1)):
            self.axes[e.axis] = int(round(e.value))
            self.changed = True
        elif e.type == pygame.JOYHATMOTION:
            self.axes[0] = e.value[0]
            self.axes[1] = -e.value[1]
            self.changed = True


class HotrodFilter:
    def __init__(self):
        k = pygame
        self.upKeys     = [k.K_r, k.K_KP8]
        self.downKeys   = [k.K_f, k.K_KP2]
        self.leftKeys   = [k.K_d, k.K_KP4]
        self.rightKeys  = [k.K_g, k.K_KP6]

        self.buttonKeys = [k.K_1, k.K_2, k.K_3, k.K_4, k.K_z, k.K_x,
                           k.K_c, k.K_a, k.K_s, k.K_q, k.K_w, k.K_e, k.K_LALT,
                           k.K_LCTRL, k.K_LSHIFT, k.K_SPACE, k.K_LEFTBRACKET,
                           k.K_RIGHTBRACKET]


    def handleEvent(self, event):
        "Turn keyboard events into joystick events as appropriate"
        # A key press means a non-neutral stick movement or a button press
        if (event.type == pygame.KEYDOWN):
            # Stick movement
            if self.upKeys.count(event.key) > 0:
                post(Event(pygame.JOYAXISMOTION, axis=1, value=-1))
            elif self.downKeys.count(event.key) > 0:
                post(Event(pygame.JOYAXISMOTION, axis=1, value=1))
            elif self.leftKeys.count(event.key) > 0:
                post(Event(pygame.JOYAXISMOTION, axis=0, value=-1))
            elif self.rightKeys.count(event.key) > 0:
                post(Event(pygame.JOYAXISMOTION, axis=0, value=1))

            # Button press
            elif self.buttonKeys.count(event.key) > 0:
                post(Event(pygame.JOYBUTTONDOWN,
                      button = self.buttonKeys.index(event.key)))

        # A key release means a stick release or a button release
        elif (event.type == pygame.KEYUP):
            # Stick release
            if (self.upKeys.count(event.key) > 0 or
            self.downKeys.count(event.key) > 0):
                post(Event(pygame.JOYAXISMOTION, axis=1, value=0))
            elif (self.leftKeys.count(event.key) > 0 or
                 self.rightKeys.count(event.key) > 0):
                post(Event(pygame.JOYAXISMOTION, axis=0, value=0))

            # Button release
            elif self.buttonKeys.count(event.key) > 0:
                post(Event(pygame.JOYBUTTONUP,
                      button = self.buttonKeys.index(event.key)))



class Display:
    def __init__(self, xr, yr, ifbc, js):
        self.xRes, self.yRes = xr, yr
        self.inactiveFramesBeforeClear = ifbc
        self.inactiveFrames = self.inactiveFramesBeforeClear      # initial clear
        self.frames = 0

        self.framesFont = pygame.font.Font('atkins.ttf', 8)
        self.joyState = js
        self.xOffset = self.xOffsetBase = 3
        self.xOffsetStep = 28


    def nextFrame(self):
        "Advances the framecount, checks for inactivity, and draws and/or resets"
        self.frames += 1
        if self.joyState.hasChanged():
            if self.inactiveFrames >= self.inactiveFramesBeforeClear:
                self.frames = 0
                self.reset()
            self.draw()
            self.inactiveFrames = 0
            self.xOffset += self.xOffsetStep
        else:
            self.inactiveFrames += 1


    def reset(self):
        "Clears the screen and resets xOffset"
        self.xOffset = self.xOffsetBase
        pygame.display.get_surface().fill (pygame.color.Color('black'))


    def draw(self):
        self.drawFrames()
        self.drawJoyState()
        pygame.display.update()


    def drawFrames(self):
        "Writes the current frame number underneath the joystick state display"
        white = pygame.color.Color('white')
        framesSurface = self.framesFont.render (str(self.frames), 0, white)
        xFramesOffset = self.xOffset
        yFramesOffset = yRes - 15	# magic number
        scr = pygame.display.get_surface()
        scr.blit (framesSurface, (xFramesOffset, yFramesOffset))


    def drawJoyState(self):
        "Calculates the position to draw the joystate in and draws it"
        yJoyStateOffset = self.yRes - 40     # magic number
        joyState.draw(self.xOffset, yJoyStateOffset)


# Non-class startup functions

def initJoysticks():
    "Init all detected joysticks and print info."
    pygame.joystick.init()
    count = pygame.joystick.get_count()
    for i in range(count):
        pygame.joystick.Joystick(i).init()

    if count == 1:
        titleMessage('1 gameport / USB joystick found')
    else:
        titleMessage(str(count) + ' gameport or USB joysticks found')


def titleMessage (message):
    font = pygame.font.Font('dpcomic.ttf', 30)
    surf = font.render(message, 1, pygame.color.Color('white'))
    pygame.display.get_surface().blit (surf, (50, 135))	# magic numbers
    pygame.display.update()


def initScreen (xr, yr):
    "Set up the window"
    xRes, yRes = xr, yr
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption('Button Masher')
    icon = pygame.image.load('icon.bmp')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode ((xRes, yRes))
    screen.fill (pygame.color.Color('black'))


def initFrameEvent(fps):
    "Set up the next-frame event to go off every 1/60th of a second"
    NEXTFRAME = pygame.USEREVENT + 1
    pygame.time.set_timer (NEXTFRAME, 1000/fps)
    return NEXTFRAME


def showTitleScreen():
    titlePicture = pygame.image.load('title.png')
    pygame.display.get_surface().blit(titlePicture, (0, 0))
    pygame.display.update()


# Program entry point

xRes, yRes = 782, 182	# Stops 'slices' of arrows/circles appearing
initScreen (xRes, yRes)
showTitleScreen()

initJoysticks()
joyState = JoystickState()
hotFilter = HotrodFilter()
framesPerSecond = 60
NEXTFRAME = initFrameEvent (framesPerSecond)
display = Display (xRes, yRes, framesPerSecond/2, joyState)

while 1:
    for event in pygame.event.get():
        hotFilter.handleEvent(event)
        joyState.handleEvent(event)

        if event.type == NEXTFRAME:
            display.nextFrame()

        elif (event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and
            event.key == 27):
            sys.exit()

