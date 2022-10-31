import sys
import re
import os
from dotenv import load_dotenv
import ast
import time
from datetime import datetime

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

original_stdout = sys.stdout # Save a reference to the original standard output

with open('TeamUpAutoBook.log', 'w') as f:
    sys.stdout = f

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

url = os.environ['MAIN_URL']

##############################################################################
def book_class():

    users = list(ast.literal_eval(os.environ['USERS']))
    passwords = list(ast.literal_eval(os.environ['PASSWORDS']))

    for index in range(len(users)):

        print("Booking for: " + users[index] + "\n")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # site
        driver.get(os.environ['LOGIN_URL'])

        username = driver.find_element(By.ID, "id_email")
        username.send_keys(users[index] + Keys.RETURN)
        username = driver.find_element(By.NAME, "password")
        username.send_keys(passwords[index] + Keys.RETURN)

        buttons = driver.find_elements(By.XPATH, '//button')

        list_button = ""

        for button in buttons:
            if re.search('list', button.accessible_name, re.IGNORECASE):
                list_button = button

        list_button.click()

        Scrolldown(driver)

        day_elements = driver.find_elements(By.CLASS_NAME, "single-day")

        # Build regex check based on days specified
        booking_schedule = list(ast.literal_eval(os.environ['BOOKING_SCHEDULE']))

        print(booking_schedule)

        for day in day_elements:
            # print("Title: " + day.accessible_name)
            day_and_date = day.text.split('\n')[0]

            if re.search('Top', day_and_date):
                day_and_date = day.text.split('\n')[1]

            date_info = day_and_date.replace('(','')
            date_info = date_info.replace(')','')

            day_of_week = date_info.split(' ')[0]
            month = date_info.split(' ')[1]
            date = date_info.split(' ')[2]
            date = re.sub('\D', '', date)

            today = datetime.today().date()
            test_month = float(datetime.strptime(month, '%b').strftime("%m"))
            this_month = float(today.strftime("%m"))

            if test_month < this_month: # gone into next year
                date = datetime.strptime(str(int(today.strftime("%Y"))+1) + ' ' + month + ' ' + date + ' ' + day_of_week + ' ' + today.strftime("%X"), '%Y %b %d %A %X').date()
            else:
                date = datetime.strptime(today.strftime("%Y") + ' ' + month + ' ' + date + ' ' + day_of_week + ' ' + today.strftime("%X"), '%Y %b %d %A %X').date()

            delta_days = date - today
            delta_days = int(delta_days.days)
            if delta_days < 2:
                print("Skipping day as within 2 days...")
                continue
            elif delta_days > 14:
                print("Cannot book further than 2 weeks in advance, finishing...")
                break

            for booking_event in booking_schedule:
                class_name_and_time = r"^.*?\b" + booking_event[0][0] + r"\b.*?\b" + booking_event[0][1] + r"\b.*?\b" + booking_event[0][2]
                days_to_book_regex_string = ""

                for item in booking_event[1]:
                    days_to_book_regex_string += item + "|"
                days_to_book_regex_string = days_to_book_regex_string.rstrip(days_to_book_regex_string[-1])

                day_to_book_regex = re.compile(days_to_book_regex_string)

                if day_to_book_regex.match(day_and_date):
                    # print("REGEX Search string: " + class_name_and_time)
                    events = day.find_elements(By.CLASS_NAME, "offering-container")

                    print(day_and_date)

                    for event in events:
                        event_name = event.accessible_name
                        # print("\tEvent: " + event.accessible_name)

                        if re.search(class_name_and_time, event_name, re.MULTILINE | re.IGNORECASE | re.UNICODE):
                            # check to see if already booked
                            already_booked_check = "registered|waitlisted|waitlist"

                            if re.search(already_booked_check, event_name, re.MULTILINE | re.IGNORECASE | re.UNICODE):
                                print("-->\t\tAlready booked: " + str(day_and_date) + " : " + str(event_name) + "\n")
                            else:
                                print("-->\t\tLooking to book: " + str(day_and_date) + " : " + str(event_name) + "\n")

                                if event:
                                    event.click()
                                    dialog_window = driver.find_element(By.XPATH, "//div[@role='dialog']")
                                    if dialog_window:
                                        try:
                                            join_button = WebDriverWait(driver, 10).until(
                                                EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Join') or contains(., 'Book')]"))
                                            )

                                            if join_button:
                                                # WebDriverWait(driver,1)
                                                join_button.click()

                                        finally:
                                            driver.close()

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
def main(args: list) -> None:
    book_class()

if __name__ == '__main__':
    main(sys.argv[1:])