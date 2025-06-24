from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_wrestlers(tournament_url: str, wait_time: int = 5) -> pd.DataFrame:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(tournament_url)
    time.sleep(wait_time)

    driver.switch_to.frame("contentFrame")

    select = Select(driver.find_element("name", "bracketSelector"))

    wrestlers = []

    for option in select.options:
        weight_class = option.text
        select.select_by_visible_text(weight_class)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
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
