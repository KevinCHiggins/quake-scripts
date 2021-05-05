import command

 # for testing using the old shape functions...
class LoadGeometry(command.GeoCommand):
	def __init__(self, brushes):
		self.brushes = brushes
	def execute(self):
		command.GeoCommand._geo = self.brushes
		print("Loaded " + str(len(self.brushes)) + " brushes into geo " + str(id(command.GeoCommand._geo)) + " which now holds " + str(len(command.GeoCommand._geo)) + "brushes.")