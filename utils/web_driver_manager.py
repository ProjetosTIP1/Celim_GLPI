import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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
        options.add_argument("--disable-notifications")

        # Path to local chromedriver (specifically for version 146.0.7680.165)
        base_dir = os.getcwd()
        local_driver_path = os.path.join(
            base_dir, "chromedriver-win64", "chromedriver-win64", "chromedriver.exe"
        )

        if os.path.exists(local_driver_path):
            service = Service(local_driver_path)
        else:
            # Fallback to standard management if local driver is missing
            try:
                service = Service(ChromeDriverManager().install())
            except Exception:
                # If both fail, let Selenium Manager (native) try its best
                return webdriver.Chrome(options=options)

        return webdriver.Chrome(service=service, options=options)
