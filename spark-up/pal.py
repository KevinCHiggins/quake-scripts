import colorio
import sys
import math
import random
pal_file = open('quake1palette.pal', 'r')
pal_str = pal_file.readlines()
pal_str = pal_str[3:]
pal_ok = []
pal = []
found = {}
def rgb_to_oklab(c):
	linear = colorio.cs.SrgbLinear()
	oklab = colorio.cs.OKLAB()
	c_srgb = linear.from_rgb255(c)
	c_xyz = linear.to_xyz100(c_srgb)
	return oklab.from_xyz100(c_xyz)

for el in pal_str:
	pal_ok.append(rgb_to_oklab(tuple(map(int, el.split()))))
	pal.append(tuple(map(int, el.split())))
pal_file.close()

def euclid_dist(c1, c2):
	return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)

def redmean_variance(c1, c2): # I'm leaving out the square root as I think it's unnecessary when comparing only

	r_bar = (c1[0] + c2[0]) / 2.0 # (R1 + R2) / 2... also 
	return ((2 + (r_bar / 256.0)) * (c1[0] - c2[0])**2)		+ (4.0 * (c1[1] - c2[1])**2)	+ ((2 + ((255 - r_bar) / 256)) * (c1[2] - c2[2])**2)

def euclid_dist_from_index(c1, i):
	return euclid_dist(c1, pal[i])

def redmean_variance_from_index(c1, i):
	return redmean_variance(c1, pal[i])

def ciede2000_dist_from_index(c1_ok, i):

	#c2_lab = colorio.cs.OKLAB.fromrgb255(c2)
	return colorio.diff.ciede2000(c1_ok, pal_ok[i])
def ciede2000_dist_convert_to_ok(c1, c2):

	#c2_lab = colorio.cs.OKLAB.fromrgb255(c2)
	return colorio.diff.ciede2000(rgb_to_oklab(c1), rgb_to_oklab(c2))
def find_index_of_nearest_by_CIE(rgb_col):
	shortest = sys.float_info.max
	best_indexed = 0
	ok_col = rgb_to_oklab(rgb_col)
	for i in range(0, len(pal)):
		dist = ciede2000_dist_from_index(ok_col, i)
		if dist < shortest:
			shortest = dist
			best_indexed = i
	return best_indexed	
def find_index_of_nearest_by_euclid(rgb_col):
	shortest = sys.float_info.max
	best_indexed = 0
	for i in range(0, len(pal)):
		dist = euclid_dist_from_index(rgb_col, i)
		if dist < shortest:
			shortest = dist
			best_indexed = i
	return best_indexed	

def find_index_of_nearest_by_redmean(rgb_col):
	shortest = sys.float_info.max
	best_indexed = 0
	for i in range(0, len(pal)):
		dist = redmean_variance_from_index(rgb_col, i)
		if dist < shortest:
			shortest = dist
			best_indexed = i
	return best_indexed	


def paletted(pixel_data):
	paletted_l = []
	for rgb_col in pixel_data:
		print("Processing colour " + str(rgb_col))
		if rgb_col not in found:
			found[rgb_col] = find_index_of_nearest_by_redmean(rgb_col)
		paletted_l.append(found[rgb_col])
	return paletted_l
#rand_col = pal[23]
#for col in pal:
#	print("Euclidean distance: " + str(euclid_dist(col, rand_col)))
#	print("CIEDE2000 distance: " + str(ciede2000_dist(col, rand_col)))

#for i in range(0, 10):
#	t = (random.randrange(0, 256, 1), random.randrange(0, 256, 1), random.randrange(0, 256, 1))
#	#print("Closest to " + str(t) + " is " + str(pal[find_index_of_nearest(t, pal)]) + ", Euclidean: " + str(pal[find_index_of_nearest_euclid(t, pal)]))
#	print("Closest to " + str(t) + " is " + str(pal[find_index_of_nearest_by_redmean(t)]))