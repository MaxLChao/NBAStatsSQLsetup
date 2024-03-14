from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pickle
# set up the webdriver (update the path to your chromedriver)
driver = webdriver.Chrome('./chromedriver')

# go to the ryver website
# this is for debug
# driver.get('https://mskilab.ryver.com/index.html#forums/1096675/chat')
# this is for tips
driver.get('https://mskilab.ryver.com/index.html#forums/1065347/chat')

# find the username field
username_field = driver.find_element(By.ID, 'loginusername')
username_field.clear()

# enter your ryver username
username_field.send_keys('BLAH')

# find the password field
password_field = driver.find_element(By.ID, 'loginpassword')
password_field.clear()

# enter your ryver password
password_field.send_keys('PASSWORD')

# submit the form to log in
password_field.submit()
print('password submitted')

time.sleep(10)  # wait for the page to load

# function to scroll to load older messages
def scroll_to_load_old_messages():
    scroll_element = driver.find_element(By.CLASS_NAME, "scroll-container")
    last_height = -1
    while True:
        driver.execute_script("arguments[0].scrollTop = 0", scroll_element)
        time.sleep(2)  # allow time for loading messages

        new_height = driver.execute_script("return arguments[0].scrollTop;", scroll_element)
        if new_height == last_height:
            break
        last_height = new_height

# def scroll_to_load_old_messages():
#     scroll_element = driver.find_element(By.CLASS_NAME, "scroll-container")
#     last_height = -1
#     driver.execute_script("arguments[0].scrollTop = 0", scroll_element)
#     time.sleep(2)  # allow time for loading messages

# navigate to the required channel, make sure it's fully loaded
time.sleep(5)

# scroll up to load old messages
scroll_to_load_old_messages()

time.sleep(2)

# find all messages in the channel
messages = driver.find_elements(By.CLASS_NAME, "chat-message__content")
# extract the username and message content
messages_data = []
for message in messages:
    username_element = message.find_element(By.CLASS_NAME, "chat-message__from")
    nameelem = username_element.find_element(By.CLASS_NAME, "chat-message__from-name")
    username = nameelem.text
    time_elem = username_element.find_element(By.CLASS_NAME,"chat-message__from-time")
    time = time_elem.get_attribute("title")
    # text:
    if message.find_elements(By.CLASS_NAME, 'chat-message__events'):
        content_element = message.find_element(By.CLASS_NAME, "chat-message__events")
        content = content_element.text
    else:
        content = "None"
    #fi

    # images:
    image_elements = message.find_elements(By.CSS_SELECTOR, '.embed__photo-src img')
    images = []
    for image_element in image_elements:
        image_src = image_element.get_attribute("data-img-src")
        images.append(image_src)
        #print(images)
    if not images:
        images = "None"

    messages_data.append({"username": username,
                          "time": time,
                          "content": content,
                          "images": images})



# writing out via this:
output = open('tips.pkl', 'wb')
pickle.dump(messages_data, output)
output.close()

# Save messages to a tab-delimited text file
with open('ryver_messagestips.txt', 'w') as file:
    for message in messages_data:
        # Concatenate image sources with tab delimiter
        image_sources = "\t".join(message['images']) if message['images'] != "None" else "None"
        file.write(f"{message['username']}\t{message['time']}\t{message['content']}\t{image_sources}\n")

# close the web driver
driver.close()
