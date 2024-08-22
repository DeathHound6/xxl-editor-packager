from enum import Enum
from dataclasses import dataclass

# List indexes align with XXL config ids
GAME_NAMES = [
    "Asterix XXL",
    "Asterix XXL2",
    "Arthur and the Invisibles",
    "Asterix at the Olympic Games",
    "Spyro",
    "Alice in Wonderland",
    "How to Train your Dragon"
]
PLATFORM_NAMES = [
    "Steam",
    "PS2",
    "GCN",
    "PSP",
    "Wii",
    "Xbox360",
    "PS3"
]


class Platform(Enum):
    KWN = 0
    KP2 = 1
    KGC = 2
    KPP = 3
    KRV = 4
    KXE = 5
    KP3 = 6


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
