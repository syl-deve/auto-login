import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config():
    """
    Loads the configuration from config.json.
    """
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Error: config.json not found. Please ensure the file exists.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Could not decode config.json. Please check its format.")
        sys.exit(1)

def initialize_driver():
    """
    Initializes and returns a Selenium Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment for headless mode
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def perform_login(driver, config):
    """
    Performs the login sequence.
    """
    login_url = config.get("login_url")
    if not login_url:
        print("Error: login_url not found in config.json")
        return False

    print(f"Navigating to initial login page: {login_url}")
    driver.get(login_url)

    # Wait for the page to be fully loaded
    print("Waiting for page to load completely...")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    import time
    time.sleep(2) # Give SPA more time to render

    # Click the initial login button
    initial_login_button_selector = config['selectors'].get('initial_login_button')
    if not initial_login_button_selector:
        print("Error: initial_login_button selector not found in config.json")
        return False

    print(f"Clicking initial login button: {initial_login_button_selector}")
    initial_button = None
    try:
        # Wait for the element to be present in DOM
        initial_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, initial_login_button_selector))
        )
        
        # Scroll into view if not already
        driver.execute_script("arguments[0].scrollIntoView(true);", initial_button)
        
        # Always attempt JavaScript click
        print("Attempting JavaScript click for initial login button...")
        driver.execute_script("arguments[0].click();", initial_button)

    except Exception as e:
        print(f"Error clicking initial login button: {e}")
        print(f"Current URL: {driver.current_url}")
        driver.save_screenshot("initial_button_click_error.png")
        print("Screenshot saved to initial_button_click_error.png")
        return False

    # Wait for ADFS username field to appear (indicating ADFS page loaded)
    adfs_username_field_selector = config['selectors'].get('adfs_username_field')
    if not adfs_username_field_selector:
        print("Error: adfs_username_field selector not found in config.json")
        return False

    print(f"Waiting for ADFS username field: {adfs_username_field_selector}")
    try:
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, adfs_username_field_selector))
        )
    except Exception as e:
        print(f"Error waiting for ADFS username field: {e}")
        return False

    # Enter username and password
    password_field_selector = config['selectors'].get('adfs_password_field')
    adfs_login_button_selector = config['selectors'].get('adfs_login_button')

    if not password_field_selector or not adfs_login_button_selector:
        print("Error: ADFS password field or login button selector not found in config.json")
        return False

    print("Entering credentials...")
    username_field.send_keys(config.get('username'))
    driver.find_element(By.CSS_SELECTOR, password_field_selector).send_keys(config.get('password'))

    # Click ADFS login button
    print(f"Clicking ADFS login button: {adfs_login_button_selector}")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, adfs_login_button_selector))
        )
        login_button.click()
    except Exception as e:
        print(f"Error clicking ADFS login button: {e}")
        return False

    print("Login sequence initiated.")
    return True

def main():
    """
    Main function to run the auto-login script.
    """
    config = load_config()
    print("Configuration loaded successfully.")
    
    driver = initialize_driver()
    try:
        print("WebDriver initialized.")
        if perform_login(driver, config):
            print("Login process completed. Check browser for status.")
            # Keep the browser open for a moment to verify
            import time
            time.sleep(10) # Increased sleep time to 10 seconds to verify login
        else:
            print("Login process failed.")
    finally:
        print("Closing WebDriver.")
        driver.quit()

if __name__ == "__main__":
    main()
