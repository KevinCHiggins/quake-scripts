from vgio.quake import map
from string import Template
import subprocess
import keyboard

# This script requires the vgio and keyboard modules to be installed using pip, i.e. with these shell commands:
# pip install vgio
# pip install keyboard

# This script is intended to set up a new Quake map for editing in TrenchBroom. It inputs the name of the map, without file extension, and creates:
#  - a blank map with preloaded texture wads (specified in wad_names, and accessible at wad_path)
#  - a batch file in the same directory (map_path) as the blank map, which can be run to compile the map (assuming the build tools are in tools_path) and launch Quake (from quake_path)
# It also:
#  - launches TrenchBroom with the new map
#  - minimises its own command prompt window
# Kevin Higgins, 15/12/20

def win_format(str):
	return str.replace("/", "\\") # double backslashes for paths, as Windows demands backslashes which need a preceding backslash escape code

# most of these actually get converted to using backslashes via calls to win_format(..) in the parameter list for batch_template.substitute(..)
wad_names = ["C:/Users/Kevin/Programs/Quake Stuff/TrenchBroom/Textures.wad"] # add more to the list if desired
wad_path = "" # THIS IS FUNCTIONAL and can be used to prefix any path or partial path to the texts in wad_names, but it can also be simply kept blank and the entire path kept in wad_names
		# if you prefer to keep wads in various locations
map_path = "C:/Users/Kevin/Maps/"
editor_path = "C:/Users/Kevin/Programs/Quake Stuff/TrenchBroom/"
tools_path = "C:/Users/Kevin/Programs/Quake Stuff/TrenchBroom/ericw-tools/bin/"
quake_path = "C:/quake/"
quake_subdir = "id1/maps/"

print("Enter name for new empty map, with no file extension:")
name = input()
assert(name.find(".") == -1)

map_file = open(map_path + name + ".map", "w")
batch_file = open(map_path + name + ".bat", "w")

ws = map.Entity()
setattr(ws, "spawnflags", "0")
setattr(ws, "classname", "worldspawn")
wads_concat = "" # we're gonna fill this single string (which will be a Worldspawn attr) with full wad paths and filenames delimited by semicolons, as per .MAP format
assert(len(wad_names) != 0)
for wn in wad_names:
	wads_concat = wads_concat + wad_path + wn + ";"
wads_concat = wads_concat[0:-1] #  remove final semicolon
setattr(ws, "wad", wads_concat)
map_file.write(map.dumps([ws]))
map_file.close()

# use a string template and a multiline string as the source for the batch script
batch_template = Template("""
cd ${active_path}\n
copy ${src_path}${filename} ${dest_path}${filename}
qbsp ${dest_path}${filename}\n
light -extra -soft -bounce C:\\quake\\id1\\maps\\${filename}\n
vis -fast ${dest_path}${filename}\n
cd ${game_path}\n
quakespasm.EXE +map ${map_name}
""")
batch_file.write(batch_template.substitute(map_name = name, filename = name + ".map", active_path = win_format(tools_path), src_path = win_format(map_path), dest_path = win_format(quake_path + quake_subdir), game_path = win_format(quake_path)))
batch_file.close()

# use subprocess.Popen instead of subProcess.run because Popen doesn't wait for the subprocess to complete, allowing us to do more stuff after launching TrenchBroom
subprocess.Popen([win_format(editor_path) + "TrenchBroom", win_format(map_path) + name + ".map"])

# hack to minimise command prompt so we can get straight to editing (if this script was run from a command prompt window)
keyboard.send("alt+space")
keyboard.send("n")