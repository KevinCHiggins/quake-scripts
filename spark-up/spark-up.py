from vgio.quake.spr import Spr, SpriteFrame
import os
import simplepal
from PIL import Image

source_path = '/home/quake/id1/progs'
dest_path = '/home/quake/sparks/progs'
image_path = '/home/kevin/Pictures'
pal_path = '/home/kevin/dev/python/quake-scripts/spark-up'

source_frame_names = ['timeline_test0000.png','timeline_test0001.png', 'timeline_test0002.png', 'timeline_test0003.png', 'timeline_test0004.png', 'timeline_test0005.png', ]

os.chdir(dest_path)
s_test = Spr.open('s_explod.spr', 'w') # open a new file for writing

# hard-coded constants for now
WIDTH = 56
HEIGHT = 56
FRAMES_AMOUNT = 6
ORIGIN = (int(0 - WIDTH / 2), int(HEIGHT / 2))

def assign_attr(spr, w, h, frames_amount):
	spr.identity = 			b'IDSP'
	spr.version = 			1
	spr.type = 				2
	spr.bounding_radius = 	39.597999572753906
	spr.width = 			w
	spr.height = 			h
	spr.number_of_frames = 	frames_amount
	spr.sync_type = 		0
	spr.beam_length =		0.0

assign_attr(s_test, WIDTH, HEIGHT, FRAMES_AMOUNT)
print("Attributes of s_test...")
print("Identity: " + 		str(s_test.identity))
print("Version:" + 			str(s_test.version))
print("Type:" + 			str(s_test.type))
print("Radius: " + 			str(s_test.bounding_radius))
print("Width: " + 			str(s_test.width))
print("Height: " + 			str(s_test.height))
print("Claimed frames: " +	str(s_test.number_of_frames)) # VGIO doesn't check this attribute against frame data at this stage
print("Beam length: " + 	str(s_test.beam_length))
print("Sync type: " + 		str(s_test.sync_type))

def load_and_convert_sprite_frame(name, palette):

	os.chdir(image_path)
	guru = Image.open(name)
	guru.show()
	# print("Image type is " + str(type(guru)))
	guru_data = list(guru.getdata())
	return tuple(palette.paletted(guru_data)) 

os.chdir(pal_path)
quake_variant_builder = simplepal.PaletteFactory('quake1palette.pal')
quake_transparency = quake_variant_builder.create(t_mapping = ((0, 0, 0), 255))
for i in range(0, FRAMES_AMOUNT):
	new_frame = SpriteFrame()
	new_frame.origin = ORIGIN
	new_frame.width = WIDTH
	new_frame.height = HEIGHT
	new_frame.pixels = load_and_convert_sprite_frame(source_frame_names[i], quake_transparency)
	s_test.frames.append(new_frame)
s_test.close()
