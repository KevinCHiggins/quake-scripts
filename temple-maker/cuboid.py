def create_cuboid_brush(corner_a, corner_b, texture = "elwall2_4"):	# corners must not both be on any grid-parallel plane
	# check for being on the same grid-parallel plane
	# make sides as tuples of tuples
	defaults = {"x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1}
	brush = 
		[
		{"tri": ((0, 0, 0), (1, 0, 0), (0, 1, 0)), "tex": "elwall2_4", "x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1},
		{"tri": ((0, 0, 0), (1, 0, 0), (1, 0, 1)), "tex": "elwall2_4", "x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1},
		{"tri": ((0, 1, 0), (1, 1, 0), (1, 1, 1)), "tex": "elwall2_4", "x_off": 0, "y_off": 0, "rot": 0, "x_sc": 1, "y_sc": 1}
		]

	brush = []
	# make 3 tris containing corner_a 
	brushes.append(concatPlane((corner_a, (corner_a[0], corner_a[1], corner_b[2]), corner_a[0], corner_b[1], corner_a[2])), texture, defaults)
	brushes.append(concatPlane((corner_a, (corner_a[0], corner_a[1], corner_b[2]), corner_b[0], corner_a[1], corner_a[2])), texture, defaults)
	brushes.append(concatPlane((corner_a, (corner_a[0], corner_b[1], corner_b[2]), corner_b[0], corner_a[1], corner_a[2])), texture, defaults)

	# and 3 containing corner_b
	brushes.append(concatPlane((corner_b, (corner_b[0], corner_a[1], corner_b[2]), corner_b[0], corner_b[1], corner_a[2])), texture, defaults)
	brushes.append(concatPlane((corner_b, (corner_b[0], corner_a[1], corner_b[2]), corner_a[0], corner_b[1], corner_b[2])), texture, defaults)
	brushes.append(concatPlane((corner_b, (corner_b[0], corner_b[1], corner_a[2]), corner_a[0], corner_b[1], corner_b[2])), texture, defaults)
	return brush

def concatPlane(tri, tex, defs):
	return {"tri": tri, "tex": tex}.update(defs)

	