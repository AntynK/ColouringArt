class Color:
    def __init__(self, color: tuple[int, ...]):
        self.color = color[:4]
        if len(self.color) == 4 and self.color[-1] != 255:
            self.color = (*self.color[:3], 255)

        self._generate_grayscale()

    def _generate_grayscale(self):
        color = sum(self.color[:3]) // 3
        if color == 0:
            color = 10
        self.grayscale = (
            (color, color, color)
            if len(self.color) == 3
            else (color, color, color, 255)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.color})"
