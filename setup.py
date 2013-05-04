from distutils.core import setup
import py2exe, sys

setup(name="Button Masher",
	windows=[{"script" : "buttonmasher.py",
			"icon_resources": [(1, "buttonmasher.ico")]}],
	console=[{"script" : "joysticktest.py",
			"icon_resources": [(1, "buttonmasher.ico")]}],
	data_files=[
		(".", ["icon.bmp", "arrow5.png", "arrow8.png", "arrow9.png", "button.png",
		"title.png", "buttonmasher.py", "joysticktest.py",
		"atkins.ttf", "dpcomic.ttf", "README.md", "LICENSE.TXT"])])

