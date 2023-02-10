from pathlib import Path

from argparse import ArgumentParser

from converter.convert_to_pickart import convert_to_pickart
from converter.convert_to_png import convert_to_png

parser = ArgumentParser()

parser.add_argument("-i", "--input", default="input")
parser.add_argument("-o", "--output", default="output")
parser.add_argument("-m", "--mode", choices=("0", "1"), default="0")

args = parser.parse_args()


def main():
    input_dir: Path = Path(args.input)
    output_dir: Path = Path(args.output)
    if input_dir.name == "input":
        input_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.is_dir():
        print(f"'{input_dir}' folder does not exist.")
        return
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "0":
        for filename in input_dir.glob("*.png"):
            print(f"Converting '{filename}'.")
            convert_to_pickart(filename, output_dir)
    elif args.mode == "1":
        for filename in input_dir.glob("*.pickart"):
            print(f"Converting '{filename}'.")
            convert_to_png(filename, output_dir)


if __name__ == "__main__":
    main()
