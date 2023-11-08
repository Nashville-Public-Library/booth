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

    driver.implicitly_wait(5)

    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")

    email.send_keys(EV().VIC_user)
    password.send_keys(EV().VIC_pass)

    submit = driver.find_element(by=By.CLASS_NAME, value="mat-mdc-raised-button")
    submit.click()

    # now we're logged in

    driver.implicitly_wait(10)

    '''this is so ugly. TODO REFACTOR so it makes sense!'''
    shifts = driver.find_elements(By.CLASS_NAME, 'column-details-desktop')
    # driver.quit()
    return shifts

def filter_data(booth: str, shift: str, hour: str):
    text_to_remove = ('• Other - Talking Library\Staff Service', '• Other - Talking Library\Collection Service', 
                'AM Newspaper Reading', 'The Tennessean', '1 more needed', 'Account Staff', booth, hour)
    for text in text_to_remove:
        shift = shift.replace(text, '')
    booth_return = shift.strip()
    if booth_return == '':
        booth_return = 'Empty'
    return booth_return

def get_scrape_and_filter():
    '''
    get all the elements via selenium and loop through them to match booth numbers and hours. start out assuming all booths are closed,
    and update the dictionary only when there is a match.
    '''
    booth1 = "Booth 1"
    booth2 = "Booth 2"
    booth3 = "Booth 3"

    schedule = {'booth1_1': "CLOSED", 'booth2_1': "CLOSED",'booth3_1': "CLOSED",
                'booth1_2': "CLOSED", 'booth2_2': "CLOSED", 'booth3_2': "CLOSED"}
    
    shifts = scrape()
    for shift in shifts:
        shift = shift.text
        if (booth1 in shift) and (hour1() in shift):
            schedule['booth1_1'] = filter_data(booth=booth1, shift=shift, hour=hour1())

        if (booth2 in shift) and (hour1() in shift):
            schedule['booth2_1'] = filter_data(booth=booth2, shift=shift, hour=hour1())

        if (booth3 in shift) and (hour1() in shift):
            schedule['booth3_1'] = filter_data(booth=booth3, shift=shift, hour=hour1())


        if (booth1 in shift) and (hour2() in shift):
            schedule['booth1_2'] = filter_data(booth=booth1, shift=shift, hour=hour2())

        if (booth2 in shift) and (hour2() in shift):
            schedule['booth2_2'] = filter_data(booth=booth2, shift=shift, hour=hour2())

        if (booth3 in shift) and (hour2() in shift):
            schedule['booth3_2'] = filter_data(booth=booth3, shift=shift, hour=hour2())

    return schedule