"""
automation_framework.config.driver_manager - Centralized driver creation and management.

This module uses Selenium Manager to automatically handle browser and driver
executables, simplifying the driver setup process and ensuring compatibility.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from .settings import settings 

class DriverManager:
    """
    Manages the lifecycle of the Selenium WebDriver instance using Selenium Manager.

    This class provides a centralized method to instantiate the Chrome driver
    with configured options, relying on Selenium Manager to locate or download
    the appropriate ChromeDriver executable that matches the installed Chrome/Chromium version.
    """

    @staticmethod
    def get_driver():
        """
        Creates and returns a configured Chrome WebDriver instance.

        Uses Selenium Manager to automatically find or download ChromeDriver.
        Applies settings from the global 'settings' object for user profile,
        headless mode, and anti-detection measures. Does not set a specific window size,
        allowing the browser to use its default size or size determined by the OS/desktop environment.

        Returns:
            selenium.webdriver.Chrome: The configured Chrome WebDriver instance.
        """
        chrome_options = Options()

        if settings.BROWSER_HEADLESS:
            chrome_options.add_argument("--headless=new") 

        if settings.USER_DATA_DIR and settings.PROFILE_NAME:
            chrome_options.add_argument(f"--user-data-dir={settings.USER_DATA_DIR}")
            chrome_options.add_argument(f"--profile-directory={settings.PROFILE_NAME}")

        if settings.AVOID_DETECTION:
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

        service = ChromeService() 

        driver = webdriver.Chrome(service=service, options=chrome_options)

        if settings.AVOID_DETECTION:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.implicitly_wait(settings.IMPLICIT_WAIT)
        driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)

        return driver

    @staticmethod
    def quit_driver(driver):
        """
        Safely quits the provided WebDriver instance.

        Args:
            driver (selenium.webdriver.Remote): The driver instance to quit.
        """
        if driver:
            driver.quit()

