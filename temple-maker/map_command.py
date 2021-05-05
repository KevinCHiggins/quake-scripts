import command
import entity
# command to write the map to disk
class WriteMapToFile(command.MapCommand):
	def __init__(self, filename):
		self.filename = filename
	def execute(self):
		file = open(self.filename, "w")
		output = ""
		#print("Writing map. " + str(len(command.MapCommand._map)) + " entities.")
		for entity in command.MapCommand._map:
			print(entity.attributes)
			output += entity.toMapFormat()
		file.write(output)

# adds a worldspawn entity or overwrites the current one if there is one already
class SetWorldspawn(command.MapCommand):
	def __init__(self, wad_path, sunlit = True):
		self.sunlit = sunlit
		self.wad_path = wad_path
	def execute(self):
		world = entity.Entity("worldspawn")
		world.attributes.update({"wad": self.wad_path, "_point_format": "1"}) # can move to defaults or data later
		if self.sunlit:
			# can move to defaults or data later
			world.attributes.update({"_sunlight": "250", "_sunlight_mangle": "0 -80 0"})

		if command.MapCommand.map_has_worldspawn(self):
	   		del _map[0] # still a bit lopsided, that we're reaching into the entity list in this way... no, I suppose it works. All Map Commands are allowed do this stuff
		command.MapCommand._map.insert(0, world) 

# adds a point entity with given attributes
class AddPointEntity(command.MapCommand):
	def __init__(self, classname, pos, ang = 0):
		self.ang = ang
		self.classname = classname
		self.pos = pos
	def execute(self):
		point_entity = entity.Entity(self.classname)
		point_entity.attributes.update({"origin": str(self.pos[0]) + " " + str(self.pos[1]) + " " + str(self.pos[2]), "angle": str(self.ang)}) # not gorgeous but should do it
		#print("_map length " + str(len(command.MapCommand._map)))
		command.MapCommand._map.append(point_entity)
		#print("_map length " + str(len(command.MapCommand._map)))
		#print(str(command.MapCommand._map[len(command.MapCommand._map) - 1].attributes))
# adds whatever geometry is in the _geo class variable, to the map as an entity with the given attributes
class AddToNewBrushEntity(command.GeoCommand, command.MapCommand):
	def __init__(self, classname, extra_attributes = {}):
		self.classname = classname
		self.extra_attributes = extra_attributes
	def execute(self):
		
		print("Building brush entity, currently geo " + str(id(command.GeoCommand._geo)) + " has " + str(len(command.GeoCommand._geo)) + " brushes.")
		brush_entity = entity.Entity(classname = "func_detail", brushes = command.GeoCommand._geo)
		command.MapCommand._map.append(brush_entity)
		print(command.MapCommand._map[len(command.MapCommand._map) - 1])
# adds whatever geometry is in the _geo class variable, to the map in the worldspawn entity - note there must have been a worldspawn previously set
class AddToWorldspawn(command.GeoCommand, command.MapCommand):
	def execute(self):
		if command.MapCommand.map_has_worldspawn(self):
			print("Adding to worldspawn from " + str(id(command.GeoCommand._geo)) + " " + str(len(command.GeoCommand._geo)) + " brushes.")
			command.MapCommand._map[0].brushes = command.MapCommand._map[0].brushes + (command.GeoCommand._geo) # this seems a little raw...
		else:
			raise Exception("No worldspawn in map!") # we could arguably insert a worldspawn, except we don't know what parameters are appropriate