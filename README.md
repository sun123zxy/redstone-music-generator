# Redstone Music Generator

## Description

Automating building process of redstone music in Minecraft with Python scripts and MIDI files.

What this project aiming at is rather reminiscent of some old-fashioned command-block redstone music dating back 2016--2018, especially inspired by [1U_s' redstone music collection of Perfect Cherry Blossom](https://www.bilibili.com/video/BV1Gs411i7K9/). Check [here](https://www.bilibili.com/video/BV1KT421e7EF/) for a demo video.

Developed under Minecraft Java Edition 1.12.2, Python 3.8.3 and [Raspberry Jam Mod 0.94](https://github.com/arpruss/raspberryjammod/releases/tag/0.94). Python requirements are declared in `requirements.txt`. (Anyway I guess it is compatible with Minecraft 1.8 - 1.12.2 and any version of Python 3)

Note that the directory `mcpi/` is copied from the sample scripts in Raspberry Jam Mod directly.

## Installation

1. Install python (with pip) and Minecraft (with Forge) if you haven't done so yet.
2. Install [Raspberry Jam Mod](https://github.com/arpruss/raspberryjammod) with [instructions](https://www.instructables.com/Python-coding-for-Minecraft/). However, you should keep `.minecaft/mcpipy/` empty, and not using the `.exe` installer is suggested.
3. Copy all files of this repository into `.minecaft/mcpipy/`.
4. In `.minecraft/mcpipy/`, execute `pip install -r requirements.txt`.
5. (optional) Install resourcepack `realpiano`, a sound resourcepack made by lkrb. ([offical page](http://lkrb.net/blog/54.html) (already invalid), you may download it [here](https://www.cr173.com/soft/277354.html))

## Start

Functionalities are packed as modules, so it is suggested to write your own scripts to call them. Serveral sample scripts are provided in `sample/` for reference. For a quick start, with a Minecraft world running, you may execute `python -m sample.advancing` (for example) to run a sample script. Before that, a valid MIDI file should be placed at `my_script/music.mid`. Note that you should always execute commands in the root directory of this repository, running scripts as modules (with `python -m`).

## Maintenance

This project is developed mainly for personal use. It may iterate fast (or do not iterate at all!). Maintenance is not guaranteed. Nevertheless, issues and pull requests are always welcome.

## Q&A

- `falling_block` coordinates not consistent with the generated keyboard
  
  see [Issue #4](https://github.com/sun123zxy/redstone-music-generator/issues/4).
