from sys import version_info

if version_info < (3, 12):
    raise RuntimeError('mathemagician requires Python 3.12')

from .path import path_init
path_init()

from .game import Game
from .profile import ProfileInstance


def main():
    game = Game()
    game.run()


def test():
    pass


if __name__ == '__main__':
    main()
