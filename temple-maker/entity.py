# may subclass into point and brush later
def create_point(classname, pos, ang):
	point_entity = Entity(classname)
	point_entity.attributes.update({"origin": str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]), "angle": str(ang)}) # not gorgeous but should do it
	return point_entity
def create_worldspawn(brushes):
        world = Entity("worldspawn", brushes)
        world.attributes.update({"wad": "C:\\Users\\Kevin\\Programs\\Quake Stuff\\TrenchBroom\\Textures.wad", "_point_format": "1"})
        return world
def create_lit_worldspawn(brushes):
        world = create_worldspawn(brushes)
        world.attributes.update({"_sunlight": "250", "_sunlight_mangle": "0 -80 0"})
        return world
class Entity:
	def __init__(self, classname = "worldspawn", brushes = []):
		self.attributes = {"spawnflags": "0",
		"classname": classname}
		self.brushes = brushes
	
	def serialiseTriangle(self, tri): # because I want a slightly different format to Python's str()
		output = ""
		for p in tri:
			output += "( "
			for i in p:
				output += str(i)
				output += " "

			output += ") "
		return output
	def texAttrsStr(self, int): # writes -0 instead of 0... not sure if needed, just going by example map file
		if int != 0:
			return str(int)
		return "-" + str(int)
	def toMapFormat(self):
		output = ""	
		output += "{\n"
		for key in self.attributes:
			output += "\""
			output += key
			output += "\" \""
			output += self.attributes[key]
			output += "\"\n"
		if len(self.brushes) > 0:
			for br in self.brushes:
				output += "{\n"
				for face in br:
					
					output += self.serialiseTriangle(face["tri"])
					output += face["tex"]
					output += " "
					output += self.texAttrsStr(face["x_off"])
					output += " "
					output += self.texAttrsStr(face["y_off"])
					output += " "
					output += self.texAttrsStr(face["rot"])
					output += " "
					output += self.texAttrsStr(face["x_sc"])
					output += " "
					output += self.texAttrsStr(face["y_sc"])
					output += "\n"
				output += "}\n"
		output += "}\n"
		return output
