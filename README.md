# booth

![tests](https://github.com/Nashville-Public-Library/booth/actions/workflows/main.yml/badge.svg)

[api.nashvilletalkinglibrary.com](https://api.nashvilletalkinglibrary.com)

 a simple web app to assist with TL booth schedule, and for other purposes...

 ----

 ## Read this before deploying!

 ### Selenium

 I tried uploading a linux binary of the chrome driver at root of project and passing in that location when creating the `driver = webdriver.Chrome(...)` instance. this did not work. long story short, I found [selenium's preferred method](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-driver-management-software) is using [webdriver manager](https://github.com/SergeyPirogov/webdriver_manager). this will install it for you, and also keep it up to date with the latest version.

 even still, when running this on EC2, chrome failed to start properly. it seems this is because webdriver manager does install the web driver, but not Chome itself. so you need to add a [predeploy hook](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html) to do this; that's what the bash script in `.platform\hooks\predeploy\` is for. note that Amazon's version of Linux doesn't use `apt/apt-get` for packages; it uses `yum`.

 once I got this working, Chrome still complained. the error was `Chrome failed to start: exited abnormally.` this has something to do with the virtual display settings. the solution was provided on [SO](https://stackoverflow.com/questions/22424737/unknown-error-chrome-failed-to-start-exited-abnormally). also note that according to one commentator, `no-sandbox` needs to be passed in as the first argument (I don't know why.)

 ### .ebextensions

 It SEEMS all EC2 instances default to a different time zone (It's UTC, i think). We're able to change our instance's timezone with a `.config` file. This is the `change_timezone.config` file in the `.ebextensions` folder.

### Testing
Run `pytest` at the top level directory to run the basic tests.

### Misc

Don't forget to continually update your `requirement.txt` file as you go (via `pip freeze > requirements.txt`).
