from datetime import datetime

def now():
    current_hour = datetime.now().strftime('%H')

    if int(current_hour) <= 11:
        lead_hour = f'{current_hour}:00 a - '.lstrip('0')
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
    if int(current_hour) == 15:
        trail_hour = '4:30 p'

    final_hour = f'{lead_hour}{trail_hour}'
    return final_hour

print(now())