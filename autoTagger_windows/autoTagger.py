# imports
import os
import sys

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import re

from selenium.webdriver.support.wait import WebDriverWait

"""The following are the different helper methods used in the main script"""

def inputPhase():
    # get input from user
    email = input("What's your email? ")
    pw = input("What's your password? ")
    date = input("Enter date in MM/DD/YYYY format: ")

    info = checkInput(email,pw, date)   # loops through and checks input

    return info

def checkInput(email,pw, date):

    if not email.endswith("@signs.com"):
        while not email.endswith("@signs.com"):
            email = input("Email not valid. Try again: ")

    if not re.match('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', date):
        while not re.match('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', date):
            date = input("Date not valid. Try again: ")
    return [email,pw,date]

def loginPhase():
    # notify user of progress
    print("Loading information...")
    # login phase
    login_button = browser.find_elements_by_id("Google")
    login_button.pop()
    button = login_button.pop()
    button.send_keys(Keys.ENTER)

    time.sleep(.9)  # slight waiting period

    # input the input
    try:
        email_box = browser.find_element_by_class_name("whsOnd").send_keys(email + Keys.ENTER)
    except selenium.common.exceptions.NoSuchElementException:
        wait = WebDriverWait(browser, 10)
        email_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "whsOnd")))
        email_box.send_keys(email + Keys.ENTER)

    time.sleep(2)  # slight waiting period
    # pw
    wait = WebDriverWait(browser, 10)
    pw_box = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    pw_box.send_keys(pw + Keys.ENTER)

def getPage():
    # go to date
    try:
        fromDate = browser.find_element_by_name("custSegfrom")
        fromDate.clear()
        fromDate.send_keys(date)
    except:
        browser.quit()
        print("You did not put in the right password. Please restart program")

    toDate = browser.find_element_by_name("custSegto")
    toDate.clear()
    toDate.send_keys(date + Keys.ENTER)
    time.sleep(1)
    browser.find_element_by_id("custSegDateSubmit").send_keys(Keys.ENTER)

    time.sleep(2.4)
    browser.set_window_size(5000, 5000)
    browser.set_window_position(2000, 2000)  # hides window



def beginTags():

    # drop-down fill-ins to set up tags
    list = browser.find_elements_by_class_name("ddl-customerSegmentation-agent")
    agents = []
    while list:
        agents.append(list.pop())
    return agents

def autoTag(bugs):

    # get max pages
    wait = WebDriverWait(browser, 10)
    maxi = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))
    maxPages = int(maxi.get_attribute("data-pagecount"))
    currPage = 1

    while currPage <= maxPages:

        # print current page to terminal
        print("Filling tags for page " + str(currPage) + "...")

        # Setup new page attributes
        scroll = 0
        count = 0
        past_loc = 0
        curr_loc = 0

        agents = beginTags()


        while agents:
            count += 1
            agent = agents.pop()
            try:
                curr_loc = agent.location.get('y')
                select = Select(agent)
                current = select.first_selected_option.text
            except:
                time.sleep(1.5)
                beginTags()
                continue


            scroll += curr_loc - past_loc   # get scroll value

            # scroll based on current order. helps with debugging for some reason
            if count > 6:
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            else:
                browser.execute_script("window.scrollTo(0,scroll)")

            try:
                for option in select.options:
                    if option.text == email:
                        if current == "unassigned":     # only assigns agents to ones not previously assigned to!
                            # try-catch block for weird exceptions
                            try:
                                select.select_by_visible_text(email)
                                break
                            except:
                                print("bug detected")
                                bugs += 1
                                continue
            except:
                time.sleep(1.5)
                beginTags()
                continue


            try:
                past_loc = agent.location.get('y')
            except:
                time.sleep(1.5)
                beginTags()
                continue

        currPage += 1
        if currPage <= maxPages:
            # next page click
            wait = WebDriverWait(browser, 10)
            next = wait.until(EC.presence_of_element_located((By.LINK_TEXT, str(currPage))))
            browser.execute_script("arguments[0].click();", next)
            browser.execute_script("window.scrollTo(0,0)")
            time.sleep(1)


"""The main script"""

# input and get global variables
input = inputPhase()
email = input[0]
pw = input[1]
date = input[2]

# notify user that program is running
print("Running...")

# initial setup of browser
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

browser = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))  #windows specific
browser.maximize_window()
browser.set_window_position(2000,2000)  # hides window

# go to bacon website
browser.get("https://bacon.signs.com/CustomerServicePortal/CustomerSegmentationIndex")


time.sleep(.5)  # slight waiting period

loginPhase()

time.sleep(7)   # slight waiting period

getPage()

# bug counter
bugs = 0

autoTag(bugs)

browser.quit()  # close the browser

print("Done! Caught " + str(bugs) + " bugs.")

time.sleep(30)   # sleep for half a minute, then close program.
