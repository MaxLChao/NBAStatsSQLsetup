from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import pickle
import os
os.chdir("/Users/Max_1/Documents/code/NBAStatsSQLsetup")

# set up the webdriver (update the path to your chromedriver)
#driver = webdriver.Chrome('/Users/Max_1/Documents/code/NBAStatsSQLsetup/chromedriver/chromedriver-mac-arm64/chromedriver')
# apparently cant pass the chromedriver direct link lmao
driver = webdriver.Chrome()


# player height weigth draft pick and years
#driver.get('https://www.nba.com/stats/players/bio')
#time.sleep(2)
# select dropdown menu to load all and then select
#dropdowns = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9")
                                
#drpdown = Select(driver.find_element(By.CLASS_NAME,'DropDown_select__4pIg9'))
#print(drpdown)
#drpdown.select_by_value("-1")
# ok issue is that there are 26 select boxes with that label lol
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable(dropdowns[-1])).click()
#Select(dropdowns[-1]).select_by_value("-1")
#time.sleep(2) # allow load of all players

# get entire table
#tab = driver.find_element(By.CLASS_NAME, "Crom_table__p1iZz")
#download the table
#lines = tab.text
# out
#f = open('./tables/raws/nbaplayerbackground.txt',"w")
#f.writelines(lines)
#f.close()

# grabbing per game stats across all other pages
url = "https://www.nba.com/stats/players/"
tab_list = ["bio", "traditional", "advanced", "misc", "scoring", "usage", "opponent", "defense", "estimated-advanced"]

for i in tab_list:
    link = url + i
    driver.get(link)
    time.sleep(2)
    dropdowns = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9")
    Select(dropdowns[-1]).select_by_value("-1")
    time.sleep(2) # allow load of all players
    # writing out
    tab = driver.find_element(By.CLASS_NAME, "Crom_table__p1iZz")
    #download the table
    lines = tab.text
    # out
    path_out = './tables/raws/' + i + '.txt'
    f = open(path_out,"w")
    f.writelines(lines)
    f.close()

# close the web driver
driver.close()
