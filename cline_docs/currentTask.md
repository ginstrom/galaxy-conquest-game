## Current Objective
Add test coverage for game.config module

## Context
The game.config module handles loading and applying configuration settings from TOML files and command-line arguments. Currently, it lacks proper test coverage.

## Approaches Tried

### Attempt 1: Direct Module Patching
```python
@pytest.fixture
def mock_settings():
    with patch('game.config.settings', create=True) as mock_settings:
        yield mock_settings
```
- **Issue**: Failed because the settings module is imported in config.py using relative import `from . import settings`
- **Error**: AttributeError: module 'game.config' does not have the attribute 'settings'
- **Lesson**: Need to patch where module is used, not where it's defined

### Attempt 2: Root Module Patching
```python
@pytest.fixture
def mock_settings():
    with patch('settings', create=True) as mock_settings:
        yield mock_settings
```
- **Issue**: unittest.mock requires a module path with at least one dot
- **Error**: TypeError: Need a valid target to patch. You supplied: 'settings'
- **Lesson**: Cannot patch root-level modules directly with unittest.mock

### Attempt 3: Command-line Argument Handling
- Modified config.py to accept args parameter in load_config:
```python
def load_config(default_config_path='config.toml', args=None):
    # ...
    args = parser.parse_args(args)
```
- Updated test calls to pass empty args list
- **Result**: Fixed argument parsing issues but didn't solve settings mocking problem
- **Lesson**: Need to handle both module mocking and argument parsing

### Attempt 4: sys.modules with Encoded Bytes
```python
mock_file = mock_open()
mock_file.return_value.read.return_value = SAMPLE_CONFIG.encode('utf-8')
```
- **Issue**: TOML parser expects strings, not bytes
- **Error**: Warning: Could not load configuration file: Expecting something like a string
- **Lesson**: Need to handle both file mocking and gettext bytes issues

## Final Solution: Combined Approach

1. Mock Settings via sys.modules:
```python
@pytest.fixture
def mock_settings():
    mock_settings = MagicMock()
    # Set default values...
    original_settings = sys.modules.get('settings', None)
    sys.modules['settings'] = mock_settings
    yield mock_settings
    # Restore original...
```

2. Mock gettext to Handle Bytes Issues:
```python
@pytest.fixture(autouse=True)
def mock_gettext():
    """Mock gettext to avoid bytes issues with mock_open."""
    with patch('gettext.find'), \
         patch('gettext.translation'), \
         patch('gettext.gettext', side_effect=lambda x: x):
        yield
```

3. Use String Content with mock_open:
```python
mock_file = mock_open(read_data=SAMPLE_CONFIG)
```

### Benefits of Final Solution:
1. Properly mocks settings module at import level
2. Handles both absolute and relative imports
3. Maintains test isolation with proper cleanup
4. Avoids bytes/string conversion issues
5. Supports all test scenarios:
   - Default configuration
   - TOML file loading
   - Command-line overrides
   - Invalid configuration handling
   - Partial configuration

## Results
- All 7 test cases passing:
  - test_load_config_defaults
  - test_load_config_from_toml
  - test_load_config_with_cli_override
  - test_apply_config
  - test_parse_arguments
  - test_load_config_invalid_toml
  - test_load_config_partial_toml
- Achieved 90% code coverage for game.config module
- Clean test isolation with no side effects
- Comprehensive testing of all configuration scenarios

## Lessons Learned
1. When mocking imports, consider where the module is used rather than where it's defined
2. sys.modules is more flexible than unittest.mock for module-level mocking
3. Mock file operations need to consider both the file system and content format
4. Fixture composition (mock_settings + mock_gettext) can solve complex testing scenarios
5. Auto-use fixtures can provide global test environment setup
