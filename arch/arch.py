from vgio.quake import map
import math
import sys
import getopt

# constructs an arch with the shape of a sector of angle ang_degs, horizontally centred (X) on the origin, standing flush with and above the origin (Y), with depth (Z) depth

# to simplify the code I just use literal 0 as the origin - I don't see any use case for an origin variable

# defaults or test values

# I'm inconsistent with use of plane coords that are at the verts of the brush, or further out, at the bounds of entire arch (which is easier to figure out and type in but
# just conceivably in unusual circumstances could cause rounding or range errors when using a part of the arch at the edge of the map, or for further processing)

# could have a "-v" vertical ends option for sub-180-degree angles

# would be nice to use the correct terms intrados and extrados in the code and comments!

help_msg = """Accepted options are:
--sides <no. of sides> --width <width> --triangles --fractional --angle <segment angle> --name <map filename> --ring <ring thickness> --help.
Single-letter abbreviations preceded by a single hyphen may be used:
-s <no. of sides> -w <width> -t -f -a <segment angle> -n <map filename> -r <ring thickness>
Angles are in degrees, units are Quake world units. Omit triangles option to create vertical quadrilateral blocks.
Omit ring option or set it at 0 to carve the arch out of a rectangular block.
Omit fractional option to use integer coordinates for inner (and outer if ring thickness is set) arch vertices."""

try:
	opts, args = getopt.getopt(sys.argv[1:], "hs:w:tfa:n:r:g", ["help", "sides=", "width=", "triangles", "fractional", "angle=", "name=", "ring=", "gothic"])
except getopt.GetoptError:
	print(help_msg)
	sys.exit(2)
# DEFAULTS
sides = 8
width = 128
use_tris = False # TODO
floating_point_coords = False # TODO
ang_degs = 180
map_path = "C:/Users/Kevin/Maps/"
depth = 16
name = ""
ring_thickness = 0 # TODO
gothic = False
print(opts)
for opt, arg in opts:
	if opt in ["-s", "--sides"]:
		sides = int(arg)
		if sides < 0:
			print("Number of sides must be a positive integer.")
			sys.exit(2)		
	elif opt in ["-w", "--width"]:
		width = int(arg)
		if width < 0:
			print("Width must be a positive integer.")
			sys.exit(2)
		# might be good to throw a commonsense max limit here
	elif opt in ["-t", "--triangles"]:
		use_tris = True
		print("Set use_tris to ")
		print(use_tris)
	elif opt in ["-f", "fractional"]:
		floating_point_coords = True
	elif opt in ["-a", "--angle"]:
		ang_degs = float(arg)
	elif opt in ["-n", "--name"]:
		name = arg
	elif opt in ["-r", "--ring"]:
		ring_thickness = int(arg)
		if ring_thickness < 0:
			print("Ring thickness must be a positive integer.")
			sys.exit(2)
	elif opt in ["-h", "--help"]:

		print(help_msg)
		sys.exit(2)
	elif opt in ["-g", "--gothic"]:
		gothic = True
if width % 2 != 0:
	print("Width must be an even number")
	sys.exit(2)
if width < sides:
	print("Width can't be less than the amount of sides.") # would be better to do checks as to whether every brush is valid, but for now a crude check
	sys.exit(2)
if name == "":
	print("Enter name for map file to write generated arch into, with no file extension:")
	name = input()
map_file = open(map_path + name + ".map", "w")

ang_rads = (ang_degs / 360) * math.tau
start_ang_rads = math.pi / 2 - (ang_rads / 2) # angle of mid point of sector - half the sector angle = angle of end vertex of sector
end_ang_rads = math.pi / 2 + (ang_rads / 2) # angle of mid point of sector + half the sector angle = angle of start vertex of sector (going clockwise e.g. on unit circle)

width_on_unit_circle = math.cos(start_ang_rads) - math.cos(end_ang_rads) # get the difference between the cosines of the end and start points on the unit circle
scale_mult = width / width_on_unit_circle
print(start_ang_rads / (math.tau) * 360)
print(math.sin(start_ang_rads))

def create_default_plane():
	pl = map.Plane() 
	pl.texture_name = "metal5_4"
	pl.offset = (0, 0)
	pl.rotation = 0
	pl.scale = (1, 1)
	return pl
def cond_round(float):
	if floating_point_coords:
		return float
	else:
		return round(float)

height = cond_round(scale_mult)


points_2d = [] # a list of coords of vertices of the inside of the arch viewed face on, with no depth, as two-element tuples using floating point world units (scaled)

step_rads = ang_rads / sides # rotation from point to point of the inside of the arch, in radians



