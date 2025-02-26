#!/usr/bin/env python3
"""
Galaxy Conquest - A space exploration game.

This is the main entry point for the Galaxy Conquest game. It handles command-line
arguments, configuration loading, and initializes the game.
"""

import sys
import argparse

from game.game import Game
from game.logging_config import configure_logging
from game.config import load_config, apply_config, parse_arguments


def main(argv):
    # Load configuration first
    config = load_config()
    
    # Apply configuration to settings
    apply_config(config)
    
    # Parse arguments (which can override config)
    args = parse_arguments(argv)
    
    # Configure logging (use log level from config or command line)
    log_level = args.log_level or config['logging']['level']
    configure_logging(log_level)
    
    # Initialize and run game
    game = Game()
    game.run()

if __name__ == '__main__':
    main(sys.argv)
