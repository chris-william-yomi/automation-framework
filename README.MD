# Automation Framework

A practical Python automation framework for web and desktop tasks, built around the **Page Object Model (POM)**. It provides pre-built helper methods to reduce boilerplate, improve maintainability, and standardize error handling — without over-engineering.

> ✅ You define elements once.  
> ✅ You reuse them in page methods.  
> ✅ You compose workflows from those methods.  
> ✅ The framework handles waits, retries, logging, and debugging.

## 📁 Project Structure

```
src/
└── automation_framework/
    ├── config/
    │   └── settings.py            # ← MUST be configured first (paths to Chrome/ChromeDriver)
    ├── platforms/
    │   ├── web/
    │   │   └── selenium_helper.py  # Inherited by page classes
    │   └── desktop/
    │       └── pyautogui_helper.py # Inherited by desktop page classes
    ├── utils/                     # Logging, exceptions, screenshots, debug helpers
    └── app/
        └── your_project/
            ├── pages/             # Page Object classes (inherit from helpers)
            ├── workflow/          # Atomic user flows (e.g., "login", "upload_photo")
            └── data/              # Optional: test data, credentials
```

---

## 🔧 Setup (Mandatory)

1. **Edit `src/automation_framework/config/settings.py`**  
   Update these paths to match your system:
   ```python
   USER_DATA_DIR = "/your/chrome/profile/dir"
   PROFILE_NAME = "Default" 
   ```
   -> only if you have a profile if not you can just assert None
   ```python
   USER_DATA_DIR = None
   PROFILE_NAME = None
   ```

2. **Install the framework:**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install the package and its dependencies
   pip install -e .
   ```

---

## 🧱 How to Build a Page (POM Best Practice)

Your page class **inherits from `SeleniumHelper`**, so you can call its methods directly — including element locators — and store the *resulting WebElement* as an instance variable.

### Example: `pages/login_page.py`

```python
from selenium.webdriver.common.by import By
from automation_framework.platforms.web.selenium_helper import SeleniumHelper

class LoginPage(SeleniumHelper):
    """
    Page Object for the login screen.
    
    Elements are resolved at initialization (lazy or eager depending on strategy),
    ensuring they're ready when used in methods.
    """

    def __init__(self, driver):
        super().__init__(driver)
        # 🔹 Define elements using helper methods — returns WebElements (not locators)
        self.username_field = self.find_by_aria_label(
            aria_label="username",
            match_type="exact",
            tag="input",
            condition="visible"
        )
        self.password_field = self.find_by_aria_label(
            aria_label="password",
            match_type="exact",
            tag="input",
            condition="visible"
        )
        self.login_button = self.find_by_data_test_id(
            "login-button",
            condition="clickable"
        )

    def enter_credentials(self, username: str, password: str) -> None:
        """
        Fill username and password fields.
        
        Uses the pre-located WebElements stored in self.*.
        """
        self.type_text(self.username_field, username)
        self.type_text(self.password_field, password)

    def click_login(self) -> None:
        """
        Click the login button.
        """
        self.click_element(self.login_button)

    def login(self, username: str, password: str) -> None:
        """
        Full login flow: enter credentials + click login.
        """
        self.enter_credentials(username, password)
        self.click_login()
```

✅ **Why this is correct POM**:
- Elements are located *once* during `__init__` (or lazily if you prefer — but this version is eager for clarity).
- Methods operate on *WebElements*, not locators — no repeated locating.
- All helper methods (`type_text`, `click_element`, etc.) are inherited and available.
- If selectors change, update only the `find_*` call — not every method that uses the element.

> 💡 For desktop automation, inherit from `PyautoguiHelper` and use methods like `locate_image_on_screen()`, `click_and_wait()`, etc., in the same pattern.

---

## 📋 Workflow Files (Simple & Composable)

A workflow file is just a Python script that orchestrates page methods:

```python
# workflow/login_test.py
from automation_framework.config.driver_manager import DriverManager
from automation_framework.app.your_project.pages.login_page import LoginPage

def main():
    driver = DriverManager.get_driver()
    try:
        page = LoginPage(driver)
        page.login("test@example.com", "secret123")
        # → next steps: verify dashboard, etc.
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
```

No magic. No frameworks inside frameworks. Just functions calling page methods.

---

## 🛠️ Key Helper Methods (Inherited)

| Method | Purpose |
|--------|---------|
| `find_by_data_test_id(id)` | ✅ Best practice for test automation |
| `find_by_aria_label(aria_label, ...)` | ✅ Accessible, semantic, stable |
| `click_element(locator_or_element)` | Safe click with wait + error capture |
| `type_text(locator_or_element, text)` | Type with auto-clear and wait |
| `wait_for_element_visible(locator)` | Explicit wait (for debugging or complex flows) |
| `locate_image_on_screen(path)` | Desktop: find UI elements by image |
| `human_like_typing(text)` | Desktop: realistic typing with random delays |

All methods log failures with screenshots, page source, and context via `automation_logger`.

---

## 🤝 Note on Development

This framework was written with the assistance of AI tools. I'm transparent about this because:
- It's honest,
- It reflects how modern development often works (AI as copilot),
- And it prevents misunderstandings later.

The AI helped implement the technical patterns correctly (POM, exception hierarchy, Selenium/PyAutoGUI integration), while the architecture, requirements, and oversight came from the developer. Credit is shared where due.

You're not "using AI code" — you're using a tool-assisted, well-structured framework that saves time and reduces errors.

---

## ✅ Requirements

- Python 3.10+
- Chromium/Chrome (v115+ recommended)
- ChromeDriver (matching browser version)

Dependencies are automatically installed when you run `pip install -e .`

---

This is not a miracle framework. It's a pragmatic one — designed to get your automations running quickly, reliably, and maintainably.  

— Built with care, and full transparency.