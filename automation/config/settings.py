"""
automation_framework.config.settings - Configuration management for automation framework.

This module provides centralized configuration settings for browser automation,
including browser behavior parameters, user profile settings, and anti-detection
settings for web automation. Selenium Manager handles driver executables automatically.
"""

from pathlib import Path

class Settings:
    """
    Centralized configuration management for browser automation settings.

    This class encapsulates browser automation parameters excluding driver paths,
    which are managed automatically by Selenium Manager. It includes settings
    for user profiles, timeouts, and anti-detection flags.
    """

    USER_DATA_DIR = "/home/crealab/.config/chromium"  
    """
    Directory containing the user profile data.
    This path stores browser settings, bookmarks, history, and other user-specific
    data. Using an existing profile preserves cookies and preferences, improving
    automation reliability for sites requiring authentication or customization.
    """

    PROFILE_NAME = "Default" 
    """
    Specific profile name within the user data directory.
    Allows selection of a particular user profile when Chromium supports
    multiple profiles. 'Default' is typically used for the main user profile.
    """

    BROWSER_HEADLESS = False 
    """
    Controls whether the browser runs in headless mode.
    Headless mode runs the browser without GUI, which is faster and suitable
    for server environments. Set to True for CI/CD pipelines or when visual
    feedback isn't needed.
    """ 

    IMPLICIT_WAIT = 10
    """
    Implicit wait time in seconds for element discovery.
    The browser will wait up to this duration for elements to appear before
    throwing exceptions. Balances between responsiveness and reliability.
    """

    PAGE_LOAD_TIMEOUT = 30
    """
    Maximum time in seconds to wait for page loads.
    Prevents indefinite waits when pages fail to load completely, ensuring
    automation continues processing rather than hanging indefinitely.
    """

    AVOID_DETECTION = True
    """
    Enables browser configuration options to avoid automation detection.
    When enabled, applies various techniques to make automation less detectable
    by websites that may block or limit automated access.
    """

    @classmethod
    def validate_paths(cls):
        """
        Verify that critical configuration directories exist.

        Checks if the USER_DATA_DIR exists. If not, creates it.
        Selenium Manager handles driver paths, so we don't validate them here.
        """
        # Check if user data dir exists and create if missing
        if not Path(cls.USER_DATA_DIR).exists():
            print(f"Warning: User data directory not found: {cls.USER_DATA_DIR}")
            print("Creating directory...")
            Path(cls.USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
        else:
            print(f"User data directory confirmed: {cls.USER_DATA_DIR}")

settings = Settings()
'''
Global settings instance following singleton pattern
This ensures consistent configuration access across all application modules
'''
settings.validate_paths() 