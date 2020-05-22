
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

# notify user that program is running
print("Running...")

# initial setup of browser
browser = webdriver.Safari()
browser.maximize_window()
browser.set_window_position(2000,2000)

browser.get("https://bacon.signs.com/CustomerServicePortal/CustomerSegmentationIndex")

time.sleep(1.5)

login_button = browser.find_elements_by_id("Google")
login_button.pop()
button = login_button.pop()
button.send_keys(Keys.ENTER)


time.sleep(2.4)

# input the input
try:
    email_box = browser.find_element_by_class_name("whsOnd").send_keys(email + Keys.ENTER)
except selenium.common.exceptions.NoSuchElementException:
    time.sleep(1)
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
browser.set_window_size(5000,5000)

# get max pages
maxPages = int(browser.find_element_by_class_name("pagination").get_attribute("data-pagecount"))
currPage = 1

# bug counter
bugs = 0


while currPage <= maxPages:

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

    while agents:
        count += 1
        agent = agents.pop()
        try:
            curr_loc = agent.location.get('y')
            select = Select(agent)
            current = select.first_selected_option.text
            if current == "unassigned":
                agent.send_keys(Keys.ENTER)
            else:
                continue
        except selenium.common.exceptions.ElementNotInteractableException:
            continue
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(1.25)
            curr_loc = agent.location.get('y')
            select = Select(agent)
            current = select.first_selected_option.text
            if current == "unassigned":
                agent.send_keys(Keys.ENTER)
            else:
                continue

        scroll += curr_loc - past_loc

        if count > 6:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        else:
            browser.execute_script("window.scrollTo(0,scroll)")

        for option in select.options:
            if option.text == email:
            # try-catch block for weird exceptions
                try:
                    select.select_by_visible_text(email)
                    break
                except:
                    print("bug detected")
                    bugs += 1
                    continue

        try:
            past_loc = agent.location.get('y')
        except selenium.common.exceptions.ElementNotInteractableException or selenium.common.exceptions.WebDriverException:
            continue


    currPage += 1
    if currPage <= maxPages:
        # next page click
        next = browser.find_element_by_link_text(str(currPage))
        browser.execute_script("arguments[0].click();", next)
        browser.execute_script("window.scrollTo(0,0)")
        time.sleep(1.5)

print("Done! Caught " + str(bugs) + " bugs.")

