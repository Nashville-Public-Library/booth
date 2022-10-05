import os
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from pyvirtualdisplay import Display


def now():
    current_hour = datetime.now().strftime('%H')

    if int(current_hour) <= 11:
        # booth schedule begins at 9am, but we want to start showing the schedule at 8am
        if int(current_hour) == 8:
            lead_hour = '9:00 a - '
        else:
            lead_hour = f'{current_hour}:00 a - '.lstrip('0')
    elif int(current_hour) == 12:
        lead_hour = '12:00 p - '
    else:
        lead_hour = int(current_hour) - 12
        lead_hour = f'{lead_hour}:00 p - '.lstrip('0')

    if int(current_hour) == 12:
        trail_hour = int(current_hour) - 11
        trail_hour = f'{trail_hour}:00 p'
    elif int(current_hour) <= 11:
        trail_hour = int(current_hour) + 1
        trail_hour = f'{trail_hour}:00 a'.lstrip('0')
    else:
        trail_hour = int(current_hour) - 11
        trail_hour = f'{trail_hour}:00 p'.lstrip('0')

    #3-4:30pm is a special case. deal with this separately.
    
    if int(current_hour) ==15 or int(current_hour) == 16:
        lead_hour = '3:00 p - '
        trail_hour = '4:30 p'

    final_hour = f'{lead_hour}{trail_hour}'
    return final_hour


def scrape():

    # cd = os.getcwd()
    # driver_location = f'{cd}/geckodriver'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), chrome_options=chrome_options)
    
    driver.get('https://www.volgistics.com/ex/portal.dll/?FROM=15495')

    email = driver.find_element(by=By.NAME, value="LN")
    password = driver.find_element(by=By.NAME, value="PW")

    VIC_user = os.environ['VIC_user']
    VIC_pass = os.environ['VIC_password']

    email.send_keys(VIC_user)
    password.send_keys(VIC_pass)

    submit = driver.find_element(by=By.NAME, value="Go")
    submit.click()

    # now we're logged in

    my_schedule = driver.find_element(by=By.NAME, value='Sch')
    my_schedule.click()

    a = driver.find_elements(By.CLASS_NAME, value='a')
    for i in a:
        today = i.find_elements(By.CLASS_NAME, value='e')
        for n in today:
            day_as_number = datetime.now().strftime('%d').lstrip('0')
            if n.text == day_as_number:
                b = i.find_elements(By.TAG_NAME, value='td')
                for c in b:
                    c = c.text
                    c = c.replace('[Other - Talking Library\\', '')
                    c = c.replace('Staff Service]', '')
                    c = c.replace('Collection Service]', '')
                    booth1 = 'Booth 1'
                    booth2 = 'Booth 2'
                    booth3 = 'Booth 3'
                
                    if (booth1 in c) and (now() in c):
                        booth1_return = c
                        booth1_return = booth1_return.replace(booth1, '')
                        booth1_return = booth1_return.replace(now(), '')
                        booth1_return = booth1_return.strip()
                    if (booth2 in c) and (now() in c):
                        booth2_return = c
                        booth2_return = booth2_return.replace(booth2, '')
                        booth2_return = booth2_return.replace(now(), '')
                        booth2_return = booth2_return.strip()
                    if (booth3 in c) and (now() in c):
                        booth3_return = c
                        booth3_return = booth3_return.replace(booth3, '')
                        booth3_return = booth3_return.replace(now(), '')
                        booth3_return = booth3_return.strip()

    driver.quit()

    if booth1_return == '':
        booth1_return = 'Empty'
    if booth2_return == '':
        booth2_return = 'Empty'
    if booth3_return == '':
        booth3_return = 'Empty'

    return booth1_return, booth2_return, booth3_return
