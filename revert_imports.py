#!/usr/bin/env python3
"""
Script to revert pygame-ce imports back to pygame imports.
"""
import os
import re

def update_file(file_path):
    """Update pygame-ce imports back to pygame imports in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace 'import pygame_ce as pygame' with 'import pygame'
    updated_content = re.sub(r'^import pygame_ce as pygame$', 'import pygame', content, flags=re.MULTILINE)
    
    # Replace 'import pygame_ce.' with 'import pygame.'
    updated_content = re.sub(r'^import pygame_ce\.', 'import pygame.', updated_content, flags=re.MULTILINE)
    
    # Replace 'from pygame_ce' with 'from pygame'
    updated_content = re.sub(r'^from pygame_ce', 'from pygame', updated_content, flags=re.MULTILINE)
    
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
