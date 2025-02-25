# Contributing Guide

This document provides guidelines for contributing to the Galaxy Conquest game project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone git@github.com:yourusername/galaxy-conquest-game.git
cd galaxy-conquest-game
```

3. Set up the development environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Create a branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Style

The project follows PEP 8 style guidelines with a few modifications:

- Line length: 88 characters maximum
- Indentation: 4 spaces
- File encoding: UTF-8

We use the following tools to enforce code style:

- **flake8**: For linting
- **black**: For code formatting

Run these tools before submitting a pull request:

```bash
# Run flake8 to check for style issues
flake8 game tests

# Run black to format code
black game tests
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `InfoPanel`, `GalaxyView`)
- **Functions/Methods**: snake_case (e.g., `draw_text`, `handle_event`)
- **Variables**: snake_case (e.g., `player_score`, `current_system`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_PLANETS`, `DEFAULT_COLOR`)

### Documentation

All code should be documented:

- **Modules**: Include a docstring at the top of each file explaining its purpose
- **Classes**: Include a docstring explaining the class's purpose and behavior
- **Methods/Functions**: Include a docstring explaining parameters, return values, and behavior

Example:

```python
def calculate_resource_production(planet_type, planet_size):
    """
    Calculate resource production for a planet.
    
    Args:
        planet_type (PlanetType): The type of the planet
        planet_size (float): The size of the planet in arbitrary units
        
    Returns:
        dict: A dictionary mapping resource types to production amounts
    """
    # Implementation
```

### Testing

All new features should include tests:

1. Write tests before implementing the feature (Test-Driven Development)
2. Ensure tests cover both normal operation and edge cases
3. Run the full test suite before submitting a pull request

```bash
# Run the full test suite
python -m pytest

# Run tests with coverage
python -m pytest --cov=game tests/
```

See the [Testing Guide](testing.md) for more detailed information.

## Pull Request Process

1. Update the documentation to reflect any changes
2. Run all tests and ensure they pass
3. Run code style checks and fix any issues
4. Update the CHANGELOG.md file with your changes
5. Submit a pull request with a clear description of the changes

### Pull Request Template

```markdown
## Description
[Describe the changes you've made]

## Related Issue
[Link to any related issues]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Checklist
- [ ] I have read the CONTRIBUTING.md document
- [ ] My code follows the code style of this project
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass
- [ ] I have updated the documentation accordingly
- [ ] I have updated the CHANGELOG.md file
```

## Branching Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/***: New features
- **bugfix/***: Bug fixes

## Commit Messages

Write clear, descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add planet resource visualization

- Add resource icons for each resource type
- Implement resource bar display
- Add tooltips for resource information

Fixes #123
```

## Code Review Process

All submissions require review:

1. Maintainers will review your pull request
2. Feedback may be given for necessary changes
3. Once approved, your changes will be merged

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
