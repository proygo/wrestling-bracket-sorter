from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_wrestlers():
    url = "https://www.trackwrestling.com/predefinedtournaments/MainFrame.jsp?newSession=false&TIM=1750793545778&pageName=%2Fpredefinedtournaments%2FBracketViewer.jsp&twSessionId=gpewflalse"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
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

    driver.quit()
    return pd.DataFrame(wrestlers)
