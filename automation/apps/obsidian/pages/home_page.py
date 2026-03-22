import os
from typing import Optional, Tuple
from automation_framework.platforms.desktop.pyautogui_helper import PyautoguiHelper 
from automation_framework.utils.logger import automation_logger 

class HomePage(PyautoguiHelper):
    """
    Page Object for the file management area in Obsidian desktop app.
    
    This class provides methods to locate and interact with UI elements like
    'New Note' and 'New Folder' buttons using image recognition.
    """
    DEFAULT_SEARCH_AREA = (93, 43, 300, 360)
    """Default screen area (x, y, width, height) to search for buttons."""

    def __init__(
        self, 
        screenshot_folder: str, 
        default_confidence: float = 0.8, 
        default_delay: float = 2.0, 
        fail_safe: bool = False,
    ):
        """
        Initializes the FilesPage helper.

        Args:
            screenshot_folder (str): The directory path where image files
                (e.g., 'new_note_button.png') are stored for recognition.
            default_confidence (float, optional): Default confidence level for image recognition (0.0 to 1.0).
                Defaults to 0.8.
            default_delay (float, optional): Default delay between operations
                in seconds. Defaults to 1.0.
            fail_safe (bool, optional): Enable PyAutoGUI's fail-safe (move mouse to corner to abort). 
                Defaults to False.
        """
        super().__init__(default_confidence=default_confidence, default_delay=default_delay, fail_safe=fail_safe, context='App: Obsidian, Page: HomePage')
        self.screenshot_folder = screenshot_folder
        automation_logger.info(
            f"FilesPage initialized with screenshot folder: {screenshot_folder}",
            extra={"screenshot_folder": screenshot_folder}
        )

    def _find_new_note_button(self) -> Optional[Tuple[int, int]]:
        """
        Locates the 'New Note' button image on the screen within the default search area.

        Returns:
            Optional[Tuple[int, int]]: The (x, y) center coordinates if found, else None.
        """
        image_path = os.path.join(self.screenshot_folder, 'new_note_button.png')
        location = self.locate_image_on_screen(
            image_path=image_path,
            search_area=self.DEFAULT_SEARCH_AREA,
            max_attempts=1,
            retry_interval=1.0
        )
        if location:
            automation_logger.info(
                f"'New Note' button found at {location}.",
                extra={
                    "image_path": image_path,
                    "location": location,
                    "search_area": self.DEFAULT_SEARCH_AREA
                }
            )
        else:
            automation_logger.warning(
                f"Failed to find 'New Note' button image: {image_path}",
                extra={
                    "image_path": image_path,
                    "search_area": self.DEFAULT_SEARCH_AREA
                }
            )
        return location

    def _find_new_folder_button(self) -> Optional[Tuple[int, int]]:
        """
        Locates the 'New Folder' button image on the screen within the default search area.

        Returns:
            Optional[Tuple[int, int]]: The (x, y) center coordinates if found, else None.
        """
        image_path = os.path.join(self.screenshot_folder, 'new_folder_button.png')
        location = self.locate_image_on_screen(
            image_path=image_path,
            search_area=self.DEFAULT_SEARCH_AREA,
            max_attempts=1, 
            retry_interval=1.0
        )
        if location:
            automation_logger.info(
                f"'New Folder' button found at {location}.",
                extra={
                    "image_path": image_path,
                    "location": location,
                    "search_area": self.DEFAULT_SEARCH_AREA
                }
            )
        else:
            automation_logger.warning(
                f"Failed to find 'New Folder' button image: {image_path}",
                extra={
                    "image_path": image_path,
                    "search_area": self.DEFAULT_SEARCH_AREA
                }
            )
        return location

    def click_new_note(self) -> bool:
        """
        Attempts to find and click the 'New Note' button.

        Returns:
            bool: True if the button was found and clicked, False otherwise.
        """
        location = self._find_new_note_button()
        if location:
            x, y = location
            self.click_and_wait(offset_x=x, offset_y=y)
            automation_logger.info(
                "Successfully clicked 'New Note' button.",
                extra={
                    "click_coordinates": (x, y),
                    "screenshot_folder": self.screenshot_folder
                }
            )
            return True
        else:
            automation_logger.error(
                "Could not click 'New Note' button as it was not found.",
                extra={
                    "screenshot_folder": self.screenshot_folder,
                    "target_image": os.path.join(self.screenshot_folder, 'new_note_button.png'),
                    "search_area": self.DEFAULT_SEARCH_AREA
                }
            )
            return False

    def click_new_folder(self) -> bool:
        """
        Attempts to find and click the 'New Folder' button.

        Returns:
            bool: True if the button was found and clicked, False otherwise.
        """
        location = self._find_new_folder_button()
        if location:
            x, y = location
            self.click_and_wait(offset_x=x, offset_y=y)
            automation_logger.info(
                "Successfully clicked 'New Folder' button.",
                extra={
                    "click_coordinates": (x, y),
                    "screenshot_folder": self.screenshot_folder
                }
            )
            return True
        else:
            automation_logger.error(
                "Could not click 'New Folder' button as it was not found.",
                extra={
                    "screenshot_folder": self.screenshot_folder,
                    "target_image": os.path.join(self.screenshot_folder, 'new_folder_button.png'),
                    "search_area": self.DEFAULT_SEARCH_AREA
                }
            )
            return False

    def create_new_note(self, note_name: str):
        """
        Creates a new note in Obsidian by clicking the new note button, typing the name, and confirming.

        This method orchestrates the process of creating a new note within the Obsidian application.
        It first clicks the 'New Note' button using the `click_new_note` method. Then, it types
        the desired `note_name` into the filename field using `human_like_typing` for naturalistic
        input. Finally, it presses the Enter key using `press_key_multiple_times` (defaulting to one press)
        to confirm the note creation and proceed.

        Args:
            note_name (str): The desired name for the new note.
                Example: "Meeting Notes 2024-02-23", "Project Ideas".
                Special characters handled by `human_like_typing` will be processed accordingly.
        """
        #  Step 1: create new note
        self.click_new_note()

        # Step 2: set the title
        self.human_like_typing(text=note_name)
        self.press_key_multiple_times() 
