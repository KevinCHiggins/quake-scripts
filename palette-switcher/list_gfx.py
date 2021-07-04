from vgio.quake.pak import PakFile
from vgio.quake.lmp import Lmp
from vgio.quake.spr import Spr
from vgio.quake.mdl import Mdl
import map_pal
# for simplicity, just extract PAK contents to temp dirs, process .lmp, .spr and .mdl
# entries and move them into the usual Quake directory structure so
# that they will then override what's in the PAKs. This meets the MVP
# and lets us repeat the process on the same directory.

import os
import shutil


dir_to_process = '/home/quake/pal_sw' 
# note that models, sprites and maps contain multiple graphics 

# actually I don't think there's any point to this... well
LEGEND = {'sprites': '.spr', 'levels': '.bsp', 'models': '.mdl', '2d image lumps': '.lmp'}
def sort_into_dict_by_extension(collection, legend):
	d = {}
	for file_type, file_extension in legend.items():
		d[file_type] = [filename for filename in collection if filename[-4:] == file_extension]
	if d['2d image lumps']:
		d['2d image lumps'] = [filename for filename in d['2d image lumps'] if (not 'palette.lmp' in filename and not 'colormap.lmp' in filename)]
	return d



# WHADDABOUT .MAP and .WAD?

# extract each PAK to a temp directory with the same name as it (but without the extension)
# 
with os.scandir(dir_to_process) as dir_root_files:
	os.chdir(dir_to_process)
	pak_files = [i for i in dir_root_files if i.name[-4:].upper() == '.PAK']
	pak_entries_by_pak = {i.name : [] for i in pak_files}
	try:
		for pak_filename in pak_entries_by_pak:
			pak_path = dir_to_process +'/' + pak_filename
			extracted_path = pak_path[:-4]
			os.mkdir(extracted_path)
			with PakFile(pak_path, 'a') as pak_file:
				os.chdir(extracted_path)
				pak_file.extractall()
			subdir = '/gfx/'
			with os.scandir(extracted_path + subdir) as gfx:
				l = [entry for entry in gfx if entry.is_file() and not (entry.name == 'pop.lmp' or entry.name == 'palette.lmp' or entry.name == 'colormap.lmp') ]
				print(l)
				for lmp_entry in l:
					print('Opening {0}'.format(extracted_path + subdir + lmp_entry.name))
					with Lmp.open(extracted_path + subdir + lmp_entry.name) as lmp:
						print('First pixel: {}'.format(lmp.pixels[0]))
			subdir = '/progs/'
			with os.scandir(extracted_path + subdir) as progs:
				l = [entry for entry in progs if entry.is_file() and entry.name[-4:] == '.spr']
				print(l)
				for spr_entry in l:
					print('Opening {0}'.format(extracted_path + subdir + spr_entry.name))
					with Spr.open(extracted_path + subdir + spr_entry.name) as spr:
						for frame in spr.frames:
							print('First pixel of frame: {}'.format(frame.pixels[0]))
			with os.scandir(extracted_path + subdir) as progs:

				l = [entry for entry in progs if entry.is_file() and entry.name[-4:] == '.mdl']
				print(l)
				for mdl_entry in l:
					print('Opening {0}'.format(extracted_path + subdir + mdl_entry.name))
					with Mdl.open(extracted_path + subdir + mdl_entry.name) as mdl:
						for skin in mdl.skins:
							print('First pixel os skin: {}'.format(skin.pixels[0]))
	except (FileExistsError, FileNotFoundError, AttributeError) as error:
		print(error)

	for pak_filename in pak_entries_by_pak:

		
		path = dir_to_process + '/' + pak_filename[:-4]
		
		if os.path.exists(path):
			print('Cleaning up temp directory {}'.format(path))
			shutil.rmtree(path)
