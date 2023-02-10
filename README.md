# Colouring art
It is a simple time killer game, in which you have to paint an image.

## Setup
Firstly you need to download Colouring art.exe(or source code) and assets.bak file, after that run .exe file or source code(file colouring_art.pyw), the game will create some folders.

In the game by default there are 2 images, but you can add your images.
(They are in the arts folder).

## Adding custom images
You can use the Art convertor.exe(or art_converter.py) utility, it is a simple console program which by default converts images from input folder to output folder. You can change the input folder with flag -i and the output folder with flag -o(output directory will be created automatically if it does not exist).

## About .pickart file
Game uses .pickart files(pick - name of python built-in module [pickle](https://docs.python.org/3.9/library/pickle.html)), files are compressed with [gzip](https://docs.python.org/3.9/library/gzip.html).

File structure:
```
{
    "info":{
        "size": (1, 1),
        "version": 1
    },
    "palette":[(int, int, int), ...],
    "pixels": [
        [(color_index, is_painted), ...]
    ]
}
```
"info" contains the size of image and version of file.

"palette" contains tuples with 3 ints (r, g, b), they must be less or equal 255 and bigger or equal 0.

"pixels" is a 2d array which contains color_index(int) and painted(bool).

## Security
[Pickle](https://docs.python.org/3.9/library/pickle.html) module has security issues, the game does not use standard pickle.load(), instead it uses [restricted loader](https://docs.python.org/3/library/pickle.html#restricting-globals) which blocks all external classes.
