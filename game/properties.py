"""Properties and generators for game entities."""

import random
import numpy as np
from scipy.stats import beta
from .enums import StarType, PlanetType, ResourceType
from .constants import (
    YELLOW, RED, LIGHT_BLUE, BLUE, GREEN, ORANGE,
)

# Beta distribution parameters
MEAN = 0.5
VARIANCE = 0.02

# Calculate alpha and beta parameters for the beta distribution
_temp = MEAN * (1 - MEAN) / VARIANCE - 1
ALPHA = MEAN * _temp
BETA = (1 - MEAN) * _temp

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
    # Resource probabilities for each planet type
    RESOURCE_PROBABILITIES = {
        PlanetType.TERRESTRIAL: {
            ResourceType.MINERALS: 0.8,
            ResourceType.WATER: 0.6,
            ResourceType.ORGANIC: 0.4,
            ResourceType.RARE_ELEMENTS: 0.2,
            ResourceType.GASES: 0.1,
            ResourceType.ENERGY: 0.1,
            ResourceType.CRYSTALS: 0.1
        },
        PlanetType.GAS_GIANT: {
            ResourceType.GASES: 0.9,
            ResourceType.ENERGY: 0.4,
            ResourceType.RARE_ELEMENTS: 0.1,
            ResourceType.MINERALS: 0.1,
            ResourceType.WATER: 0.1,
            ResourceType.ORGANIC: 0.1,
            ResourceType.CRYSTALS: 0.1
        },
        PlanetType.ICE_WORLD: {
            ResourceType.WATER: 0.9,
            ResourceType.MINERALS: 0.3,
            ResourceType.GASES: 0.2,
            ResourceType.RARE_ELEMENTS: 0.1,
            ResourceType.ENERGY: 0.1,
            ResourceType.ORGANIC: 0.1,
            ResourceType.CRYSTALS: 0.1
        },
        PlanetType.DESERT: {
            ResourceType.MINERALS: 0.7,
            ResourceType.RARE_ELEMENTS: 0.3,
            ResourceType.ENERGY: 0.2,
            ResourceType.GASES: 0.1,
            ResourceType.WATER: 0.1,
            ResourceType.ORGANIC: 0.1,
            ResourceType.CRYSTALS: 0.1
        },
        PlanetType.VOLCANIC: {
            ResourceType.MINERALS: 0.8,
            ResourceType.ENERGY: 0.6,
            ResourceType.RARE_ELEMENTS: 0.4,
            ResourceType.GASES: 0.1,
            ResourceType.WATER: 0.1,
            ResourceType.ORGANIC: 0.1,
            ResourceType.CRYSTALS: 0.1
        },
        PlanetType.OCEANIC: {
            ResourceType.WATER: 1.0,
            ResourceType.ORGANIC: 0.7,
            ResourceType.GASES: 0.3,
            ResourceType.MINERALS: 0.1,
            ResourceType.RARE_ELEMENTS: 0.1,
            ResourceType.ENERGY: 0.1,
            ResourceType.CRYSTALS: 0.1
        }
    }
    
    PROPERTIES = {
        PlanetType.TERRESTRIAL: {
            'color': GREEN,
            'min_size': 8,
            'max_size': 12
        },
        PlanetType.GAS_GIANT: {
            'color': ORANGE,
            'min_size': 14,
            'max_size': 20
        },
        PlanetType.ICE_WORLD: {
            'color': LIGHT_BLUE,
            'min_size': 6,
            'max_size': 10
        },
        PlanetType.DESERT: {
            'color': YELLOW,
            'min_size': 8,
            'max_size': 12
        },
        PlanetType.VOLCANIC: {
            'color': RED,
            'min_size': 8,
            'max_size': 14
        },
        PlanetType.OCEANIC: {
            'color': BLUE,
            'min_size': 10,
            'max_size': 16
        }
    }

    @staticmethod
    def get_random_type():
        return random.choice(list(PlanetType))

    @staticmethod
    def generate_resources(planet_type):
        """
        Generate resource values for a planet of the given type.
        
        Args:
            planet_type (PlanetType): The type of planet
            
        Returns:
            dict: A dictionary with resource types as keys and resource amounts as values
        """
        resources = {}
        
        # Get resource probabilities for this planet type
        planet_resources = PlanetProperties.RESOURCE_PROBABILITIES[planet_type]
        
        # Generate a value for every resource type
        for resource_type in ResourceType:
            # Check if this resource type is common for this planet type
            if random.random() < planet_resources.get(resource_type, 0.1):
                # Generate a higher value (using the standard beta distribution)
                beta_value = beta.rvs(ALPHA, BETA)
                amount = int(round(beta_value * 100))
            else:
                # Generate a lower value for uncommon resources
                # Use a modified beta distribution with lower mean
                low_mean = 0.1
                low_temp = low_mean * (1 - low_mean) / VARIANCE - 1
                low_alpha = low_mean * low_temp
                low_beta = (1 - low_mean) * low_temp
                
                beta_value = beta.rvs(low_alpha, low_beta)
                amount = int(round(beta_value * 100))
            
            resources[resource_type] = amount
        
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
