import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryLine
from pygame_gui.windows import UIConsoleWindow
from settings import DEBUG
from game.logging_config import configure_logging, get_logger
import cmd

logger = get_logger(__name__)


class ConsoleCommand(cmd.Cmd):
    """Command processor for the debug console."""
    
    intro = 'Debug Console - Type help or ? to list commands.'
    prompt = '> '
    
    def __init__(self, debug_instance):
        """
        Initialize the command processor.
        
        Args:
            debug_instance: The Debug instance this processor is attached to
        """
        super().__init__()
        self.debug = debug_instance
        self.game = debug_instance._game
    
    def do_clear(self, arg):
        """Clear the console output window."""
        self.debug._clear_console()
    
    def do_toggle(self, arg):
        """Toggle debug display overlay on/off."""
        self.debug.toggle()
        self.debug._add_to_console(f"Debug display: {'ON' if self.debug.enabled else 'OFF'}")
    
    def do_test_scroll(self, arg):
        """Add multiple lines of text to test console scrolling functionality."""
        self.debug._add_to_console("Testing scrolling functionality...")
        for i in range(1, 31):
            self.debug._add_to_console(f"Test line {i} - This is a test line to demonstrate scrolling in the debug console")
        self.debug._add_to_console("Scroll test complete. You should be able to scroll up to see all lines.")
    
    def do_systems(self, arg):
        """List all star systems in the game with their indices (0-based)."""
        if not self.game or not hasattr(self.game, 'star_systems'):
            self.debug._add_to_console("Error: Game instance or star systems not available")
            return
            
        if not self.game.star_systems:
            self.debug._add_to_console("No star systems found")
            return
            
        self.debug._add_to_console("Star Systems:")
        for i, system in enumerate(self.game.star_systems):
            self.debug._add_to_console(f"{i}. {system.name}")
    
    def default(self, line):
        """Handle unknown commands."""
        self.debug._add_to_console(f"Unknown command: {line}")
    
    def emptyline(self):
        """Do nothing on empty line."""
        pass
    
    def postcmd(self, stop, line):
        """After command processing."""
        return False  # Never stop the command loop


