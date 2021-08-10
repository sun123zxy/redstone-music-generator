# Redstone Music Generator

A project based on Raspberry Jam Mod aimed to automate redstone-music building process in Minecraft, using python scripts and MIDI file.

The project is developed under Minecraft Java Edition 1.12.2, Python 3.8.3 and [Raspberry Jam Mod 0.94](https://github.com/arpruss/raspberryjammod/releases/tag/0.94). Python requirements are declared in `requirements.txt`. (Anyway I guess it is compatible with Minecraft 1.8~1.12.2 and any version of Python 3) 

`mine.py` and files in `mcpi/` in the repository come from the sample scripts in Raspberry Jam Mod, which are the basic requirements.

## Install

1. Install python (with pip) and Minecraft (with Forge) if you haven't installed them yet.
2. Install [Raspberry Jam Mod](https://github.com/arpruss/raspberryjammod) as it instructs ([a more detailed official instruction](https://www.instructables.com/Python-coding-for-Minecraft/)), but keep `.minecaft/mcpipy/` empty. Also, not using the `.exe` installer is suggested.
3. Put all this repository files into `.minecaft/mcpipy/`.
4. In `.minecraft/mcpipy/`, execute `pip install -r requirements.txt`.
5. (optional) Install resourcepack `realpiano`, a sound resourcepack made by lkrb. ([offical page](http://lkrb.net/blog/54.html) (already invalid), you may download it [here](https://www.cr173.com/soft/277354.html))
6. (optional) Suggest install [WorldEdit](https://www.curseforge.com/minecraft/mc-mods/worldedit) and [VoxelMap](https://www.curseforge.com/minecraft/mc-mods/voxelmap/) mod to assist in your building process.

## Quickstart

1. In `main.py`:

   ```python
   """
   entry point
   """
   import sample.quickstart
   ```

   It will execute `sample/quickstart.py` via `main.py` as an entry point.
   
2. Create a new world in Minecraft.

3. Execute `python main.py`. Or you can execute `/py main.py` in your Minecraft console.

4. Enjoy the music!

## Further Instructions

`MIDIHandler` will show lots of useful information of the MIDI file when being initialized. Suggest having a look at them before generating.

The project presets various redstone music styles. In `sample/` directory, there are sample scripts which show the usage of them.

Try them, modify configurations or write your own script as you like.

Note that you should always run your script via `main.py` as an entry point.

