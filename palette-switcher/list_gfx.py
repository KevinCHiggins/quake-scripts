from vgio.quake.pak import PakFile
from vgio.quake.lmp import Lmp
# for simplicity, just process PAKs. This meets the MVP.

import os


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

os.chdir(dir_to_process)
dir_root_files = os.scandir(dir_to_process)
pak_files = [i for i in dir_root_files if i.name[-4:].upper() == '.PAK']
pak_entries_by_pak = {i.name : [] for i in pak_files}
for pak_filename in pak_entries_by_pak:
	with PakFile(dir_to_process +'/' + pak_filename, 'a') as pak_file:
		pak_entries = [i for i in pak_file.namelist() if i[-4:] == '.bsp' or i[-4:] == '.lmp' or i[-4:] == '.spr' or i[-4:] == '.mdl']
		pak_entries = sort_into_dict_by_extension(pak_entries, LEGEND)
		for lmp_filename in [p for p in pak_entries['2d image lumps'] if not p == 'gfx/pop.lmp']: # seems like one non-standard file in PAK1.PAK?
			print('Attempting to open {} from {}'.format(lmp_filename, pak_filename))
			file_like_object = pak_file.open(lmp_filename)
			print(file_like_object)
			with Lmp.open(file_like_object, 'r') as lmp_file:
				print('{} from {} in {}'.format(lmp_file.pixels[0], lmp_filename, pak_filename))
				with Lmp.open('scratch_pad', 'w') as scratch_pad:
					scratch_pad.width = lmp_file.width
					scratch_pad.height = lmp_file.height
					new_pixels = list(lmp_file.pixels)
					new_pixels[0] = 255
					scratch_pad.pixels = tuple(new_pixels)
			# if in append mode, this corrupts the archive and it can't be read from
			# pak_file.write('scratch_pad', 'lmp_filename')
			print(pak_file.namelist())