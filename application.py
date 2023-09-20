'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

# AWS EB default is to look for flask instance variable called application.
from app import app as application

if __name__ == '__main__':
    application.run(debug=True)