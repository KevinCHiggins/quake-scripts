from vgio.quake.pak import PakFile
from vgio.quake.lmp import Lmp
# for simplicity, just process PAKs. This meets the MVP.

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

			with os.scandir(extracted_path + '/' + 'gfx') as gfx:
				l = [entry for entry in gfx if entry.is_file() and not (entry.name == 'pop.lmp' or entry.name == 'colormap.lmp' or entry.name == 'palette.lmp') ]
				print(l)
				for lmp_dir_entry in l:
					print('Opening {0}'.format(extracted_path + '/' + 'gfx' + '/'+ lmp_dir_entry.name))
					with Lmp.open(extracted_path + '/' + 'gfx' + '/' + lmp_dir_entry.name) as lmp:
						print(lmp.pixels[0])
	except (FileExistsError, FileNotFoundError, AttributeError) as error:
		print(error)
	for pak_filename in pak_entries_by_pak:

		path = dir_to_process + '/' + pak_filename[:-4]
		if os.path.exists(path):
			shutil.rmtree(path)