class Debug:
    def __init__(self, game=None, ui_manager=None):
        self._game = game
        self._font = None
        self._debug_info = []
        self._margin = 10
        self._line_height = 25
        self._bg_padding = 5
        self._enabled = DEBUG  # Initialize with settings value
        self._console_visible = False
        self._ui_manager = ui_manager
        self._console_initialized = False
        self._console_height = 200  # Height of the console area
        self._console_window = None
        self._command_processor = ConsoleCommand(self)
        self._initialize_console()
    
    def set_ui_manager(self, ui_manager):
        """Set the UI manager for the debug console."""
        self._ui_manager = ui_manager
        self._initialize_console()
    
    def _initialize_console(self):
        """Initialize the console UI elements."""
        if self._ui_manager and not self._console_initialized:
            screen = pygame.display.get_surface()
            screen_width = screen.get_width()
            
            # Calculate available width (excluding info panel)
            # Assuming info panel is approximately 300px wide on the right
            available_width = screen_width - 300
            
            # Create a console window instead of separate elements
            self._console_window = UIConsoleWindow(
                rect=pygame.Rect((0, 0), (available_width, self._console_height)),
                manager=self._ui_manager,
                window_title='Debug Console',
                visible=False
            )
            
            # Initialize with welcome message (plain text, no HTML)
            self._console_window.add_output_line_to_log("Debug Console - Type 'help' for available commands")
            
            logger.debug("Debug console initialized")
            self._console_initialized = True
    
    def toggle(self):
        """Toggle debug display on/off."""
        self._enabled = not self._enabled
        if not self._enabled:
            self.clear()
            self.hide_console()
    
    @property
    def enabled(self):
        """Get current debug state."""
        return self._enabled
    
    def _ensure_font_initialized(self):
        """Ensure the font is initialized when needed."""
        if self._font is None and self._enabled:
            self._font = pygame.font.Font(None, 24)
    
    def clear(self):
        """Clear all debug information for the current frame."""
        if self._enabled:
            self._debug_info.clear()
    
    def add(self, info, color=(255, 255, 255), pos=None):
        """
        Add debug information to be displayed.
        
        Args:
            info: String or value to display
            color: RGB tuple for text color (default: white)
            pos: Optional (x, y) position. If None, will be added to list
        """
        if self._enabled:
            self._debug_info.append({
                'text': str(info),
                'color': color,
                'pos': pos
            })
    
    def toggle_console(self):
        """Toggle the debug console visibility."""
        if not self._console_initialized and self._ui_manager:
            self._initialize_console()
            
        if self._console_initialized:
            if self._console_visible:
                self.hide_console()
            else:
                self.show_console()
    
    def show_console(self):
        """Show the debug console."""
        if self._console_initialized:
            self._console_visible = True
            self._console_window.show()
            
            # Explicitly try to focus the input text entry
            if hasattr(self._console_window, 'focus'):
                self._console_window.focus()
            
            # Find and focus the input text entry component inside the console window
            if hasattr(self._console_window, 'command_entry'):
                self._console_window.command_entry.focus()
                
            logger.debug("Debug console shown")
    
    def hide_console(self):
        """Hide the debug console."""
        if self._console_initialized:
            self._console_visible = False
            self._console_window.hide()
            logger.debug("Debug console hidden")

    def handle_event(self, event):
        """
        Handle events for the debug console.
        
        Args:
            event: Pygame event to handle
        
        Returns:
            bool: True if the event was handled by the console, False otherwise
        """
        if not self._console_initialized:
            return False
            
        # Toggle console with backtick key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                if not self._console_visible:
                    self.show_console()
                else:
                    self.hide_console()
                return True
            elif event.key == pygame.K_ESCAPE and self._console_visible:
                self.hide_console()
                return True # Consume the event
        
        # Handle window events first as the console might need to be brought to front
        if event.type == pygame.MOUSEBUTTONDOWN and self._console_visible:
            # Click inside console window should focus it
            if hasattr(self._console_window, 'get_abs_rect') and self._console_window.get_abs_rect().collidepoint(event.pos):
                if hasattr(self._console_window, 'command_entry'):
                    self._console_window.command_entry.focus()
        
        # Let the console window handle its own events
        if self._console_visible and hasattr(self._console_window, 'process_event'):
            # Check if console handled the event
            if self._console_window.process_event(event):
                # Look for UI text entry finished events that might come from the console
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    # Try to find the text that was entered
                    text = None
                    if hasattr(event, 'text'):
                        text = event.text
                    elif hasattr(event, 'ui_element') and hasattr(event.ui_element, 'get_text'):
                        text = event.ui_element.get_text()
                    
                    if text:
                        self._process_command(text)
                return True
            
        return False
    
    def _process_command(self, command):
        """
        Process a command entered in the console.
        
        Args:
            command: Command string to process
        """
        command = command.lstrip('`').strip()
        if not command:
            return
            
        # Add command to output
        self._add_to_console(f"> {command}")
        
        # Use the command processor to handle the command
        self._command_processor.onecmd(command)
    
    def _add_to_console(self, text):
        """
        Add text to the console output.
        
        Args:
            text: Text to add to the console
        """
        if self._console_initialized:
            # Remove any HTML tags for plain text display
            clean_text = text
            self._console_window.add_output_line_to_log(clean_text)
    
    def _clear_console(self):
        """Clear the console output."""
        if self._console_initialized:
            # UIConsoleWindow doesn't have a direct clear method, but we can
            # create a new console with the same parameters
            visible = self._console_visible
            position = self._console_window.get_relative_rect()
            
            # Kill the old console
            self._console_window.kill()
            
            # Create a new one
            self._console_window = UIConsoleWindow(
                rect=position,
                manager=self._ui_manager,
                window_title='Debug Console',
                visible=visible
            )
            
            # Initialize with welcome message (plain text)
            self._console_window.add_output_line_to_log("Debug Console - Type 'help' for available commands")
            
            # Focus the input if the console is visible
            if visible and hasattr(self._console_window, 'command_entry'):
                self._console_window.command_entry.focus()
    
    def draw(self, surface):
        """
        Draw all debug information to the surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self._enabled or self._console_visible:
            return
            
        self._ensure_font_initialized()
        y = self._margin
        
        for info in self._debug_info:
            text_surface = self._font.render(info['text'], True, info['color'])
            text_rect = text_surface.get_rect()
            
            if info['pos'] is None:
                # Default position on left side
                text_rect.topleft = (self._margin, y)
                y += self._line_height
            else:
                # Custom position
                text_rect.topleft = info['pos']
            
            # Draw background rectangle
            bg_rect = text_rect.inflate(self._bg_padding * 2, self._bg_padding * 2)
            pygame.draw.rect(surface, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(surface, (128, 128, 128), bg_rect, 1)
            
            # Draw text
            surface.blit(text_surface, text_rect)

# Module-level functions that use the game's debug instance

def set_ui_manager(ui_manager):
    """
    Set the UI manager for the debug console.
    
    Args:
        ui_manager: pygame_gui UIManager instance
    """
    # This function is no longer needed as the UI manager is passed directly to the Debug instance
    # It's kept for backward compatibility
    logger.warning("set_ui_manager is deprecated. Pass UI manager to Game's debug instance directly.")

def handle_debug_event(event):
    """
    Handle events for the debug console.
    
    Args:
        event: Pygame event to handle
        
    Returns:
        bool: True if the event was handled by the console, False otherwise
    """
    # This function should be called with game.debug.handle_event(event) instead
    logger.error("handle_debug_event called directly. Use game.debug.handle_event(event) instead.")
    return False

def toggle_console():
    """Toggle the debug console visibility."""
    # This function should be called with game.debug.toggle_console() instead
    logger.error("toggle_console called directly. Use game.debug.toggle_console() instead.")

def debug(info, color=(255, 255, 255), pos=None):
    """
    Add debug information to be displayed on screen.
    If debug is disabled, this function becomes a no-op.
    
    Args:
        info: String or value to display
        color: RGB tuple for text color (default: white)
        pos: Optional (x, y) position. If None, will be added to list
    """
    # This function should be called with game.debug.add(info, color, pos) instead
    logger.error("debug called directly. Use game.debug.add(info, color, pos) instead.")

def clear_debug():
    """Clear all debug information for the current frame."""
    # This function should be called with game.debug.clear() instead
    logger.error("clear_debug called directly. Use game.debug.clear() instead.")

def draw_debug(surface):
    """
    Draw all debug information to the surface.
    If debug is disabled, this function becomes a no-op.
    
    Args:
        surface: Pygame surface to draw on
    """
    # This function should be called with game.debug.draw(surface) instead
    logger.error("draw_debug called directly. Use game.debug.draw(surface) instead.")

def toggle_debug():
    """Toggle debug display on/off."""
    # This function should be called with game.debug.toggle() instead
    logger.error("toggle_debug called directly. Use game.debug.toggle() instead.")

def is_debug_enabled():
    """Get current debug state."""
    # This function should be called with game.debug.enabled instead
    logger.error("is_debug_enabled called directly. Use game.debug.enabled instead.")
    return False