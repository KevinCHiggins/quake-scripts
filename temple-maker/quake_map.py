import edifices
import entity
import shapes
#import command
import geo_command
import map_command

#####testBrush = shapes.create_cuboid_brush([1, 1, 1], [0, 0, 0]) # list not tuple so we can do more error correction inside shapes
DEFAULT_TEXTURE = "metal5_4"
DEFAULT_WAD_PATH = "C:\\Users\\Kevin\\Programs\\Quake Stuff\\TrenchBroom\\Textures.wad"
print("Using WAD path defined in quake_map.py: " + DEFAULT_WAD_PATH)
num_cols = int(input("Please enter a small even number for how many columns should front the edifice: "))
edifice = edifices.roofed_column_grid(num_cols, num_cols * 2 + 1, (0, 0, 0), 700, 280)
commands = []
commands.append(map_command.SetWorldspawn(wad_path = DEFAULT_WAD_PATH, sunlit = True))
commands.append(geo_command.LoadGeometry(edifice["brushes"]))
commands.append(map_command.AddToNewBrushEntity("func_detail"))
bound_corner_a = (edifice["corner_a"][0] - 2048, edifice["corner_a"][1] - 2048, edifice["corner_a"][2] - 16) # give ourselves some room...
bound_corner_b = (edifice["corner_b"][0] + 2048, edifice["corner_b"][1] + 2048, edifice["corner_b"][2] + 16)
boundingRoom = shapes.create_room(bound_corner_a, bound_corner_b)
commands.append(geo_command.LoadGeometry(boundingRoom))
commands.append(map_command.AddToWorldspawn())
commands.append(map_command.AddPointEntity("info_player_start", (-40, -40, 80)))
commands.append(map_command.WriteMapToFile("py_oct.map"))
for command in commands: 
	print("Executing " + type(command).__name__)
	command.execute()

#roomEnt = entity.create_lit_worldspawn(brushes = boundingRoom)
#edEnt = entity.Entity(classname = "func_detail", brushes = edifice["brushes"]) # each column should be a different func_detail, but...
#playEnt = entity.create_point("info_player_start", (-40, -40, 80), 0)
#testMap = [roomEnt, edEnt, playEnt]
#testFile = open("C:\\quake\\id1\\maps\\py_oct.map", "w")

#toMapFile(testMap, testFile)

