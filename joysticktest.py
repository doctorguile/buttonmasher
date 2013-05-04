import pygame, sys

print "This program gives details of all joysticks recognised by Pygame/SDL."
print "If your joystick simulates a keyboard, like the Hotrod, then this"
print "won't tell you anything. However, the Hotrod is supported in"
print "Button Masher."

pygame.display.init()
screen = pygame.display.set_mode ((350, 50))
pygame.display.set_caption('joysticktest (see console for output)')

pygame.joystick.init()
count = pygame.joystick.get_count()
print
print "Joysticks found:", count
print
for i in range(count):
	joy = pygame.joystick.Joystick(i)
	joy.init()
	print "Joystick", i
	print  "  Name:   ", joy.get_name()
	print  "  Axes:   ", joy.get_numaxes()
	print  "  Buttons:", joy.get_numbuttons()
	print

print "Events:"

while 1:
	event = pygame.event.wait()
	if event.type == pygame.JOYAXISMOTION:
		print "Joystick:", event.joy, " axis:", event.axis, " value:", event.value
	elif event.type == pygame.JOYBUTTONDOWN:
		print "Joystick:", event.joy, " button", event.button, "pressed"
	elif event.type == pygame.JOYBUTTONUP:
		print "Joystick:", event.joy, " button", event.button, "released"
	elif event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
		sys.exit()

