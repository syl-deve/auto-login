import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

    # Step 1: Navigate to the initial login page
    print(f"Navigating to initial login page: {login_url}")
    driver.get(login_url)

    # Wait for the page to be fully loaded
    print("Waiting for page to load completely...")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(2) # Give SPA more time to render for Single Page Applications

    # Step 2: Click the initial login button
    initial_login_button_selector = config['selectors'].get('initial_login_button')
    if not initial_login_button_selector:
        print("Error: initial_login_button selector not found in config.json")
        return False

    print(f"Clicking initial login button: {initial_login_button_selector}")
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

    # Step 3: Handle ADFS login (enter credentials and click login button)
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

    # Step 4: Wait for mobile push notification approval and redirection to target page
    target_page_url = config.get('target_page_url')
    if not target_page_url:
        print("Error: target_page_url not found in config.json")
        return False

    print(f"Waiting for redirection to target page: {target_page_url}")
    print("Please approve the login on your mobile device.")
    try:
        WebDriverWait(driver, 60).until(EC.url_to_be(target_page_url))
        print("Successfully redirected to target page.")

        # Add a delay to ensure the page is fully rendered
        time.sleep(5)
        
        # Step 5: Wait for and click the post-login target element (e.g., "RBS 3.0" button)
        post_login_target_selector = config['selectors'].get('post_login_target_selector')
        if not post_login_target_selector:
            print("Error: post_login_target_selector not found in config.json")
            driver.save_screenshot("post_login_target_selector_not_found.png")
            print("Screenshot saved to post_login_target_selector_not_found.png")
            return False

        print(f"Waiting for post-login target element: {post_login_target_selector}")
        target_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, post_login_target_selector))
        )
        time.sleep(2) # Additional sleep before clicking
        print(f"Attempting JavaScript click for post-login target element: {post_login_target_selector}")
        driver.execute_script("arguments[0].click();", target_element)
        print("Post-login action completed.")

        # Step 6: Click the first checkbox
        checkbox_1_selector = config['selectors'].get('checkbox_1_selector')
        if not checkbox_1_selector:
            print("Error: checkbox_1_selector not found in config.json")
            driver.save_screenshot("checkbox_1_selector_not_found.png")
            print("Screenshot saved to checkbox_1_selector_not_found.png")
            return False

        print(f"Waiting for checkbox 1: {checkbox_1_selector}")
        checkbox_1_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, checkbox_1_selector))
        )
        print(f"Attempting JavaScript click for checkbox 1: {checkbox_1_selector}")
        driver.execute_script("arguments[0].click();", checkbox_1_element)
        print("Checkbox 1 clicked.")

        # Step 7: Click the second checkbox
        checkbox_2_selector = config['selectors'].get('checkbox_2_selector')
        if not checkbox_2_selector:
            print("Error: checkbox_2_selector not found in config.json")
            driver.save_screenshot("checkbox_2_selector_not_found.png")
            print("Screenshot saved to checkbox_2_selector_not_found.png")
            return False

        print(f"Waiting for checkbox 2: {checkbox_2_selector}")
        checkbox_2_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, checkbox_2_selector))
        )
        print(f"Attempting JavaScript click for checkbox 2: {checkbox_2_selector}")
        driver.execute_script("arguments[0].click();", checkbox_2_element)
        print("Checkbox 2 clicked.")

    except Exception as e:
        print(f"Error during post-login actions: {e}")
        print(f"Current URL: {driver.current_url}")
        driver.save_screenshot("post_login_action_error.png")
        print("Screenshot saved to post_login_action_error.png")
        return False

    # Step 8: Login sequence successfully initiated
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
            time.sleep(10) # Increased sleep time to 10 seconds to verify login
        else:
            print("Login process failed.")
    finally:
        print("Closing WebDriver.")
        driver.quit()

if __name__ == "__main__":
    main()