import pyperclip, pyautogui
import time, random
from typing import Optional, Tuple

from automation_framework.utils.logger import automation_logger
from automation_framework.utils.exceptions import PyAutoGUIError

class PyautoguiHelper():
    """
    A comprehensive desktop automation helper class built around PyAutoGUI functionality.

    This class provides a high-level interface for desktop automation tasks including
    mouse operations, keyboard interactions, image recognition, and human-like typing
    simulations. It encapsulates PyAutoGUI's core functionality with enhanced error
    handling, logging, and retry mechanisms to create robust automation workflows.

    The helper includes configurable settings for confidence thresholds in image
    recognition, timing delays between operations, and fail-safe mechanisms to prevent
    runaway automation scripts. All operations are logged through the integrated
    automation logger for debugging and monitoring purposes.

    Key features include:
    - Mouse operations: precise clicking, dragging, and coordinate-based movements
    - Keyboard operations: shortcut execution, multiple key presses, and human-like typing
    - Image recognition: screen element detection with retry logic and confidence matching
    - Configuration management: adjustable sensitivity, timing, and safety settings

    The class follows a consistent error handling pattern using custom exception types
    and provides detailed logging for all operations to facilitate debugging and
    troubleshooting in automated environments.

    Args:
        default_confidence (float, optional): Default confidence level for image recognition
                                            operations (0.0 to 1.0). Higher values require
                                            closer matches. Defaults to 0.8.
        default_delay (float, optional): Default delay between operations in seconds.
                                       Provides timing control for smoother automation.
                                       Defaults to 1.0 second.
        fail_safe (bool, optional): Enable PyAutoGUI's built-in fail-safe mechanism.
                                  When enabled, moving the mouse to the upper-left
                                  corner of the screen will abort running scripts.
                                  Defaults to False for uninterrupted automation.
        context (str, optional): A descriptive string indicating the origin of the helper
                               instance (e.g., 'App: Obsidian, Page: FilesPage').
                               Used for enhanced logging and debug capture to identify
                               where operations originate. Defaults to None.

    Example:
        >>> # Initialize with default settings
        >>> helper = PyautoguiHelper()
        >>> # Initialize with custom configuration
        >>> helper = PyautoguiHelper(
        ...     default_confidence=0.9,
        ...     default_delay=0.5,
        ...     fail_safe=True
        ... )
        >>> # Use for desktop automation tasks
        >>> helper.click_and_wait(offset_x=100, offset_y=200)
        >>> helper.execute_keyboard_shortcut(['ctrl', 'c'])
        >>> location = helper.locate_image_on_screen("./assets/button.png")
    """

    def __init__(
        self, 
        default_confidence: float = 0.8,
        default_delay: float = 1.0,
        fail_safe: bool = False,
        context: str = None
    ):
        """
        Initialize PyAutoGUI helper with configuration and safety settings.

        Args:
            default_confidence (float): Default confidence level for image recognition (0.0 to 1.0)
            default_delay (float): Default delay between operations in seconds
            fail_safe (bool): Enable PyAutoGUI's fail-safe (move mouse to corner to abort)
            context (str, optional): A descriptive string indicating the origin of the helper
                                   instance (e.g., 'App: Obsidian, Page: FilesPage').
                                   Used for enhanced logging and debug capture. Defaults to None.
        """
        self.default_confidence = default_confidence
        self.default_delay = default_delay
        self.context = context

        # Set up PyAutoGUI configurations
        pyautogui.FAILSAFE = fail_safe

        automation_logger.info(
            f"PyautoguiHelper initialized with confidence={default_confidence}, delay={default_delay}s",
            extra={"context": context}
        )

    def click_and_wait(
        self,
        offset_x: int = 0,
        offset_y: int = 0,
        how_many_clicks: int = 1,
        wait_after_click: Optional[float] = None,
        use_right_click: bool = False  
    ):
        """
        Perform mouse click at specified screen coordinates and wait for a specified duration.

        This method provides precise coordinate-based mouse interaction using PyAutoGUI, allowing
        for both single and multiple clicks at exact screen positions. It includes built-in
        waiting functionality and comprehensive error handling for reliable desktop automation
        operations. The method supports both left and right mouse clicks, making it suitable
        for various interaction scenarios including context menus, drag operations, and
        standard button interactions.

        The implementation includes safety intervals between clicks and smooth movement
        duration to simulate natural user behavior and avoid triggering anti-automation
        detection mechanisms. Error handling ensures that click failures are properly
        logged and converted to application-specific exceptions.

        Args:
            offset_x (int, optional): X-coordinate on the screen where the click should occur.
                                    Represents the horizontal position from the left edge of
                                    the screen in pixels. Defaults to 0 (leftmost edge).
            offset_y (int, optional): Y-coordinate on the screen where the click should occur.
                                    Represents the vertical position from the top edge of
                                    the screen in pixels. Defaults to 0 (topmost edge).
            how_many_clicks (int, optional): Number of consecutive clicks to perform at the
                                          specified coordinates. Use 1 for single click,
                                          2 for double-click, etc. Defaults to 1.
            wait_after_click (Optional[float], optional): Time in seconds to wait after
                                                        performing the click operation.
                                                        If None (default), uses the
                                                        class's default_delay value set
                                                        during initialization.
            use_right_click (bool, optional): When True, performs a right mouse button click
                                            which typically opens context menus. When False
                                            (default), performs left mouse button click
                                            for standard interactions.

        Example:
            >>> helper = PyautoguiHelper()
            >>> # Single left click at coordinates (100, 200)
            >>> helper.click_and_wait(offset_x=100, offset_y=200)
            >>> 
            >>> # Double left click at coordinates with custom wait
            >>> helper.click_and_wait(
            ...     offset_x=300, 
            ...     offset_y=400, 
            ...     how_many_clicks=2, 
            ...     wait_after_click=1.5
            ... )
            >>> # Right click at coordinates
            >>> helper.click_and_wait(
            ...     offset_x=500, 
            ...     offset_y=600, 
            ...     use_right_click=True
            ... )
        """
        wait_time = wait_after_click if wait_after_click is not None else self.default_delay

        try:
            if use_right_click:
                pyautogui.rightClick(
                    x=offset_x,
                    y=offset_y,
                    interval=0.1,
                    duration=0.5
                )
            else:
                pyautogui.click(
                    x=offset_x,
                    y=offset_y,
                    clicks=how_many_clicks,
                    interval=0.1,
                    duration=0.5,
                )

            automation_logger.info(
                message=f'Click realized at position, x={offset_x}, y={offset_y}',
                extra={
                    'click_duration': 0.5,
                    'clicks_performed': how_many_clicks,
                    'use_right_click': use_right_click,
                    'wait_after_click': wait_time 
                }
            )
        except Exception as e:
            error_msg = f'Failed to click on the element at position x={offset_x}, y={offset_y}'
            automation_logger.error(
                message=error_msg, 
                extra={
                    'clicks_requested': how_many_clicks,
                    'use_right_click': use_right_click,
                    'wait_after_click': wait_time 
                }
            )
            raise PyAutoGUIError(
                operation='click',
                target=f'x={offset_x}, y={offset_y}',
                reason=''
            ) from e

        time.sleep(wait_time)

    def drag_object_to_position(
        self,
        x_coordinate: int,
        y_coordinate: int,
        movement_duration: float = 1.0,
        post_drag_pause: Optional[float] = None
    ) -> None:
        """
        Performs a mouse drag operation from current mouse position to specified screen coordinates.

        This method executes a complete drag-and-drop operation by pressing and holding the mouse button
        at the current cursor position, smoothly moving the cursor to the target coordinates, and
        releasing the mouse button to complete the drop action. The method is particularly useful for
        file operations, UI element manipulation, slider controls, and any scenario requiring precise
        mouse movement with dragging functionality.

        The implementation includes smooth movement with configurable duration and automatic mouse
        button state management to ensure reliable drag operations. It also provides comprehensive
        error handling to maintain proper mouse state even when operations fail.

        ⚠️ Important: Ensure an object is already selected or under the cursor before calling this method.

        Args:
            x_coordinate (int): Target X coordinate on the screen for the drag destination.
                                Represents the horizontal position from the left edge of the screen
                                in pixels. Must be a positive integer value.
            y_coordinate (int): Target Y coordinate on the screen for the drag destination.
                                Represents the vertical position from the top edge of the screen
                                in pixels. Must be a positive integer value.
            movement_duration (float, optional): Time in seconds for the smooth movement from
                                            current position to target position. Controls
                                            the speed of the drag operation to simulate
                                            natural user behavior. Defaults to 1.0 second.
            post_drag_pause (Optional[float], optional): Time in seconds to wait after
                                                    completing the drag operation before
                                                    continuing. Allows time for the target
                                                    application to process the drop action.
                                                    If None (default), uses the class's
                                                    default_delay value set during initialization.

        Raises:
            ValueError: When coordinates are not valid integers or contain negative values.
            PyautoguiOperationError: When pyautogui fails during the drag operation due to
                                system limitations, mouse state issues, or application
                                interference. The exception includes detailed context
                                about the operation and failure reason.

        Example:
            >>> helper = PyautoguiHelper()
            >>> # Drag from current mouse position to coordinates (300, 400) with default timing
            >>> helper.drag_mouse_to_position(300, 400)
            >>> # Drag with custom movement speed and longer pause
            >>> helper.drag_mouse_to_position(
            ...     x_coordinate=500,
            ...     y_coordinate=600,
            ...     movement_duration=2.0,
            ...     post_drag_pause=1.5
            ... )
            >>> # Drag file to folder with fast movement
            >>> helper.drag_mouse_to_position(100, 200, movement_duration=0.5)
        """
        if not isinstance(x_coordinate, int) or not isinstance(y_coordinate, int):
            raise ValueError("Target coordinates (x_coordinate, y_coordinate) must be integers.")

        wait_time = post_drag_pause if post_drag_pause is not None else self.default_delay

        try:
            pyautogui.mouseDown()
            
            pyautogui.moveTo(x_coordinate, y_coordinate, duration=movement_duration)
            
            pyautogui.mouseUp()
            
            time.sleep(wait_time)

            automation_logger.info(
                message=f'Drag operation completed successfully to position ({x_coordinate}, {y_coordinate})',
                extra={
                    'target_position': (x_coordinate, y_coordinate),
                    'movement_duration': movement_duration,
                    'post_drag_pause': wait_time
                }
            )

        except Exception as e:
            pyautogui.mouseUp() 
            error_msg = f"Failed to drag object to position ({x_coordinate}, {y_coordinate})"
            automation_logger.error(
                message=error_msg,
                extra={
                    'target_position': (x_coordinate, y_coordinate),
                    'movement_duration': movement_duration,
                    'post_drag_pause': wait_time,
                    'error_details': str(e)
                }
            )
            raise PyAutoGUIError(
                operation='drag_mouse_to_position',
                target=f'position ({x_coordinate}, {y_coordinate})',
                reason=f"Drag operation failed: {str(e)}"
            ) from e

    def execute_keyboard_shortcut(
        self,
        keys: list,
        post_execution_delay: Optional[float] = None
    ) -> None:
        """
        Execute a keyboard shortcut by simulating simultaneous key presses with configurable post-execution delay.

        This method provides a reliable way to send keyboard shortcuts to the active application
        using PyAutoGUI's hotkey functionality. It's particularly useful for triggering
        common application functions like copy/paste (Ctrl+C, Ctrl+V), switching windows
        (Alt+Tab), saving documents (Ctrl+S), or any other keyboard shortcut that would
        normally be used during manual operation.

        The method handles key normalization by converting all inputs to lowercase for
        consistency, and includes built-in timing intervals to ensure proper key sequence
        execution. It also provides comprehensive error handling and logging for debugging
        purposes when shortcuts fail to execute properly.

        Args:
            keys (list): A list of keys that make up the keyboard shortcut.
                Each element should be a valid PyAutoGUI key name such as
                'ctrl', 'shift', 'alt', 'cmd', 'win', or specific letters.
                Example: ['ctrl', 'c'] for copy, ['alt', 'tab'] for window switching,
                ['ctrl', 'shift', 'n'] for new window in many applications.
            post_execution_delay (Optional[float], optional): Time in seconds to wait after executing the shortcut.
                This delay allows the application time to process the
                keyboard input and complete the associated action.
                If None (default), uses the class's default_delay value set during initialization.

        Raises:
            PyautoguiOperationError: When the keyboard shortcut execution fails due to
                invalid key names, system limitations, or application
                state issues. The exception includes detailed context
                about the requested shortcut and failure reason.

        Example:
            >>> helper = PyautoguiHelper()
            >>> # Send Ctrl+C to copy selected text
            >>> helper.execute_keyboard_shortcut(['ctrl', 'c'])
            >>> # Send Alt+Tab to switch windows
            >>> helper.execute_keyboard_shortcut(['alt', 'tab'])
            >>> # Send Ctrl+Shift+N for new window with longer delay
            >>> helper.execute_keyboard_shortcut(['ctrl', 'shift', 'n'], post_execution_delay=3)
            >>> # Send Command+Space for Spotlight search on Mac
            >>> helper.execute_keyboard_shortcut(['command', 'space'])
        """
        wait_time = post_execution_delay if post_execution_delay is not None else self.default_delay
        try:
            normalized_keys = [key.lower() for key in keys]

            pyautogui.hotkey(*normalized_keys, interval=0.1)
            time.sleep(wait_time)

            automation_logger.info(
                message=f'Shortcut executed successfully: {keys}',
                extra={
                    'keys_executed': keys,
                    'normalized_keys': normalized_keys,
                    'post_execution_delay': wait_time
                }
            )

        except Exception as e:
            error_msg = f"Failed to execute shortcut: {keys}"
            automation_logger.error(
                message=error_msg,
                extra={
                    'requested_keys': keys,
                    'normalized_keys': [key.lower() for key in keys],
                    'post_execution_delay': wait_time,
                    'error_details': str(e)
                }
            )
            raise PyAutoGUIError(
                operation='execute_keyboard_shortcut',
                target=str(keys),
                reason=f"Shortcut execution failed: {str(e)}"
            ) from e

    def human_like_typing(
        self, 
        text: str, 
        min_delay: float = 0.03, 
        max_delay: float = 0.08,
        additional_special_chars: Optional[list] = None
    ):
        """
        Type text with random delays to simulate natural human typing patterns with special character handling.

        This method provides realistic text input simulation by typing each character individually
        with randomized timing delays that mimic human typing variations. It intelligently handles
        special characters that may not be properly processed through standard keyboard input
        by using clipboard operations for reliable character insertion. The method ensures
        smooth, natural-looking text entry that avoids the mechanical speed of automated typing.

        The implementation differentiates between regular characters that can be typed directly
        and special characters that require clipboard-based input to ensure proper character
        encoding and handling across different applications and input methods.

        Args:
            text (str): The complete text string to be typed character by character.
                       Supports alphanumeric characters, punctuation, and special characters.
                       Example: "Hello World! This costs $25.99"
            min_delay (float, optional): Minimum delay in seconds between keystrokes.
                                       Controls the fastest possible typing speed to simulate
                                       quick typists. Lower values create faster typing.
                                       Defaults to 0.03 seconds (30 milliseconds).
            max_delay (float, optional): Maximum delay in seconds between keystrokes.
                                       Controls the slowest possible typing speed to simulate
                                       deliberate typists. Higher values create slower typing.
                                       Defaults to 0.08 seconds (80 milliseconds).
            additional_special_chars (list, optional): Additional characters to treat as special
                                                    that should be handled via clipboard operations.
                                                    Use this for locale-specific characters or
                                                    symbols that don't register properly with
                                                    standard keyboard input. Example: ['£', '€', '¥'].
                                                    Defaults to None.

        Example:
            >>> helper = PyautoguiHelper()
            >>> # Type with default timing and special character handling
            >>> helper.human_like_typing("Hello $world@ how are you?")
            >>> 
            >>> # Type with custom timing for slower appearance
            >>> helper.human_like_typing(
            ...     "Important message", 
            ...     min_delay=0.1, 
            ...     max_delay=0.3
            ... )
            >>> # Include additional special characters for locale-specific input
            >>> helper.human_like_typing(
            ...     "Price: 100€", 
            ...     additional_special_chars=['€', '£', '¥']
            ... )
        """
        base_special_chars = {
            '$', '&', '@', "'", '"', '<', '>', '|', '\\', '/', '•', '-', '-', "'"
            '*', '?', '!', '#', '%', '^', '+', '=', '~', '`',
            'á', 'à', 'â', 'ã', 'é', 'è', 'ê', 'í', 'ì', 'î', 'ó', 
            'ò', 'ô', 'õ', 'ú', 'ù', 'û', 'ç', 'ñ', 'Á', 'À', 'Â', 
            'Ã', 'É', 'È', 'Ê', 'Í', 'Ì', 'Î', 'Ó', 'Ò', 'Ô', 'Õ', 'Ú', 'Ù', 'Û', 'Ç', 'Ñ'
        }

        if additional_special_chars:
            base_special_chars.update(additional_special_chars)

        try:
            for char in text:
                if char in base_special_chars:
                    pyperclip.copy(char)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(random.uniform(min_delay, max_delay))
                else:
                    pyautogui.write(char)
                    time.sleep(random.uniform(min_delay, max_delay))

            automation_logger.info(
                message=f'Human-like typing completed successfully',
                extra={
                    'text_length': len(text),
                    'min_delay': min_delay,
                    'max_delay': max_delay,
                    'additional_special_chars_count': len(additional_special_chars) if additional_special_chars else 0
                }
            )
        except Exception as e:
            error_msg = f'Failed to perform human-like typing: {str(e)}'
            automation_logger.error(
                message=error_msg,
                extra={
                    'text_length': len(text),
                    'min_delay': min_delay,
                    'max_delay': max_delay,
                    'additional_special_chars': additional_special_chars
                }
            )
            raise PyAutoGUIError(
                operation='human_like_typing',
                target=text[:50] + '...' if len(text) > 50 else text,
                reason=str(e)
            ) from e

    def locate_image_on_screen(
        self,
        image_path: str,
        search_area: Optional[Tuple[int, int, int, int]] = None,
        max_attempts: int = 5,
        retry_interval: float = 4.0,
        match_confidence: Optional[float] = None
    ) -> Optional[Tuple[int, int]]:
        """
        Locate an image on the screen with retry logic and configurable search parameters.

        This method searches for a specified image file on the screen using image recognition,
        with the ability to retry multiple times with specified intervals. It's particularly
        useful for desktop automation scenarios where visual elements need to be identified
        and located for further interaction. The method can search the entire screen or
        focus on a specific area for improved performance and accuracy.

        The implementation includes robust error handling and logging to track the search
        process and provide debugging information when images are not found. Confidence
        threshold can be adjusted to balance between false positives and missed detections.

        Args:
            image_path (str): Path to the image file to search for on screen.
                            Should be a valid image file (PNG, JPG, BMP, etc.) that
                            represents the visual element you want to locate.
                            Example: "/path/to/button_image.png" or "./assets/menu_icon.jpg"
            search_area (Optional[Tuple[int, int, int, int]], optional): Screen area to search in,
                            defined as (x, y, width, height).
                            When None (default), searches
                            the entire screen. Use this to limit search area and improve performance.
                            Example: (100, 100, 500, 300)
            max_attempts (int, optional): Maximum number of search attempts before giving up.
                            Each attempt will be separated by the specified interval.
                            Use higher values for elements that may take time to appear.
                            Defaults to 5 attempts.
            retry_interval (float, optional): Time in seconds to wait between search attempts.
                            Allows time for dynamic content to load or appear.
                            Fractional seconds are supported for precise timing.
                            Defaults to 1.0 second.
            match_confidence (Optional[float], optional): Matching confidence threshold between 0 and 1.
                                                    Higher values require closer matches.
                                                    If None (default), uses the class's
                                                    default_confidence value set during initialization.

        Returns:
            Optional[Tuple[int, int]]: The center coordinates of the found image
            as (x, y) if located successfully. Returns None if the image
            is not found after all attempts are exhausted. The coordinates represent the
            center point of the matched image on the screen.

        Example:
            >>> helper = PyautoguiHelper()
            >>> # Find an icon anywhere on screen with default settings
            >>> icon_location = helper.locate_image_on_screen("./assets/save_icon.png")
            >>> if icon_location:
            ...     print(f"Icon found at: {icon_location}")  # e.g., (320, 240)
            ...     x, y = icon_location
            ...     # Use x, y for further actions
            >>> 
            >>> # Find image in specific area with custom retry settings
            >>> button_location = helper.locate_image_on_screen(
            ...     "./assets/submit_button.png",
            ...     search_area=(0, 0, 800, 600),  # Search in top-left quadrant
            ...     max_attempts=10,
            ...     retry_interval=0.5
            ... )
            >>> # Find image with custom confidence
            >>> logo_location = helper.locate_image_on_screen(
            ...     "./assets/company_logo.png",
            ...     match_confidence=0.9,  # Very strict matching
            ...     max_attempts=3
            ... )
        """

        effective_confidence = match_confidence if match_confidence is not None else self.default_confidence

        for attempt in range(max_attempts):
            try:
                location = pyautogui.locateCenterOnScreen(
                    image=image_path,
                    minSearchTime=10,
                    region=search_area,
                    confidence=effective_confidence
                )

                if location is not None:
                    automation_logger.info(
                        f"Image found on attempt {attempt + 1}",
                        extra={
                            "image_path": image_path,
                            "location": location,
                            "search_area": search_area,
                            "confidence_used": effective_confidence,
                            "attempts_made": attempt + 1
                        }
                    )
                    return location

                automation_logger.debug(
                    f"Attempt {attempt + 1}: Image not found",
                    extra={
                        "image_path": image_path,
                        "search_area": search_area,
                        "confidence_threshold": effective_confidence
                    }
                )
            except Exception as e:
                automation_logger.capture_pyautogui_debug(
                    operation='locate_image_on_screen',
                    target=f'Image: {image_path.basename()} / Search Area: {search_area}',
                    error=f"Image '{image_path}' not found after {max_attempts} attempts",
                    context=self.context
                )  
                automation_logger.warning(
                    f"Attempt {attempt + 1}: Error during image search - {str(e)}",
                    extra={
                        "image_path": image_path,
                        "search_area": search_area
                    }
                )

            if attempt < max_attempts - 1:
                time.sleep(retry_interval)

        error_msg = f"Image '{image_path}' not found after {max_attempts} attempts"
        automation_logger.error(
            error_msg,
            extra={
                "image_path": image_path,
                "search_area": search_area,
                "confidence_threshold": effective_confidence,
                "max_attempts": max_attempts,
                "retry_interval": retry_interval
            }
        )

        raise PyAutoGUIError(
            operation='locate_image_on_screen',
            target=image_path,
            reason=error_msg
        )

        return None  

    def press_key_multiple_times(
        self,
        key: str = 'enter',
        repetitions: int = 1,
        interval_between_presses: float = 0.1,
        post_press_delay: Optional[float] = None
    ) -> None:
        """
        Press a specific keyboard key multiple times with configurable timing parameters.

        This method provides precise control over keyboard key presses, allowing for repeated
        key presses with customizable intervals between presses and a final delay after the
        sequence completes. It's particularly useful for scenarios like confirming selections,
        navigating through lists, accepting default options, or triggering repeated actions
        that require multiple key presses.

        The method handles key normalization by converting the input to lowercase for
        consistency, and includes built-in timing intervals to ensure proper key press
        execution. It also provides comprehensive error handling and logging for debugging
        purposes when key presses fail to execute properly.

        Args:
            key (str, optional): The keyboard key to press. Should be a valid PyAutoGUI key name
                            such as 'enter', 'tab', 'space', 'backspace', 'escape', arrow keys,
                            or any letter/number key. Defaults to 'enter' for confirming actions.
            repetitions (int, optional): Number of times to press the key. Use this to repeat
                                    the same key press multiple times in sequence.
                                    Defaults to 1 press. Example: 3 means press the key 3 times.
            interval_between_presses (float, optional): Time in seconds to wait between each key press.
                                                    This interval ensures proper spacing between
                                                    consecutive key presses for reliable detection
                                                    by applications. Defaults to 0.1 seconds.
            post_press_delay (Optional[float], optional): Time in seconds to wait after all key
                                                    presses are completed. This delay allows
                                                    the application time to process all the
                                                    key presses and complete associated actions.
                                                    If None (default), uses the class's
                                                    default_delay value set during initialization.

        Raises:
            PyautoguiOperationError: When the key press execution fails due to invalid key names,
                                system limitations, or application state issues. The exception
                                includes detailed context about the requested key and failure reason.

        Example:
            >>> helper = PyautoguiHelper()
            >>> # Press Enter once (default behavior)
            >>> helper.press_key_multiple_times()
            >>> # Press Tab 5 times to navigate through form fields
            >>> helper.press_key_multiple_times(key='tab', repetitions=5)
            >>> # Press Enter 3 times with custom intervals
            >>> helper.press_key_multiple_times(
            ...     key='enter',
            ...     repetitions=3,
            ...     interval_between_presses=0.2,
            ...     post_press_delay=1.0
            ... )
            >>> # Press Escape to close dialogs repeatedly
            >>> helper.press_key_multiple_times(key='esc', repetitions=2, interval_between_presses=0.5)
            >>> # Press arrow down 10 times to scroll through a list
            >>> helper.press_key_multiple_times(key='down', repetitions=10, interval_between_presses=0.05)
        """
        wait_time = post_press_delay if post_press_delay is not None else self.default_delay
        normalized_key = key.lower()
        
        try:
            pyautogui.press(normalized_key, presses=repetitions, interval=interval_between_presses)
            time.sleep(wait_time)

            automation_logger.info(
                message=f'Key pressed successfully: {key} x {repetitions}',
                extra={
                    'key_pressed': normalized_key,
                    'repetitions': repetitions,
                    'interval_between_presses': interval_between_presses,
                    'post_press_delay': wait_time
                }
            )

        except Exception as e:
            error_msg = f"Failed to press key: {key} x {repetitions} times"
            automation_logger.error(
                message=error_msg,
                extra={
                    'requested_key': key,
                    'normalized_key': normalized_key,
                    'repetitions': repetitions,
                    'interval_between_presses': interval_between_presses,
                    'post_press_delay': wait_time,
                    'error_details': str(e)
                }
            )
            raise PyAutoGUIError(
                operation='press_key_multiple_times',
                target=f'{key} x {repetitions}',
                reason=f"Key press execution failed: {str(e)}"
            ) from e



