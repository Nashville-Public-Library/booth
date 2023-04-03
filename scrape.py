'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

def hour1():
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
    elif int(current_hour) < 11:
        if int(current_hour) == 8:
            trail_hour = '10:00 a'
        else:
            trail_hour = int(current_hour) + 1
            trail_hour = f'{trail_hour}:00 a'.lstrip('0')
    elif int(current_hour) == 11:
        trail_hour = '12:00 p'
    else:
        trail_hour = int(current_hour) - 11
        trail_hour = f'{trail_hour}:00 p'.lstrip('0')

    #3-4:30pm is a special case. deal with this separately.
    if int(current_hour) == 15 or int(current_hour) == 16:
        lead_hour = '3:00 p - '
        trail_hour = '4:30 p'

    final_hour = f'{lead_hour}{trail_hour}'
    return final_hour

def hour2():
    current_hour = datetime.now().strftime('%H')
    current_hour = int(current_hour) + 1

    if current_hour <= 11:
        # booth schedule begins at 9am, but we want to start showing the schedule at 8am
        if current_hour == 9:
            lead_hour = '10:00 a - '
        else:
            lead_hour = f'{current_hour}:00 a - '.lstrip('0')
    elif current_hour == 12:
        lead_hour = '12:00 p - '
    else:
        lead_hour = (current_hour) - 12
        lead_hour = f'{lead_hour}:00 p - '.lstrip('0')

    if current_hour == 13:
        trail_hour = (current_hour) - 11
        trail_hour = f'{trail_hour}:00 p'.lstrip('0')
    elif current_hour < 11:
        if current_hour == 9:
            trail_hour = '11:00 a'
        else:
            trail_hour = (current_hour) + 1
            trail_hour = f'{trail_hour}:00 a'.lstrip('0')
    elif (current_hour) == 11:
        trail_hour = '12:00 p'
    else:
        trail_hour = (current_hour) - 11
        trail_hour = f'{trail_hour}:00 p'.lstrip('0')

    #3-4:30pm is a special case. deal with this separately.
    if current_hour == 15:
        lead_hour = '3:00 p - '
        trail_hour = '4:30 p'
    
    if current_hour >= 16:
        lead_hour = 'Rest of Day'
        trail_hour = ''

    final_hour = f'{lead_hour}{trail_hour}'
    return final_hour


def scrape():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    '''
    need to declare a specific version here. if you leave this blank, 
    it will automatically use the latest version. This caused an issues recently.
    The newest version of the driver only supported the newest version of the browser,
    but that version of the browser was in beta only. Therefore, our 'Yum Install' command
    on Linux wouldn't download it. So, for now, just use a recent known working version.
    '''
    os_name = os.name
    if os_name == 'nt':
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, cache_valid_range=300).install()), options=chrome_options)
    else:
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, cache_valid_range=300, version='109.0.5414.74').install()), options=chrome_options)

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

    '''this is so ugly. TODO REFACTOR so it makes sense!'''
    days = driver.find_elements(By.CLASS_NAME, value='a')
    for day in days:
        day_of_month = day.find_elements(By.CLASS_NAME, value='e')
        for i in day_of_month:
            day_as_number_to_match = datetime.now().strftime('%d').lstrip('0')
            if i.text == day_as_number_to_match:
                assignments = day.find_elements(By.TAG_NAME, value='td')
                for assignment in assignments:
                    assignment = assignment.text
                    # strip out text we don't want/need
                    assignment = assignment.replace('[Other - Talking Library\\', '')
                    assignment = assignment.replace('Staff Service]', '')
                    assignment = assignment.replace('Collection Service]', '')

                    booth1 = 'Booth 1'
                    booth2 = 'Booth 2'
                    booth3 = 'Booth 3'
                
                    # all of this is to remove the extra text so we're only returning the name of the volunteer
                    if (booth1 in assignment) and (hour1() in assignment):
                        booth1_return = assignment
                        booth1_return = booth1_return.replace(booth1, '')
                        booth1_return = booth1_return.replace(hour1(), '')
                        booth1_return = booth1_return.strip()

                    if (booth2 in assignment) and (hour1() in assignment):
                        booth2_return = assignment
                        booth2_return = booth2_return.replace(booth2, '')
                        booth2_return = booth2_return.replace(hour1(), '')
                        booth2_return = booth2_return.strip()

                    if (booth3 in assignment) and (hour1() in assignment):
                        booth3_return = assignment
                        booth3_return = booth3_return.replace(booth3, '')
                        booth3_return = booth3_return.replace(hour1(), '')
                        booth3_return = booth3_return.strip()

                    #SECOND HOUR
                    
                    if (booth1 in assignment) and (hour2() in assignment):
                        booth1_return2 = assignment
                        booth1_return2 = booth1_return2.replace(booth1, '')
                        booth1_return2 = booth1_return2.replace(hour2(), '')
                        booth1_return2 = booth1_return2.strip()

                    if (booth2 in assignment) and (hour2() in assignment):

                        booth2_return2 = assignment
                        booth2_return2 = booth2_return2.replace(booth2, '')
                        booth2_return2 = booth2_return2.replace(hour2(), '')
                        booth2_return2 = booth2_return2.strip()

                    if (booth3 in assignment) and (hour2() in assignment):
                        booth3_return2 = assignment
                        booth3_return2 = booth3_return2.replace(booth3, '')
                        booth3_return2 = booth3_return2.replace(hour2(), '')
                        booth3_return2 = booth3_return2.strip()

    driver.quit()

    # first hour

    if 'booth1_return' in locals():
        if booth1_return == '':
            booth1_return = 'Empty'
    else:
        booth1_return = 'CLOSED'

    if 'booth2_return' in locals():
        if booth2_return == '':
            booth2_return = 'Empty'
    else:
        booth2_return = 'CLOSED'

    if 'booth3_return' in locals():
        if booth3_return == '':
            booth3_return = 'Empty'
    else:
        booth3_return = 'CLOSED'
    
    # second hour

    if 'booth1_return2' in locals():
        if booth1_return2 == '':
            booth1_return2 = 'Empty'
    else:
        booth1_return2 = 'CLOSED'

    if 'booth2_return2' in locals():
        if booth2_return2 == '':
            booth2_return2 = 'Empty'
    else:
        booth2_return2 = 'CLOSED'

    if 'booth3_return2' in locals():
        if booth3_return2 == '':
            booth3_return2 = 'Empty'
    else:
        booth3_return2 = 'CLOSED'


    return booth1_return, booth2_return, booth3_return, booth1_return2, booth2_return2, booth3_return2

def check_banner():
    banner = open('message.txt', 'r')
    banner = banner.read()

    if banner == '':
        banner == False
        
    return banner