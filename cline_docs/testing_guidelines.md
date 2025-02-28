# Galaxy Conquest Testing Guidelines

## Core Principles

1. **Hardware Independence**: Tests run without specific hardware requirements
2. **High Coverage**: Minimum 80% code coverage across the codebase
3. **Isolation**: Components testable in isolation via dependency injection
4. **Reproducibility**: Consistent results across environments
5. **Maintainability**: Clear, modifiable, and extensible tests

## Test Types

### Unit Tests
- Test individual components in isolation
- Mock all external dependencies
- Cover normal operation and edge cases

### Integration Tests
- Verify component interactions
- Minimal mocking, focus on external dependencies
- Test end-to-end functionality

## Mock Objects

- **MockSurface**: Replaces pygame.Surface for testing drawing operations
- **MockFont**: Simulates text rendering without font initialization
- **MockGame**: Provides game context for testing components

## Dependency Injection

Components should accept dependencies through their constructor:

```python
# In production code
class PlanetView:
    def __init__(self, game, font_manager=None):
        self.game = game
        self.font_manager = font_manager or FontManager()
```

## Coverage Targets

- Overall project: 80%+
- Core game logic: 90%+
- UI components: 75%+

Generate coverage reports with:
```bash
make coverage  # Creates HTML report in htmlcov/ directory
```

## Edge Case Testing

Test all components with:
1. Default/minimal parameters
2. Boundary conditions
3. Error conditions
4. State transitions

## Test Organization

- Mirror production code structure
- Focus each test file on a single module
- Use descriptive test names

## Best Practices

1. Write tests first when adding features (TDD)
2. Keep tests simple and focused
3. Use descriptive test names
4. Add comments for complex assertions
5. Avoid test interdependence
6. Clean up resources after tests
7. Use parameterized tests for similar cases
8. Maintain test quality (tests are production code)

## Continuous Improvement

1. Regularly review coverage reports
2. Address areas with low coverage
3. Refactor tests as the codebase changes
4. Update guidelines as new best practices emerge
