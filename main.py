import re
import os
from dotenv import load_dotenv
import ast
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

url = os.environ['MAIN_URL']

##############################################################################
def book_class():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # site
    driver.get(os.environ['LOGIN_URL'])

    username = driver.find_element(By.ID, "id_email")
    username.send_keys(os.environ['USER'] + Keys.RETURN)
    username = driver.find_element(By.NAME, "password")
    username.send_keys(os.environ['PASSWORD'] + Keys.RETURN)

    buttons = driver.find_elements(By.XPATH, '//button')

    list_button = ""

    for button in buttons:
        if re.search('list', button.accessible_name, re.IGNORECASE):
            list_button = button

    list_button.click()

    Scrolldown(driver)

    print("done")

    day_elements = driver.find_elements(By.CLASS_NAME, "single-day")

    # Build regex check based on days specified
    booking_schedule = list(ast.literal_eval(os.environ['BOOKING_SCHEDULE']))

    for day in day_elements:
        day_and_date = day.text.split('\n')[0]
        if re.search('Top', day_and_date):
            day_and_date = day.text.split('\n')[1]

        for booking_event in booking_schedule:
            class_name_and_time = booking_event[0]
            days_to_book_regex_string = ""

            for item in booking_event[1]:
                days_to_book_regex_string += item + "|"
            days_to_book_regex_string = days_to_book_regex_string.rstrip(days_to_book_regex_string[-1])

            day_to_book_regex = re.compile(days_to_book_regex_string)

            if day_to_book_regex.match(day_and_date):
                # print(day_and_date)
                events = day.find_elements(By.CLASS_NAME, "offering-container")
                for event in events:
                    if re.search(class_name_and_time, event.accessible_name, re.IGNORECASE):
                        print("Looking to book: " + day_and_date + " : " + event.accessible_name)

    driver.close()

    return False


def Scrolldown(driver):
    y = 5000
    for timer in range(0, 7):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 5000
        time.sleep(0.5)


##############################################################################

# Main function

book_class()
