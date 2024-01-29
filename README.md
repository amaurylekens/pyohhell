# pyohhell

A Oh Hell card game engine

## Installation

```bash
$ pip install pyohhell
```

## Usage

`pyohhell` can be used to play a Oh hell card game as follows:

```python
from pyohhell.game_engine import GameEngine
from pyohhell.player import Player

game_engine = GameEngine()
player_1 = Player(1)
player_2 = Player(2)
game_engine.subscribe_player(player_1)
game_engine.subscribe_player(player_2)
game_engine.play_game(seed=42)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pyohhell` was created by amaurylekens. It is licensed under the terms of the MIT license.

## Credits

`pyohhell` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
