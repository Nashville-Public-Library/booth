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

from app.booth.hours import hour1, hour2
from app.ev import EV


def scrape():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    '''
    need to declare a specific version here. if you leave this blank, 
    it will automatically use the latest version. This caused an issues.
    The newest version of the driver only supported the newest version of the browser,
    but that version of the browser was in beta only. Therefore, our 'Yum Install' command
    on Linux wouldn't download it. So, for now, just use a recent known working version.
    '''
    os_name = os.name
    if os_name == 'nt':
        driver = webdriver.Chrome(service=ChromiumService(executable_path='chromedriver.exe'), options=chrome_options)
    else:
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, cache_valid_range=300, version='114.0.5735.16').install()), options=chrome_options)

    date_for_URL = datetime.now().strftime('%m%d%Y')
    driver.get(f'https://www.volgistics.com/vicnet/15495/schedule?view=day&date={date_for_URL}')

    driver.implicitly_wait(3)

    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")

    email.send_keys(EV().VIC_user)
    password.send_keys(EV().VIC_pass)

    submit = driver.find_element(by=By.CLASS_NAME, value="mat-mdc-raised-button")
    submit.click()

    # now we're logged in

    driver.implicitly_wait(5)

    '''this is so ugly. TODO REFACTOR so it makes sense!'''
    shifts = driver.find_elements(By.CLASS_NAME, 'column-details-desktop')
    for shift in shifts:
        # strip out non-needed text
        shift = shift.text.replace('• Other - Talking Library\Staff Service', '')
        shift = shift.replace('• Other - Talking Library\Collection Service', '')
        shift = shift.replace('AM Newspaper Reading', '')
        shift = shift.replace('The Tennessean', '')
        shift = shift.replace('1 more needed', '')
        shift = shift.replace('Account Staff', '')

        booth1 = 'Booth 1'
        booth2 = 'Booth 2'
        booth3 = 'Booth 3'
        
        # all of this is to remove the extra text so we're only returning the name of the volunteer
        if (booth1 in shift) and (hour1() in shift):
            booth1_return = shift
            booth1_return = booth1_return.replace(booth1, '')
            booth1_return = booth1_return.replace(hour1(), '')
            booth1_return = booth1_return.strip()

        if (booth2 in shift) and (hour1() in shift):
            booth2_return = shift
            booth2_return = booth2_return.replace(booth2, '')
            booth2_return = booth2_return.replace(hour1(), '')
            booth2_return = booth2_return.strip()

        if (booth3 in shift) and (hour1() in shift):
            booth3_return = shift
            booth3_return = booth3_return.replace(booth3, '')
            booth3_return = booth3_return.replace(hour1(), '')
            booth3_return = booth3_return.strip()

        #SECOND HOUR

        if (booth1 in shift) and (hour2() in shift):
            booth1_return2 = shift
            booth1_return2 = booth1_return2.replace(booth1, '')
            booth1_return2 = booth1_return2.replace(hour2(), '')
            booth1_return2 = booth1_return2.strip()

        if (booth2 in shift) and (hour2() in shift):

            booth2_return2 = shift
            booth2_return2 = booth2_return2.replace(booth2, '')
            booth2_return2 = booth2_return2.replace(hour2(), '')
            booth2_return2 = booth2_return2.strip()

        if (booth3 in shift) and (hour2() in shift):
            booth3_return2 = shift
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


    return {'booth1_1': booth1_return, 'booth2_1': booth2_return,'booth3_1': booth3_return, 
            'booth1_2': booth1_return2, 'booth2_2': booth2_return2, 'booth3_2': booth3_return2}