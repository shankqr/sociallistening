from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import random

with open("config2.json") as json_file:  # read json
    data = json.load(json_file)  # store json

driver = webdriver.Firefox()  # open browser, make sure browser driver in path
driver.get("https://www.facebook.com")  # go to facebook

element1 = driver.find_element_by_id("email")  # locate email box
element2 = driver.find_element_by_id("pass")
element1.send_keys(data["email"])  # insert email into box
element2.send_keys(data["password"], Keys.ENTER)  # insert password
time.sleep(random.uniform(1, 2))  # wait 2 seconds
driver.get(data["link"])
time.sleep(random.uniform(2, 4))

y = 0
while y < data["commentClick"]:
    try:
        elem2 = driver.find_element_by_class_name(data["contentClass"])  # find first div that content all comment.
        elem1 = elem2.find_element_by_class_name("UFIPagerLink")
        elem1.click()  # reveal more comment
        y = y + 1
        time.sleep(random.uniform(1, 2))
    except:
        y = data["commentClick"]

x = 0
while x < data["replyClick"]:
    try:
        elem3 = driver.find_element_by_class_name("UFIReplySocialSentenceLinkText.UFIReplySocialSentenceVerified")
        elem3.click()  # reveal reply
        x = x+1
        time.sleep(random.uniform(1, 2))
    except:
        x = data["replyClick"]


elem3 = elem2.find_elements_by_class_name(data["commenterClass"]) # take commenter from elem2 only
elem4 = elem2.find_elements_by_class_name(data["commentClass"])  # take comment
elem5 = elem2.find_elements_by_class_name(data["dateClass"])  # take date


elem_list1 = []
elem_list2 = []
elem_list3 = []

for e in elem5:  # convert date into string
    elem_list3.append(e.text)
for e in elem4:  # convert comment into string
    elem_list2.append(e.text)
for e in elem3:  # convert commenter into string
    elem_list1.append(e.text)


print(elem_list1)
print(elem_list2)
print(elem_list3)
print(len(elem_list1))
print(len(elem_list2))
print(len(elem_list3))
