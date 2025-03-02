#!/usr/bin/env python3
"""
Script to update pygame imports to pygame-ce imports.
"""
import os
import re

def update_file(file_path):
    """Update pygame imports to pygame-ce imports in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace 'import pygame' with 'import pygame_ce as pygame'
    updated_content = re.sub(r'^import pygame$', 'import pygame_ce as pygame', content, flags=re.MULTILINE)
    
    # Replace 'import pygame.' with 'import pygame_ce.'
    updated_content = re.sub(r'^import pygame\.', 'import pygame_ce.', updated_content, flags=re.MULTILINE)
    
    # Replace 'from pygame' with 'from pygame_ce'
    updated_content = re.sub(r'^from pygame', 'from pygame_ce', updated_content, flags=re.MULTILINE)
    
    # Don't modify pygame_gui imports
    updated_content = updated_content.replace('import pygame_ce_gui', 'import pygame_gui')
    updated_content = updated_content.replace('from pygame_ce_gui', 'from pygame_gui')
    
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes needed for {file_path}")

def process_directory(directory):
    """Process all Python files in a directory recursively."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                update_file(file_path)

if __name__ == "__main__":
    process_directory('game')
    process_directory('tests')
    print("Import updates complete!")
