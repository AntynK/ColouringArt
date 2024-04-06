# Colouring art
#### [Українська версія](README_UA.md)

It is a simple time killer game, in which you have to paint an image.

## Setup
Firstly you need to download `Colouring art.exe`(or source code) and `assets.bak` file, after that run .exe file or source code(`colouring_art.pyw`), the game will create some folders.

File `assets.bak` must be in the same folder as game. This file constains all fonts and images for game.

In the game by default there are 2 images, but you can add your images.

## Adding custom images
You can use [pickart](https://pypi.org/project/Pickart/) module to convert PNG files.
Put converted images(.pickart) in categories folder(`arts\<category_name>`).

## Adding custom categories
By default game has one category `plants` with two images. You can change existing category or add new one.

### Category structure
All categories are located in `arts` folder.

```
<category_name>
    |-icon.png
    |-style.json
    |-*.pickart
```
`icon.png` - image that will be displayed on main window. If it is omitted game will use default image.

`style.json` - category style. Configures background colour.

`*.pickart` - [Pickart file](https://pypi.org/project/Pickart/) with any name(with extension `.pickart`). Category can have multiple `*.pickart` files.

### `style.json` file structure
```Python
{
    "bg": [red, green, blue, alpha]
}
```
`bg` - list of integers in range from 0 to 255(including). `alpha` - optional.


## Security
[Pickle](https://docs.python.org/3.9/library/pickle.html) module has security issues, the game does not use standard pickle.load(), instead it uses [restricted loader](https://docs.python.org/3/library/pickle.html#restricting-globals) which blocks all external classes.