ws = map.Entity()
setattr(ws, "spawnflags", "0")
setattr(ws, "classname", "worldspawn")



# fill a list with the arch inner curve vertices, which we'll use for both quadrilateral and triangular sectioned brushes
for i in range(sides + 1):
	# pretty annoying that sin(pi) != 0
	# the points in this case are simply the verts of the inside of the arch, seen from the front, without depth (2D, just X and Z - which is height in Quake - coords)
	points_2d.append((cond_round(math.cos(start_ang_rads + step_rads * i) * scale_mult), cond_round(math.sin(start_ang_rads + step_rads * i) * scale_mult)))

if ring_thickness == 0:
	if use_tris == False: # quadrilateral sectioned brushes
		for i in range(sides):
			x1 = points_2d[i][0]
			z1 = points_2d[i][1]
			x2 = points_2d[i + 1][0]
			z2 = points_2d[i + 1][1]
			br = map.Brush()
			if z1 == height: # this brush has a triangular section and therefore no right side; define front and back in terms of z2 (left side)
				pl = create_default_plane()
				pl.points = ((x1, depth, height), (x2, depth, height), (x2, depth, z2)) # The back
				br.planes.append(pl)	
				pl = create_default_plane()
				pl.points = ((x2, 0, height), (x1, 0, height), (x1, 0, z2)) # The front
				br.planes.append(pl)
				pl = create_default_plane()
				pl.points = ((x2, depth, height), (x2, 0, height), (x2, 0, z2)) # The left side
				br.planes.append(pl)
			elif z2 == height: # this on ehas a triangular section and therefore no left side; define front and back in terms of z1 (right side)
				pl = create_default_plane()
				pl.points = ((x1, depth, height), (x2, depth, height), (x2, depth, z1)) # The back
				br.planes.append(pl)	
				pl = create_default_plane()
				pl.points = ((x2, 0, height), (x1, 0, height), (x1, 0, z1)) # The front
				br.planes.append(pl)
				pl = create_default_plane()
				pl.points = ((x1, 0, height), (x1, depth, height), (x1, depth, z1)) # The right side
				br.planes.append(pl)
			else: # normal 4-sided section, with a left and a right side
				pl = create_default_plane()
				pl.points = ((x1, depth, height), (x2, depth, height), (x2, depth, z2)) # The back
				br.planes.append(pl)	
				pl = create_default_plane()
				pl.points = ((x2, 0, height), (x1, 0, height), (x1, 0, z2)) # The front
				br.planes.append(pl)
				pl = create_default_plane()
				pl.points = ((x2, depth, height), (x2, 0, height), (x2, 0, z2)) # The left side
				br.planes.append(pl)	
				pl = create_default_plane()
				pl.points = ((x1, 0, height), (x1, depth, height), (x1, depth, z1)) # The right side
				br.planes.append(pl)
			pl = create_default_plane()
			pl.points = ((x1, 0, height), (x2, 0, height), (x2, depth, height)) # The top
			br.planes.append(pl)
			pl = create_default_plane()
			pl.points = ((x1, 0, z1), (x1, depth, z1), (x2, depth, z2)) # The bottom
			br.planes.append(pl)
			ws.brushes.append(br)
	else: # use triangles - I think this should render faster as there are less triangles in the end - mostly included as a matter of preference
		# fill points array with a sequence of lines which are the inner edges of the arch, in 2D, and including
		# the vertical right and left edges of the entire block. The order of line segment endpoints is always higher endpoint second.
		lines = []	

		right_x = cond_round(width / 2) # store coords of bounds of entire structure
		left_x = 0 - right_x

		# right edge
		lines.append(((right_x, 0), (right_x, height)))
		# lines of arch inner curve (sides)
		for i in range(sides):
			if i < sides / 2:
				lines.append((points_2d[i], points_2d[i + 1]))
			else:
				lines.append((points_2d[i + 1], points_2d[i]))		
		# left edge
		lines.append(((left_x, 0), (left_x, height)))
		print(lines)
		print(math.floor(sides) / 2)
		for i in range(sides + 1):
			if not i == math.floor(sides / 2): # if not at middle part of arch, which is a special case to be skipped whether even and odd numbers of sides 
				if i == math.floor(sides / 2 + 1) and sides % 2 == 1: # check whether we're at block after middle part (really "second middle part") 
					print("Keystone brush.")
					print(str(i))
					print(lines[i])
					print(lines[i + 1])
					br = map.Brush()
					pl = create_default_plane()
					pl.points = ((lines[i][0][0], 0, lines[i][0][1]), (lines[i][0][0], depth, lines[i][0][1]), (lines[i - 1][0][0], depth, lines[i - 1][0][1])) # left side
					br.planes.append(pl)
					pl = create_default_plane()
					pl.points = ((lines[i][1][0], depth, lines[i][1][1]), (lines[i][1][0], 0, lines[i][1][1]), (lines[i + 1][0][0], 0, lines[i + 1][0][1])) # right side
					br.planes.append(pl)				
					pl = create_default_plane()
					pl.points = ((right_x, 0, lines[i][0][1]), (right_x, depth, lines[i][0][1]), (left_x, depth, lines[i][0][1])) # bottom 
					br.planes.append(pl)
					pl = create_default_plane()
					pl.points = ((right_x, 0, height), (left_x, 0, height), (left_x, depth, height)) # top
					br.planes.append(pl)
					pl = create_default_plane()
					pl.points = ((right_x, 0, height), (right_x, 0, 0), (left_x, 0, 0)) # front (taking the simple option...)
					br.planes.append(pl)
					pl = create_default_plane()
					# inverse order again
					pl.points = ((left_x, depth, 0), (right_x, depth, 0), (right_x, depth, height)) # back
					br.planes.append(pl)
					ws.brushes.append(br)
				else:					
					print("Standard brush. i is" + str(i))
					br = map.Brush()
					pl = create_default_plane()
					pl.points = ((lines[i][0][0], 0, lines[i][0][1]), (lines[i][1][0], 0, lines[i][1][1]), (lines[i][1][0], depth, lines[i][1][1])) # left side
					br.planes.append(pl)
					pl = create_default_plane()
					# note we invert order of points to make this plane face the other way, knowing we've ordered all our pairs of endpoints highest second
					pl.points = ((lines[i + 1][1][0], depth, lines[i + 1][1][1]), (lines[i + 1][1][0], 0, lines[i + 1][1][1]), (lines[i + 1][0][0], 0, lines[i + 1][0][1])) # right side
					br.planes.append(pl)				
					pl = create_default_plane()
					pl.points = ((right_x, 0, height), (left_x, 0, height), (left_x, depth, height)) # top
					br.planes.append(pl)
					pl = create_default_plane()
					pl.points = ((right_x, 0, height), (right_x, 0, 0), (left_x, 0, 0)) # front
					br.planes.append(pl)
					pl = create_default_plane()
					# inverse order again

					pl.points = ((left_x, depth, 0), (right_x, depth, 0), (right_x, depth, height)) # back
					br.planes.append(pl)
					ws.brushes.append(br)
