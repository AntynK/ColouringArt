from dataclasses import dataclass, field


@dataclass
class PickartFileData:
    info: dict = field(default_factory=dict)
    palette: list = field(default_factory=list)
    pixels: list = field(default_factory=list)
