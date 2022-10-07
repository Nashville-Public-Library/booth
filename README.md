# booth
 a simple web app to assist with TL booth schedule

 ----

 DON'T FORGET TO SET ENVIRONMENT VARIABLES AS EXPLAINED IN THE `.EBEXTENSIONS` SECTION BELOW

 ## notes on deploying to AWS EB

 ### Selenium

 I tried uploading a linux binary of the chrome driver at root of project and passing in that location when creating the `driver = webdriver.Chrome(...)` instance. this did not work. long story short, I found [selenium's preferred method](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-driver-management-software) is using [webdriver manager](https://github.com/SergeyPirogov/webdriver_manager). this will install it for you, and also keep it up to date.

 even still, when running this on EC2, chrome fails to start properly. it seems this is because webdriver manager does install the web driver, but not Chome itself. so you need to add a [predeploy hook](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html) to do this; that's what the bash script in `.platform\hooks\predeploy\` is for. note that Amazon's version of Linux doesn't use `apt/apt-get` for packages; it uses `yum`.

 once I got this working, Chrome still complained. the error was `Chrome failed to start: exited abnormally.` this has something to do with the virtual display settings. the solution was provided on [SO](https://stackoverflow.com/questions/22424737/unknown-error-chrome-failed-to-start-exited-abnormally). also note that according to one commentator, `no-sandbox` needs to be passed in as the first argument (I don't know why.)

 ### .ebextensions

 our EC2 instance defaults to a different time zone (It's UTC, i think). we could deal with this in the code directly, but that seems messy; we don't want to have to change things directly depending on where it's run. instead we're able to change our instance's timezone with a `.config` file.

 the `options.config` file sets the environment variables, so our VIC username/password are not stored in the source.

 IMPORTANT: If you do not see a `options.config` file inside the `.ebestensions` folder it's because I decided to `gitignore` this file. here's what the file should look like:

    option_settings:
      - option_name:  VIC_user
        value:  your_VIC_username
      - option_name:  VIC_password
        value:  your_VIC_password

nothing should be enclosed in quotes.

### Misc

don't forget to continually update your `requirement.txt` file as you go (via `pip freeze > requirements.txt`).
