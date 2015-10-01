# The Games DB API wrapper for Python


[![Build Status](https://travis-ci.org/rogerhil/thegamesdb.svg?branch=master)](https://travis-ci.org/rogerhil/thegamesdb)


Based on the The Games DB API: http://wiki.thegamesdb.net/index.php/Main_Page

## Installation

    $ python setup.py install


## Usage examples
```python
>>> from thegamesdb import TheGamesDb
>>> api = TheGamesDb()
```


## Platform Resource

```python
>>> api.platform
<PlatformResource get,list,games>
>>> platforms = api.platform.list()
>>> len(platforms)
59
>>> platforms[:5]
[<Platform: 3DO>, <Platform: Amiga>, <Platform: Amstrad CPC>, \
<Platform: Android>, <Platform: Arcade>]
>>> p = platforms[0]
>>> p
<Platform: 3DO>
>>> p.id, p.name, p.manufacturer
('25', '3DO', 'Panasonic')
>>> p.overview[:69] + ' (...)'
'The 3DO Interactive Multiplayer (often called simply 3DO) is a video  (...)'
>>> p = api.platform.get(id=p.id)
>>> p
<Platform: 3DO>
>>> threedo_games = p.games()
>>> len(threedo_games)
148
>>> threedo_games[:5]
[<Game: Mad Dog McCree (3DO)>, <Game: AD&D: Slayer (3DO)>, \
<Game: Blade Force (3DO)>, <Game: Battle Chess (3DO)>, \
<Game: Brain Dead 13 (3DO)>]
```

## Game Resource

```python
>>> api.game
<GameResource get,list>
>>> games = api.game.list(name='x-men')
>>> len(games)
100
>>> games[:5]
[<Game: X-Men (Sega 32X)>, <Game: X-Men (Arcade)>, \
<Game: X-Men (Sega Genesis)>, <Game: X-Men (Sega Mega Drive)>, \
<Game: X-Men (Sega Game Gear)>]
>>> games[30].id
'2468'
>>> game = api.game.get(2468)
>>> game
<Game: X-Men: Children Of The Atom (Arcade)>
>>> game.name, game.platform, game.publisher, game.developer
('X-Men: Children Of The Atom', 'Arcade', 'Capcom', 'Capcom')
```
