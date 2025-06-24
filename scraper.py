# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

def create_chrome_driver():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in some environments

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_wrestlers(tournament_url: str, wait_time: int = 5) -> pd.DataFrame:
    driver = create_chrome_driver()
    driver.get(tournament_url)
    time.sleep(wait_time)  # Wait for page to load fully

    # Switch to the iframe that contains the bracket viewer content
    driver.switch_to.frame("contentFrame")

    # Locate the bracketSelector dropdown
    select = Select(driver.find_element("name", "bracketSelector"))

    wrestlers = []

    # Loop through all weight classes (brackets)
    for option in select.options:
        weight_class = option.text.strip()
        select.select_by_visible_text(weight_class)
        time.sleep(3)  # Allow bracket to load

        # Parse the current page source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all wrestler cells (adjust selector if Trackwrestling updates site)
        names = soup.find_all("td", class_="wrestler")

        for td in names:
            text = td.get_text(" ", strip=True)
            if "(" in text:
                try:
                    name_part, rest = text.split("(", 1)
                    name = name_part.strip()
                    grade = rest.split(")")[0].strip()
                    school = rest.split(")")[1].replace("-", "").strip()
                    wrestlers.append({
                        "Name": name,
                        "Grade": grade,
                        "School": school,
                        "Weight Class": weight_class
                    })
                except Exception:
                    continue

    driver.quit()
    return pd.DataFrame(wrestlers)
