import math
def create_room(corner_a, corner_b, wall_thickness = 16, wall_texture = "elwall2_4", floor_texture = "elwall2_4", ceiling_texture = "elwall2_4"):
	fixed = fixed_cuboid(corner_a, corner_b)
	corner_a = fixed[0] # the program will stop here if there was an error in fixed_cuboid
	corner_b = fixed[1]
	# check there's enough room to make walls
	if (corner_b[0] - corner_a[0] < (wall_thickness * 2) or corner_b[1] - corner_a[1] < (wall_thickness * 2) or corner_b[2] - corner_a[2] < (wall_thickness * 2)):
		return []

	brushes = []
	# floor
	brushes.append(create_cuboid_brush(corner_a, [corner_b[0], corner_b[1], corner_a[2] + wall_thickness]))
	# ceiling
	brushes.append(create_cuboid_brush(corner_b, [corner_a[0], corner_a[1], corner_b[2] - wall_thickness], "sky4"))
	# front and back walls
	brushes.append(create_cuboid_brush([corner_a[0], corner_a[1], corner_a[2] + wall_thickness], [corner_a[0] + wall_thickness, corner_b[1], corner_b[2] - wall_thickness]))
	brushes.append(create_cuboid_brush([corner_b[0], corner_b[1], corner_b[2] - wall_thickness], [corner_b[0] - wall_thickness, corner_a[1], corner_a[2] + wall_thickness]))
	# left and right walls
	print("corner_b x - thick: " + str(corner_b[0] - wall_thickness))
	brushes.append(create_cuboid_brush([corner_a[0] + wall_thickness, corner_a[1], corner_a[2] + wall_thickness], [corner_b[0] - wall_thickness, corner_a[1] + wall_thickness, corner_b[2] - wall_thickness]))
	brushes.append(create_cuboid_brush([corner_b[0] - wall_thickness, corner_b[1], corner_b[2] - wall_thickness], [corner_a[0] + wall_thickness, corner_b[1] - wall_thickness, corner_a[2] + wall_thickness]))
	return brushes
def get_archaic_neck_side(base_side):
        return int((base_side / 4) * 3)
def get_archaic_capital_side(base_side):
        return base_side + int(base_side / 2)
        
def get_oct_prism_width(base_side):
        result = math.floor((base_side) / math.sqrt(2))
        if result % 2 != 0:
                result = result + 1
        return result
# return a 
def get_pediment_height(width, num_columns_across):
	return width * 4 / (num_columns_across + 14)

# replication of calculations in create_doric_capital
def get_ab_height(base_side, full_height):
	diff = get_archaic_capital_side(base_side) - get_archaic_neck_side(base_side)
	cap_height = int(full_height / 7)
	cyl_height = int(diff / 15)
	return (cap_height - (cyl_height * 5))


def get_fillet_height(column_height):
	return math.floor(column_height / 200) + 1
# returns two corners defined as 3-part vectors, with the second corner's parts all being greater than the corresponding part in the first
# this has been changed so as to no longer modify the lists it is passed
# and also to return a tuple, not a list
def fixed_cuboid(corner_a, corner_b):

	# check for being on the same grid-parallel plane... BTW this doesn't check for them being colinear!
	if corner_a[0] == corner_b[0]:
		print("Error: cuboid would have no extent along x axis")
		return
	elif corner_a[1] == corner_b[1]:
		print("Error: cuboid would have no extent along y axis")
		return
	elif corner_a[2] == corner_b[2]:
		print("Error: cuboid would have no extent along z axis")
	corner_c = []
	corner_d = []
	corner_c.append(corner_a[0] if corner_a[0] < corner_b[0] else corner_b[0])
	corner_c.append(corner_a[1] if corner_a[1] < corner_b[1] else corner_b[1])
	corner_c.append(corner_a[2] if corner_a[2] < corner_b[2] else corner_b[2])
	corner_d.append(corner_a[0] if corner_a[0] > corner_b[0] else corner_b[0])
	corner_d.append(corner_a[1] if corner_a[1] > corner_b[1] else corner_b[1])
	corner_d.append(corner_a[2] if corner_a[2] > corner_b[2] else corner_b[2])
	return [(corner_c[0], corner_c[1], corner_c[2]), (corner_d[0], corner_d[1], corner_d[2])]

