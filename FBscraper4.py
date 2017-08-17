from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import json
import re
import random
import pymongo

# developed using python 3.6
# need selenium and pymongo installed
# put the firefox geckodriver to the PATH to configure selenium

with open("config.json") as json_file:  # read json
    data = json.load(json_file)  # store json
    data["keyword"] = re.sub(' ', '%2B', data["keyword"].rstrip())  # replace space in keyword with %2B

driver = webdriver.Firefox()  # open browser, make sure browser driver in path
driver.get("https://www.facebook.com")  # go to facebook

element1 = driver.find_element_by_id("email")  # locate email box
element2 = driver.find_element_by_id("pass")
element1.send_keys(data["email"])  # insert email into box
element2.send_keys(data["password"], Keys.ENTER)  # insert password
time.sleep(random.uniform(1, 3))  # random float number and wait 1~3 seconds
driver.get("https://www.facebook.com/search/str/" + data["keyword"]+"/stories-keyword/stories-public?")
time.sleep(random.uniform(1, 2))

scroll = 0
while scroll < data['scrollNo']:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down
    time.sleep(random.uniform(2, 5))
    scroll = scroll+1

# locate all the element with same class name that was passed and store into a list
elem1 = driver.find_elements_by_class_name(data["posterClass"])  # poster
elem2 = driver.find_elements_by_class_name(data["dateClass"])  # date div
elem3 = driver.find_elements_by_class_name(data["contentClass"])  # content div
elem4 = driver.find_elements_by_class_name(data["likeClass"])  # like div
elem5 = driver.find_elements_by_class_name(data["commentClass"])  # comment&share div

elem_list1 = []  # poster
elem_list2 = []  # date
elem_list3 = []  # Content
elem_list4 = []  # like
elem_list5 = []  # link
elem_list6 = []  # comment
elem_list7 = []  # share

for e in elem5:  # store number of share in a list
    if e.text.find("Share") == -1:  # if no share
        elem_list7.append('')
    elif e.text.find("Comments") >= 0:  # if has comments
        elem_list7.append(e.text.split(" Comments")[1].split(" Share")[0])
    elif e.text.find("Comment") >= 0:  # if has one comment
        elem_list7.append(e.text.split(" Comment")[1].split(" Share")[0])
    else:
        elem_list7.append(e.text.split(" Share")[0])

for e in elem5:  # store number of comment
    if e.text.find("Comment") == -1:  # if comment not found
        elem_list6.append('')
    else:
        elem_list6.append(e.text.split(" Comment")[0])

for e in elem2:  # store post link
    elem_list5.append(e.find_element_by_css_selector('a').get_attribute('href'))
for e in elem4:  # store number of like
    elem_list4.append(e.text.split("\n")[0])
for e in elem3:  # store content
    elem_list3.append(e.text)

for e in elem2:  # convert and store date
    e = e.text
    if e.find("Yesterday") >= 0:
        e = e[13:]
        h = int(e.split(":")[0])
        m = int(e.split(":")[1][0:2])
        if e.find("pm") >= 0:
            h = h + 12

        t = datetime.now() - timedelta(1)
        t = t.replace(hour=h, minute=m)
        elem_list2.append(t)

    elif e.find("minutes") >= 0:
        m = int(e.split(' ')[0])
        t = datetime.now() - timedelta(minutes=m)
        elem_list2.append(t)

    elif e.find("hours") >= 0:
        h = int(e.split(' ')[0])
        t = datetime.now() - timedelta(hours=h)
        elem_list2.append(t)
    elif e.find(",") >= 0:
        if e.find("am") >= 0:
            t = datetime.strptime(e, "%B %d, %Y at %H:%Mam")
            elem_list2.append(t)
        else:
            t = datetime.strptime(e, "%B %d, %Y at %H:%Mpm")
            t = t + timedelta(hours=12)
            elem_list2.append(t)

    elif e.find("hour") >= 0:
        t = datetime.now() - timedelta(hours=1)
        elem_list2.append(t)
    elif e.find("minute") >= 0:
        t = datetime.now() - timedelta(minutes=1)
        elem_list2.append(t)
    else:
        if e.find("am") >= 0:
            t = datetime.strptime(str(datetime.now().year)+e, "%Y%B %d at %H:%Mam")
            elem_list2.append(t)
        else:
            t = datetime.strptime(str(datetime.now().year) + e, "%Y%B %d at %H:%Mpm")
            t = t + timedelta(hours=12)
            elem_list2.append(t)

for e in elem1:
    elem_list1.append(e.text)

# db information
dbuser = "adibax"
dbpass = "adikacak"
dbname = "firstDB"
client = pymongo.MongoClient("mongodb://adibax:adikacak@first-shard-00-00-rq3zy.mongodb.net:27017,"
                             "first-shard-00-01-rq3zy.mongodb.net:27017,first-shard-00-02-rq3zy.mongodb.net:27017"
                             "/admin?ssl=true&replicaSet=First-shard-0&authSource=admin")
#  db link

db = client.test  #select test database
#  insert to mongodb
c = 0
for i in elem_list1:
    result = db.facebook.insert_one(
     {

        "poster": elem_list1[c],
        "date": elem_list2[c],
        "content": elem_list3[c],
        "like": elem_list4[c],
        "link": elem_list5[c],
        "comment": elem_list6[c],
        "share": elem_list7[c]
     }
    )
    c = c + 1


print(elem_list1)
print(elem_list2)
print(elem_list3)
print(elem_list4)
print(elem_list5)
print(elem_list6)
print(elem_list7)

print(len(elem_list1))  # print number of item in list
print(len(elem_list2))
print(len(elem_list3))
print(len(elem_list4))
print(len(elem_list5))
print(len(elem_list6))
print(len(elem_list7))
