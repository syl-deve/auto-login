# Auto-Login Script

## Project Title and Description
This project provides an automated login solution for web services using Selenium WebDriver. It handles initial login page interactions, ADFS authentication, mobile push notification approvals, and post-login actions such as clicking specific elements on the target page.

## Features
- Automated navigation to login URL.
- Handling of initial login button clicks.
- ADFS username and password input.
- Waiting for mobile push notification approval for multi-factor authentication.
- Post-login actions, including clicking specific elements (e.g., menu items, checkboxes).
- Configuration via `config.json` for easy customization of URLs, credentials, and selectors.

## Prerequisites
- Python 3.x
- `uv` (a fast Python package installer and resolver) - if not installed, run `pip install uv`
- Google Chrome or Chromium browser installed on your system.

## Installation
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd auto-login
    ```

2.  **Create and activate a Python virtual environment using `uv`:**
    ```bash
    uv venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install required Python packages:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Configuration
1.  **Create `config.json`:** Copy `config.json.example` to `config.json`.
    ```bash
    cp config.json.example config.json
    ```

2.  **Edit `config.json`:** Open `config.json` and update the following fields with your actual login details and specific selectors:
    -   `login_url`: The initial URL of the login page.
    -   `username`: Your login username.
    -   `password`: Your login password.
    -   `selectors`: A dictionary containing CSS selectors for various elements:
        -   `initial_login_button`: Selector for the button to initiate the login process.
        -   `adfs_username_field`: Selector for the username input field on the ADFS page.
        -   `adfs_password_field`: Selector for the password input field on the ADFS page.
        -   `adfs_login_button`: Selector for the login button on the ADFS page.
        -   `post_login_target_selector`: Selector for an element to click after successful login (e.g., a menu item).
        -   `checkbox_1_selector`: Selector for the first checkbox to click after post-login action.
        -   `checkbox_2_selector`: Selector for the second checkbox to click after post-login action.
    -   `retry`: Configuration for retry attempts (currently not fully implemented, but placeholders are there).
        -   `attempts`: Number of retry attempts.
        -   `delay_seconds`: Delay between retry attempts.
    -   `target_page_url`: The expected URL after a successful login and any post-login actions.

    **Important:** Do not commit `config.json` to version control as it contains sensitive information. It is already ignored by `.gitignore`.

## Usage
1.  **Activate your virtual environment (if not already active):**
    ```bash
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

2.  **Run the script:**
    ```bash
    python main.py
    ```

3.  **Approve mobile notification:** When prompted by the script, approve the login request on your mobile device for multi-factor authentication.

## Troubleshooting
-   **`selenium.common.exceptions.TimeoutException`:** This usually means a selector is incorrect, the page structure has changed, or the element took too long to appear. Verify your selectors in `config.json` using your browser's developer tools.
-   **`selenium.common.exceptions.NoSuchElementException`:** Similar to `TimeoutException`, indicates an element could not be found. Double-check selectors.
-   **`initial_button_click_error.png`, `post_login_action_error.png`, `checkbox_1_click_error.png`, `checkbox_2_click_error.png`:** These screenshots are saved when an error occurs during the respective click actions. Review them to understand the page state at the time of failure.
-   **`config.json` not found or decode error:** Ensure `config.json` exists and is a valid JSON format.