def create_doric_column(origin, full_height, base_side, texture):
	brushes = []
	if full_height % 7 != 0:
		print("Full column height must be divisible by 7 as capital takes up 1/7th of height")
		return
	shaft_height = int((full_height / 7) * 6)
	shaft = create_shaft(origin, shaft_height, base_side, False, texture)
	for brush in shaft:
		brushes.append(brush)
	capital = create_doric_capital((origin[0], origin[1], origin[2] + shaft_height), get_archaic_capital_side(base_side), get_archaic_neck_side(base_side), int(full_height / 7), texture)
	for brush in capital:
		brushes.append(brush)
	return brushes
# rough and ready capitals with a 2:5 slope on the underside...
def create_doric_capital(origin, large_side = 360, small_side = 180, capital_height = 100, texture = "metal5_4"):
	if large_side % 5 != 0 or small_side % 5 != 0:
		print("Sides must be evenly divisible by 5")
		return
	brushes = []
	width_diff = large_side - small_side
	height = int((width_diff / 15) * 4) # because of the Archaic Doric 1.5x capital width, we know we can divide by 3... THAT U CAN DIV BY FIVE is UNWARRANTED ASSUMPTION THO!
	brushes.append(create_oct_prism(origin, small_side, height, width_diff, texture))
	cyl_orig = (origin[0], origin[1], origin[2] + height) # shift up to put cylinder flush with top of flaring part
	cyl_height = int(width_diff / 15) # cylinder is much less high
	brushes.append(create_oct_prism(cyl_orig, large_side, cyl_height, 0, texture))
	ab_disp = get_oct_prism_width(large_side) / 2
	ab_height = capital_height - (cyl_height * 5)
	#print("ab_heihgt" + str(ab_height) + " width diff " + str(width_diff) + " height " + str(height) + " cap height " + str(capital_height))
	# abacus has same height as all of capital (flaring out and back in)

	ab = create_cuboid_brush((cyl_orig[0] - ab_disp, cyl_orig[1] - ab_disp, cyl_orig[2] + cyl_height), (cyl_orig[0] + ab_disp, cyl_orig[1] + ab_disp, cyl_orig[2] + cyl_height + ab_height), texture)
	brushes.append(ab)
	return brushes

# creates an 8-sided upright prism by dividing the upright-oriented sides of the given cuboid in five
# and cutting appropriate faces that intersect those division points
# top flare is the difference in the side of the entire top square vs the entire bottom square
def create_shaft(origin, height, base_side, roman = False, texture = "metal5_4"):

	brushes = []
	shrinkage_fraction = 4
	if base_side % (shrinkage_fraction * 2) != 0:
		print("Base square side is not evenly divisble by " + str(shrinkage_fraction * 2))
		return
	base_half = base_side / 2
	neck_half_shrinkage = base_half / shrinkage_fraction;
	neck_half_shrinkage = neck_half_shrinkage - (neck_half_shrinkage % 5); # magic number of five is due to our octagon construction in 5ths of a square side
	segments_amount = neck_half_shrinkage / 5; #  should put in a limit for really fat columns to avoid stupid amounts of segments (every time curve crosses 5 units)
	curr_seg_half_side = base_half # we start at the bottom ring of full (base_side) width, and we'll keep shrinking going upwards
	neck_half_side = curr_seg_half_side - neck_half_shrinkage
	neck_fraction = neck_half_side / base_half # the fraction of neck width as to base width - equals 1 minus (1 over shrinkage_fraction). 6 -> 5/6
	neck_projection_ang = math.acos(neck_fraction)
	curr_bottom = origin[2] # this will incrementally rise up to be the origin of each prism
	while (curr_seg_half_side > neck_half_side):
		print("Segment half side: " + str(curr_seg_half_side))
		next_seg_half_side = curr_seg_half_side - 5
		next_seg_width_fraction = next_seg_half_side / base_half # the fraction of the current seg width as to base width
		# find proportion of angle needed to cut arc at given width to (greater) angle cutting arc at neck width, then multiply this by column height to get seg height
		seg_height = (math.acos(next_seg_width_fraction) / neck_projection_ang) * height
		seg_height = round(seg_height) # keep things integer
		print("Base Width " + str(curr_seg_half_side) + " top width " + str(next_seg_half_side) +  " height " + str(seg_height) + " bottom " + str(curr_bottom))
		brushes.append(create_oct_prism((origin[0], origin[1], curr_bottom), curr_seg_half_side * 2, (seg_height - curr_bottom), -10, texture))
		curr_bottom = seg_height
		curr_seg_half_side = next_seg_half_side
	return brushes