else:
	outer_points_2d = [] # verts of outside of ring
	for i in range(sides + 1):
		
		outer_mult = scale_mult + ring_thickness
		outer_points_2d.append((cond_round(math.cos(start_ang_rads + step_rads * i) * outer_mult), cond_round(math.sin(start_ang_rads + step_rads * i) * outer_mult)))
		print("Loopin")
		print(outer_points_2d)
	print(outer_points_2d)
	print(sides)
	for i in range(sides):
		x1 = points_2d[i][0]
		z1 = points_2d[i][1]
		x2 = points_2d[i + 1][0]
		z2 = points_2d[i + 1][1]
		ox1 = outer_points_2d[i][0]
		oz1 = outer_points_2d[i][1]
		ox2 = outer_points_2d[i + 1][0]
		oz2 = outer_points_2d[i + 1][1] 
		br = map.Brush()
		
		pl = create_default_plane()
		pl.points = ((x1, depth, z1), (ox1, depth, oz1), (ox2, depth, oz2)) # The back
		br.planes.append(pl)	
		pl = create_default_plane()
		pl.points = ((x2, 0, z2), (ox2, 0, oz2), (ox1, 0, oz1)) # The front
		br.planes.append(pl)
		pl = create_default_plane()
		pl.points = ((x1, 0, z1), (ox1, 0, oz1), (ox1, depth, oz1)) # The clockwise side
		br.planes.append(pl)	
		pl = create_default_plane()
		pl.points = ((x2, 0, z2), (x2, depth, z2), (ox2, depth, oz2)) # The anticlockwise side
		br.planes.append(pl)
		pl = create_default_plane()
		pl.points = ((ox1, 0, oz1), (ox2, 0, oz2), (ox2, depth, oz2)) # The outer side
		br.planes.append(pl)
		pl = create_default_plane()
		pl.points = ((x1, 0, z1), (x1, depth, z1), (x2, depth, z2)) # The inner side
		br.planes.append(pl)
		ws.brushes.append(br)
map_file.write(map.dumps([ws]))
map_file.close()


