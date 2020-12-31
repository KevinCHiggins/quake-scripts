### Quake Scripts

#### Python scripts for automating Quake 1 level design tasks

**Makemap** - this utility reduces clicks needed to start a new Quake 1 mapping project using [TrenchBroom](https://kristianduske.com/trenchbroom/). To use it you will need to **edit the path definitions** in lines 25-32. It:

1. Creates an empty map file with preloaded texture archives (so you don't need to configure that in TrenchBroom each time)
2.  Creates a batch script, *with the same name and location as the map, e.g. ```C:\maps\mymap.map``` and ```C:\maps\mymap.bat```*, you can execute anytime you wish to build the map and launch it in Quake
3. Launches the blank map in Trenchbroom

Makemap has the following dependencies:

- Python (tested on Python 3.8.0)
- an installation of Quake 1 from which you can load a texture .WAD archive (and to play your map)
- an engine that works on your system, I recommend [QuakeSpasm](http://quakespasm.sourceforge.net/)
- [TrenchBroom](https://kristianduske.com/trenchbroom/), the excellent modern Quake map editor
- build tools to compile levels, such as [Eric Wa's](https://ericwa.github.io/ericw-tools/)
- these Python packages which can be installed using [pip](https://pypi.org/project/pip/):
  - keyboard
  - vgio ([Joshua Skelton's library](http://joshuaskelton.com/projects/vgio/) for accessing and processing Quake (and other game) file formats)

**Temple-maker** - see README.md in the ```temple-maker``` subdirectory of this repo

**Arch** - see README.md in the ```arch``` subdirectory of this repo

Kevin Higgins, 16/12/20