"""This script runs to go to facebook in a Safari browser.
Then it enters a fake email and password and clicks enter
"""
# imports
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


# get input from user
email = input("What's your email?")
pw = input("What's your password?")
date = input("Enter date in MM/DD/YYYY format:")


# initial setup of browser
browser = webdriver.Safari()
browser.maximize_window()
browser.get_window_size()
print(browser.get_window_size())

browser.get("https://bacon.signs.com/CustomerServicePortal/CustomerSegmentationIndex")

time.sleep(2)

login_button = browser.find_elements_by_id("Google")
login_button.pop()
button = login_button.pop()
print(button.location)
button.send_keys(Keys.ENTER)


time.sleep(2.8)
# input the input
email_box = browser.find_element_by_class_name("whsOnd").send_keys(email + Keys.ENTER)

time.sleep(2)
# pw
pw_box = browser.find_element_by_class_name("Xb9hP").send_keys(pw + Keys.ENTER)

time.sleep(7)
# go to date
fromDate = browser.find_element_by_name("custSegfrom")
fromDate.clear()
fromDate.send_keys(date)
toDate = browser.find_element_by_name("custSegto")
toDate.clear()
toDate.send_keys(date + Keys.ENTER)
time.sleep(1)
browser.find_element_by_id("custSegDateSubmit").send_keys(Keys.ENTER)

time.sleep(5)


# get max pages
maxPages = browser.find_element_by_class_name("pagination").get_attribute("data-pagecount")
currPage = 1


# drop-down fill-ins
list = browser.find_elements_by_class_name("ddl-customerSegmentation-agent")
agents = []
while list:
    agents.append(list.pop())


#Create the object for Action Chains
actions = ActionChains(browser)
scroll = 0
count = 0
past_loc = 0
curr_loc = 0
bugs = 0

while agents:
    count += 1
    agent = agents.pop()

    curr_loc = agent.location.get('y')
    scroll += curr_loc - past_loc
    if count > 6:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    else:
        browser.execute_script("window.scrollTo(0,scroll)")

    agent.send_keys(Keys.ENTER)
    select = Select(agent)

    for option in select.options:
        if option.text == email:
        #try-catch block for weird exceptions
            try:
                select.select_by_visible_text(email)
            except selenium.common.exceptions.ElementNotInteractableException:
                print("bug detected")
                bugs += 1
            break
    past_loc = agent.location.get('y')

currPage += 1
# next page click
next = browser.find_element_by_link_text(str(currPage))
browser.execute_script("arguments[0].click();", next)

