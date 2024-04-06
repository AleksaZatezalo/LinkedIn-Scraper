"""
Author: Aleksa Zatezalo
Date Created: April 2024
Descripton: A scraping functionality made to gather Data on SerbLink's LinkedIn page.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import time

# Selenium Functions
def createDriver(path):
    """
    Creates the driver needed to browse the web.
    """

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    return driver

def authenticate(driver, username, password):
    """
    Authenticate to LinkedIn in order to browse it. Uses browser driver browser.
    """

    driver.get("https://www.linkedin.com/")
    time.sleep(1)
    email = driver.find_element(By.ID, "session_key")
    passwd = driver.find_element(By.ID, "session_password")
    email.send_keys(username)
    passwd.send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

# Beautiful Soup 4 scraping functions
def scrapeProfile(followerURL, driver):
    """
    Scrapes a user profile found at followerURL url. 
    The variable driver is the selenium web driver.
    """

    # Go to profile page and scroll to the bottom
    driver.get(followerURL)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
    time.sleep(3)

    # Get page http as lxml
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    # Scrapes User Info
    intro = soup.find('div', {'class': 'mt2 relative'})
    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()
    
    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    works_at = works_at_loc.get_text().strip()
    
    location_loc = intro.find_all("span", {'class': 'text-body-small inline t-black--light break-words'})
    location = location_loc[0].get_text().strip()

    dictionary = {
    "name": name,
    "works_at": works_at,
    "location": location
    }

    json_object = json.dumps(dictionary, indent=4)

    return json_object


def scrapeProfiles(followTxt, driver):
    """Scrapes a list of followers URLs found from followersTxt."""
    
    followers = open(followTxt, 'r')
    lines = followers.readlines()
    info = open('follows.json', 'w')

    for line in lines:
        profile = scrapeProfile(line, driver)
        info.write(profile)
    followers.close()
    info.close()