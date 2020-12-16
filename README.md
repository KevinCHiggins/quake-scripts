### Quake Scripts

#### Python scripts for automating Quake 1 level design tasks

**makemap** - this utility is for minimising clicks needed to start a new Quake 1 mapping project using [TrenchBroom](https://kristianduske.com/trenchbroom/). It:

1. Creates an empty map file with preloaded texture archives (so you don't need to configure that in TrenchBroom each time) and also
2.  Creates a batch script, *with the same name and location as the map, e.g. ```C:\maps\mymap.map``` and ```C:\maps\mymap.bat```*, you can execute anytime you wish to build the map and launch it in Quake.
3. Launches the blank map in Trenchbroom.

The makemap utility has the following dependencies:

- Python (tested on Python 3.8.0)
- an installation of Quake 1 from which you can load a texture .WAD archive (and to play your map)
- an engine that works on your system, I recommend [QuakeSpasm](http://quakespasm.sourceforge.net/)
- [TrenchBroom](https://kristianduske.com/trenchbroom/), the excellent modern Quake map editor
- build tools to compile levels, such as [Eric Wa's](https://ericwa.github.io/ericw-tools/)
- these Python packages which can be installed using [pip](https://pypi.org/project/pip/):
  - keyboard
  - vgio ([Joshua Skelton's library](http://joshuaskelton.com/projects/vgio/) for accessing and processing Quake (and other game) file formats)

**temple-maker** - see README.md in the ```temple-maker``` subdirectory of this repo

Kevin Higgins, 16/12/20