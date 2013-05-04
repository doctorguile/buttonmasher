Button Masher
v0.3.0
Copyright (C) 2004 Matthew Bennett
web:   http://buttonmasher.sourceforge.net
email: cascadeofprawns@users.sourceforge.net


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License (LICENSE.TXT) for more details.


Description
-----------
Button Masher is a simple tool to help you analyze and improve your execution
of fighting game moves, combos, etc. It displays each joystick input as it
happens, along with the frame number of the change, similar to the display
in the practice mode of some games.

Button Masher is written in Python (http://python.org) and uses the ace
Pygame library (http://pygame.org).


Requirements
------------
A joystick or gamepad. The following devices are known to work:

USB:
* Hori 'Soul Calibur II' PSX joystick with 'Boom' PSX->USB adapter
* Saitek 'P150' gamepad

Gameport:
* Gravis GamePad Pro (Thanks Buttermaker)

Keyboard port:
* Hotrod SE

If Pygame can't detect any joysticks, you'll be informed at the title screen
See the Troubleshooting section if this happens. Note that the computer
considers the Hotrod to be a keyboard, not a joystick, so although it is
supported by Button Masher, it won't count towards the number of joysticks
detected.


Instructions
------------
Use the joystick to practice your execution. Button Masher will show you
exactly what you input, and the frame number of each action. (A frame is
1/60th of a second, as in most fighters.)

To clear the screen, do nothing for 1/2 a second, and then the next time you
press a button or move the stick, the screen will automatically clear before
showing what you did.

Note: In order to allow any one of many plugged-in joysticks to be used,
Button Masher doesn't distinguish between events from different joysticks.
You can therefore use any joystick without having to explicitly select it.


Troubleshooting
---------------
No joystick detected / Nothing happens / Program crashes / Weird behaviour:

1. Make sure your joystick is plugged in properly. If it is a Hotrod,
   then although Pygame can't recognise it as a joystick, it *will* work
   in Button Masher 0.3.0 or later.

2. Check whether your OS recognises your joystick, and that it works in
   other programs.

3. Run the included 'joysticktest.exe' (or 'joysticktest.py') to see whether
   Pygame recognises your joystick, and what it thinks it is. Moving the stick
   and pressing the buttons should produce output to the console/shell.

   If joysticktest does not indicate that your joystick is recognised
   and working, maybe Pygame doesn't like it. Try http://pygame.org
   for help.

4. If you've tried all of the above, and it works in joysticktest but not in
   Button Masher, send me a copy of the output from joysticktest, the type
   of the joystick/gamepad/adapter, and a description of the problem,
   and I'll try to fix it.


Changes
-------
0.2.5 -> 0.3.0
    Added support for Hotrod joystick (effectively a keyboard)

0.2.4 -> 0.2.5
    Decreased reset wait time


Credits
-------
Frame number font: 'Atkins'  (c) Pixietype (http://www.pixitype.com)
Title screen font: 'DPComic' (c) codeman38 (http://zone38.net)
Zangief (c) Capcom
