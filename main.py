import json
import sys

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

def main():
    """
    Main function to run the auto-login script.
    """
    config = load_config()
    print("Configuration loaded successfully.")
    print(f"Attempting to log in to: {config.get('login_url')}")
    # --- Main automation logic will be added below ---

if __name__ == "__main__":
    main()
