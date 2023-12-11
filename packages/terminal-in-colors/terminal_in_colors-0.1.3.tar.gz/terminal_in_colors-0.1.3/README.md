# terminal-in-colors

Give color to your terminal, using 256 colors or RGB, use bold, italic, underline, among others, in a simple and uncomplicated way.


<p>
<img src="img.png" alt='img' />
</p>


# Instalation

You can install simply using a command, thank *PyPi*.

```bash
$ pip install termina-in-colors
```

# Usage

```python
from terminal_in_color.ColorTerminal import ColorTerminal

string = "Hi"

c = ColorTerminal()

print(c.paint(string, color="red", blink="slow"))
```

# Methods Available

* `paint(string, color, bold, italic, underline, overline, doubleunderline, blink, background, opaque)` - Formats the string using the available options, returns a string.
	- string: text to apply format.
	- color: color by name like "red", by number, or RGB using list of numbers [0, 0, 0].
	- bold: True or False.
	- italic: True or False .
	- underline: True or False.
	- overline: True or False.
	- doubleunderline: True or False.
	- blink: "slow" or "rapid".
	- background: color by name like "red", by number, or RGB using list of numbers [0, 0, 0].
	- opaque: True or False.

* `find(color, exact)` - Searches by color.
    - color: name of color, integer, and returns list to RGB.
    - exact: True or False, optional.

* `clear()` - return string to clear format colors.

* `print_all()` - Print all 256 colors.`


# Documentation

-> **[https://kurotom.github.io/terminal_in_colors/](https://kurotom.github.io/terminal_in_colors/)**
