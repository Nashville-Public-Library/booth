# booth

![tests](https://github.com/Nashville-Public-Library/booth/actions/workflows/main.yml/badge.svg)
[![GitHub issues](https://img.shields.io/github/issues/Nashville-Public-Library/booth.png)](https://github.com/Nashville-Public-Library/booth/issues)
[![last-commit](https://img.shields.io/github/last-commit/Nashville-Public-Library/booth)](https://github.com/Nashville-Public-Library/booth/commits/main)


[api.talkinglibrary.nashville.gov](https://api.talkinglibrary.nashville.gov)

 a simple web app to assist with various backend TL things...

 ----

## Server Config

move this elsewhere...


## Volunteer Photos
Crop the photo to be a headshot and copy it to `static/img/vol/`. The file should be labelled the same way their name shows up in VIC, but remove the space between the first and last name. If the name in VIC is Steve Rogers, the photo should be `SteveRogers.jpg`. All photos must be a .JPG.

## Misc
Don't forget to continually update your `requirement.txt` file as you go: 
````python
pip freeze > requirements.txt
````

## Development

- Clone this depository
    ````bash
    git clone https://github.com/Nashville-Public-Library/booth.git
    ````

- cd into the folder in the terminal or open the folder in your IDE
    ````bash
    cd booth
    ````

- Create a virtual environment
    ````bash 
    py -m venv venv
    ````
    - Depending on your OS, you may need to use `python` or `python3` instead of `py`

- Activate virtual environment
    - On Windows:

    ````bash
    venv\Scripts\activate
    ````
    - On Mac:

    ````bash
    source venv/bin/activate
    ````

    >[IMPORTANT]
    >If done correctly, you should see `(venv)` in the terminal. Don't run the rest of these commands unless you see `(venv)` in the terminal.

- Update pip
    ````bash
    pip install --upgrade pip
    ````

- Install dependencies
    ````bash
    pip install -r requirements.txt
    ````

    - Depending on your OS, you may need to run `pip3` instead of `pip`

- Install Browser Drivers
    ````bash
    playwright install chromium
    ````

- Run Pytest
    ````bash
    pytest
    ````
    If there are failing tests, you may have installed something incorrectly...

- Start the site
    ````bash
    flask run --debug
    ````
    To open the site in your browser, follow the directions in your terminal


- Deactivate Virtual Environment
    
    If you need to deactivate the virtual environment, type/run the following in the terminal:
    ````bash
    deactivate
    ````


