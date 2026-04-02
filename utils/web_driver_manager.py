import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebDriverFactory:
    """
    Factory class to create and configure Selenium WebDriver instances.
    Handles specific versioning issues by prioritizing local drivers.
    """

    @staticmethod
    def create_chrome_driver(headless=True):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        # Base directory resolution
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.abspath(".")

        # Candidate paths for the chromedriver executable
        candidate_paths = [
            os.path.join(base_dir, "chromedriver.exe"),
            os.path.join(base_dir, "chromedriver-win64", "chromedriver-win64", "chromedriver.exe")
        ]

        # Use the first one that exists
        local_driver_path = None
        for path in candidate_paths:
            if os.path.exists(path):
                local_driver_path = path
                break

        if not local_driver_path:
            error_msg = (
                "ChromeDriver nao encontrado! Favor colocar o 'chromedriver.exe' na pasta raiz do bot.\n"
                "Caminhos verificados:\n" + "\n".join(f"- {p}" for p in candidate_paths)
            )
            # Log to console if bot_log is not available here, otherwise it will be raised and caught in main
            raise FileNotFoundError(error_msg)

        # Create the service with the local driver
        service = Service(local_driver_path)
        return webdriver.Chrome(service=service, options=options)
