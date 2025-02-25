"""
Views package for Galaxy Conquest game.

Provides the view classes for different game states:
- GalaxyView: Renders the galaxy map with star systems
- SystemView: Renders a star system with its orbiting planets
- PlanetView: Renders detailed planet information
- InfoPanel: Base class for information panels
- GalaxyViewInfoPanel: Information panel for galaxy view
- SystemViewInfoPanel: Information panel for system view
- PlanetViewInfoPanel: Information panel for planet view
"""

from game.views.galaxy import GalaxyView
from game.views.system import SystemView
from game.views.planet import PlanetView
from game.views.infopanel import (
    InfoPanel, 
    GalaxyViewInfoPanel, 
    SystemViewInfoPanel, 
    PlanetViewInfoPanel
)

__all__ = [
    'GalaxyView', 
    'SystemView', 
    'PlanetView', 
    'InfoPanel',
    'GalaxyViewInfoPanel',
    'SystemViewInfoPanel',
    'PlanetViewInfoPanel'
]
