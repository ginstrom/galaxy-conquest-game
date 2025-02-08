"""Properties and generators for game entities."""

import random
from .enums import StarType, PlanetType, ResourceType
from .constants import (
    YELLOW, RED, LIGHT_BLUE, BLUE, GREEN, ORANGE,
)

class StarProperties:
    PROPERTIES = {
        StarType.MAIN_SEQUENCE: {
            'color': YELLOW,
            'min_size': 4,
            'max_size': 6,
            'min_planets': 2,
            'max_planets': 5,
            'probability': 0.4
        },
        StarType.RED_GIANT: {
            'color': RED,
            'min_size': 8,
            'max_size': 12,
            'min_planets': 1,
            'max_planets': 3,
            'probability': 0.3
        },
        StarType.WHITE_DWARF: {
            'color': LIGHT_BLUE,
            'min_size': 2,
            'max_size': 4,
            'min_planets': 0,
            'max_planets': 2,
            'probability': 0.2
        },
        StarType.BLUE_GIANT: {
            'color': BLUE,
            'min_size': 6,
            'max_size': 10,
            'min_planets': 3,
            'max_planets': 6,
            'probability': 0.1
        }
    }

    @staticmethod
    def get_random_type():
        return random.choices(
            list(StarType),
            weights=[StarProperties.PROPERTIES[t]['probability'] for t in StarType]
        )[0]

class PlanetProperties:
    PROPERTIES = {
        PlanetType.TERRESTRIAL: {
            'color': GREEN,
            'min_size': 8,
            'max_size': 12,
            'possible_resources': [
                (ResourceType.MINERALS, 0.8),
                (ResourceType.WATER, 0.6),
                (ResourceType.ORGANIC, 0.4),
                (ResourceType.RARE_ELEMENTS, 0.2)
            ]
        },
        PlanetType.GAS_GIANT: {
            'color': ORANGE,
            'min_size': 14,
            'max_size': 20,
            'possible_resources': [
                (ResourceType.GASES, 0.9),
                (ResourceType.ENERGY, 0.4),
                (ResourceType.RARE_ELEMENTS, 0.1)
            ]
        },
        PlanetType.ICE_WORLD: {
            'color': LIGHT_BLUE,
            'min_size': 6,
            'max_size': 10,
            'possible_resources': [
                (ResourceType.WATER, 0.9),
                (ResourceType.MINERALS, 0.3),
                (ResourceType.GASES, 0.2)
            ]
        },
        PlanetType.DESERT: {
            'color': YELLOW,
            'min_size': 8,
            'max_size': 12,
            'possible_resources': [
                (ResourceType.MINERALS, 0.7),
                (ResourceType.RARE_ELEMENTS, 0.3),
                (ResourceType.ENERGY, 0.2)
            ]
        },
        PlanetType.VOLCANIC: {
            'color': RED,
            'min_size': 8,
            'max_size': 14,
            'possible_resources': [
                (ResourceType.MINERALS, 0.8),
                (ResourceType.ENERGY, 0.6),
                (ResourceType.RARE_ELEMENTS, 0.4)
            ]
        },
        PlanetType.OCEANIC: {
            'color': BLUE,
            'min_size': 10,
            'max_size': 16,
            'possible_resources': [
                (ResourceType.WATER, 1.0),
                (ResourceType.ORGANIC, 0.7),
                (ResourceType.GASES, 0.3)
            ]
        }
    }

    @staticmethod
    def get_random_type():
        return random.choice(list(PlanetType))

    @staticmethod
    def generate_resources(planet_type):
        resources = []
        for resource, probability in PlanetProperties.PROPERTIES[planet_type]['possible_resources']:
            if random.random() < probability:
                amount = random.randint(50, 100)  # Random resource amount between 50-100
                resources.append({'type': resource, 'amount': amount})
        return resources

class NameGenerator:
    PREFIXES = [
        "Alpha", "Beta", "Gamma", "Delta", "Nova", "Proxima", "Sirius",
        "Vega", "Rigel", "Antares", "Polaris", "Centauri", "Cygnus",
        "Lyra", "Orion", "Andromeda", "Cassiopeia", "Perseus"
    ]
    
    SUFFIXES = [
        "Prime", "Minor", "Major", "Core", "Binary", "Nexus", "Gateway",
        "Hub", "Cluster", "Network", "System", "Complex", "Station"
    ]
    
    NUMBERS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    
    @classmethod
    def generate_name(cls):
        if random.random() < 0.3:  # 30% chance for a number suffix
            return f"{random.choice(cls.PREFIXES)} {random.choice(cls.NUMBERS)}"
        else:
            return f"{random.choice(cls.PREFIXES)} {random.choice(cls.SUFFIXES)}"
