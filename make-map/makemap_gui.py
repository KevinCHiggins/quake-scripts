from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
from vgio.quake import map as q1map
import subprocess
import sys

l = os.listdir()
wads_found = list(filter(lambda name: name[-4:] == ".wad", l))

map_path = "C:/Users/Kevin/Maps"
editor_path = os.getcwd() # assumes that TrenchBroom is in current working directory - i.e. this script must be started in the Trenchbroom directory
wad_path = editor_path # assumes that WADs are kept in the root of the TrenchBroom directory

def launch():
    wad_names = list(map(lambda i: wads_found[i], wads_box.curselection()))

    name = map_name.get()
    if len(name) == 0:
        messagebox.showerror("Invalid map name", "The map name must not be empty.")
        return 1
        
    map_file = open(map_path + "/" + name + ".map", "w") # note that forward slashes work fine even in Windows
    
    ws = q1map.Entity()
    setattr(ws, "spawnflags", "0")
    setattr(ws, "classname", "worldspawn")
    wads_concat = "" # we're gonna fill this single string (which will be a Worldspawn attr) with full wad paths and filenames delimited by semicolons, as per .MAP format
    if len(wad_names) != 0:
        for wn in wad_names:
            print ("wads_concat" + str(type(wads_concat)))
            print ("wad_path" + str(type(wad_path)))
            print ("wn" + str(type(wn)))
            wads_concat = wads_concat + wad_path + "/" + wn + ";"
        wads_concat = wads_concat[0:-1] #  remove final semicolon
        setattr(ws, "wad", wads_concat)
    if len(mods_box.curselection()) == 1: # mods_box uses selectmode = "browse" so length can only be 0 or 1
        # curselection() returns a list of **indices** (in this case of length 1)
        # so I use that index to index my hardcoded mods list, taking the 2nd member of the tuple thus found which is the mod directory, and the 3rd which is the FGD's filename
        setattr(ws, "_tb_mod", mods_hardcoded[mods_box.curselection()[0]][1]) 
        setattr(ws, "_tb_def", "external:" + mods_hardcoded[mods_box.curselection()[0]][2]) 
    map_file.write("// Game: Quake\n// Format: Standard\n// entity 0\n")
    map_file.write(q1map.dumps([ws]))
    map_file.close()
    
    # use subprocess.Popen instead of subProcess.run because Popen doesn't wait for the subprocess to complete, allowing us to do more stuff after launching TrenchBroom
    # currently we assume that the script is in the TrenchBroom directory
    subprocess.Popen(["TrenchBroom", map_path + "/" + name + ".map"])
    
    sys.exit(0)
    
root = Tk()

mm_frame = ttk.Frame(root, padding = (10, 10, 10, 10))
mm_frame.pack()

wads_label = Label(mm_frame, text = "WAD(s)")
wads_label.pack()

wads_found_var = StringVar(value = wads_found)  # Python list must be made into string representation for Tkinter
wads_box = Listbox(mm_frame, listvariable = wads_found_var, selectmode = "extended", exportselection="False") # "MULTIPLE" is an obsolete selectmode not to be used
wads_box.pack()

mods_label = Label(mm_frame, text = "Mod (optional)")
mods_label.pack()
mods_hardcoded = [("Arcane Dimensions 1.8", "ad", "ad_1_8.fgd"), ("Copper", "copper", "copper.fgd"), ("Quoth 2.2", "quoth", "quoth2.fgd")] # should be moved to a config file
mods_var = StringVar(value = list(map(lambda tuple: tuple[0], mods_hardcoded)))
mods_box = Listbox(mm_frame, listvariable = mods_var, selectmode="browse", exportselection="False")
mods_box.pack()

tb_check_var = IntVar()
tb_check_var.set(1) # default ticked - later we'll save/load this in/from a config file
tb_check_but = Checkbutton(mm_frame, text = "Launch Trenchbroom", variable = tb_check_var)
tb_check_but.pack()

map_name_label = Label(mm_frame, text = "Map name (without extension)")
map_name_label.pack()

map_name = StringVar()
map_name_entry = Entry(mm_frame, textvariable = map_name)
map_name_entry.pack()

launch_but = Button(mm_frame, text = "Create!", command = launch)
launch_but.pack()

root.mainloop()