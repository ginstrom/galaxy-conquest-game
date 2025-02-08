"""Enums for the Galaxy Conquest game."""

from enum import Enum

class StarType(Enum):
    MAIN_SEQUENCE = "Main Sequence Star"
    RED_GIANT = "Red Giant"
    WHITE_DWARF = "White Dwarf"
    BLUE_GIANT = "Blue Giant"

class ResourceType(Enum):
    MINERALS = "Minerals"
    CRYSTALS = "Crystals"
    GASES = "Gases"
    ORGANIC = "Organic Matter"
    ENERGY = "Energy Source"
    WATER = "Water"
    RARE_ELEMENTS = "Rare Elements"

class PlanetType(Enum):
    TERRESTRIAL = "Terrestrial"
    GAS_GIANT = "Gas Giant"
    ICE_WORLD = "Ice World"
    DESERT = "Desert"
    VOLCANIC = "Volcanic"
    OCEANIC = "Oceanic"

class GameState(Enum):
    STARTUP_MENU = "startup_menu"
    GALAXY = "galaxy"
    SYSTEM = "system"
    GALAXY_MENU = "galaxy_menu"
    SYSTEM_MENU = "system_menu"