def create_oct_prism(origin, side, height, top_flare, texture):

	defaults = {"x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1}
	brush = []
	#div = int((corner_b[0] - corner_a[0]) / 5) # we have checked that the cuboid's x and y dimensions are equal, so this division is applicable to any side

	square_corner_a = square_corners(origin, side)[0]
	square_corner_b = square_corners(origin, side)[1]
	if (top_flare % 10) != 0:
		return
	top_square_corner_a = square_corners(origin, side + top_flare)[0]
	top_square_corner_b = square_corners(origin, side + top_flare)[1]	
	# working on each side of the containing cuboid in turn, cutting the two planes which also intersect the next side (going anticlockwise)

	for i in range(4):
		# 1/5th along this side to 2/5ths along next side, going low high low
		tri1 = (point_on_divided_side(square_corner_a, square_corner_b, origin[2], 1, i), point_on_divided_side(top_square_corner_a, top_square_corner_b, origin[2] + height, 1, i), point_on_divided_side(square_corner_a, square_corner_b, origin[2], 2, i + 1))
		brush.append(concat_face(tri1, texture, defaults))
		# 3/5th along this side to 4/5ths along next side, going low high low
		tri2 = (point_on_divided_side(square_corner_a, square_corner_b, origin[2], 3, i), point_on_divided_side(top_square_corner_a, top_square_corner_b, origin[2] + height, 3, i), point_on_divided_side(square_corner_a, square_corner_b, origin[2], 4, i + 1))
		brush.append(concat_face(tri2, texture, defaults))		
	# top and bottom (z extent)
	cuboid_corner_a = (square_corner_a[0], square_corner_a[1], origin[2])
	cuboid_corner_b = (square_corner_b[0], square_corner_b[1], origin[2] + height) 
	brush.append(concat_face((cuboid_corner_b, (square_corner_b[0], square_corner_a[1], origin[2] + height), (square_corner_a[0], square_corner_b[1], origin[2] + height)), texture, defaults))
	brush.append(concat_face((cuboid_corner_a, (square_corner_b[0], square_corner_a[1], origin[2]), (square_corner_a[0], square_corner_b[1], origin[2])), texture, defaults))
	#print("Coming out of oct prism, brush is " + str(brush))
	return brush
# return two 2D points which are the diagonally opposed corners, with the one nearest the origin first, of the square sitting around the given centre point
def square_corners(centre, side):
	if (side % 10) != 0:
		print("Side of square must be divisible by 10")
		return
	half_side = int(side / 2)
	return((centre[0] - half_side, centre[1] - half_side), (centre[0] + half_side, centre[1] + half_side))
def point_on_divided_side(corner_a, corner_b, z, m, n): # point m fifths along nth upright side of cuboid, at height z
	div = int((corner_b[0] - corner_a[0]) / 5)
	if m > 5:
		return
	n = n % 4
	x = 0
	y = 0
	if n == 0:
		x = corner_a[0] + div * m
		y = corner_a[1]
	elif n == 1:
		x = corner_b[0]
		y = corner_a[1] + div * m
	elif n == 2:
		x = corner_b[0] - div * m
		y = corner_b[1]
	elif n == 3:
		x = corner_a[0]
		y = corner_b[1] - div * m
	return (x, y, z)
# rotated means by 90 degrees
def create_roof_prism_brush(corner_a, corner_b, rotated = False, texture = "elwall2_4"):
	brush = []
	if rotated:
		# define y extent (gables)
		brush.append(concat_face((corner_b, (corner_a[0], corner_b[1], corner_b[2]), (corner_b[0], corner_b[1], corner_a[2])), texture, defaults))
		brush.append(concat_face((corner_a, (corner_a[0], corner_a[1], corner_b[2]), (corner_b[0], corner_a[1], corner_a[2])), texture, defaults))
		# find half-way mark for roof ridge
		ridge_x = corner_b[0] - int((corner_b[0] - corner_a[0]) / 2)

		# bottom
		brush.append(concat_face((corner_a, (corner_b[0], corner_a[1], corner_a[2]), (corner_a[0], corner_b[1], corner_a[2])), texture, defaults))

		brush.append(concat_face(((ridge_x, corner_b[1], corner_b[2]), (corner_b[0], corner_b[1], corner_a[2]), (corner_b[0], corner_a[1], corner_a[2])), texture, defaults))
		brush.append(concat_face((corner_a, (corner_a[0], corner_b[1], corner_a[2]), (ridge_x, corner_a[1], corner_b[2])), texture, defaults))
	return brush
def create_cuboid_brush(corner_a, corner_b, texture = "elwall2_4"):	
	fixed = fixed_cuboid(corner_a, corner_b)
	corner_a = fixed[0] # the program will stop here if there was an error in fixed_cuboid
	corner_b = fixed[1]
	# make sides as tuples of tuples
	defaults = {"x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1}
#		brush = [
#		{"tri": ((0, 0, 0), (1, 0, 0), (0, 1, 0)), "tex": "elwall2_4", "x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1},
#		{"tri": ((0, 0, 0), (1, 0, 0), (1, 0, 1)), "tex": "elwall2_4", "x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1},
#		{"tri": ((0, 1, 0), (1, 1, 0), (1, 1, 1)), "tex": "elwall2_4", "x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1}
#		]

	brush = []
	# make 3 tris containing corner_a 
	# calc p2 first
	# 0 0 1, 0 1 0... -x
	# define x extent
	brush.append(concat_face((corner_b, (corner_b[0], corner_b[1], corner_a[2]), (corner_b[0], corner_a[1], corner_b[2])), texture, defaults))
	brush.append(concat_face((corner_a, (corner_a[0], corner_b[1], corner_a[2]), (corner_a[0], corner_a[1], corner_b[2])), texture, defaults))
	# define y extent
	brush.append(concat_face((corner_b, (corner_a[0], corner_b[1], corner_b[2]), (corner_b[0], corner_b[1], corner_a[2])), texture, defaults))
	brush.append(concat_face((corner_a, (corner_a[0], corner_a[1], corner_b[2]), (corner_b[0], corner_a[1], corner_a[2])), texture, defaults))
	# z extent
	brush.append(concat_face((corner_b, (corner_b[0], corner_a[1], corner_b[2]), (corner_a[0], corner_b[1], corner_b[2])), texture, defaults))
	brush.append(concat_face((corner_a, (corner_b[0], corner_a[1], corner_a[2]), (corner_a[0], corner_b[1], corner_a[2])), texture, defaults))

	print("Length of brush: " + str(len(brush)))
	print("First face of brush: "+ str(brush[0]))
	return brush

def concat_face(tri, tex, defs):
	#print("Type of tri in concat_face " + str(type(tri)))
	face = {"tri": tri, "tex": tex}
	face.update(defs)
	#print("concatFace returning: " + str(face))
	return face

	
