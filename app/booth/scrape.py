'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from datetime import datetime

from playwright.sync_api import sync_playwright

from app.ev import EV
from app.booth.utils import date_is_weekend


def scrape_VIC(date: datetime):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        date = date.strftime('%m%d%Y')
        page.goto(f'https://www.volgistics.com/vicnet/15495/schedule?view=day&date={date}')

        email = page.locator("[name='email']")
        password = page.locator("[name='password']")

        email.fill(EV().VIC_user)
        password.fill(EV().VIC_pass)

        submit = page.locator('#log-in-button')
        submit.click()

        # now we're logged in

        page.wait_for_selector('.column-details-desktop') # wait for new page to load

        initial_shift = page.locator('.column-details-desktop')
        shifts = initial_shift.all()
        ret_val: list = []
        for shift in shifts:
            text = shift.text_content()
            ret_val.append(text)

        return ret_val

def remove_extra_text(booth: str, shift: str, hour: str) -> str:
    text_to_remove = ('• Other - Talking Library\Staff Service', '• Other - Talking Library\Collection Service', 
                'AM Newspaper Reading', 'The Tennessean', 'Nashville Ledger', 'Nashville Scene', '"', '1 more needed', 'Account Staff', booth, hour)
    for text in text_to_remove:
        shift = shift.replace(text, '')
    booth_return = shift.strip()
    if booth_return == '':
        booth_return = 'Empty'
    return booth_return

def get_scrape_and_filter(date) -> dict:
    '''
    get all the elements via selenium and loop through them to match booth numbers and hours. start out assuming all booths are closed,
    and update the dictionary only when there is a match.p
    '''
    booth1 = "Booth 1"
    booth2 = "Booth 2"
    booth3 = "Booth 3"
    newspaper = "AM Newspaper Reading"
    
    schedule = {
        "newspaper": [],
        "9": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "10": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "11": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "12": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "13": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "14": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "15": {"booth1": "closed", "booth2": "closed", "booth3": "closed"}
    }

    # no need to run this function on weekends
    if date_is_weekend(date=date):
        return schedule

    nine = "9:00am - 10:00am"
    ten = "10:00am - 11:00am"
    eleven = "11:00am - 12:00pm"
    twelve = "12:00pm - 1:00pm"
    one = "1:00pm - 2:00pm"
    two = "2:00pm - 3:00pm"
    three = "3:00pm - 4:30pm"
    
    try:
        shifts = scrape_VIC(date)
    except Exception as e:
        print(e)
        return schedule
    for shift in shifts:

        if newspaper in shift:
            schedule["newspaper"].append(remove_extra_text(booth=newspaper, shift=shift, hour="9:00am - 11:00am"))

        if (booth1 in shift) and (nine in shift):
            schedule['9']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=nine)

        if (booth2 in shift) and (nine in shift):
            schedule['9']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=nine)

        if (booth3 in shift) and (nine in shift):
            schedule['9']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=nine)

        
        if (booth1 in shift) and (ten in shift):
            schedule['10']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=ten)

        if (booth2 in shift) and (ten in shift):
            schedule['10']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=ten)

        if (booth3 in shift) and (ten in shift):
            schedule['10']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=ten)

        
        if (booth1 in shift) and (eleven in shift):
            schedule['11']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=eleven)

        if (booth2 in shift) and (eleven in shift):
            schedule['11']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=eleven)

        if (booth3 in shift) and (eleven in shift):
            schedule['11']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=eleven)

        
        if (booth1 in shift) and (twelve in shift):
            schedule['12']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=twelve)

        if (booth2 in shift) and (twelve in shift):
            schedule['12']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=twelve)

        if (booth3 in shift) and (twelve in shift):
            schedule['12']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=twelve)

        
        if (booth1 in shift) and (one in shift):
            schedule['13']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=one)

        if (booth2 in shift) and (one in shift):
            schedule['13']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=one)

        if (booth3 in shift) and (one in shift):
            schedule['13']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=one)


        if (booth1 in shift) and (two in shift):
            schedule['14']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=two)

        if (booth2 in shift) and (two in shift):
            schedule['14']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=two)

        if (booth3 in shift) and (two in shift):
            schedule['14']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=two)
        

        if (booth1 in shift) and (three in shift):
            schedule['15']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=three)

        if (booth2 in shift) and (three in shift):
            schedule['15']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=three)

        if (booth3 in shift) and (three in shift):
            schedule['15']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=three)
   
    return schedule