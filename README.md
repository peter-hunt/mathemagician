# Mathemagician
Mathemagician is a command-line RPG game based on maths, puzzles and coding. And yes, I have just created another command-line game because I'm lazy. The project is aimed to gamify maths learning and to make a fun and maths teaching and game-mechanic-ally mathematically appealing (at least to me) RPG game.

The game will create a folder to store settings, profiles and other saved data in the folder `~/mathemagician`, where you can find the profile save files.

## Table of Contents
- [Mathemagician](#mathemagician)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Warnings](#warnings)
  - [Stories](#stories)

## Usage

**This project requires Python 3.12+**

It's recommended to install the game as a `pip` library to be able to run this from anywhere. To install Mathemagician, enter the main project folder `mathemagician`, not the one in the main folder, and use the following command:
```
python3 setup.py install
```

And to run the game with it installed in `pip`, use the following command:
```
python3 -m mathemagician
```

However, otherwise, you can just run the game from within the project folder and do:
```
python3 -m mathemagician
```

## Warnings

This project is under heavy development, so the data structures used for saving data might change. If your save file goes outdated, sorry, but it's probably not going to be usable again.

## Stories

This project is structurally much better than my [Skyblock Remake](https://github.com/peter-hunt/skyblock), which I made around two years ago and don't wish to keep working on it because its code is just disgusting. Feel free to learn from or use my code for your project with the `myjson` submodule, which is a prettier JSON file encoder, and `cliengine.py`, which modulizes the creation of CLI interfaces, which I did not do for Skyblock Remake, which was a mistake, or just any other code. I also incorporated the game assets data inside the code folder to not have to do a separate `skyblock-data` repository to pull from to update the game content, leading to issues like auto-updating the data to be incompatible with the current game code and just having to update it. Now, however, for a game update, you need to replace this game folder with the newly downloaded one.
