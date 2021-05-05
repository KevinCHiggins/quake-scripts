from vgio.quake.spr import Spr, SpriteFrame
import os
import simplepal
from PIL import Image

source_path = '/home/quake/id1/progs'
dest_path = '/home/quake/sparks/progs'
image_path = '/home/kevin/Pictures'
pal_path = '/home/kevin/dev/python/quake-scripts/spark-up'

frame_names = ['timeline_test0000.png','timeline_test0001.png', 'timeline_test0002.png', 'timeline_test0003.png', 'timeline_test0004.png', 'timeline_test0005.png', ]

os.chdir(source_path)
s_explod = Spr.open('s_explod.spr')
os.chdir(dest_path)
s_test = Spr.open('s_explod.spr', 'w') # open a new file for writing

# print all attributes
print("Identity: " + str(s_explod.identity))
print("Version:" + str(s_explod.version))
print("Type:" + str(s_explod.type))
print("Radius: " + str(s_explod.bounding_radius))
print("Width: " + str(s_explod.width))
print("Height: " + str(s_explod.height))
print("Frames: " + str(s_explod.number_of_frames))
print("Beam length: " + str(s_explod.beam_length))
print("Sync type: " + str(s_explod.sync_type))
curr_frame = 0
# load all frames into separate instances of SpriteFrame
print("Attribute of sprite frames from s_explod")
for i in range(0, s_explod.number_of_frames):
	curr_frame = s_explod.frames[i]
	print("Frame width: " + str(curr_frame.width))

print("Origin " + str(curr_frame.origin))
# copy attributes into s_test

s_test.identity = 			s_explod.identity
s_test.version = 			s_explod.version
s_test.type = 				s_explod.type
s_test.bounding_radius = 	s_explod.bounding_radius
s_test.width = 				56
s_test.height = 			56
s_test.number_of_frames = 	s_explod.number_of_frames 
s_test.sync_type = 			s_explod.sync_type
s_test.beam_length =		s_explod.beam_length
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
	print("Image type is " + str(type(guru)))
	guru_data = list(guru.getdata())

	


	return tuple(palette.paletted(guru_data)) # 

os.chdir(pal_path)
quake_variant_builder = simplepal.PaletteFactory('quake1palette.pal')
quake_transparency = quake_variant_builder.create(t_mapping = ((0, 0, 0), 255))
for i in range(0, s_explod.number_of_frames):
	new_frame = SpriteFrame()
	new_frame.origin = curr_frame.origin
	new_frame.width = 56
	new_frame.height = 56
	new_frame.pixels = load_and_convert_sprite_frame(frame_names[i], quake_transparency)
	s_test.frames.append(new_frame)
s_test.close()
