from enum import Enum
from dataclasses import dataclass

# List indexes align with XXL config game id
GAME_NAMES = [
    "Asterix XXL",
    "Asterix XXL2",
    "Arthur and the Invisibles",
    "Asterix at the Olympic Games",
    "Spyro",
    "Alice in Wonderland",
    "How to Train your Dragon"
]


class Platform(Enum):
    KWN = 0  # pc
    KP2 = 1  # ps2
    KGC = 2  # gcn
    KPP = 3  # psp
    KRV = 4  # wii
    KXE = 5  # xbox360
    KP3 = 6  # ps3


@dataclass
class XXLProjectEditor:
    initial_level: int = None


@dataclass
class XXLProjectGame:
    id: int = None
    is_remaster: bool = None
    platform: Platform = None


@dataclass
class XXLProjectMeta:
    name: str = None


@dataclass
class XXLProjectPaths:
    game_module: str = None
    input_path: str = None
    output_path: str = None


@dataclass
class XXLProject:
    editor: XXLProjectEditor = None
    format_version: str = None
    game: XXLProjectGame = None
    meta: XXLProjectMeta = None
    paths: XXLProjectPaths = None
