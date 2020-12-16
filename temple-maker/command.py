import entity
# Note this here is a simplification of the standard Command pattern - rather than the external client telling the command which receiver (i.e what map, entity or list
# of brushes to modify, commands build their own entities or else use a common map and working copy of geometry, each stored in a class variable.
# I'm liking this for now because I don't want to pass around entities, geometry or the whole map between commands in the client... it's an unnecessary
# complication because I'm building single maps with no overlapping geometry. So I keep it all private to this module.
# Later I may change this if stuff like translating/cloning of geometry becomes more desirable (which I'd say it will).

# None of these should be instantiated (hence the exceptions), they are intended to be subclassed in the map and geometry modules
class Command:
	def execute(self):
		raise NotImplementedError
# sets up a _map class variable - the common map list all subclasses will append to - and any convenience functions associated with it
class MapCommand(Command):
	_map = [] # class variable accessible to all MapCommands... 
	def map_has_worldspawn(self):
		# check first entity in list... this relies on the fact that setting worldspawn only ever leaves one worldspawn entity, at position 0
		if len(self._map) > 0 and self._map[0].attributes["classname"] == "worldspawn":
			return True
		else:
			return False
	def execute(self):
		raise NotImplementedError

# superclass of a command to take geometry from the working copy of geometry and put it in the map
class GeoCommand(Command):
	_geo = [] # class variable for **current working copy of geometry** - this is made accessible to create geometry commands so that they can add to it
	def execute(self):
		raise NotImplementedError