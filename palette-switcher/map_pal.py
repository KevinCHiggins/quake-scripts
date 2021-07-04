# load new palette (JASC)
# load source palette (LMP)
# make map of source indices to new indices

from vgio.quake.lmp import Lmp

def map_from_src_to_dest_unrestricted(src, dest):
	map = []
		for col in src:
			map.append(index_to_least_variant(col, dest))
def map_from_src_to_dest_fullbrights_separate(src, dest):
	map = []
	norm_range = range(0, 224)
	for i in norm_range:
		map.append(index_to_least_variant(src, dest, norm_range))
	fullbright_range = range(224, 256)
	for i in fullbright_range:
		map.append(index_to_least_variant(src, dest, norm_range))
	return map
def load_jasc_pal(file_path)
	pal = []
	with open(file_path, 'r') as pal_file:	
		pal_str = pal_file.readlines()
		pal_str = pal_str[3:] 
		for el in pal_str:
			pal.append(tuple(map(int, el.split())))
		pal_file.close()
	return pal
def load_quake_pal(file_path)
	with Lmp.open(file_path, 'r') as pal_file:
		return pal_file.palette

def redmean_variance(c1, c2): # No square root as Wikipedia suggests it's unnecessary when finding least distances, hence "variance"
	r_bar = (c1[0] + c2[0]) / 2.0 # These formulae are from Wikipedia's Colour Difference article
	return ((2 + (r_bar / 256.0)) * (c1[0] - c2[0])**2)		+ (4.0 * (c1[1] - c2[1])**2)	+ ((2 + ((255 - r_bar) / 256)) * (c1[2] - c2[2])**2)

def index_to_least_variant(rgb_col, pal_data, pal_range=range(0, 256)): 
	least = 584971 # higher than of redmean_variance((0,0,0),(255,255,255)), so works as a max
	index_to_col_with_least = 0
	# brute force through whole palette
	for i in pal_range:
		dist = self.redmean_variance(rgb_col, pal_data[i])
		if dist < least:
			least = dist
			index_to_col_with_least = i
	return index_to_col_with_least