from datetime import datetime

def are_we_closed():
    current_hour = datetime.now().strftime('%H')
    current_hour = int(current_hour)

    current_day = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']

    if current_hour < 8 or current_hour > 16:
        return True

    if current_day in weekend:
        return True
    
    return False

def check_banner():
    banner = open('message.txt', 'r')
    banner = banner.read()

    if banner == '':
        banner == False
        
    return banner