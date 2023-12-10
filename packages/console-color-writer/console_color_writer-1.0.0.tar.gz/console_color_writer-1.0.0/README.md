# console_color_writer

[![Downloads](https://static.pepy.tech/badge/dumb-menu)](https://pepy.tech/project/dumb-menu)

write lines with color tags !


## Installation

```
pip install console_color_writer
```

https://pypi.org/project/dumb-menu/

https://github.com/cornradio/dumb_menu (I want stars ⭐ uwu)

## Usage

example:

```python
from console_color_writer import *

print_green('ok','some info text ...')
print_yellow('alert','some info text ...')
print_red('bad','some info text ...')
print_cyan('some info text ... only cyan')
print_magenta('some info text ... only magenta')
print_white('only white text here (super white)')

print('\nhere some tag example:')
print_green_tag('ok','some info text ...')
print_yellow_tag('alert','some info text ...')
print_red_tag('bad','some info text ...')

print('\nthat all ... color makes the world better !')
```

![Imgur](https://i.imgur.com/gMQB4L7.png)



## Get help

Get help ➡️ [Github issue](https://github.com/cornradio/dumb_menu/issues)

## Update log



`1.0.0` first release

## how to upload a new version (for me)

en: https://packaging.python.org/tutorials/packaging-projects/ 

zh: https://python-packaging-zh.readthedocs.io/zh_CN/latest/minimal.html#id2

> make sure have twine installed first

1. change `setup.py`
2. testing `py setup.py develop`
3. `py setup.py sdist`
4. `twine upload dist/*`

test code :
```
py

from console_color_writer import *

print_green('ok','some info text ...')
print_yellow('alert','some info text ...')
print_red('bad','some info text ...')
print_cyan('some info text ... only cyan')
print_magenta('some info text ... only magenta')
print_white('only white text here (super white)')
dumb_menu.demo()
```